from django.forms import ModelForm
from django import forms
from .models import *


class CustomerShipp(ModelForm):
    invoice = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkboxInvoice',}),required=False)
    class Meta:
        model   = ShippingAddress
        fields  = [ 'city', 'country','zip_code','adress',
                    'phone','email','recipient','invoice','invoiceRecipient',
                    'invoiceAdress','invoiceZip','invoiceCity','invoiceNip','date_added','customer','order']
        widgets ={
          'city'            :forms.TextInput(attrs={'class':'shippForm'}),
          'country'         :forms.TextInput(attrs={'class':'shippForm'}),
          'zip_code'        :forms.TextInput(attrs={'class':'shippForm'}),
          'adress'          :forms.TextInput(attrs={'class':'shippForm'}),
          'email'           :forms.TextInput(attrs={'class':'shippForm'}),
          'recipient'       :forms.TextInput(attrs={'class':'shippForm'}),
          'phone'           :forms.TextInput(attrs={'class':'shippForm'}),
          'invoiceRecipient':forms.TextInput(attrs={'class':'shippForm'}),
          'invoiceAdress'   :forms.TextInput(attrs={'class':'shippForm'}),
          'invoiceZip'      :forms.TextInput(attrs={'class':'shippForm'}),
          'invoiceCity'     :forms.TextInput(attrs={'class':'shippForm'}),
          'invoiceNip'      :forms.TextInput(attrs={'class':'shippForm'}),
          'date_added'      :forms.TextInput(attrs={'type':'hidden'}),
          'customer'        :forms.TextInput(attrs={'type':'hidden'}),
          'order'           :forms.TextInput(attrs={'type':'hidden'}),
       }
  