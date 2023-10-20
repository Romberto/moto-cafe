from django import forms
from django.contrib.auth.models import User

from product.models import Product


class AuthForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "название категории"
        self.fields['username'].widget.attrs['class'] = 'form-control mb-2 w-75'
