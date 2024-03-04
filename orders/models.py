"""
Defining Models for orders application
"""
# pylint: disable=no-member
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Product
from profiles.models import User, TimeStampMixin


class Cart(TimeStampMixin):
    """
    Cart Model.
    """
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=False)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.product.title


class Order(TimeStampMixin):
    """
    Order Model.
    """
    class Status(models.TextChoices):
        """
        Choices for status.
        """
        PAID = 'PAID', _('Paid')
        CANCELLED = 'CANCLED', _('Cancelled')
        COMPLETED = 'COMPLTD', _('Completed')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=15)
    total_amount = models.IntegerField(default=0)
    status=models.CharField(choices=Status.choices, max_length=15)
    def __str__(self):
        return self.customer.email


class Item(models.Model):
    """
    Order Item
    """
    class Status(models.TextChoices):
        """
        Choices for status
        """
        PAID = 'PAID', _('Paid')
        CANCELLED = 'CANCLED', _('Cancelled')
        COMPLETED = 'COMPLTD', _('Completed')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    status = models.CharField(choices=Status.choices, max_length=15)

    def __str__(self):
        return self.product.title
