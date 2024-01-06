from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.forms import TextInput, Textarea
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email"
        ]


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'min': '14', 'max': '100'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    city = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "age",
            "avatar",
            "city",
            "address",
        ]


class LogInForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'



