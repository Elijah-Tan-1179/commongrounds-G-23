from django.contrib import admin
from .models import ProductType, Product


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType


class ProductAdmin(admin.ModelAdmin):
    model = Product


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
