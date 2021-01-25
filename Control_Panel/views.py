from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.defaultfilters import slugify
from mainpage.decorators import *
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *







@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['admin'])
def controlPanelView(request):
    user = request.user.customer

    return render(request,'adminPanel/controlPanel.html')




@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['admin'])
def controlPanelOrders(request):

    user = request.user.customer
    qs = OrderItem.objects.filter(order__complete=True) 
    products = qs.filter(order__customer=user)
    shipments = ShippingAddress.objects.all().order_by("-id");

    context={
        'shipments':shipments
    }

    return render(request,'adminPanel/controlPanelOrder.html', context)



@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['admin'])
def controlPanelOrdersDetail(request, pk):
    shipments = ShippingAddress.objects.get(transaction_id=pk)
    qs        = OrderItem.objects.filter(transaction_id=pk) 
    if request.method == "POST":
        processed = request.POST['processed']
        shipments.processed = processed
        shipments.save()

          #sending mail
        send_mail(
        'Zamówienie'+pk+' zostało przekazane do wysyłki',
        'Witaj',
        'cryptotechacc@gmail.com',
        [shipments.email],
        fail_silently=False,
)

        return redirect(controlPanelView)

    context={
        'shipments':shipments,
        'qs':qs,
      
    }

    return render(request,'adminPanel/controlPanelOrderDetail.html', context)

