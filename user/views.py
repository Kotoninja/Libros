from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.urls import reverse


from .forms import LoginForm, RegistrationForm, ResetPasswordEmail
from .tokens import account_activation_token


def activate_email(request, user, to_email):
    context = {
        "user": user.username,
        "domain": get_current_site(request).domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
        "protocol": "https" if request.is_secure() else "http",
    }
    message = render_to_string("template_activate_account.html", context=context)
    email = EmailMessage("Activate your user account.", message, to=[to_email])
    if email.send():
        messages.success(
            request,
            f"Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.",
        )
        user.save()
    else:
        messages.error(
            request,
            f"Problem sending confirmation email to {to_email}, check if you typed it correctly.",
        )

def activate(request,uidb64,token):
    user = User.objects.get(pk = force_str(urlsafe_base64_decode(uidb64)))

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect(reverse("user:profile"))
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect(reverse("library:home"))
    
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
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                )
                
                activate_email(request=request, user=user, to_email=user.email)
                return redirect("user:login")
        else:
            get_errors_from_form(request=request, form=form)
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
    return render(request, "user/settings.html", context=context)


def reset_password_user(request):
    context = {}

    if request.method == "POST":
        form = ResetPasswordEmail(request.POST)
    else:
        form = ResetPasswordEmail()

    context |= {"form": form}
    return render(request, "user/reset_password_user.html", context=context)
