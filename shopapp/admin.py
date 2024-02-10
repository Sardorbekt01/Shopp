from django.contrib import admin
from .models import *

admin.site.register(Admin)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ShopCart)
admin.site.register(Order)
admin.site.register(OrderItem)
