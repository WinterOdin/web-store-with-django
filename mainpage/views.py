from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


from django.conf import settings
from django.db.models import Q
from taggit.models import Tag
from .decorators import *

from .models import *
from .forms import *
import datetime
import logging
import stripe
import json



API_KEY = settings.STRIPE_PRIVATE_KEY
logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def stripe_webhooks(request):

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SIGNING_KEY
        )
        logger.info("Event constructed correctly")
    except ValueError:
        # Invalid payload
        logger.warning("Invalid Payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        logger.warning("Invalid signature")
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'charge.succeeded':
        # object has  payment_intent attr
       pass

    return HttpResponse(status=200)








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

def searchQueryset(query):
    queryset = []
    if query is not None:
        queries  = query.split(" ")
        for x in queries:
            products = Product.objects.filter(
                Q(title__icontains=x)|Q(description__icontains=x)|Q(category__category__icontains=x)|Q(producent__icontains=x)|Q(id__icontains=x)
            ).distinct()

            for product in products:
                queryset.append(product)
        return list(set(queryset)) 





def recommendedProducts(request):
    categoryList = Category.objects.all()
    tags         = Product.tags.all()
    formsMailing = MailingForm() 
    cart         = usersCart(request)    
    productsInfo = Product.objects.filter(recommend=True).order_by('-id')[:6]
    newest       = Product.objects.all().order_by('-id')[:10]

    if request.method == "POST":
        query = request.POST.get('search_bar')    
        productsInfo = searchQueryset(query)
        context      = {
            'newest':newest,
            'query':query,
            'tags':tags,
            "productsInfo":productsInfo,
            'categoryList':categoryList,
            'formsMailing':formsMailing
        }
        context={**context, **cart}
        
        return render(request,'products.html', context)
    
    context      = {
        'newest':newest,
        'tags':tags,
        "productsInfo":productsInfo,
        'categoryList':categoryList,
        'formsMailing':formsMailing,
        }
    context={**context, **cart}

    return render(request,'products.html', context)



def tagListView(request, slug):
    formsMailing = MailingForm() 
    cart         = usersCart(request)  
    categoryList = Category.objects.all()
    tags         = Product.tags.all()
    SelectedTag  = get_object_or_404(Tag, slug=slug)
    productsInfo = Product.objects.filter(tags=SelectedTag)
    newest       = Product.objects.all().order_by('-id')[:10]
    context      = {
        'newest':newest, 
        "tags":tags,
        "productsInfo":productsInfo,
        'categoryList':categoryList,
        'formsMailing':formsMailing
    }
 
    return render(request,'products.html', context)




def categoryListView(request, category):

    formsMailing = MailingForm()  
    categoryList = Category.objects.all()
    productsInfo = Category.objects.get(category=category)
    productsInfo = Product.objects.filter(category=productsInfo)
    cart         = usersCart(request)  
    newest       = Product.objects.all().order_by('-id')[:10]
    tags         = Product.tags.all()
    categoryEmpty = 0
    print(categoryEmpty)
    context      = {
        'newest':newest, 
        "tags":tags,
        "productsInfo":productsInfo,
        'categoryList':categoryList,
        'categoryEmpty':categoryEmpty,
        'formsMailing':formsMailing,
        
    }
    context={**context, **cart}
    return render(request,'products.html', context)



def helpView(request):
    category = HelpCategory.objects.all()
    categoryInfo = HelpCategoryContent.objects.all()
    cart         = usersCart(request)
    formsMailing = MailingForm()  
    context         ={
       'category':category,
       'categoryInfo':categoryInfo,
       'formsMailing':formsMailing
    }
    context={**context, **cart}
    return render(request,'helpPage.html', context)


    
def productDetail(request, id):
    product         = Product.objects.get(id=id)
    productPictures = Product.objects.filter(id=id).values().first()
    cart            = usersCart(request)  
    formsMailing    = MailingForm()
    context         ={
        "product":product,
        "formsMailing":formsMailing 
    }
    context={**context, **cart}
    return render(request,'productDetail.html', context)



def cartDetail(request):
    newest       = Product.objects.all().order_by('-id')[:10]
    cart = usersCart(request)
    context         ={
        "newest":newest,
    }
    context={**context, **cart}
    return render(request,'cart.html',context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product  = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == "add":
        if orderItem.quantity < product.stock:
            orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    
    if orderItem.quantity <= 0 or action=='delete':
        orderItem.delete()

    return JsonResponse("item was added", safe=False)


@login_required(login_url='login')
def checkoutDetail(request):
    customer = request.user.customer
    cart    = usersCart(request)
    forms   = CustomerShipp(instance=customer)
    paymentType = PaymentType.objects.all()
    emailUser = request.user.email
    order, created  = Order.objects.get_or_create(customer=customer, complete=False)
    total           = int(order.get_cart_total)
    shipContractors = ShipmentMethod.objects.all()
    context ={
        'forms':forms,
        'emailUser':emailUser,
        'customer':customer,
        'shipContractors':shipContractors,
        'paymentType':paymentType
    }
    context={**context, **cart}
    return render(request,'checkout.html',context)





@login_required(login_url='login')
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    customer       = request.user.customer
    
    if request.method == "POST" and request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.transaction_id = transaction_id
        order.save()

        shipPrice = ShipmentMethod.objects.get(contractor = request.POST["contractor"])
        totalPrice = int(order.get_cart_total + shipPrice.price) 
     
        customerOnWebsite = request.user.customer
        values = request.POST.copy()
        values['transaction_id'] = transaction_id
        values['shipType'] = request.POST['contractor']
        values['totalPrice'] = totalPrice
      

        forms = CustomerShipp(values)
        if forms.is_valid():
            order.complete = True
            order.save()

            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                product = item.product
                product.stock = product.stock - item.quantity
                product.save()
                item.transaction_id = transaction_id
                item.save()

           
            adding = forms.save(commit=False)
            adding.customer = customerOnWebsite
            adding.order    = order
            adding.save()

            request.session['values'] = values

        if values['paymentType'] == "card":
      


            customer = request.user.customer
            emailUser = request.user.email
            stripe.api_key  = API_KEY
            payment_intent  = stripe.PaymentIntent.create(
                amount      = totalPrice*100,
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
            recepient   = values['recipient']
            city        = values['city']
            country     = values['country']
            postal_code = values['zip_code']
            adress      = values['adress']
            email       = values['email']
            customer = request.user.customer
            emailUser = request.user.email
            stripe.api_key  = API_KEY

            payment_intent  = stripe.PaymentIntent.create(
                amount      = totalPrice*100,
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


@login_required(login_url='login')
def cardPayment(request):
    payment_intent_id = request.POST['payment_intent_id']
    payment_method_id = request.POST['payment_method_id']
    customer = request.user.customer
    values = request.session.get('values', None)
   
    stripe.api_key  = API_KEY

    customer    = stripe.Customer.create(
        name    = values.get('recipient'),
        email   = values.get('email'),
        phone   = values.get('phone'),
        address = {
            "line1":values.get('adress'),
            "city":values.get('city'),
            "country":values.get('country'),
            "postal_code":values.get('zip_code'),
        },)

    stripe.PaymentIntent.modify(
        payment_intent_id,
        payment_method = payment_method_id,
        description    = values.get('transaction_id'),
        customer       = customer,
    )   

    confirmation = stripe.PaymentIntent.confirm(
        payment_intent_id,
    )   


    if confirmation.status == 'requires_action':
        pi = stripe.PaymentIntent.retrieve(
            payment_intent_id
        )
        payment_intent_secret = pi.client_secret
        stripe_public_key     = settings.STRIPE_PUBLIC_KEY 
        context = {
            'payment_intent_secret':payment_intent_secret,
            'stripe_public_key':stripe_public_key
        }
        return render(request,"3dsc.html",context)


    for key in list(request.session.keys()):
        if not key.startswith("_"): 
            del request.session[key]

    return render(request,'home')


@login_required(login_url='login')       
def successP24(request):
    customer = request.user.customer
    context = {
          'customer':customer  
    }
    return render(request,'orderPayed.html',context)

def Holder(request):
    transaction_id = datetime.datetime.now().timestamp()
    customer       = request.user.customer
    
    if request.method == "POST" and request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.complete = True
        order.transaction_id = transaction_id
        order.save()
        
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            product = item.product
            product.stock = product.stock - item.quantity
            product.save()
            item.transaction_id = transaction_id
            item.save()

        payment_intent_id = request.POST['payment_intent_id']
        payment_method_id = request.POST['payment_method_id']
        stripe.api_key  = API_KEY

        customer    = stripe.Customer.create(
            name    = request.POST['recipient'],
            email   = request.POST['email'],
            phone   = request.POST['phone'],
            address = {
                "line1":request.POST['adress'],
                "city":request.POST['city'],
                "country":request.POST['country'],
                "postal_code":request.POST['zip_code'],
            },)

        stripe.PaymentIntent.modify(
            payment_intent_id,
            payment_method = payment_method_id,
            description    = transaction_id,
            customer       = customer,
        )   

        confirmation = stripe.PaymentIntent.confirm(
            payment_intent_id,
        )   

      
        customerOnWebsite = request.user.customer
        values = request.POST.copy()
        values['transaction_id'] = transaction_id
        values['shipType'] = request.POST['contractor']
        values.pop('payment_method_id')
        values.pop('payment_intent_id')
        forms = CustomerShipp(values)
        print(forms.is_valid())
        if forms.is_valid():
            adding = forms.save(commit=False)
            adding.customer = customerOnWebsite
            adding.order    = order
            adding.save()


        if confirmation.status == 'requires_action':
            pi = stripe.PaymentIntent.retrieve(
                payment_intent_id
            )

            payment_intent_secret = pi.client_secret
            stripe_public_key     = settings.STRIPE_PUBLIC_KEY 
            context = {
                'payment_intent_secret':payment_intent_secret,
                'stripe_public_key':stripe_public_key
            }

            return render(request,"3dsc.html",context)

        return render(request,'policy.html')




















































def policyDetail(request):
    return render(request,'policy.html')


def mailingList(request):
    if request.method == "POST":
        forms = MailingForm(request.POST)
        print(request.POST)
        print(forms.is_valid())
        if forms.is_valid():
            forms.save()
            
            return redirect('home')

    return redirect('home')


#def creatingOrder(request, orderID):
   # values = request.POST.copy()
   # values['date_added'] = orderID
    #orderedItemForm = ShippingAddress(values)
    #if orderedItemForm.is_valid():
       # order.complete = True
       # orderedItemForm.save()

    #return 0