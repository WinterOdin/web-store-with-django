  
from django.urls import path
from Control_Panel import views as panel


urlpatterns = [

	path('control', panel.controlPanelView, name='control'),


]