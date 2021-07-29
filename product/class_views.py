from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import *
from .models import *


class CategoryListView(ListView):
    model = Category
    template_name = 'products/home.html'
    context_object_name = 'categories'


class SearchListView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if not q:
            return Product.objects.none()
        print(queryset)
        print("111111")
        queryset = queryset.filter(Q(name__icontains=q) | Q(description__icontains=q))
        print(queryset)
        return queryset


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.kwargs)
        slug = self.kwargs.get('slug')
        print(slug)
        queryset = queryset.filter(category__slug=slug)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        print(kwargs)
        context['category'] = self.kwargs.get('slug')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'id'


class IsAdminCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


class ProductCreateView(IsAdminCheckMixin, CreateView):
    model = Product
    template_name = 'products/create_product.html'
    form_class = CreateProductForm
    context_object_name = 'product_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context


class ProductUpdateView(IsAdminCheckMixin, UpdateView):
    model = Product
    template_name = 'products/update_product.html'
    form_class = UpdateProductForm
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context


class ProductDeleteView(IsAdminCheckMixin, DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('home')
