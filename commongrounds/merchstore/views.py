from .models import ProductType, Product
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class ProductListView(ListView):
    model = ProductType
    template_name = 'merchstore/product_list.html'

    def get_queryset(self):
        return ProductType.objects.prefetch_related('product_set').all()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore/product_detail.html'