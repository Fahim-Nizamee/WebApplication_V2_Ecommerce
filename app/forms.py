from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext ,gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer

from app.models import Customer

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    password2 = forms.CharField(label=_("Confirm Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    email = forms.CharField(label=_("Email"),widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels={'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"),widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password  = forms.CharField(label=_("Old Password"), strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-Password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"),max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-Password','class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields = ['name','mobilenumber','country','city','zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),'mobilenumber':forms.TextInput(attrs={'class':'form-control'}),'country':forms.TextInput(attrs={'class':'form-control'}),'city':forms.TextInput(attrs={'class':'form-control'}),'zipcode':forms.NumberInput(attrs={'class':'form-control'})}
        