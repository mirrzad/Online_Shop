from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):

    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(50)
        ]
    )
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}))
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز عبور'})
        )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('کلمه های عبور با یکدیگر مغایرت دارند.')


class LoginForm(forms.Form):

    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(50)
        ]
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )


class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(50)
        ]
    )


class ResetPasswordForm(forms.Form):

    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}))
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز عبور'})
        )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('کلمه های عبور با یکدیگر مغایرت دارند.')
