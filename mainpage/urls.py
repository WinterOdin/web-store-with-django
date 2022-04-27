  
from django.urls import path
from . import views
from authentication import views as auth
from user import views as user
from . import cryptoApi as price

urlpatterns = [
	path('', views.recommendedProducts, name='home'),


	path('detail/<str:id>/', views.productDetail, name='detail'),
	path('tag/<slug:slug>/', views.tagListView, name='tag'),
	path('category/<str:category>/', views.categoryListView, name='category'),

	path('updateItem', views.updateItem, name='updateItem'),
	path('cart', views.cartDetail, name='cart'),

	path('help', views.helpView, name='help'),
	path('policy', views.policyDetail, name='policy'),
	path('rules', views.rulesDetail, name='rules'),
	
	path('contact', views.contactDetail, name='contact'),

	path('processOrder', views.processOrder, name='processOrder'),
	path('checkout', views.checkoutDetail, name='checkout'),
	path('cardPayment', views.cardPayment, name='cardPayment'),

	path('stripe-webhooks', views.stripe_webhooks, name='stripe_webhooks'),
	path('success', views.successP24, name='success'),

	path('mailing', views.mailingList, name='mailing'),

	path('contact-us', views.contactMail, name='contact-us'),
	path('configure', views.miningStation, name='configure'),
	path('about-us', views.aboutUs, name='about-us'),

	path('priceAPI', price.crypto_api_prices, name='priceAPI'),

	path('mail-send-conf', views.mailSendConf, name='mail-send-conf')
	
]
