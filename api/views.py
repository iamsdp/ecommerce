""" API VIEWS """
# pylint: disable=line-too-long, no-member
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
        RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView)

from profiles.models import User
from products.models import Product
from orders.models import Order, Item

from .permissions import IsShopUser
from .serializers import (ShopUserRegisterSerializer, UserSerializer, OrderItemSerializer,
            CustomerRegisterSerializer, ShopProductSerializer, CreateProductSerializer)


class ShopCreateAPIView(CreateAPIView):
    """ Sign up for Shop """
    queryset = User.objects.all()
    serializer_class = ShopUserRegisterSerializer

    def perform_create(self, serializer):
        """ Need to pass request, To avoid error : save() missing 1 required positional argument 'request'. """
        serializer.save(self.request)

shop_create_api_view = ShopCreateAPIView.as_view()


class CustomerCreateAPIView(CreateAPIView):
    """ Sign up for Shop """
    queryset = User.objects.all()
    serializer_class = CustomerRegisterSerializer

    def perform_create(self, serializer):
        """ Need to pass request, To avoid error : save() missing 1 required positional argument 'request'. """
        serializer.save(self.request)

customer_create_api_view = CustomerCreateAPIView.as_view()


class UserUpdateAPIView(RetrieveUpdateAPIView):
    """ Logged in user can update own Profile """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """ Get current logged in User """
        return self.request.user

user_update_api_view = UserUpdateAPIView.as_view()


# -------------------------------- SHOP User --------------------------------

class ProductListByShopUserAPI(ListAPIView):
    """ List products under logged in Shop User """
    permission_classes = [IsAuthenticated, IsShopUser]
    serializer_class = ShopProductSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        """ Filter queryset, Get Products Listed by current logged in Seller """
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(seller = self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

product_list_by_shop_user = ProductListByShopUserAPI.as_view()


class ShopProductDetailAPIView(RetrieveAPIView):
    """ Get a particluar product's details where products listed by logged in Shop User """
    permission_classes = [IsAuthenticated, IsShopUser]
    serializer_class = ShopProductSerializer
    queryset = Product.objects.all()

shop_product_detail_api_view = ShopProductDetailAPIView.as_view()


class CreateProductByShopUserAPI(CreateAPIView):
    """ Create a Product """
    permission_classes = [IsAuthenticated, IsShopUser]
    serializer_class = CreateProductSerializer
    queryset = Product.objects.all()

create_product_by_shop_user = CreateProductByShopUserAPI.as_view()


class UpdateProductByShopUser(RetrieveUpdateDestroyAPIView):
    """ Update and Delete the product - Show product only if it is listed by Seller """
    permission_classes = [IsAuthenticated, IsShopUser]
    serializer_class = ShopProductSerializer
    queryset = Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """ Get Product Listed by current logged in Seller only """
        instance = Product.objects.get(id=kwargs['pk'], seller=self.request.user.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

update_product_by_shop = UpdateProductByShopUser.as_view()


class CustomerOrderbyShop(ListAPIView):
    """ Orders under a Shop """
    permission_classes = [IsAuthenticated, IsShopUser]
    serializer_class = OrderItemSerializer
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        """ Filter queryset, Get Products Listed by current logged in Seller """
        queryset = self.filter_queryset(self.get_queryset())
        products_under_shop = Product.objects.filter(seller = self.request.user)
        queryset = queryset.filter(product__in = products_under_shop)
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)

customer_order_by_shop = CustomerOrderbyShop.as_view()
