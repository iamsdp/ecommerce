"""
URLS
"""
# pylint: disable=line-too-long
from django.urls import path

from .views import (product_create_view, product_list_view, product_update_view,
                product_delete_view, customer_order_list_view, order_sales_view, all_products_list,
                product_under_shop_list_view, publish_product_view, rate_product_update_view)


urlpatterns = [
        path('shopdashboard/', product_list_view, name='shopdashboard'),
        path('shopdashboard/create/', product_create_view, name= 'product_create_list'),
        path('shopdashboard/list/<pk>/update', product_update_view, name= 'product_list_update'),
        path('shopdashboard/list/<pk>/delete/', product_delete_view, name='product_list_delete'),
        path('shopdashboard/list/publish/<id>', publish_product_view, name='publish_product_view'),
        path('shopdashboard/customer-orders/', customer_order_list_view, name='customer_order'),
        path('shopdashboard/order-sales/', order_sales_view, name='order_sales'),
        path('products-list', all_products_list, name='all_product_list'),
        path('admindashb/products-under-shop/<id>', product_under_shop_list_view, name='products_under_shop'),
        path('provide/rating/<id>/<int:rating>', rate_product_update_view, name='rate_product_update_view'),
]
