from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.template.defaultfilters import slugify
from mainpage.decorators import *
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import json
from django.db.models import Q
from mainpage.views import searchQueryset
from django.contrib.admin.views.decorators import staff_member_required





@login_required(login_url='login')
@staff_member_required
def controlPanelView(request):
    user = request.user.customer
    products = Product.objects.filter(stock = 0)
    context={
        'products':products
    }

    return render(request,'adminPanel/controlPanel.html', context)



@login_required(login_url='login')
@staff_member_required
def controlPanelOrders(request):

    user = request.user.customer
    qs = OrderItem.objects.filter(order__complete=True) 
    products = qs.filter(order__customer=user)
    shipments = ShippingAddress.objects.all().order_by("-id");

    if request.method == "POST":
        query = request.POST.get('searchProduct')      
        shipments = []
        if query is not None:
            queries  = query.split(" ")
            for x in queries:
                pr = ShippingAddress.objects.filter(
                    Q(transaction_id__icontains=x)|Q(email__icontains=x)|Q(adress__icontains=x)|Q(phone__icontains=x)|Q(invoiceNip__icontains=x)
                ).distinct()

                for product in pr:
                    shipments.append(product)
        
        context={
            'shipments':shipments
        }

    context={
        'shipments':shipments
    }
    return render(request,'adminPanel/controlPanelOrder.html', context)



@login_required(login_url='login')
@staff_member_required
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


@login_required(login_url='login')
@staff_member_required
def controlPanelProductsDetailPaying(request, pk):
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





@login_required(login_url='login')
@staff_member_required
def controlPanelProducts(request):
    user     = request.user.customer
    products = Product.objects.all().order_by('stock')

    if request.method == "POST":
        query = request.POST.get('searchProduct')    
        products = searchQueryset(query)
        context      = {
            'products':products,
        }
    context={
        'products':products
    }
    return render(request,'adminPanel/adminProducts.html', context)


@login_required(login_url='login')
@staff_member_required
def controlPanelProductsDetail(request,pk):

    product = Product.objects.get(id=pk)
    forms = AdminProduct(instance=product)
    if request.method == "POST":
        forms = AdminProduct(request.POST,instance=product)
        print(forms.is_valid())
        if forms.is_valid():
            forms.save()

    context={
        'forms':forms,
        'product':product,
    }
    return render(request,'adminPanel/adminProductAction.html', context)

@login_required(login_url='login')
@staff_member_required
def controlPanelProductsAdd(request):

    forms = AdminProduct()
    if request.method == "POST":
        forms = AdminProduct(request.POST)
        if forms.is_valid():
            forms.save()

            return render(request,'adminPanel/controlPanel.html')
    context={
        'forms':forms,

    }
    return render(request,'adminPanel/adminProductAction.html', context)



@login_required(login_url='login')
@staff_member_required
def controlPanelCategories(request):
    categories = Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'adminPanel/adminCategories.html', context)


@login_required(login_url='login')
@staff_member_required
def controlPanelShipMethod(request):
    shipp = ShipmentMethod.objects.all()
    context={
        'shipp':shipp
    }
    return render(request,'adminPanel/adminShipment.html', context)


@login_required(login_url='login')
@staff_member_required
def controlPanelCategoryDetail(request,pk):

    category = Category.objects.get(id=pk)
    forms = AdminCategory(instance=category)
    if request.method == "POST":
        forms = AdminCategory(request.POST,instance=category)
        if forms.is_valid():
            forms.save()

        
    context={
       'forms':forms
    }
    return render(request,'adminPanel/adminProductAction.html', context)


@login_required(login_url='login')
@staff_member_required
def controlPanelCategoryAdd(request):

    forms = AdminCategory()
    if request.method == "POST":
        forms = AdminCategory(request.POST)
        if forms.is_valid():
            forms.save()

    context={
       'forms':forms
    }
    return render(request,'adminPanel/adminProductAction.html', context)




@login_required(login_url='login')
@staff_member_required
def controlPanelContractorDetail(request,pk):

    contractor = ShipmentMethod.objects.get(id=pk)
    forms = AdminContractor(instance=contractor)
    if request.method == "POST":
        forms = AdminContractor(request.POST,instance=contractor)
        if forms.is_valid():
            forms.save()

    context={
       'forms':forms
    }
    return render(request,'adminPanel/adminProductAction.html', context)

@login_required(login_url='login')
@staff_member_required
def controlPanelContractorAdd(request):


    forms = AdminContractor()
    if request.method == "POST":
        forms = AdminContractor(request.POST)
        if forms.is_valid():
            forms.save()

    context={
       'forms':forms
    }
    return render(request,'adminPanel/adminProductAction.html', context)




@login_required(login_url='login')
@staff_member_required
def controlPanelHelpList(request):

    categories = HelpCategory.objects.all()
    context={
       'categories':categories
    }
    return render(request,'adminPanel/adminHelpCategories.html', context)


@login_required(login_url='login')
@staff_member_required
def controlPanelHelpDetail(request,pk):

    helpCat = HelpCategory.objects.get(id=pk)
    forms = AdminHelp(instance=helpCat)
    if request.method == "POST":
        forms = AdminHelp(request.POST,instance=helpCat)
        if forms.is_valid():
            forms.save()

    context={
       'forms':forms
    }
    return render(request,'adminPanel/adminProductAction.html', context)


@login_required(login_url='login')
@staff_member_required
def controlPanelHelpAdd(request):

    forms = AdminHelp()
    if request.method == "POST":
        forms = AdminHelp(request.POST)
        if forms.is_valid():
            forms.save()

    context={
       'forms':forms
    }
    return render(request,'adminPanel/adminProductAction.html', context)











@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['admin'])
def controlPanelCategoryContentList(request):

    categories = HelpCategoryContent.objects.all()
    context={
       'categories':categories
    }
    return render(request,'adminPanel/adminHelpContent.html', context)





@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['admin'])
def controlPanelCategoryContentDetail(request,pk):

    catContent = HelpCategoryContent.objects.get(id=pk)
    forms = AdminHelpContent(instance=catContent)
    if request.method == "POST":
        forms = AdminHelpContent(request.POST,instance=catContent)
        if forms.is_valid():
            forms.save()

    context={
       'forms':forms
    }
    return render(request,'adminPanel/adminProductAction.html', context)


@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['admin'])
def controlPanelCategoryContentAdd(request):

    forms = AdminHelpContent()
    if request.method == "POST":
        forms = AdminHelpContent(request.POST)
        if forms.is_valid():
            forms.save()

    context={
       'forms':forms
    }
    return render(request,'adminPanel/adminProductAction.html', context)
