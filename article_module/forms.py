from django import forms


class CommentForm(forms.Form):
    text = forms.CharField(label='متن نظر', widget=forms.Textarea(
        attrs={
            'placeholder': 'نظر شما...',
        })
    )

