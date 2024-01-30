from django.contrib.auth import login, logout
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from utils.email import send_email
from .models import User
from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from django.utils.crypto import get_random_string


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        context = {'register_form': register_form}
        return render(request, 'account_module/register_page.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            if User.objects.filter(email__iexact=user_email).exists():
                register_form.add_error('email', 'ایمیل تکراری است.')
            else:
                new_user = User(email=user_email,
                                email_activation_code=get_random_string(72),
                                is_active=False, username=user_email)

                new_user.set_password(user_password)
                new_user.save()
                send_email('فعالسازی حساب ', new_user.email, {'user': new_user}, 'emails/active_account.html')
                return redirect(reverse('login_page'))
        context = {'register_form': register_form}
        return render(request, 'account_module/register_page.html', context)


class LoginView(View):

    def get(self, request):
        login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request, 'account_module/login_page.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                password = user.check_password(user_password)
                if password:
                    login(request, user)
                    return redirect(reverse('index_page'))
                else:
                    login_form.add_error('email', 'کاربری با این مشخصات یافت نشد.')
            else:
                login_form.add_error('email', 'کاربری با این مشخصات یافت نشد.')

        context = {'login_form': login_form}
        return render(request, 'account_module/login_page.html', context)


class ActivationView(View):

    def get(self, request, email_activation_code):
        user = User.objects.filter(email_activation_code__iexact=email_activation_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_activation_code = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))
            else:
                return render(request, '/')
        raise Http404


class ForgotPassword(View):

    def get(self, request):
        forgot_password_form = ForgotPasswordForm()
        context = {'forgot_pass_form': forgot_password_form}
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request):
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            user_email = forgot_password_form.cleaned_data.get('email')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی رمز عبور', user.email, {'user': user}, 'emails/reset_password.html')
                return redirect(reverse('login_page'))

        context = {'forgot_pass_form': forgot_password_form}
        return render(request, 'account_module/forgot_password.html', context)


class ResetPassword(View):
    def get(self, request, active_code):
        user = User.objects.filter(email_activation_code__iexact=active_code).first()
        if user is not None:
            reset_password_form = ResetPasswordForm()
            context = {'reset_pass_form': reset_password_form, 'user': user}
            return render(request, 'account_module/reset_password.html', context)
        else:
            return redirect(reverse('login_page'))

    def post(self, request, active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user = User.objects.filter(email_activation_code__iexact=active_code).first()
        if reset_password_form.is_valid():
            if user is not None:
                new_user_pass = reset_password_form.cleaned_data.get('password')
                user.set_password(new_user_pass)
                user.email_activation_code = get_random_string(72)
                user.is_active = True
                user.save()
                return redirect(reverse('login_page'))
            else:
                return redirect(reverse('login_page'))

        context = {'reset_pass_form': reset_password_form, 'user': user}
        return render(request, 'account_module/reset_password.html', context)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))


