from django.forms import ModelForm
from django import forms
from .models import ShippingAddress


class CustomerShipp(ModelForm):
    invoice = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkboxInvoice',}),required=False)
    
    class Meta:
        model   = ShippingAddress
        fields  = [ 'city', 'country','zip_code','adress',
                    'phone','email','recipient','invoice','invoiceRecipient',
                    'invoiceAdress','invoiceZip','invoiceCity','invoiceNip','transaction_id','customer','order','shipType']
        exclude =['processed', 'date_added']

        widgets ={
          'city'            :forms.TextInput(attrs={'class':'shippForm'}),
          'country'         :forms.TextInput(attrs={'class':'shippForm'}),
          'zip_code'        :forms.TextInput(attrs={'class':'shippForm'}),
          'adress'          :forms.TextInput(attrs={'class':'shippForm'}),
          'email'           :forms.TextInput(attrs={'class':'shippForm','type':'email'}),
          'recipient'       :forms.TextInput(attrs={'class':'shippForm'}),
          'phone'           :forms.TextInput(attrs={'class':'shippForm'}),
          'invoiceRecipient':forms.TextInput(attrs={'class':'shippForm'}),
          'invoiceAdress'   :forms.TextInput(attrs={'class':'shippForm'}),
          'invoiceZip'      :forms.TextInput(attrs={'class':'shippForm'}),
          'invoiceCity'     :forms.TextInput(attrs={'class':'shippForm'}),
          'invoiceNip'      :forms.TextInput(attrs={'class':'shippForm'}),
          'transaction_id'  :forms.TextInput(attrs={'type':'hidden'}),
          'customer'        :forms.TextInput(attrs={'type':'hidden'}),
          'order'           :forms.TextInput(attrs={'type':'hidden'}),
         
       }
  