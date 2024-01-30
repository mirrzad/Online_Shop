from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from account_module.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'عکس پروفایل'
        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='رمز عبور فعلی',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور فعلی',
            'class': 'form-control'
        }),
        validators=[validators.MaxLengthValidator(50)]
    )
    password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور جدید',
            'class': 'form-control'
        }),
        validators=[validators.MaxLengthValidator(50)]
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'تکرار رمز عبور جدید',
            'class': 'form-control'
        }),
        validators=[validators.MaxLengthValidator(50)]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('کلمه های عبور با یکدیگر مغایرت دارند.')