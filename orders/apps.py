""" Apps """
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """ App Config """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
