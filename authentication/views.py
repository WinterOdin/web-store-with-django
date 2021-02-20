from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from mainpage.decorators import *
from django.utils.translation import gettext as _



@unauthenticated_user
def loginView(request, *args, **kwargs):
    errorMsg = _("Hasło bądź email jest niepoprawne")
    if request.user.is_authenticated:
        return redirect('products')
    else:
    
        if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('products')
            else:
                messages.error(request, errorMsg, extra_tags='login')
                return redirect('login')

        context={}
    
    return render(request,'login.html', context )

@unauthenticated_user
def registerView(request, *args, **kwargs):
    succesMsg = _("Twoje konto zostało stworzone, zaloguj się")
    if request.user.is_authenticated:
        return redirect('products')
    else:
        forms = createUserForm()
        if request.method == 'POST':
            forms = createUserForm(request.POST)
            if forms.is_valid():
                user = forms.save() 
                group = Group.objects.get(name="customer")
                user.groups.add(group)
                Customer.objects.create(
                    user=user
                )
                messages.success(request, succesMsg,extra_tags='signup' )
                return redirect('login')
    
        context={
            'forms'     :forms,
         }

    return render(request,'register.html', context)


def logoutUser(request):
	logout(request)
	return redirect('products')