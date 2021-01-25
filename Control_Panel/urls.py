  
from django.urls import path
from Control_Panel import views as panel


urlpatterns = [

	path('control', panel.controlPanelView, name='control'),
	path('controlPanelOrders', panel.controlPanelOrders, name='controlPanelOrders'),
	path('controlPanelOrdersDetail/<str:pk>/', panel.controlPanelOrdersDetail, name='controlPanelOrdersDetail'),
	
]