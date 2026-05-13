from django.urls import path
from django.shortcuts import redirect
from .views import ProductListView, ProductDetailView

app_name = 'merchstore'

urlpatterns = [
    path('', lambda request: redirect('product_list')),
    path('products', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
]
