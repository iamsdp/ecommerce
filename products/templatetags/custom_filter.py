"""
Template tags
"""
from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    """ get currency attached """
    return "₹ "+str(number)

@register.filter(name='multiply')
def multiply(number, number1):
    """ Multiply """
    return number * number1

@register.filter(name='percentage')
def percentage(num1 , num2):
    """ calculate percentage """
    return (num1/num2)/100
