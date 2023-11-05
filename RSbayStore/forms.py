from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.forms import TextInput, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
            "email"
        ]


class LogInForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'



