from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class WaiterForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(WaiterForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].label = "Имя"
        self.fields['first_name'].widget.attrs['class'] = 'form-control mb-2 w-75'

        self.fields['last_name'].label = "Фамилия"
        self.fields['last_name'].widget.attrs['class'] = 'form-control mb-2 w-75'


class CustomCreateUser(UserCreationForm):


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(CustomCreateUser, self).__init__(*args, **kwargs)

        self.fields['username'].label = "UserName"
        self.fields['username'].widget.attrs['class'] = 'form-control mb-2 w-75'

