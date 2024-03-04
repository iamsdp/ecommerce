"""
Products Models.
"""
# pylint: disable=no-member, invalid-str-returned, too-few-public-methods
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from profiles.models import User, TimeStampMixin


class Category(models.Model):
    """ Category """
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Company(models.Model):
    """ Company """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Color(models.Model):
    """ Color """
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Material(models.Model):
    """ Material """
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Product(TimeStampMixin):
    """ Product """
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/')
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)], default=0)
    is_published = models.BooleanField(default=False)

    class Meta:
        """ meta """
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @staticmethod
    def get_all_products():
        """ get all products qs """
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        """ Get product qs by cat ID"""
        return Product.objects.filter(category_id = category_id)

    @staticmethod
    def get_all_products_by_company_name(company):
        """ get product qs by company name """
        return Product.objects.filter(company__name = company)

    @staticmethod
    def get_all_products_by_color_name(color):
        """ get product qs by color """
        return Product.objects.filter(color__name = color)

    @staticmethod
    def get_all_products_by_material_name(material):
        """ get product qs by material """
        return Product.objects.filter(material__name = material)
