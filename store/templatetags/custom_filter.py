"""
Template tags
"""
# pylint: disable=import-error
from django import template
from django.utils.http import urlencode
from products.models import Category, Color, Material, Company

register = template.Library()

@register.filter(name='currency')
def currency(number):
    """ Add currency """
    return "₹ "+str(number)

@register.filter(name='multiply')
def multiply(number , number1):
    """ multiply """
    return number * number1

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """ Store Url add parameter """
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

@register.simple_tag
def get_categories():
    """ Categories """
    query_set = Category.objects.all()
    return query_set

@register.simple_tag
def get_all_companies():
    """ Companies """
    query_set = Company.objects.all()
    return query_set

@register.simple_tag
def get_all_colors():
    """ colors """
    query_set = Color.objects.all()
    return query_set

@register.simple_tag
def get_material_list():
    """ Materials """
    query_set = Material.objects.all()
    return query_set
