"""
Define Forms
"""
# pylint: disable=too-few-public-methods, too-many-ancestors
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import User


class DatePickerInput(forms.DateInput):
    """ Date Picker Input """
    input_type = 'date'


class CustomerSignupForm(UserCreationForm):
    """
    Signup Form for User type - Customer
    """
    class GenderType(models.TextChoices):
        """ Gender choices """
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    first_name = forms.CharField(max_length=100,)
    last_name = forms.CharField(max_length=100,)
    email = forms.EmailField(max_length=150,)
    date_of_birth = forms.DateField(widget=DatePickerInput)
    gender = forms.ChoiceField(choices=GenderType.choices, widget=forms.RadioSelect)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = user.UserType.CUSTOMER
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        """ Class Meta """
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
                'gender','address', 'password1', 'password2', )


class ShopUserSignUpForm(UserCreationForm):
    """
    Signup Form for User type - ShopUser
    """
    class GenderType(models.TextChoices):
        """ Gender choices """
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)
    date_of_birth = forms.DateField(widget=DatePickerInput)
    gender = forms.ChoiceField(choices=GenderType.choices, widget=forms.RadioSelect)

    class Meta:
        """ Class Meta """
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
                'gender','address', 'password1', 'password2', )


class CreateShopByAdminForm(forms.ModelForm):
    """ Create SHop by admin Form """
    class GenderType(models.TextChoices):
        """ Gender choices """
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')
    date_of_birth = forms.DateField(widget=DatePickerInput)
    gender = forms.ChoiceField(choices=GenderType.choices, widget=forms.RadioSelect)

    class Meta:
        """ Meta """
        model = User
        fields = ['email', 'phone', 'first_name', 'last_name',
                'date_of_birth', 'gender', 'address',]


class ShopUserUpdateModalForm(BSModalModelForm):
    """
    Update Pop Up
    """
    class Meta:
        """ Class Meta """
        model = User
        fields = ['email','first_name','last_name', 'date_of_birth', 'gender', 'address',]
