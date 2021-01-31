  
from django.urls import path
from Control_Panel import views as panel


urlpatterns = [

	path('control', panel.controlPanelView, name='control'),
	path('controlPanelOrders', panel.controlPanelOrders, name='controlPanelOrders'),
	path('controlPanelOrdersDetail/<str:pk>/', panel.controlPanelOrdersDetail, name='controlPanelOrdersDetail'),
	path('controlPanelProducts', panel.controlPanelProducts, name='controlPanelProducts'),
	path('controlPanelCategories', panel.controlPanelCategories, name='controlPanelCategories'),
	path('controlPanelShipMethod', panel.controlPanelShipMethod, name='controlPanelShipMethod'),
	path('controlPanelProductsDetail/<int:pk>/', panel.controlPanelProductsDetail, name='controlPanelProductsDetail'),
	path('controlPanelProductsAdd', panel.controlPanelProductsAdd, name='controlPanelProductsAdd'),
	path('controlPanelCategoryDetail/<int:pk>/', panel.controlPanelCategoryDetail, name='controlPanelCategoryDetail'),
	path('controlPanelCategoryAdd', panel.controlPanelCategoryAdd, name='controlPanelCategoryAdd'),
	path('controlPanelContractorDetail/<int:pk>/', panel.controlPanelContractorDetail, name='controlPanelContractorDetail'),
	path('controlPanelContractorAdd', panel.controlPanelContractorAdd, name='controlPanelContractorAdd'),
	path('controlPanelHelpList', panel.controlPanelHelpList, name='controlPanelHelpList'),
	path('controlPanelHelpDetail/<int:pk>/', panel.controlPanelHelpDetail, name='controlPanelHelpDetail'),
	path('controlPanelHelpAdd', panel.controlPanelHelpAdd, name='controlPanelHelpAdd'),
	path('controlPanelCategoryContentList', panel.controlPanelCategoryContentList, name='controlPanelCategoryContentList'),
	path('controlPanelCategoryContentDetail/<int:pk>/', panel.controlPanelCategoryContentDetail, name='controlPanelCategoryContentDetail'),
	path('controlPanelCategoryContentAdd', panel.controlPanelCategoryContentAdd, name='controlPanelCategoryContentAdd'),

	path('controlPanelProductsDetailPaying/<int:pk>/', panel.controlPanelProductsDetailPaying, name='controlPanelProductsDetailPaying'),
]