from django.urls import path
from django.shortcuts import redirect
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, CartView, TransactionListView


urlpatterns = [
    path('', lambda request: redirect('product_list')),
    path('items', ProductListView.as_view(), name='product_list'),
    path('item/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('item/add', ProductCreateView.as_view(), name='product_create'),
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name='product_update'),
    path('cart', CartView.as_view(), name='product_cart'),
    path('transactions', TransactionListView.as_view(), name='product_transaction'),
]
