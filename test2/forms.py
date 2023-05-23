from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class CustomerForm(ModelForm):
    """
    Form for creating or updating a Customer model.
    """
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']  # Exclude the 'user' field from the form


class OrderForm(ModelForm):
    """
    Form for creating or updating an Order model.
    """
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    """
    Form for creating a new User.
    Inherits from UserCreationForm provided by Django.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
