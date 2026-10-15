from django.shortcuts import get_object_or_404, render

from catalog.forms import ContactMessageForm
from catalog.models import Product


def home(request):
    products = Product.objects.all()

    return render(
        request,
        "catalog/home.html",
        {"products": products},
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(
        request,
        "catalog/product_detail.html",
        {"product": product},
    )


def contacts(request):
    success_message = None

    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            form.save()
            success_message = "Сообщение успешно отправлено!"
            form = ContactMessageForm()
    else:
        form = ContactMessageForm()

    return render(
        request,
        "catalog/contacts.html",
        {
            "form": form,
            "success_message": success_message,
        },
    )