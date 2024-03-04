"""
Orders: Urls Module
"""
# pylint: disable=line-too-long
from django.urls import path

from .views import (add_to_cart_view, cart_list_view, cart_delete_view, remove_item_from_cart_view,
                    order_list_view, order_under_customer_list_view, order_under_shop_list_view,
                    admin_sales_percentage_view, my_orders, update_order_view, order_status_update_view,
                    admin_analytics_shop_view)


urlpatterns = [
    path('admindashb/orders-under-shop/<id>', order_under_shop_list_view, name='orders_under_shop'),
    path('admindashb/customer_admin/<id>', order_under_customer_list_view, name='orders_under_customer'),
    path('admindashb/all-orders-list', order_list_view, name='order_list_view'),
    path('cart/add/<int:id>', add_to_cart_view, name = 'add_to_cart_view'),
    path('cart/list', cart_list_view, name='cart_list_view'),
    path('cart/delete/<int:pk>/', cart_delete_view, name='cart_delete_view'),
    path('cart/remove-quantity/<int:id>/', remove_item_from_cart_view, name='remove_item_from_cart_view'),
    path('admindashb/sales-percentage', admin_sales_percentage_view, name='admin_sales_percentage_view'),
    path('my-orders/', my_orders, name='my_orders'),
    path('my-orders/update/', update_order_view, name='update_order'),
    path('shopdashboard/customer-orders/<id>', order_status_update_view, name='order_status_update_view'),
    path('admindashb/analytics/<id>', admin_analytics_shop_view, name='admin_analytics_shop_view')
]
