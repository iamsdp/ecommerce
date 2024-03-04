"""
Create your models here.
"""
from django.db import models

from products.models import Product
from profiles.models import User, TimeStampMixin

# pylint: disable=no-member
class Wishlist(TimeStampMixin):
    """
    Wish List
    """
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.product.title
