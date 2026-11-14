from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.db import models
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from catalog.forms import ContactMessageForm, ProductForm
from catalog.models import Category, Product
from catalog.services import get_products_by_category


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Product.objects.filter(is_published=True)

        if user.is_superuser or user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()

        return Product.objects.filter(
            models.Q(is_published=True) | models.Q(owner=user)
        ).distinct()


@method_decorator(cache_page(60 * 15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")

class CategoryProductsView(ListView):
    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        user = self.request.user

        products = get_products_by_category(category_id)

        if user.is_authenticated and (
            user.is_superuser
            or user.has_perm("catalog.can_unpublish_product")
        ):
            return products

        if user.is_authenticated:
            return [
                product
                for product in products
                if product.is_published or product.owner_id == user.id
            ]

        return [
            product for product in products
            if product.is_published
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category,
            pk=self.kwargs["category_id"],
        )
        return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()

        return Product.objects.filter(
            models.Q(is_published=True) | models.Q(owner=user)
        )


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        return (
            product.owner == user
            or user.has_perm("catalog.change_product")
        )

    def get_success_url(self):
        return reverse_lazy(
            "product_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        return (
            product.owner == user
            or user.has_perm("catalog.delete_product")
        )


class ProductUnpublishView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    View,
):
    permission_required = "catalog.can_unpublish_product"
    raise_exception = True

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        product.is_published = False
        product.save(update_fields=["is_published"])

        return redirect("home")


class ContactsView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactMessageForm
    success_url = reverse_lazy("contacts")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
