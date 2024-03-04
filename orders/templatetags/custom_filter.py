"""
Custom Template tags
"""
from django import template
from django.utils.http import urlencode

register = template.Library()

@register.filter(name='currency')
def currency(number):
    """ Add currency SYmbol at the begining """
    return "₹ "+str(number)

@register.filter(name='multiply')
def multiply(number , number1):
    """ Multiply two numbers """
    return number * number1

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """ Add url parameter """
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
