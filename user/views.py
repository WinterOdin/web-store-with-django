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
import logging
import stripe
from django.conf import settings

API_KEY = settings.STRIPE_PRIVATE_KEY
logger = logging.getLogger(__name__)

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





def orderView(request):
    cart     = usersCart(request)
    user = request.user.customer
    qs = OrderItem.objects.filter(order__complete=True) 
    products = qs.filter(order__customer=user).order_by('-date_added')
    
    context={
        'products':products
    }
    context={**context, **cart}
    return render(request,'orders.html', context)


def orderViewDetail(request, pk):
    shipments = ShippingAddress.objects.get(transaction_id=pk)
    qs        = OrderItem.objects.filter(transaction_id=pk) 
    paymentType = PaymentType.objects.all()
    transaction_id = pk
    
    values = request.POST.copy()
    values['transaction_id'] = transaction_id
    values['email'] = shipments.email
    values['phone'] = shipments.phone
    values['adress'] = shipments.adress
    values['city'] = shipments.city
    values['country'] = shipments.country
    values['zip_code'] = shipments.zip_code
    request.session['values'] = values
   
    if request.method == "POST" and request.user.is_authenticated:
        
        if values['paymentType'] == "card":
                customer = request.user.customer
                emailUser = request.user.email
                stripe.api_key  = API_KEY
                payment_intent  = stripe.PaymentIntent.create(
                    amount      = shipments.totalPrice*100,
                    currency    = 'pln',
                    payment_method_types = ['card'],
                    description = transaction_id
                )
                publicKey       = settings.STRIPE_PUBLIC_KEY
                secretKeyIntent = payment_intent.client_secret
                payment_intent_id = payment_intent.id

                context = {
                    'transaction_id':transaction_id,
                    'emailUser':emailUser,
                    'publicKey':publicKey,
                    'secretKeyIntent':secretKeyIntent,
                    'payment_intent_id':payment_intent_id,
                }
                return render(request, "cardPay.html" , context)


        elif values['paymentType'] == "p24":
                recepient   = shipments.recipient
                city        = shipments.city
                country     = shipments.country
                postal_code = shipments.zip_code
                adress      = shipments.adress
                email       = shipments.email
                customer = request.user.customer
                emailUser = request.user.email
                stripe.api_key  = API_KEY

                payment_intent  = stripe.PaymentIntent.create(
                    amount      = shipments.totalPrice*100,
                    currency    = 'pln',
                    payment_method_types = ['p24'],
                    description = transaction_id,
                )

                publicKey       = settings.STRIPE_PUBLIC_KEY
                secretKeyIntent = payment_intent.client_secret
                payment_intent_id = payment_intent.id

                context = {
                    'transaction_id':transaction_id,
                    'emailUser':emailUser,
                    'publicKey':publicKey,
                    'secretKeyIntent':secretKeyIntent,
                    'payment_intent_id':payment_intent_id,
                    'recepient':recepient,
                    'city':city,
                    'country':country,
                    'postal_code':postal_code,
                    'adress':adress,
                    'email':email,
                }
                return render(request, "p24Pay.html" , context)
    context={
        'shipments':shipments,
        'qs':qs,
        'paymentType':paymentType,
    }
    return render(request,'detailAboutOrder.html', context)


def refundsView(request):

    context={}
    return render(request,'refunds.html', context)

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
