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
    OrderPlaced
)


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']


@admin.register(Product)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category',
                    'product_image']


@admin.register(Cart)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(OrderPlaced)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'customer_info', 'product', 'product_info', 'quantity', 'ordered_date',
                    'status']

    @staticmethod
    def customer_info(obj):
        link = reverse("admin:Main_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    @staticmethod
    def product_info(obj):
        link = reverse("admin:Main_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)