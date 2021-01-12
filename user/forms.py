from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class customerUpdate(ModelForm):
    class Meta:
        model   = ShippingAddress
        fields  = ['city', 'country','zip_code','adress','phone',]
        exclude = ['customer','order','date_added']
        widgets ={
          'city'      :forms.TextInput(attrs={'class':'updateForm',}),
          'country'   :forms.TextInput(attrs={'class':'updateForm',}),
          'zip_code'  :forms.TextInput(attrs={'class':'updateForm',}),
          'adress'    :forms.TextInput(attrs={'class':'updateForm',}),
          'phone'     :forms.TextInput(attrs={'class':'updateForm',}),
            
       }
  