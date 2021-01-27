
from django.forms import ModelForm
from django import forms
from .models import *
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import *

class AdminProduct(forms.ModelForm):
    recommend = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkboxInvoice',}),required=False)
    #description_pl = forms.CharField(widget=RichTextUploadingField())
    #description_en = forms.CharField(widget=RichTextUploadingField())
    tags            = TagField()
    pic1            = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'shippForm imgInput',}),required=False)
    pic2            = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'shippForm imgInput' ,}),required=False)
    pic3            = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'shippForm imgInput',}),required=False)
    pic4            = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'shippForm imgInput',}),required=False)
    class Meta:
        model   = Product
        fields  = [ 'recommend', 'title_en','title_pl',
                    'producent','stock','priceNormal','pricePromo','condition','description_pl',
                    'description_en','category','tags','pic1','pic2','pic3','pic4',]
      

        widgets ={
          'title_pl'        :forms.TextInput(attrs={'class':'shippForm'}),
          'title_en'        :forms.TextInput(attrs={'class':'shippForm'}),
          'producent'       :forms.TextInput(attrs={'class':'shippForm'}),
          'stock'           :forms.NumberInput(attrs={'class':'shippForm'}),
          'pricePromo'      :forms.NumberInput(attrs={'class':'shippForm'}),
          'priceNormal'     :forms.NumberInput(attrs={'class':'shippForm'}),
          'condition'       :forms.TextInput(attrs={'class':'shippForm'}),
          'description_pl'  :forms.Textarea(),
          'description_en'  :forms.Textarea(),
          'category'        :forms.Select(),
          'tags'            :forms.TextInput(attrs={'class':'shippForm'})
       }
  

class AdminCategory(forms.ModelForm):  
    class Meta:
        model   = Category
        fields  = ['category_pl','category_en']
    
        widgets ={
          'category_pl'        :forms.TextInput(attrs={'class':'shippForm'}),
          'category_en'        :forms.TextInput(attrs={'class':'shippForm'}),
       }
        

class AdminContractor(forms.ModelForm):    
    class Meta:
        model   = ShipmentMethod
        fields  = ['contractor','price']
    
        widgets ={
          'contractor'        :forms.TextInput(attrs={'class':'shippForm'}),
          'price'        :forms.NumberInput(attrs={'class':'shippForm'}),
       }
        

class AdminHelp(forms.ModelForm):    
    class Meta:
        model   = HelpCategory
        fields  = ['category_pl','category_en', 'categoryIcon']
    
        widgets ={
          'category_pl'        :forms.TextInput(attrs={'class':'shippForm'}),
          'category_en'        :forms.TextInput(attrs={'class':'shippForm'}),
          'categoryIcon'       :forms.TextInput(attrs={'class':'shippForm'}),
       }
        
class AdminHelpContent(forms.ModelForm):    
    class Meta:
        model   = HelpCategoryContent
        fields  = ['category','helpTitle_en','helpTitle_pl', 'description_en','description_pl']
    
        widgets ={
          'category'          :forms.Select(),
          'helpTitle_en'      :forms.TextInput(attrs={'class':'shippForm'}),
          'helpTitle_pl'      :forms.TextInput(attrs={'class':'shippForm'}),
          'description_en'    :forms.Textarea(),
          'description_pl'    :forms.Textarea(),   
       }
        