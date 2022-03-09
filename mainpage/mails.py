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

def configuratorMail(data):

    subject = '!-Konfiguracja koparki-!'

    plaintext = template.loader.get_template('payment_email_txt.txt')
    htmltemp = template.loader.get_template('payment_email_html.html')

    c = {
        'email':'biuro@wwtechnology.pl',
        'domain':'ww-tech.pl',
        'site_name': 'ww-tech',
        'protocol': 'https',
        'price' : data["price"],
        'cards' : data["cards"],
        'quantity' : data["quantity"],
        'crypto_type' : data["crypto_type"],
        'name' : data["name"],
        'surname' : data["surname"],
        'phone' : data["phone"],
        'email_customer' : data["email"],
        'story' : data["story"],
    }
    text_content = plaintext.render(c)
    html_content = htmltemp.render(c)
    try:
        msg = EmailMultiAlternatives(subject, text_content, 'Konfigurator WW-tech <support@ww-tech.pl>', ['biuro@wwtechnology.pl'], headers = {'Reply-To': data["email"]})
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

def contactMail(data):

    subject = '!-Konfiguracja koparki-!'

    plaintext = template.loader.get_template('payment_email_txt.txt')
    htmltemp = template.loader.get_template('payment_email_html.html')

    c = {
        'email':'biuro@wwtechnology.pl',
        'domain':'ww-tech.pl',
        'site_name': 'ww-tech',
        'protocol': 'https',
        'name' : data["name"],
        'surname' : data["surname"],
        'phone' : data["phone"],
        'email_customer' : data["email"],
        'story' : data["story"],
    }
    text_content = plaintext.render(c)
    html_content = htmltemp.render(c)
    try:
        msg = EmailMultiAlternatives(subject, text_content, 'Pytanie na WW-tech <support@ww-tech.pl>', ['biuro@wwtechnology.pl'], headers = {'Reply-To': data["email"]})
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

