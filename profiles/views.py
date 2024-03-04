"""
Profiles Views
"""
from django.core import mail
from django.views import View
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, FormView

from bootstrap_modal_forms.generic import BSModalUpdateView
from .custom_mixin import CustomerAcessRequiredMixin, AdminAcessRequiredMixin

from .models import User
from .admin import UserChangeForm
from .forms import ShopUserSignUpForm, ShopUserUpdateModalForm,CreateShopByAdminForm


#pylint: disable=line-too-long, no-member, no-self-use, too-many-ancestors
class LoginRedirectView(LoginRequiredMixin, View):
    """
    Redirect to appropriate account page.
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

login_redirect_view = LoginRedirectView.as_view()


class UserAccountSettingView(View):
    """
    Redirect User to appropriate user account setting page.
    """
    def get(self, request):
        """ GET redirect """
        if self.request.user.is_authenticated:
            if self.request.user.is_shopuser:
                return redirect('shop_user_dashboard')
            if self.request.user.is_staff:
                return redirect('admin_dashboard')
            if self.request.user.is_customer:
                return render(request, 'customer_settings.html')

        return redirect(reverse('store'))

user_account_setting_view = UserAccountSettingView.as_view()


class UserUpdateView(UpdateView):
    """ Update customer Data """
    model = User
    form_class = UserChangeForm
    template_name = 'userdata_update.html'
    success_url = reverse_lazy("login_redirect_view")

    def get_object(self, queryset=None):
        return self.request.user

user_update_view = UserUpdateView.as_view()


class ShopUserRegisterForm(FormView):
    """ Shop User Registration Form """
    form_class = ShopUserSignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy("store")

    def form_valid(self, form):
        """ Customuzation in form submission """
        user = form.save()
        user.refresh_from_db()
        user.email = form.cleaned_data.get('email')
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.date_of_birth =form.cleaned_data.get('date_of_birth')
        user.gender =  form.cleaned_data.get('gender')
        user.address = form.cleaned_data.get('address')
        user.user_type = user.UserType.SHOPUSER
        user.is_active = False
        user.save()

        subject = 'Shop Account Activation Request'
        from_email = 'spatil@deqode.com'
        to_email = 'spatil@deqode.com'
        username = user.email
        abs_url = self.request.build_absolute_uri(reverse('activate_shop', kwargs={'pk':user.pk}))
        context = {'username': username, 'url': abs_url}
        html_message = render_to_string('email/email.html', context)
        plain_message = strip_tags(html_message)
        mail.send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
        return super().form_valid(form)

shop_user_register_form = ShopUserRegisterForm.as_view()


class ActivateShopView(AdminAcessRequiredMixin, DetailView):
    """ Admin can activate Shop User account request """
    model = User
    template_name = 'activate_shop.html'

    def get(self, request, *args, **kwargs):
        """ Link Deactivation logic """
        user = User.objects.get(pk=self.kwargs['pk'])

        if not user.is_active and not user.is_disabled_by_admin:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

        return HttpResponse("<h3>Dear Admin, This Link is expired. !!!<h3>")

activate_shop = ActivateShopView.as_view()


class ActionActivateShop(AdminAcessRequiredMixin, View):
    """ Activate Shop User """
    def get(self, request, id):
        """ set status - Active """
        shopuser = User.objects.get(id = id)
        if not shopuser.is_active and not shopuser.is_disabled_by_admin:
            shopuser.is_active = True
            shopuser.save()
            return HttpResponse("<h1>User is now activated...!!!</h1>")

action_activate_shop = ActionActivateShop.as_view()


class ActionRejectShopView(AdminAcessRequiredMixin, View):
    """ Reject Shop User Activation Request """
    def post(self, request, id):
        """ Disable user from database """        
        reject_note = request.POST.get('reject_note')
        shopuser = User.objects.get(id = id)
        if not shopuser.is_active and not shopuser.is_disabled_by_admin:
            shopuser.rejection_note = reject_note
            shopuser.is_disabled_by_admin = True
            shopuser.save()
            return HttpResponse("<h1>Shop Registration request rejected successfully.</h1>")

action_reject_shop_view = ActionRejectShopView.as_view()



class RegisterRequestListView(AdminAcessRequiredMixin, ListView):
    """
    Admin: List of pending approval request of Shop users.
    """
    model = User
    template_name = 'shop_register_list.html'

    def get_queryset(self, *args, **kwargs):
        """ qs """
        object_list = super().get_queryset(*args, **kwargs)
        object_list = object_list.filter(user_type = self.request.user.UserType.SHOPUSER, is_active = bool(False), is_disabled_by_admin= bool(False))
        return object_list

register_request_list = RegisterRequestListView.as_view()


class AdminDashBoard(AdminAcessRequiredMixin, ListView):
    """ Admin Dashboard View """
    model = User
    template_name = 'admin_dashboard.html'

    def get_queryset(self, *args, **kwargs):
        """ qs """
        object_list = super().get_queryset(*args, **kwargs)
        object_list = object_list.filter(user_type = self.request.user.UserType.SHOPUSER)
        return object_list

admin_dashboard = AdminDashBoard.as_view()


class CustomerListView(AdminAcessRequiredMixin, ListView):
    """
    List of all the customers (Users of user_type: customer).
    """
    model = User
    template_name = 'customer-admin/customer_admin.html'

    def get_queryset(self, *args, **kwargs):
        """ qs """
        object_list = super().get_queryset(*args, **kwargs)
        object_list = object_list.filter(user_type=self.request.user.UserType.CUSTOMER)
        return object_list

all_customer_list = CustomerListView.as_view()


class CreateShopByAdmin(AdminAcessRequiredMixin, CreateView):
    """
    Admin can create a shop from Admin Dashboard.
    """
    form_class = CreateShopByAdminForm
    model = User
    template_name = 'admin_create_shop.html'
    success_url = reverse_lazy("admin_dashboard")

    def form_valid(self, form):
        """ set user tyep """
        form.instance.user_type = self.request.user.UserType.SHOPUSER
        return super().form_valid(form)

create_shop_by_admin = CreateShopByAdmin.as_view()


class DeleteShopByAdmin(AdminAcessRequiredMixin, View):
    """ Delete shop from admin dashboard """
    def post(self, request):
        """ delete shop """
        shop_id = request.POST.get('Object')
        shop = User.objects.filter(id = shop_id)
        shop.delete()
        return redirect('admin_dashboard')

delete_shop_by_admin = DeleteShopByAdmin.as_view()


class UpdateShopByAdminView(AdminAcessRequiredMixin, BSModalUpdateView):
    """ Update shop from admin dashboard """
    model = User
    template_name = 'modal_forms/update.html'
    form_class = ShopUserUpdateModalForm
    success_message = 'Success: Updated.'
    success_url = reverse_lazy('admin_dashboard')

update_shop_by_admin_view = UpdateShopByAdminView.as_view()


class UserDetailView(DetailView):
    """ Get user details """
    model = User
    template_name = 'user_detail.html'

user_detail_view = UserDetailView.as_view()
