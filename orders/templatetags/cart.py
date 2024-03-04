"""
Template Tags for Cart Mechanism
"""
from django import template


register = template.Library()

@register.filter(name='cart_quantity')
def cart_quantity(quantity):
    """ check if Cart is empty """
    if quantity >1:
        return True
    return False

@register.filter(name='price_total')
def price_total(price, quantity):
    """ Calculate total item price """
    return price * quantity

@register.filter(name='total_cart_price')
def total_cart_price(products , cart):
    """ Calculate Total Order price """
    total = 0
    for product in products:
        total += price_total(product , cart)

    return total
