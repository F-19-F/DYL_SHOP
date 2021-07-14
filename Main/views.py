from django.conf import UserSettingsHolder
from django.db.models import query
from django.http.request import QueryDict
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Cart, Customer, Product, OrderPlaced, User, KIND
from .forms import AddItemForm, CustomerProfileForm, CustomerRegisterForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# 主页视图
class ProductView(View):
    def get(self, request):
        totalitem = 0
        subkinds = KIND.objects.filter(PKID__isnull=False)
        # print(subkinds)
        kind_good = []
        for i in subkinds:
            goods = Product.objects.filter(kind=i)
            if len(goods) == 0:
                continue
            one = {
                'kind': i,
                'goods': goods
            }
            kind_good.append(one)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'Main/home.html', {
            'totalitem': totalitem,  # 购物车数量
            'kind_good': kind_good
        }
                      )


# 商品详情界面
class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'Main/productdetail.html', {
            'product': product,
            'item_already_in_cart': item_already_in_cart,
            'totalitem': totalitem,
        })


# 添加到购物车后重定向到购物车界面
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


# 购物车界面
@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'Main/addtocart.html',
                          {'carts': cart,
                           'totalamount': totalamount,
                           'amount': amount,
                           'totalitem': totalitem
                           })
        else:
            return render(request, 'Main/emptycart.html')


# 购物车数量添加接口
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


# 购物车数量减少接口
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity > 0:
            c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
    data = {
        'quantity': c.quantity,
        'amount': amount,
        'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)


# 移除购物车中的商品接口
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

    data = {

        'amount': amount,
        'totalamount': amount + shipping_amount
    }
    return JsonResponse(data)


def buy_now(request):
    return render(request, 'Main/buynow.html')


# 用户地址界面
@login_required
def address(request):
    totalitem = 0
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'Main/address.html',
                  {'add': add,
                   'active': 'cart',
                   'totalitem': totalitem
                   })


# 订单界面
@login_required
def orders(request):
    totalitem = 0
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'Main/orders.html', {
        'order_placed': op,
        'totalitem': totalitem
    })


# 父级种类视图
def kind(request, data=None):
    if data:
        # 非法参数
        if not data.isdigit():
            return redirect('/')
        try:
            mainkind = KIND.objects.get(KID=data)
        except:
            return HttpResponse('/')
        subkinds = KIND.objects.filter(PKID__KID=data)
        all_goods = []
        for i in subkinds:
            products = Product.objects.filter(kind=i)
            all_goods += products
        # all_goods为所有父种类为参数的商品列表
        render_data = {
            'mainkind': mainkind,
            'subkinds': subkinds,
            'goods': all_goods
        }
        return render(request, 'Main/kind.html', render_data)
    else:
        return redirect('/')


# 子种类视图
def skind(request, pkid=None, kid=None):
    if pkid:
        try:
            mainkind = KIND.objects.get(KID=pkid)
        except:
            return HttpResponse('/')
        subkinds = KIND.objects.filter(PKID__KID=pkid)
        try:
            all_goods = Product.objects.filter(kind=kid)
        except:
            return HttpResponse('/')
        render_data = {
            'mainkind': mainkind,
            'subkinds': subkinds,
            'goods': all_goods
        }
        return render(request, 'Main/kind.html', render_data)
    else:
        return redirect('/')


def search(request):
    if request.method == 'POST':
        keywords = request.POST.get('keywords')
        res = Product.objects.filter(title__contains=keywords)
        render_data = {
            'goods': res
        }
        return render(request, 'Main/searchresult.html', render_data)
    else:
        return redirect('/')


# Item Views End here
# 注册视图
class CustomerRegistrationView(View):
    @staticmethod
    def get(request):
        form = CustomerRegisterForm
        return render(request, 'Main/customerregistration.html', {'form': form})

    @staticmethod
    def post(request):
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, '注册成功!')
            form.save()
        else:
            print(form.errors)
        return render(request, 'Main/customerregistration.html', {'form': form})


@login_required
def checkout_advance(request,product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/checkout/')


# 结算视图
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'Main/checkout.html', {
        'add': add,
        'totalamount': totalamount,
        'cart_items': cart_items
    })


# 支付完成界面
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


# 个人信息添加页面
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        form = CustomerProfileForm
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'Main/profile.html', {
            'form': form,
            'active': 'cart',
            'totalitem': totalitem
        })

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, '信息修改成功!')
        return render(request, 'Main/profile.html', {
            'form': form,
            'active': 'btn-primary'
        })
