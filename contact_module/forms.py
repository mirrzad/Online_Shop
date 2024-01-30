from django import forms

from contact_module.models import ContactUs


class ContactUsForms(forms.Form):
    full_name = forms.CharField(label='نام و نام خانوادگی', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی'
        }),
        max_length=10,
        error_messages={'required': 'asdsadlaks;dlkasd'},
    )

    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        })
    )
    title = forms.CharField(label='موضوع', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'موضوع'
        })
    )
    message = forms.CharField(label='متن پیام', widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'متن پیام',
            'id': 'message'
        })
    )


class ProfileImageForm(forms.Form):
    profile_image = forms.ImageField(label='عکس کاربر')


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['title', 'full_name', 'email', 'message']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'متن پیام',
                'id': 'message'
            }),

        }
        error_messages = {
            'full_name': {
                'required': 'لطفا نام و نام خانوادگی را وارد کنید.'
            },
            'email': {
                'required': 'لطفا ایمیل را وارد کنید.'
            }
        }



