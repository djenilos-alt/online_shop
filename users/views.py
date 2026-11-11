from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from users.forms import UserLoginForm, UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            email_sent = send_mail(
                subject="Добро пожаловать!",
                message=(
                    f"Здравствуйте, {user.email}!\n\n"
                    "Вы успешно зарегистрировались в нашем интернет-магазине."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

            if email_sent:
                messages.success(
                    request,
                    "Регистрация прошла успешно! Приветственное письмо отправлено.",
                )
            else:
                messages.warning(
                    request,
                    "Регистрация прошла успешно, но письмо отправить не удалось.",
                )

            return redirect("users:login")

    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = "home"
