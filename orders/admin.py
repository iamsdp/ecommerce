"""
Register Models
"""
from django.contrib import admin

from .models import Cart, Order, Item


admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Item)
