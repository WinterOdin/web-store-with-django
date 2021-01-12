  
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

	path('checkout', views.checkoutDetail, name='checkout'),
	path('help', views.helpView, name='help'),

	
	
]
