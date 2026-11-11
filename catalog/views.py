from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from catalog.forms import ContactMessageForm, ProductForm
from catalog.models import Product


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "product_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")


class ContactsView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactMessageForm
    success_url = reverse_lazy("contacts")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
