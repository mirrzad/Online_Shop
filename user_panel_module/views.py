from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView
from account_module.models import User
from order_module.models import Order, OrderDetail
from user_panel_module.forms import EditProfileModelForm, ChangePasswordForm


@method_decorator(login_required, name='dispatch')
class UserPanelDashboardView(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard.html'


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_profile_form = EditProfileModelForm(instance=current_user)
        context = {
            'form': edit_profile_form,
            'user': current_user
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
            context = {
                'form': edit_form
            }
            return render(request, 'user_panel_module/edit_profile_page.html', context)
        context = {
            'form': edit_form
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request):
        form = ChangePasswordForm()
        context = {'form': form}
        return render(request, 'user_panel_module/change_password_page.html', context)

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(id=request.user.id).first()
            if user.check_password(form.cleaned_data.get('current_password')):
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form.add_error('password', 'رمز عبور اشتباه است.')
        context = {'form': form}
        return render(request, 'user_panel_module/change_password_page.html', context)


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'user_panel_module/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        query = super().get_queryset()
        request = self.request
        query = query.filter(user_id=request.user.id, is_paid=True)
        return query


@login_required
def user_panel_menu_component(request):
    return render(request, 'user_panel_module/components/user_panel_menu_component.html')


@login_required
def user_basket(request):
    user_order, create = Order.objects.prefetch_related('orderdetails').get_or_create(
        is_paid=False, user_id=request.user.id)
    total_amount = user_order.calculate_total_amount()

    context = {
        'order': user_order,
        'sum': total_amount,
    }
    return render(request, 'user_panel_module/user_basket.html', context)


@login_required
def order_detail(request, order_id):
    order = Order.objects.prefetch_related('orderdetails').filter(id=order_id, user_id=request.user.id).first()
    if order is None:
        return Http404('سفارش مورد ظر وجود ندارد.')
    return render(request, 'user_panel_module/order_detail.html', {'order': order})


@login_required
def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'detail_id_not_found',
            'title': 'اعلان',
            'text': 'شناسه محصول مورد نطر به درستی وارد نشده است.',
            'icon': 'error',
            'confirmButtonText': 'باشه'
        })
    delete_count, delete_dict = OrderDetail.objects.filter(
        id=detail_id, order__is_paid=False, order__user_id=request.user.id).delete()

    if delete_count == 0:
        return JsonResponse({
            'status': 'detail_order_not_found',
            'title': 'اعلان',
            'text': 'هیچ محصولی با این شناسه وجود ندارد.',
            'icon': 'error',
            'confirmButtonText': 'باشه'
        })

    user_order, create = Order.objects.prefetch_related('orderdetails').get_or_create(
        is_paid=False, user_id=request.user.id)

    total_amount = user_order.calculate_total_amount()

    context = {
        'order': user_order,
        'sum': total_amount,
    }

    return JsonResponse({
        'status': 'success',
        'data': render_to_string('user_panel_module/user_basket.html', context)
    })


@login_required
def change_order_quantity(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'detail_id_state_not_found',
        })

    order_detail = OrderDetail.objects.filter(
        id=detail_id, order__user_id=request.user.id, order__is_paid=False).first()
    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found',
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()

    else:
        return JsonResponse({
            'status': 'state_invalid',
        })


    user_order, create = Order.objects.prefetch_related('orderdetails').get_or_create(
        is_paid=False, user_id=request.user.id)

    total_amount = user_order.calculate_total_amount()

    context = {
        'order': user_order,
        'sum': total_amount,
    }

    return JsonResponse({
        'status': 'success',
        'data': render_to_string('user_panel_module/user_basket.html', context)
    })
