from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from mainpage.models import *
from django.utils.translation import gettext as _
from .forms import *
from mainpage.decorators import *
from django.contrib.auth.decorators import login_required



def usersCart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all().order_by('id')
        context ={
        'items':items,
        'orders':order,
        }
     
    else:
        try:
            cart  = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        order = {'get_cart_total':0,} 
        items = []
        for i in cart:
            product = Product.objects.get(id=i)
            if product.priceNormal is None:
                total = (product.priceNormal * cart[i]['quantity'])
            else:
                total = (product.pricePromo  * cart[i]['quantity'])
            order['get_cart_total'] += total
            item = {
                'product':{
                    'id':product.id,
                    'recommend':product.recommend,
                    'title':product.title,
                    'condition ':product.condition,
                    'title':product.title,
                    'priceNormal':product.priceNormal,
                    'pricePromo':product.pricePromo,
                    'description':product.description,
                    'category':product.category,
                    'tags':product.tags,
                    'pic1':product.pic1,
                    'pic2':product.pic2,
                    'pic3':product.pic3,
                    'pic4':product.pic4,
                },
                'get_total':total,
                'quantity':cart[i]['quantity']
            }
            items.append(item)
    context ={
        'items':items,
        'orders':order,
    }
    return context




@login_required(login_url='login')
def orderView(request):
    cart     = usersCart(request)
    user = request.user.customer
    qs = OrderItem.objects.filter(order__complete=True) 
    products = qs.filter(order__customer=user)

    context={
        'products':products
    }
    context={**context, **cart}
    return render(request,'orders.html', context)

@login_required(login_url='login')
def orderViewDetail(request, pk):
    shipments = ShippingAddress.objects.get(transaction_id=pk)
    qs        = OrderItem.objects.filter(transaction_id=pk) 
    context={
        'shipments':shipments,
        'qs':qs,
    }
    return render(request,'detailAboutOrder.html', context)

@login_required(login_url='login')
def refundsView(request):

    context={}
    return render(request,'refunds.html', context)

@login_required(login_url='login')
def userView(request):

    cart     = usersCart(request)      
    userData = request.user 
    if request.method == "POST":
         userData.delete()
         return redirect("home")
    context={
        
    }
    context={**context, **cart}
    return render(request,'user.html', context)
