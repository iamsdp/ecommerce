"""
Urls
"""
from django.urls import path

from .views import (add_to_wishlist, wish_list_view, wish_list_delete_view,
                    check_out, store_filter_view, store_login_redirect_view)


urlpatterns = [
    path('action_add_wishlist/<int:id>', add_to_wishlist, name = 'action_add_wishlist'),
    path('wish-list', wish_list_view, name='wish_list_view'),
    path('wish-list-del/<pk>/delete/', wish_list_delete_view, name='wish_list_delete'),
    path('cart/check-out/', check_out, name='check_out'),
    path('redirect', store_filter_view, name='store'),
    path('', store_login_redirect_view, name='store_login_redirect'),
]
