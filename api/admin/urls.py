""" URLs """
# pylint: disable=line-too-long
from django.urls import path

from .views import (product_list, order_item_list, customer_list, shop_user_list, update_delete_shop,
                shop_create_api_view, register_request_list)


urlpatterns = [
        path('customer/list/', customer_list, name= 'customer_list'),
        path('product/list/', product_list, name= 'product_list'),
        path('order-item/list/', order_item_list, name= 'order_item_list'),
        path('shop/list/', shop_user_list, name= 'shop_user_list'),
        path('shop/create/', shop_create_api_view, name='shop_create_api_view'),
        path('shop/modify/<pk>/', update_delete_shop, name='update_delete_shop'),
        path('shop/register-list/', register_request_list, name='register_request_list'),
]
