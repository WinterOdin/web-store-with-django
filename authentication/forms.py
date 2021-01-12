from django.forms import ModelForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class createUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'registerForm',}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'registerForm',}))
    class Meta:
        model   = User
        fields  = ['username', 'password1','password2','last_name','first_name']
        widgets ={
            'last_name'     :forms.TextInput(attrs={'class':'registerForm',}),
            'first_name'    :forms.TextInput(attrs={'class':'registerForm',}),
            
        }
    username  = forms.EmailField()
    username.widget.attrs.update({'class':'registerForm'})
    def save(self, commit=True):
        user = super(createUserForm, self).save(commit=False)
        user.email = user.username
        user.save()
        return user




class CustomPasswordResetForm(PasswordResetForm):
    email   = forms.EmailField(widget=forms.TextInput(attrs={'class':'registerForm','name':'email'}))
