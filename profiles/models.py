"""
Define Models
"""
# pylint: disable=invalid-str-returned,unused-argument,no-self-use
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class TimeStampMixin(models.Model):
    """ DateTimeField """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ class meta """
        abstract = True


class UserManager(BaseUserManager):
    """ Custom UserManager """
    def create_user(self, email, password=None):
        """ create_user """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """ Admin user creation """
        user =  self.create_user(email, password=password,)
        user.is_admin = True
        user.is_active = True
        user.user_type = user.UserType.ADMIN
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Customer User Model.
    """
    class UserType(models.TextChoices):
        """ User type choices """
        SHOPUSER = 'SU', _('Shopuser')
        CUSTOMER = 'CU', _('Customer')
        ADMIN = 'AU', _('Admin')

    class GenderType(models.TextChoices):
        """ Gender choices """
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    email = models.EmailField(verbose_name='email address', max_length=20, unique=True,)
    phone = models.CharField(max_length=15)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField(verbose_name='Date of Birth', blank=False, null=True)
    address = models.CharField(max_length=300)
    gender = models.CharField(choices=GenderType.choices, max_length=10)
    user_type = models.CharField(choices=UserType.choices, max_length=15, default=UserType.CUSTOMER)
    rejection_note = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_disabled_by_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin and self.user_type == self.UserType.ADMIN

    @property
    def is_customer(self):
        "Is the user_type - 'customer' ?"
        return self.user_type == self.UserType.CUSTOMER

    @property
    def is_shopuser(self):
        "Is the user_type - 'shopuser' ?"
        return self.user_type == self.UserType.SHOPUSER
