"""user app forms config"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """user registration form"""
    email = forms.EmailField()

    class Meta:
        """metadata"""
        model = User
        fields = ["username", "email", "password1", "password2"]
