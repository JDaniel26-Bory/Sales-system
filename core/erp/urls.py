from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.product.views import *
from core.erp.views.test.views import TestView
from core.erp.views.client.views import *
from core.erp.views.sale.views import *

app_name = 'erp'

urlpatterns = [
    # Catehory
    path('category/list/', CategoryListView.as_view(), name='categoryList'),
    path('category/add/', CategoryCreateView.as_view(), name='categoryCreate'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='categoryUpdate'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='categoryDelete'),
    # client
    path('client/list/', ClientListView.as_view(), name='clientList'),
    path('client/add/', ClientCreateView.as_view(), name='clientCreate'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='clientUpdate'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='clientDelete'),
    # product
    path('product/list/', ProductListView.as_view(), name='productList'),
    path('product/add/', ProductCreateView.as_view(), name='productCreate'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='productUpdate'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='productDelete'),
    # Home
    path('dashboard/', dashBoardView.as_view(), name='dashboard'),
    # Test
    path('test/', TestView.as_view(), name='test'),
    # Sale
    path('sale/list/', SaleListView.as_view(), name='saleList'),
    path('sale/add/', SaleCreateView.as_view(), name='saleCreate'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='saleUpdate'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='saleDelete'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='saleInvoicePdf'),
    

]
