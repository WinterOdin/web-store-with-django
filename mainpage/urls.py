  
from django.urls import path
from . import views
from authentication import views as auth
from user import views as user


urlpatterns = [
	path('', views.recommendedProducts, name='home'),


	path('detail/<str:id>/', views.productDetail, name='detail'),
	path('tag/<slug:slug>/', views.tagListView, name='tag'),
	path('category/<str:category>/', views.categoryListView, name='category'),

	path('updateItem', views.updateItem, name='updateItem'),
	path('cart', views.cartDetail, name='cart'),

	path('help', views.helpView, name='help'),
	path('policy', views.policyDetail, name='policy'),

	path('processOrder', views.processOrder, name='processOrder'),
	path('checkout', views.checkoutDetail, name='checkout'),
	path('cardPayment', views.cardPayment, name='cardPayment'),

	path('stripe-webhooks', views.stripe_webhooks, name='stripe_webhooks'),
	path('success', views.successP24, name='success'),

	path('mailing', views.mailingList, name='mailing'),

	
	
]
