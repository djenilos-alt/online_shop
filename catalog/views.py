from django.shortcuts import render

def home(request):
    return render(request, "catalog/home.html")

def contacts(request):
    success_message = None

    if request.method == "POST":
        success_message = "Сообщение успешно отправлено!"

    return render(
    request,
    "catalog/contacts.html",
    {"success_message": success_message},
)
