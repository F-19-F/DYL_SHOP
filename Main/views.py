from django.conf import UserSettingsHolder
from django.db.models import query
from django.http.request import QueryDict
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Cart, Customer, Product, OrderPlaced, User
from .forms import AddItemForm, CustomerProfileForm, CustomerRegisterForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category="TW")
        bottomwears = Product.objects.filter(category="BW")
        laptops = Product.objects.filter(category="L")
        mobiles = Product.objects.filter(category="M")
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'Main/home.html', {
            'topwears': topwears,
            'bottomwears': bottomwears,
            'laptops': laptops,
            'mobiles': mobiles,
            'totalitem': totalitem,
        }
                      )


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


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


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


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity >0:
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


# Item Views Start here

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Apple' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'Main/mobile.html', {
        'mobiles': mobiles,

    })


def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Apple' or data == 'hp':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    return render(request, 'Main/laptop.html', {
        'laptops': laptops,

    })


def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'lira' or data == 'gentlepark':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    return render(request, 'Main/topwears.html', {
        'topwears': topwears,

    })


def bottomwear(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'lira' or data == 'Richman' or data == 'gentle park ':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    return render(request, 'Main/bottomwear.html', {
        'bottomwears': bottomwears,

    })


# Item Views End here

class CustomerRegistrationView(View):
    @staticmethod
    def get(request):
        form = CustomerRegisterForm
        return render(request, 'Main/customerregistration.html', {'form': form})

    @staticmethod
    def post(request):
        form = CustomerRegisterForm(request.POST)
        if form.is_valid:
            messages.success(request, '注册成功!')
            form.save()
        return render(request, 'Main/customerregistration.html', {'form': form})


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
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        return render(request, 'Main/profile.html', {
            'form': form,
            'active': 'btn-primary'
        })


"""
class AddItemView(View):
  def get(self,request):
    form= AddItemForm
    return render(request,'Main/additem.html',{'form':form})
  def post(self,request):
    form=AddItemForm(request.POST)
    messages.success(request,'Congratulations!!  Item Added Successfully...')
    form.save('Main/home.html')
    return render(request,'Main/additem.html',{'form':form})
"""