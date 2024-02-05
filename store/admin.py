from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


class StoreAdminSite(admin.AdminSite):
    site_header = "Store Admin"
    site_title = "Store Portal"
    index_title = "Welcome to My Ecommerece"


store_admin_site = StoreAdminSite(name="store_admin")


store_admin_site.register(Customer)
store_admin_site.register(Product)
store_admin_site.register(Order)
store_admin_site.register(OrderItem)
store_admin_site.register(ShippingAddress)
