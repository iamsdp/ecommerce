"""
Custom Mixins for User Type Check and Login
"""
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class CustomerAcessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    To validate if user is logged in and is Customer only.
    """
    def test_func(self):
        return self.request.user.is_customer


class ShopUserAcessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    To validate if user is logged in and is Shop User only.
    """
    def test_func(self):
        return self.request.user.is_shopuser


class AdminAcessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    To validate if user is logged in and is Admin only.
    """
    def test_func(self):
        return self.request.user.is_staff
