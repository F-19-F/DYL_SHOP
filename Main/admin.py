from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
admin.site.site_title = "大鸭梨购物网站管理"
admin.site.site_header = "大鸭梨购物网站管理后台"
admin.site.index_header = "大鸭梨购物网站管理"

from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
    KIND,
    SHOPS
)


# 注册种类管理模型
@admin.register(KIND)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('Name', 'PKID')
    list_editable = ('PKID',)


# 注册商户管理模型
@admin.register(SHOPS)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('Name', 'KID', 'DES', 'TYPE')
    search_fields = ['Name']
    list_editable = ('TYPE',)


# 注册顾客管理模型
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']


# 注册商品管理模型
@admin.register(Product)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'kind',
                    'product_image', 'Status']
    search_fields = ['title']
    list_editable = ['kind', 'Status']


# 注册购物车管理模型
@admin.register(Cart)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


# 注册订单管理模型
@admin.register(OrderPlaced)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'customer_info', 'product', 'product_info', 'quantity', 'ordered_date',
                    'status']
    list_editable = ['status']

    @staticmethod
    @admin.display(description='客户信息')
    def customer_info(obj):
        link = reverse("admin:Main_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    @staticmethod
    @admin.display(description='商品信息')
    def product_info(obj):
        link = reverse("admin:Main_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
