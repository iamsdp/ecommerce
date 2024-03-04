"""
Custom Permission Classes
"""
from rest_framework.permissions import BasePermission


class IsShopUser(BasePermission):
    """
    Allows access only to Shop users.
    """
    def has_permission(self, request, view):
        """ Return True if user type is SHOP """
        return bool(request.user and request.user.is_shopuser)


class IsCustomer(BasePermission):
    """
    Allows access only to Customers.
    """
    def has_permission(self, request, view):
        """ Return True if user type is Customer """
        return bool(request.user and request.user.is_customer)
