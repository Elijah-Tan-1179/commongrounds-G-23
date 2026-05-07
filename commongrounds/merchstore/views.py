from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect

from .models import Product, ProductType, Transaction, Profile
from forms import ProductForm, TransactionForm, ProductUpdateForm

def get_or_create_profile(user):
    if not user or not user.is_authenticated:
        return None
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={"role": Profile.ROLE_MEMBER}
    )
    return profile


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        profile = get_or_create_profile(self.request.user)
        return profile is not None and profile.role == Profile.ROLE_SELLER

    def handle_no_permission(self):
        return redirect('merchstore:product_list')


class ProductListView(ListView):
    model = Product
    template_name = 'merchstore/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        own_products = Product.objects.none()
        all_products = Product.objects.all()

        if user.is_authenticated:
            profile = user.profile
            own_products = all_products.filter(seller=profile)
            excluded_ids = set(own_products.values_list('id', flat=True))
            all_products = all_products.exclude(id__in=excluded_ids)

        context.update({
            'own_products': own_products.distinct(),
            'products': all_products.distinct(),
            'can_create': profile is not None and profile.role == Profile.ROLE_SELLER,
        })
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'merchstore/product_detail.html'
    context_object_name = 'products'
    product = get_object_or_404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 


class ProductCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'mrechstore/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create Product'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        profile = get_or_create_profile(self.request.user)
        if profile:
            self.object.seller.add(profile)
        return response

    def get_success_url(self):
        return reverse('merchstore:product_detail', args=[self.object.pk])
    

class ProductUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'merchstore/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Event'
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        stock = product.stock.count()
        # Checks if product is in stock
        if stock == 0:
            product.status = Product.PRODUCT_STATUS_OUT_OF_STOCK
        else:
            product.status = Product.PRODUCT_STATUS_AVAILABLE
        product.save()
        form.save_m2m()
        self.object = product
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('merchstore:product_detail', args=[self.object.pk])


class CartView(ListView):
    model = Transaction
    template_name = 'merchstore/cart.html'
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            transactions = Transaction.objects.filter(buyer=user.profile).select_related('product')

        context.update({
            'transactions': transactions.distinct()
        })
        return context

class TransactionListView():
    model = Transaction
    context_object_name = 'transactions'
