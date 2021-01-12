  
from django.urls import path
from user import views as user


urlpatterns = [
	path('order', user.orderView, name='order'),
	path('user', user.userView, name='user'),
	path('refunds', user.refundsView, name='refunds'),
]