from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","username","email","password1","password2"]
        labels={
            "first_name":'Your Name',
            "password1":'password',
            "password2":'confirm password'

        }
        widgets = {
            "first_name": forms.TextInput( attrs={"class": "form-control form-label"}),
            "email": forms.TextInput(attrs={"class": "form-control form-label"}),
            "username": forms.TextInput(attrs={"class": "form-control form-label"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control form-label"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control form-label"}),
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-label","placeholder":"Enter Username"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control form-label","placeholder":"Enter Username"}))

class PlaceOrderForm(forms.Form):
    address=forms.CharField(widget=forms.Textarea)
    product=forms.CharField(max_length=120)