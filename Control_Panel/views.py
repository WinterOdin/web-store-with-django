from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.defaultfilters import slugify

from .models import *
from .forms import *
from taggit.models import Tag

def controlPanelView(request):
    tagsx    = Product.tags.all()
    current = request.user
    forms = AddProduct()
    if request.method == 'POST':
        forms = AddProduct(request.POST)
        if forms.is_valid():
            newforms = forms.save(commit=False)
            newforms.slug = slugify(newforms.title)
            newforms.save()
            forms.save_m2m()

    #a = current.customer.zip_code
    

    context={
        'tagsx':tagsx,
        'forms':forms,
    
    }
    return render(request,'controlPanel.html', context)



