from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from taggit.models import Tag
from .models import *
import json
from .forms import *
from django.db.models import Q


def usersCart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
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

def serchQueryset(query):
    queryset = []
    if query is not None:
        queries  = query.split(" ")
        for x in queries:
            products = Product.objects.filter(
                Q(title__icontains=x)|Q(description__icontains=x)|Q(category__category__icontains=x)|Q(producent__icontains=x)
            ).distinct()

            for product in products:
                queryset.append(product)
        return list(set(queryset)) 





def recommendedProducts(request):
    categoryList = Category.objects.all()
    tags         = Product.tags.all()
    cart         = usersCart(request)    
    productsInfo = Product.objects.filter(recommend=True).order_by('-id')[:6]
    newest       = Product.objects.all().order_by('-id')[:10]
    
    if request.method == "POST":
        query = request.POST.get('search_bar')    
        productsInfo = serchQueryset(query)
        context      = {
            'newest':newest,
            'query':query,
            'tags':tags,
            "productsInfo":productsInfo,
            'categoryList':categoryList,
        }
        context={**context, **cart}
        
        return render(request,'products.html', context)
    
    context      = {
        'newest':newest,
        'tags':tags,
        "productsInfo":productsInfo,
        'categoryList':categoryList,
        }
    context={**context, **cart}

    return render(request,'products.html', context)

def tagListView(request, slug):
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
    }
 
    return render(request,'products.html', context)




def categoryListView(request, category):
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
        
    }
    context={**context, **cart}
    return render(request,'products.html', context)



def helpView(request):
    category = HelpCategory.objects.all()
    categoryInfo = HelpCategoryContent.objects.all()
    cart         = usersCart(request)  
    context         ={
       'category':category,
       'categoryInfo':categoryInfo,
    }
    context={**context, **cart}
    return render(request,'helpPage.html', context)

    
def productDetail(request, id):
    product         = Product.objects.get(id=id)
    productPictures = Product.objects.filter(id=id).values().first()
    cart            = usersCart(request)  
    
    context         ={
        "product":product,
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
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    
    if orderItem.quantity <= 0 or action=='delete':
        orderItem.delete()

    return JsonResponse("item was added", safe=False)



def checkoutDetail(request):
    customer = request.user
    cart    = usersCart(request)
    forms   = CustomerShipp(instance=customer.customer)  

    context ={
        'forms':forms,
        'customer':customer,
    }
    context={**context, **cart}
    return render(request,'checkout.html',context)



