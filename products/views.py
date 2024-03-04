"""
Product Views
"""
# pylint: disable=no-member, too-many-ancestors, no-self-use, line-too-long, duplicate-code
import random
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from orders.models import Item
from profiles.models import User
from profiles.custom_mixin import (CustomerAcessRequiredMixin, ShopUserAcessRequiredMixin,
                                AdminAcessRequiredMixin)

from .models import Product


class ProductCreateView(ShopUserAcessRequiredMixin, CreateView):
    """
    To add a new product into list. Only Shop User can add the product.
    """
    model = Product
    fields = ['category', 'title', 'description', 'price', 'company', 'color', 'material', 'image']
    template_name = 'shopdash/product_create_list.html'
    success_url = reverse_lazy('shopdashboard')
    
    def form_valid(self, form):
        """
        Assign seller.
        """
        form.instance.seller = self.request.user
        return super().form_valid(form)

product_create_view = ProductCreateView.as_view()


class ShopProductListView(ShopUserAcessRequiredMixin, ListView):
    """
    This View returns the products listed by particular seller.
    Using logged user's details to verify users identity.
    """
    model = Product
    template_name = 'shopdash/product_list.html'
    def get_queryset(self, *args, **kwargs):
        """
        modify query set.
        """
        object_list = super().get_queryset(*args, **kwargs)
        seller = self.request.user
        object_list = object_list.filter(seller = seller)
        return object_list

product_list_view = ShopProductListView.as_view()


class ProductUpdateView(ShopUserAcessRequiredMixin, UpdateView):
    """
    Seller can Update the details of particular product.
    """
    model = Product
    template_name = 'shopdash/product_list_update.html'
    fields = ['category','title','description', 'price', 'company', 'color', 'material','image']
    success_url = reverse_lazy('shopdashboard')

product_update_view = ProductUpdateView.as_view()


class ProductDeleteView(ShopUserAcessRequiredMixin, DeleteView):
    """
    On ShopUser Dashboard: Seller can Delete the particular product.
    """
    model = Product
    template_name = 'shopdash/product_list_delete.html'
    success_url = reverse_lazy('shopdashboard')

product_delete_view = ProductDeleteView.as_view()


class CustomerOrderListView(ShopUserAcessRequiredMixin, ListView):
    """
    On ShopUser Dashboard: Get list of all the order under a particular Shop/seller.
    """
    model = Item
    template_name = 'shopdash/customer_order.html'
    def get_queryset(self, *args, **kwargs):
        """
        Modify queryset.
        """
        object_list = super().get_queryset(*args, **kwargs)
        seller = self.request.user
        products = Product.objects.filter(seller = seller)
        object_list = object_list.filter(product__in = products)
        return object_list

customer_order_list_view = CustomerOrderListView.as_view()


class OrderSalesView(ShopUserAcessRequiredMixin, View):
    """
    On ShopUser Dashboard: This view generated the sales percentage for a particular seller's sale.
    """
    def get(self, request):
        """
        GET Method: return context.
        """
        seller = request.user.id
        products_listed_under_seller = Product.objects.filter(seller=seller)
        item_sold_by_seller = Item.objects.filter(product__in = products_listed_under_seller, status='COMPLTD')

        count_item_sold_by_seller = 0
        for item in item_sold_by_seller:
            count_item_sold_by_seller += item.quantity

        cat_perc_sales = {}
        categories_list = list(set([ str(i.product.category) for i in item_sold_by_seller ]))
        for catgry in categories_list:
            cat_sales_count = 0
            for item in item_sold_by_seller.filter(product__category__name = catgry):
                cat_sales_count += item.quantity
            cat_perc_sales [catgry] = round((cat_sales_count/count_item_sold_by_seller)*100, 2)

        brand_perc_sales = {}
        brand_list = list(set([ str(i.product.company) for i in item_sold_by_seller ]))
        for brand in brand_list:
            brand_sales_count = 0
            for item in item_sold_by_seller.filter(product__company__name = brand):
                brand_sales_count += item.quantity
            brand_perc_sales [brand] = round((brand_sales_count/count_item_sold_by_seller)*100, 2)

        context = {}
        context['total_sales_count' ] = count_item_sold_by_seller
        context['categories'] = list(cat_perc_sales.keys())
        context['cat_sales'] = list(cat_perc_sales.values())
        context['companies'] = list(brand_perc_sales.keys())
        context['company_sales'] = list(brand_perc_sales.values())

        random_colors = []
        for _ in range(50):
            random_colors += [ str ("#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])) ]
        context['random_colors'] = random_colors

        return render(request, 'shopdash/order_sales.html', context)

order_sales_view = OrderSalesView.as_view()


class ProductListView(AdminAcessRequiredMixin, ListView):
    """
    Admin DashBoard: ListView to return the list of all product in Product table in database.
    """
    model = Product
    template_name = 'admin_all_product.html'

all_products_list= ProductListView.as_view()


class ProductUnderShopListView(AdminAcessRequiredMixin, ListView):
    """
    Admin Dashboard: Products Listed under particular seller i.e. ShopUser.
    """
    model = Product
    template_name = 'product_datatable.html'

    def get_queryset(self):
        """
        Modify Queryset.
        """
        seller = User.objects.get(id=self.kwargs['id'])
        object_list = Product.objects.filter(seller = seller)
        return object_list

product_under_shop_list_view = ProductUnderShopListView.as_view()


class PublishProductView(ShopUserAcessRequiredMixin, View):
    """ Publish Product """
    def get(self, request, id):
        """ change status to True """
        product = Product.objects.get(id = id)
        if not product.is_published:
            product.is_published = True
            product.save()

        return redirect(reverse_lazy('shopdashboard'))

publish_product_view = PublishProductView.as_view()


class RateProductUpdateView(CustomerAcessRequiredMixin, View):
    """ Provide rating """
    def get(self, request, id, rating):
        """ change status to True """
        product = Product.objects.get(id = id)

        product.rating += rating
        product.rating = product.rating/2
        product.save()

        return redirect(reverse_lazy('my_orders'))

rate_product_update_view = RateProductUpdateView.as_view()
