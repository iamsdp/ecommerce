"""
Register Models.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Product, Category, Company, Color, Material


class ProductAdmin(BaseUserAdmin):
    """
    Attributes on Admin site.
    """
    model = Product
    list_display = ('title', 'description', 'price', 'image','category','seller')
    list_filter = ('title',)
    fieldsets = ()
    add_fieldsets = ()
    search_fields = ('title',)
    ordering = ('title',)
    filter_horizontal = ()


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Color)
admin.site.register(Material)
