from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from mainpage.models import *
from django.utils.translation import gettext as _
from .forms import *





def orderView(request):


    context={}
    return render(request,'orders.html', context)


def refundsView(request):



    context={}
    return render(request,'refunds.html', context)

def userView(request):
    cart     = usersCart(request)  
    
    userData = request.user.customer
    forms = customerUpdate(instance=userData)
    if request.method == "POST":
        forms = customerUpdate(request.POST, instance=userData)
        if forms.is_valid():
            forms.save()
    
    context={
        'userData':userData,
        'forms':forms
    }
    context={**context, **cart}
    return render(request,'user.html', context)
