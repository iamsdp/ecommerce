"""
Store Views
"""
#pylint: disable=line-too-long, no-member, no-self-use, too-many-ancestors
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django_filters.views import FilterView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView

from products.models import Product
from orders.models import Order, Item, Cart
from profiles.custom_mixin import CustomerAcessRequiredMixin

from .models import Wishlist
from .filters import StoreFilter


class StoreLoginRedirectView(View):
    """
    Redirect to appropriate account page after login on store.
    """
    def get(self, request):
        """ redirect """
        if self.request.user.is_authenticated:
            if self.request.user.is_shopuser:
                return redirect('shopdashboard')
            if self.request.user.is_customer:
                return redirect('store')
            if self.request.user.is_staff:
                return redirect('admin_dashboard')
        return redirect('store')

store_login_redirect_view = StoreLoginRedirectView.as_view()


class AddtoWishList(CustomerAcessRequiredMixin, View):
    """
    Add to Wish list
    """
    def get(self, request, id):
        """
        GET Method
        """
        product = Product.objects.get(id = id)
        already_in_wishlist = Wishlist.objects.filter(customer = request.user, product = product)

        if already_in_wishlist:
            return HttpResponse('<h3>Item is already added to your wishlist.</h3>')

        wishlist_items = Wishlist(customer=request.user, product=product)
        wishlist_items.save()

        return redirect("wish_list_view")

add_to_wishlist = AddtoWishList.as_view()


class WishListView(CustomerAcessRequiredMixin, ListView):
    """ Wish List """
    model = Wishlist
    template_name = 'wishlist/wish_list_view.html'

    def get_queryset(self, *args, **kwargs):
        """ Modify qs """
        object_list = super().get_queryset(*args, **kwargs)
        object_list = object_list.filter(customer = self.request.user)

        return object_list

wish_list_view = WishListView.as_view()


class WishListDeleteView(CustomerAcessRequiredMixin, DeleteView):
    """ Delete an Item from Wish List """
    model = Wishlist
    template_name = 'wishlist/wish_list_delete.html'
    success_url = reverse_lazy('wish_list_view')

wish_list_delete_view = WishListDeleteView.as_view()


class CheckOut(CustomerAcessRequiredMixin, View):
    """ Place order """
    def get(self, request):
        """ GET Method """
        customer = request.user
        cart = Cart.objects.filter(customer=customer)
        order = Order(customer=customer)
        order.save()

        for item in cart:
            order_item = Item(order=order,
                            product=item.product,
                            quantity=item.quantity,
                            price=item.product.price,
                            )
            order_item.status=order_item.Status.PAID
            order_item.save()
            total_price_per_item = int(item.product.price)*int(item.quantity)
            order.total_amount += total_price_per_item

        order.status = order.Status.PAID
        order.address = customer.address
        order.phone = customer.phone
        order.save()

        cart.delete()
        return redirect('my_orders')

check_out = CheckOut.as_view()


class StoreFilterView(FilterView):
    """
    View Filter
    """
    model = Product
    template_name = 'store_product_filter.html'
    paginate_by = 3
    context_object_name = 'object_list'

    def get_queryset(self):
        """ return Filtered query set """
        object_list = super().get_queryset()
        object_list = object_list.filter(is_published = True)
        object_list_filter = StoreFilter(self.request.GET, queryset=object_list)
        return object_list_filter.qs

store_filter_view = StoreFilterView.as_view(filterset_class=StoreFilter,
        template_name='store_product_filter.html')
