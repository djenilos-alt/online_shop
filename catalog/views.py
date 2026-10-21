from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, FormView, ListView

from catalog.forms import ContactMessageForm
from catalog.models import Product


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ContactsView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactMessageForm
    success_url = "/contacts/"

    def form_valid(self, form):
        form.save()
        return render(
            self.request,
            self.template_name,
            {
                "form": self.form_class(),
                "success_message": "Сообщение успешно отправлено!",
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["success_message"] = self.request.GET.get("success")
        return context
