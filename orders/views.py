"""
Orders' Views
"""
# pylint: disable=no-member, too-many-ancestors, no-self-use, line-too-long
import random
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView

from profiles.models import User
from products.models import Product, Category, Company
from profiles.custom_mixin import  (CustomerAcessRequiredMixin, AdminAcessRequiredMixin,
                                    ShopUserAcessRequiredMixin)

from .models import Cart, Order, Item


class OrderListView(AdminAcessRequiredMixin, ListView):
    """
    Return the list of all the orders. Only Admin can access.
    """
    model = Item
    template_name = 'admin_all_orders.html'

order_list_view = OrderListView.as_view()


class AddtoCartView(CustomerAcessRequiredMixin, View):
    """
    Add items to the cart.
    """
    def get(self, request, id):
        """
        GET
        """
        product_id = id
        product = Product.objects.get(id=product_id)
        item_already_in_cart = Cart.objects.filter(customer=self.request.user, product=product)
        if item_already_in_cart:
            item = Cart.objects.get(customer=self.request.user, product=product)
            item.quantity += 1
            item.save()
        else:
            cart_items = Cart(customer=self.request.user, product=product)
            cart_items.save()

        return redirect("cart_list_view")

add_to_cart_view =AddtoCartView.as_view()


class RemoveItemFromCartView(CustomerAcessRequiredMixin, View):
    """
    Remove a product one quntity at a time.
    """
    def get(self, request, id):
        """
        GET Method
        """
        product_id = id
        product = Product.objects.get(id=product_id)
        item_already_in_cart = Cart.objects.filter(customer=self.request.user, product=product)
        if item_already_in_cart:
            item = Cart.objects.get(customer=self.request.user, product=product)
            if int(item.quantity) > 1:
                item.quantity -= 1
                item.save()
            elif int(item.quantity) == 1:
                redirect('cart_delete_view', pk= item.product.pk)

        return redirect("cart_list_view")

remove_item_from_cart_view = RemoveItemFromCartView.as_view()


class CartListView(CustomerAcessRequiredMixin, ListView):
    """
    Customer can see the items added.
    """
    model = Cart
    template_name = 'cart/cart_list.html'
    def get_queryset(self, *args, **kwargs):
        """
        Modify Query set
        """
        object_list = super().get_queryset(*args, **kwargs)
        object_list = object_list.filter(customer = self.request.user)
        return object_list

cart_list_view = CartListView.as_view()


class CartDeleteView(CustomerAcessRequiredMixin, DeleteView):
    """
    Remove all quntities added to Cart for a particular product.
    """
    model = Cart
    template_name = 'cart/delete.html'
    success_url = reverse_lazy('cart_list_view')

cart_delete_view = CartDeleteView.as_view()


class OrderUnderShopListView(AdminAcessRequiredMixin, ListView):
    """
    Orders Listed under particular seller i.e. ShopUser.
    """
    model = Item
    template_name = 'order_datatable.html'

    def get_queryset(self):
        """
        Modify queryset
        """
        seller = User.objects.get(id = self.kwargs['id'])
        products = Product.objects.filter(seller = seller)
        object_list = Item.objects.filter(product__in = products)
        return object_list

order_under_shop_list_view = OrderUnderShopListView.as_view()


class OrderUnderCustomerListView(AdminAcessRequiredMixin, ListView):
    """
    Orders placed by a particular customer.
    """
    model = Item
    template_name = 'order_datatable.html'
    def get_queryset(self):
        """
        Modify Query Set.
        """
        customer = User.objects.get(id = self.kwargs['id'])
        object_list = Item.objects.filter(order__customer = customer )
        return object_list

order_under_customer_list_view = OrderUnderCustomerListView.as_view()


