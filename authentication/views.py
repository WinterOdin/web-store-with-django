import django
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
from mainpage.views import searchQueryset


@unauthenticated_user
def loginView(request, *args, **kwargs):
    navbarList = Category.objects.filter(navbar=True)
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

        context={
            'navbarList': navbarList,
        }
    
    return render(request,'login.html', context )

@unauthenticated_user
def registerView(request, *args, **kwargs):
    navbarList = Category.objects.filter(navbar=True)
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
            'navbarList': navbarList,
         }

    return render(request,'register.html', context)



def logoutUser(request):
	logout(request)
	return redirect('products')




def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data)|Q(username=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					plaintext = template.loader.get_template('password_reset_email.txt')
					htmltemp = template.loader.get_template('password_email_html.html')
					c = {
					"email":user.email,
					'domain':'ww-tech.pl',
					'site_name': 'ww-tech',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https',
					}
					text_content = plaintext.render(c)
					html_content = htmltemp.render(c)
					try:
						msg = EmailMultiAlternatives(subject, text_content, 'WW-tech <support@ww-tech.pl>', [user.email], headers = {'Reply-To': 'support@ww-tech.pl'})
						msg.attach_alternative(html_content, "text/html")
						msg.send()
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					messages.info(request, "Password reset instructions have been sent to the email address entered.")
					return redirect ("password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="resetPassword.html", context={"password_reset_form":password_reset_form})