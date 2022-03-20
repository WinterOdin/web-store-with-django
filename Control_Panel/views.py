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

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django import template

from django.utils.html import strip_tags


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
                    Q(transaction_id__icontains=x)|Q(email__icontains=x)|Q(adress__icontains=x)|Q(phone__icontains=x)|Q(invoiceNip__icontains=x)|Q(recipient__icontains=x)
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

        subject = "Shipment Confirmation Email"
        htmltemp = template.loader.get_template('shipment_html.html')

        c = {
        "email":shipments.email,
        'domain':'ww-tech.pl',
        'site_name': 'ww-tech',
        'protocol': 'https',
        }
        html_content = htmltemp.render(c)
        text_content = strip_tags(htmltemp)
        try:
            msg = EmailMultiAlternatives(subject, text_content, 'WW-tech <support@ww-tech.pl>', [shipments.email], headers = {'Reply-To': 'support@ww-tech.pl'})
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

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
    if request.method == "POST":
        processed = request.POST['paying']
        shipments.payed = processed
        shipments.save()
        if processed =="no":
            values = request.session.get('values', None)
            subject = "Błąd płatności"
            htmltemp = template.loader.get_template('error_payment_email.html')

            c = {
                "email":shipments.email,
                'domain':'ww-tech.pl',
                'site_name': 'ww-tech',
                'protocol': 'https',
                'order_id' : shipments.transaction_id,
            }
            text_content = strip_tags(htmltemp)
            html_content = htmltemp.render(c)

            try:
                msg = EmailMultiAlternatives(subject, text_content, 'WW-tech <support@ww-tech.pl>', [shipments.email], headers = {'Reply-To': 'support@ww-tech.pl'})
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

        elif processed == "payed":
            values = request.session.get('values', None)
            subject = "Płatność została odnotowana"
            htmltemp = template.loader.get_template('booked_payment_email.html')

            c = {
                "email":shipments.email,
                'domain':'ww-tech.pl',
                'site_name': 'ww-tech',
                'protocol': 'https',
                'order_id' : shipments.transaction_id,
            }
            text_content = strip_tags(htmltemp)
            html_content = htmltemp.render(c)

            try:
                msg = EmailMultiAlternatives(subject, text_content, 'WW-tech <support@ww-tech.pl>', [shipments.email], headers = {'Reply-To': 'support@ww-tech.pl'})
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')


            return redirect(controlPanelView)

    context={
        'shipments':shipments,
    }

    return render(request,'adminPanel/controlPanel.html', context)





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
def controlPanelProductsDisplayed(request):
    user     = request.user.customer
    products = Product.objects.filter(display=False)

    if request.method == "POST":
        query = request.POST.get('searchProduct')    
        products = searchQueryset(query)
        context      = {
            'products':products,
        }
    context={
        'products':products
    }
    return render(request,'adminPanel/adminDisplayed.html', context)

@login_required(login_url='login')
@staff_member_required
def controlPanelProductsStock(request):
    user     = request.user.customer
    products = Product.objects.filter(stock=0)

    if request.method == "POST":
        query = request.POST.get('searchProduct')    
        products = searchQueryset(query)
        context      = {
            'products':products,
        }
    context={
        'products':products
    }
    return render(request,'adminPanel/adminStock.html', context)


@login_required(login_url='login')
@staff_member_required
def controlPanelProductsDetail(request,pk):

    product = Product.objects.get(id=pk)
    productImages = [product.pic1, product.pic2, product.pic3, product.pic4]
    forms = AdminProduct(instance=product)
    if request.method == "POST":
        forms = AdminProduct(request.POST,instance=product)
        print(forms.is_valid())
        if forms.is_valid():
            forms.save()

    context={
        'forms':forms,
        'product':product,
        'productImages':productImages,
    }
    return render(request,'adminPanel/adminProductAction.html', context)

@login_required(login_url='login')
@staff_member_required
def controlPanelProductsAdd(request):

    forms = AdminProduct()
    if request.method == "POST":
        forms = AdminProduct(request.POST,request.FILES)
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
        forms = AdminCategory(request.POST,request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('controlPanelCategories')

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
            return redirect('controlPanelShipMethod')

    context={
       'forms':forms
    }
    return render(request,'adminPanel/adminProductAction.html', context)

@login_required(login_url='login')
@staff_member_required
def controlPanelContractorAdd(request):


    forms = AdminContractor()
    if request.method == "POST":
        forms = AdminContractor(request.POST, request.FILES)
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
        forms = AdminHelp(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('controlPanelHelpList')

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
            return redirect('controlPanelCategoryContentList')

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
        forms = AdminHelpContent(request.POST,request.FILES)
        if forms.is_valid():
            forms.save()

    context={
       'forms':forms
    }
    return render(request,'adminPanel/adminProductAction.html', context)
