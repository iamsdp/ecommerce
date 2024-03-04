""" URLs """
# pylint: disable=line-too-long
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.views import PasswordResetConfirmView
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
# from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView

from .views import (shop_create_api_view, user_update_api_view, customer_create_api_view,
                product_list_by_shop_user, create_product_by_shop_user, update_product_by_shop,
                shop_product_detail_api_view, customer_order_by_shop)


urlpatterns = [
        path('openapi/', get_schema_view(
                title="Ecom API Service",
                description="API developers hpoing to use our service",
                renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer]),
                name='openapi-schema'
        ),
        path('docs/',
        TemplateView.as_view(
                template_name='documentation.html',
                extra_context={'schema_url':'openapi-schema'}), name='swagger-ui'
        ),
        path('dj-rest-auth/registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view(),),
        path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
        # For normal Sign up bcz its using dj-rest-auth views
        # path('dj-rest-auth/account-confirm-email/', VerifyEmailView.as_view(),
        #     name='account_email_verification_sent'),
        # API: password reset email was not working without this
        path('dj-rest-auth/password/reset/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(),
                name='password_reset_confirm'),
        path('dj-rest-auth/', include('dj_rest_auth.urls')),
        path('shop/create/', shop_create_api_view, name='shop_create_api_view'),
        path('customer/create/', customer_create_api_view, name='customer_create_api_view'),
        path('user/update/', user_update_api_view, name='user_update_api_view'),
        path('shop/product/list/', product_list_by_shop_user, name= 'product_list_by_shop_user'),
        path('shop/product/details/<pk>', shop_product_detail_api_view, name= 'shop_product_detail'),
        path('shop/product/create/', create_product_by_shop_user, name= 'create_product_by_shop_user'),
        path('shop/product/update/<pk>', update_product_by_shop, name= 'update_product_by_shop'),
        path('shop/orders/list/', customer_order_by_shop, name='customer_order_by_shop'),
        path('admin/', include('api.admin.urls'))
]
