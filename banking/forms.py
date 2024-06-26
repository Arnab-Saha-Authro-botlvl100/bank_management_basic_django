from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'balance', 'account_holder_name']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'balance', 'account_holder_name']