
from django.forms import ModelForm
from django import forms
from .models import *
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

class AdminProduct(forms.ModelForm):
    recommend = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkboxInvoice',}),required=False)
    description_pl = forms.CharField(widget=RichTextUploadingField())
    description_en = forms.CharField(widget=RichTextUploadingField())
    #tags           = forms.CharField(widget=TaggableManager() )
    pic1            :forms.ImageField()
    pic2            :forms.ImageField()
    pic3            :forms.ImageField()
    pic4            :forms.ImageField()

    class Meta:
        model   = Product
        fields  = [ 'recommend', 'title_en','title_pl',
                    'producent','stock','priceNormal','pricePromo','description_pl',
                    'description_en','category','tags','pic1','pic2','pic3','pic4']
      

        widgets ={
          'title_pl'        :forms.TextInput(attrs={'class':'shippForm'}),
          'title_en'        :forms.TextInput(attrs={'class':'shippForm'}),
          'recommend'       :forms.Select(),
          'producent'       :forms.TextInput(attrs={'class':'shippForm'}),
          'stock'           :forms.NumberInput(attrs={'class':'shippForm'}),
          'pricePromo'      :forms.NumberInput(attrs={'class':'shippForm'}),
          'priceNormal'     :forms.NumberInput(attrs={'class':'shippForm'}),
          #'description_pl'  :forms.Textarea(),
          #'description_en'  :forms.Textarea(),
          'category'        :forms.Select(),
          'tags'            :forms.TextInput(attrs={'class':'shippForm'}),

         
       }
  
        