class AdminSalesPercentView(AdminAcessRequiredMixin, View):
    """
    Admin can see the sales in percentage on Admin Dashboard.
    """
    def get(self, request):
        """
        GET Method.
        """
        total_products_sold = Item.objects.filter(status='COMPLTD')

        count_total_products_sold = 0
        for item in total_products_sold:
            count_total_products_sold += item.quantity

        seller_list = User.objects.filter(user_type = self.request.user.UserType.SHOPUSER, is_active = bool(True))
        sale_by_shop = {}
        for seller in seller_list:
            products = Product.objects.filter(seller = User.objects.get(id=seller.id))
            order_items = total_products_sold.filter(product__in = products)
            count_order_items = 0
            for item in order_items:
                count_order_items += item.quantity
            sale_by_shop[str(seller)] = round((count_order_items/count_total_products_sold) *100, 2)

        sale_by_category = {}
        category_list = Category.objects.all()
        for category in category_list:
            cat_sales_count = 0
            product_under_cat = Product.objects.filter(category__id = category.id)
            for item in  total_products_sold.filter(product__in=product_under_cat):
                cat_sales_count += item.quantity
            sale_by_category[str(category)] = round((cat_sales_count/count_total_products_sold) *100, 2)

        sale_by_company = {}
        company_list = Company.objects.all()
        for company in company_list:
            company_sales_count = 0
            product_under_company = Product.objects.filter(company = company)
            for item in  total_products_sold.filter(product__in=product_under_company):
                company_sales_count += item.quantity
            sale_by_company[str(company)] = round((company_sales_count/count_total_products_sold) *100, 2)

        context = {}
        context ['total_products_sold'] = count_total_products_sold

        context['sale_by_shop_label'] = list(sale_by_shop.keys())
        context['sale_by_shop_data'] = list(sale_by_shop.values())

        context['sale_by_cat_label'] = list(sale_by_category.keys())
        context['sale_by_cat_data'] = list(sale_by_category.values())

        context['sale_by_company_label'] = list(sale_by_company.keys())
        context['sale_by_company_data'] = list(sale_by_company.values())

        random_colors = []
        for _ in range(50):
            random_colors += [ str ( "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])) ]
        context['random_colors'] = random_colors

        return render(request, 'admin_sales_perctage.html', context)

admin_sales_percentage_view = AdminSalesPercentView.as_view()


class AdminAnalyticsShopView(AdminAcessRequiredMixin, View):
    """ Analytics for indivisual Shop """

    def get(self, request, id):
        all_products = Product.objects.all()
        all_order_items = Item.objects.all()

        seller = User.objects.get(id=id)

        products_listed_under_seller = all_products.filter(seller=seller)
        item_sold_by_seller_compltd = all_order_items.filter(product__in = products_listed_under_seller, status='COMPLTD')
        item_sold_by_seller_cancel = all_order_items.filter(product__in = products_listed_under_seller, status='CANCLED')
        item_sold_by_seller_paid = all_order_items.filter(product__in = products_listed_under_seller, status='PAID')

        context = {}
        context['seller'] = seller
        context['num_products_listed_under_seller'] = len(products_listed_under_seller)
        context['order_labels'] = ['Completed', 'Cancelled', 'Paid']
        context['order_data'] = [len(item_sold_by_seller_compltd), len(item_sold_by_seller_cancel), len(item_sold_by_seller_paid)]
        context['order_item_sold_date_label'] = [(item.order.created_at).strftime("%x") for item in item_sold_by_seller_compltd]
        context['order_item_sold_date_data'] = [item.quantity for item in item_sold_by_seller_compltd]
        context['count_published_products'] = len(products_listed_under_seller.filter(is_published = bool(True)))
        context['count_drafted_products'] = len(products_listed_under_seller.filter(is_published = bool(False)))

        return render(request, 'admin_analytics_shop.html', context)

admin_analytics_shop_view = AdminAnalyticsShopView.as_view()


class MyOrdersView(CustomerAcessRequiredMixin, View):
    """
    Show the orders placed by particular customer.
    """

    def get(self, request):
        """Query Set"""
        object_list = Item.objects.all()
        user = User.objects.get(id = self.request.user.id)
        order = Order.objects.filter(customer = user)
        object_list = object_list.filter(order__in = order)

        orders_data = {}
        for ord in order:
            orders_data[ord] = Item.objects.filter(order = ord)

        context = {}
        context['orders_data'] = orders_data

        return render(request, 'my_orders.html', context)

my_orders = MyOrdersView.as_view()


class UpdateOrderView(CustomerAcessRequiredMixin, View):
    """
    Update the order details: Address, Phone Or Cancel the order item.
    """
    def post(self, request):
        """ POST: Update order details """
        status = request.POST.get('status')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        item_id = request.POST.get('Order_Id')
        obj = Item.objects.get(id = item_id)
        order = Order.objects.get(id = obj.order.id)

        if status == 'cancel':
            print("canceling Order !!!")
            obj.status = obj.Status.CANCELLED
            obj.save()
            item_price = obj.quantity * obj.price
            order.total_amount -= item_price
            order.save()
        if address:
            print("Updating Address !!!")
            order.address = address
            order.save()
        if phone:
            print("Updating Phone number !!!")
            order.phone = phone
            order.save()

        return redirect('my_orders')

update_order_view = UpdateOrderView.as_view()


class OrderStatusUpdateView(ShopUserAcessRequiredMixin, View):
    """ Seller will update status of order """
    def get(self, request, id):
        """ Change order item status """
        item = Item.objects.get(id = id)
        item.status = item.Status.COMPLETED
        item.save()
        return redirect('customer_order')

order_status_update_view = OrderStatusUpdateView.as_view()
