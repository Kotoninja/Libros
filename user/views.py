from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm, ResetPasswordEmail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.core.mail import send_mail


def get_errors_from_form(request, form):
    for error_field, error_message in form.errors.as_data().items():
        messages.error(
            request,
            f"{error_field.capitalize()} : {error_message[0].message}",
            extra_tags="auth_error",
        )


def login_user(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("library:home")
            else:
                messages.error(
                    request,
                    "Incorrect username or password. Please submit the form again.",
                    extra_tags="auth_error",
                )

        else:
            get_errors_from_form(request=request, form=form)

    else:
        form = LoginForm()

    context |= {"form": form}
    return render(request, "user/login.html", context=context)


def registration(request):
    context = {}

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] != form.cleaned_data["repeat_password"]:
                messages.error(
                    request,
                    "Passwords did not occur. Please enter the same passwords in both fields.",
                    extra_tags="auth_error",
                )
            elif User.objects.filter(username=form.cleaned_data["username"]).exists():
                messages.error(
                    request, "This Username already exist", extra_tags="auth_error"
                )
            elif User.objects.filter(email=form.cleaned_data["email"]).exists():
                messages.error(
                    request, "This Email already exist", extra_tags="auth_error"
                )
            else:
                User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                )
                return redirect("user:login")
        else:
            get_errors_from_form(request=request, form=form)
    else:
        form = RegistrationForm()

    context |= {"form": form}
    return render(request, "user/registration.html", context=context)


def url_test(request):
    send_mail(subject="Test", message="Mail Django", from_email="librosshop@yandex.ru",recipient_list=["saer3rfsfdf@yandex.ru"],fail_silently=False)
    return HttpResponse("Message Send")

@login_required
def profile(request):
    return render(request, "user/profile.html")


def logout_user(request):
    logout(request)
    return redirect("user:login")


@login_required
def settings_user(request):
    context = {}
    return render(request, "user/settings.html", context=context)


def reset_password_user(request):
    context = {}

    if request.method == "POST":
        form = ResetPasswordEmail(request.POST)
    else:
        form = ResetPasswordEmail()

    context |= {"form": form}
    return render(request, "user/reset_password_user.html", context=context)

