from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session


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
                context |= {
                    "auth_errors": "Incorrect username or password. Please submit the form again."
                }
        else:
            context |= {"errors": form.errors}
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
                context |= {
                    "auth_errors": "Passwords did not occur. Please enter the same passwords in both fields."
                }
            elif User.objects.filter(username=form.cleaned_data["username"]).exists():
                context |= {"auth_errors": "This Username already exist"}
            elif User.objects.filter(email=form.cleaned_data["email"]).exists():
                context |= {"auth_errors": "This Email already exist"}
            else:
                User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                )
                return redirect("user:login")
        else:
            context |= {"errors": form.errors}
    else:
        form = RegistrationForm()
    context |= {"form": form}
    return render(request, "user/registration.html", context=context)


@login_required
def profile(request):
    return render(request, "user/profile.html")


def logout_user(request):
    logout(request)
    return redirect("user:login")

@login_required
def settings_user(request):
    context = {}
    return render(request,"user/settings.html",context=context)