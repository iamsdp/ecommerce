"""
URLS
"""
# pylint: disable=line-too-long
from django.urls import path
from allauth.account.views import email_verification_sent
from .views import (shop_user_register_form, user_account_setting_view, user_update_view,
                activate_shop, action_activate_shop, register_request_list, admin_dashboard,
                create_shop_by_admin, delete_shop_by_admin, user_detail_view, all_customer_list,
                update_shop_by_admin_view, login_redirect_view, action_reject_shop_view)


urlpatterns = [
    path('login-btn', login_redirect_view, name='login_redirect_view'),
    path('customer-settings/', user_account_setting_view, name ='customer_settings'),
    path('update_profile/', user_update_view, name = 'update_profile'),
    path('shopuser_reg/', shop_user_register_form, name = 'shopuser_registration'),
    path('admindashb/', admin_dashboard, name= 'admin_dashboard'),
    path('admindashb/shop-reg-list/', register_request_list, name='shop_register_list'),
    path('admindashb/shop-reg-list/activate_shop/<int:pk>', activate_shop, name = 'activate_shop'),
    path('admindashb/shop-reg-list/activate_shop/action_activate/<int:id>', action_activate_shop, name = 'action_activate'),
    path('admindashb/shop-reg-list/activate_shop/action_reject/<int:id>', action_reject_shop_view, name = 'action_reject_shop_view'),
    path('admindashb/createshop/', create_shop_by_admin, name= 'admin_create_shop'),
    path('admindashb/del_shop/', delete_shop_by_admin, name = 'del_shop'),
    path('admindashb/update/<int:pk>', update_shop_by_admin_view, name='update_shop_by_admin'),
    path('admindashb/shop-user-detail/<pk>', user_detail_view, name='user_detail'),
    path('admindashb/customer_admin', all_customer_list, name='customer_admin'),
]
