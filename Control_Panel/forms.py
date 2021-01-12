from django import forms
from .models import *

class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','tags']
        