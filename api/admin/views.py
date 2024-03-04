""" API VIEWS """
# pylint: disable=line-too-long, no-member
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import (CreateAPIView,
        ListAPIView, RetrieveUpdateDestroyAPIView)

from profiles.models import User
from products.models import Product
from orders.models import Item

from .serializers import (UserSerializer, ProductSerializer, OrderItemSerializer, CreateShopByAdminSerializer)


class ProductListAPI(ListAPIView):
    """ List products under logged in Shop User """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

product_list = ProductListAPI.as_view()


class OrderItemListAPI(ListAPIView):
    """ List products under logged in Shop User """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = OrderItemSerializer
    queryset = Item.objects.all()

order_item_list = OrderItemListAPI.as_view()


class CustomerListAPI(ListAPIView):
    """ All Customers """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.filter(user_type='CU')

customer_list = CustomerListAPI.as_view()


class ShopUserListAPI(ListAPIView):
    """ All Shops List"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.filter(user_type='SU')

shop_user_list = ShopUserListAPI.as_view()


class UpdateDeleteShopAPI(RetrieveUpdateDestroyAPIView):
    """ Update or Delete SHOP by Admin """
    permission_classes = [IsAuthenticated, IsAdminUser]
    def retrieve(self, request, *args, **kwargs):
        """ Shop User by ID """
        try:
            instance = User.objects.get(id=kwargs['pk'], user_type='SU')
        except:
            return Response(data={'error':'user may not exist or may not be a shop user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

update_delete_shop = UpdateDeleteShopAPI.as_view()


class ProductUnderShop(ListAPIView):
    """ All Products """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter()

product_under_shop_list = ProductUnderShop.as_view()


class OrderUnderShop(ListAPIView):
    """ Order under SHop """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = OrderItemSerializer
    queryset = Item.objects.all()

order_under_shop_list = OrderUnderShop.as_view()


class ShopCreateByAdminAPIView(CreateAPIView):
    """ Sign up for Shop """
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    serializer_class = CreateShopByAdminSerializer

    def perform_create(self, serializer):
        """ Need to pass request, To avoid error : save() missing 1 required positional argument 'request'. """
        serializer.save(self.request)

shop_create_api_view = ShopCreateByAdminAPIView.as_view()


class RegisterRequestListView(ListAPIView):
    """
    List of pending approval request of Shop users.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        """ qs """
        object_list = super().get_queryset(*args, **kwargs)
        object_list = object_list.filter(user_type='SU', is_active = bool(False), is_disabled_by_admin= bool(False))
        return object_list

register_request_list = RegisterRequestListView.as_view()
