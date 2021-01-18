  
from django.urls import path
from Control_Panel import views as panel


urlpatterns = [

	path('control', panel.controlPanelView, name='control'),
	path('controlDetail/<str:pk>/', panel.controlPanelDetail, name='controlDetail'),
	
]