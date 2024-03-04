""" Admin Serializers """
# pylint: disable=too-few-public-methods
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers
from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer

from profiles.models import User
from products.models import Product, Category, Color, Company, Material
from orders.models import Order, Item


class CreateShopByAdminSerializer(RegisterSerializer):
    """ Custom Serializer to create SHOP User """
    class GenderType(models.TextChoices):
        """ Gender choices """
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')
    username = None
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    date_of_birth = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    address = serializers.CharField()
    gender = serializers.ChoiceField(choices=GenderType.choices)

    def get_cleaned_data(self):
        """ Get Data """
        super().get_cleaned_data()
        return {
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone': self.validated_data.get('phone', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
            'gender': self.validated_data.get('gender', ''),
            'address': self.validated_data.get('address', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
        }

    def save(self, request):
        """ Save Data """
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc))
        user.address = self.cleaned_data.get('address')
        user.phone = self.cleaned_data.get('phone')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.gender = self.cleaned_data.get('gender')
        user.user_type = 'SU'
        user.save()
        self.custom_signup(request, user)
        return user


class CategorySerializer(serializers.ModelSerializer):
    """ Category """
    class Meta:
        """ Class Meta """
        model = Category
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    """ Category """
    class Meta:
        """ Class Meta """
        model = Color
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    """ Category """
    class Meta:
        """ Class Meta """
        model = Company
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    """ Category """
    class Meta:
        """ Class Meta """
        model = Material
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """ Custom User Serializer """
    class Meta:
        """ Class Meta """
        model = User
        # fields = ( 'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
        #         'gender','address')
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """ Product Serializer """
    seller = UserSerializer(many=False)
    category = CategorySerializer(many=False)
    company = CompanySerializer(many=False)
    color = ColorSerializer(many=False)
    material = MaterialSerializer(many=False)
    class Meta:
        """ Class Meta """
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """ Order Serializer """
    customer = UserSerializer(many=False)
    class Meta:
        """ Class Meta """
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    """ Order Item Serializer """
    order = OrderSerializer(many=False)
    product = ProductSerializer(many=False)
    class Meta:
        """ Class Meta """
        model = Item
        fields = '__all__'
