"""
Filters, Search, Sort for STORE page
"""
# pylint: disable=no-member, too-few-public-methods
from django import forms

import django_filters
from django_filters import widgets
from products.models import Color, Company, Material, Product, Category


class StoreFilter(django_filters.FilterSet):
    """ Filter """
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
            widget=forms.CheckboxSelectMultiple,)
    company = django_filters.ModelMultipleChoiceFilter(queryset=Company.objects.all(),
            widget=forms.CheckboxSelectMultiple,)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(),
            widget=forms.CheckboxSelectMultiple,)
    material = django_filters.ModelMultipleChoiceFilter(queryset=Material.objects.all(),
            widget=forms.CheckboxSelectMultiple,)
    price = django_filters.OrderingFilter(fields=['price','rating'], widget=widgets.LinkWidget)

    class Meta:
        """ META """
        model = Product
        fields = ['title', 'category', 'company', 'color', 'material',]
