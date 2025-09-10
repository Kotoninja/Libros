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
from django.conf import settings

from .forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordEmail,
    SettingsProfile,
    ChangePassword,
    ResetPassword,
)
from .tokens import account_activation_token


def get_errors_from_form(request, form):
    for error_field, error_message in form.errors.as_data().items():
        messages.error(
            request,
            f"{error_field.capitalize()} : {error_message[0].message}",
            extra_tags="auth_message",
        )


# def handle_uploaded_file(f):
#     with open(f"{}/file/name.txt", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


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
                if "verify_email_user" in request.session:
                    del request.session["verify_email_user"]
                login(request, user)
                return redirect("library:home")

            elif User.objects.filter(
                username=form.cleaned_data["username"]
            ).exists() and User.objects.get(
                username=form.cleaned_data["username"]
            ).check_password(form.cleaned_data["password"]):
                user = User.objects.get(username=form.cleaned_data["username"])
                if (
                    user.check_password(form.cleaned_data["password"])
                    and user is not None
                    and not user.is_active
                ):
                    request.session["verify_email_user"] = user.pk
                    return redirect("user:activate_email")

            else:
                messages.error(
                    request,
                    "Incorrect username or password. Please submit the form again.",
                    extra_tags="auth_message",
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
                    extra_tags="auth_message",
                )
            elif User.objects.filter(username=form.cleaned_data["username"]).exists():
                messages.error(
                    request, "This Username already exist", extra_tags="auth_message"
                )
            elif User.objects.filter(email=form.cleaned_data["email"]).exists():
                messages.error(
                    request, "This Email already exist", extra_tags="auth_message"
                )
            else:
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                )
                user.is_active = False
                user.save()
                request.session["verify_email_user"] = user.pk
                return redirect("user:activate_email")
        else:
            get_errors_from_form(request=request, form=form)
    else:
        form = RegistrationForm()

    context |= {"form": form}
    return render(request, "user/registration.html", context=context)


def send_email_to_activate_email(request, user, to_email):
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
            "Email send",
        )
    else:
        messages.error(
            request,
            f"Problem sending confirmation email to {to_email}, check if you typed it correctly.",
        )
    return None


def activate(request, uidb64, token):
    user = User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
            extra_tags="auth_message",
        )
        return redirect(reverse("user:login"))
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect(reverse("library:home"))


# TODO Add rate limit
def resend_email(request):
    context = {}

    try:
        user = User.objects.get(pk=request.session.get("verify_email_user", None))
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and not user.is_active:
        context = {"to_email": user.email, "user": user}
        send_email_to_activate_email(request=request, user=user, to_email=user.email)
    else:
        messages.error(request, "Oops.., Little problems with sending email")
        return redirect(reverse("library:home"))

    return render(request, "user/activate_mail.html", context=context)


@login_required
def profile(request):
    return render(request, "user/profile.html")


def logout_user(request):
    logout(request)
    return redirect("user:login")


@login_required
def settings_profile_user(
    request,
):
    if request.method == "POST":
        form = SettingsProfile(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)

            if form.cleaned_data.get("user_image"):
                pass
            if form.cleaned_data.get("nickname"):
                user.userprofile.nickname = form.cleaned_data["nickname"]  # type: ignore
            if form.cleaned_data.get("first_name"):
                user.first_name = form.cleaned_data["first_name"]
            if form.cleaned_data.get("last_name"):
                user.last_name = form.cleaned_data["last_name"]
            if form.cleaned_data.get("location"):
                user.userprofile.nickname = form.cleaned_data["location"]  # type: ignore
            if form.cleaned_data.get("email"):
                # Changing an email address is done via a letter to the user's primary email address.
                pass
                # user.last_name = form.cleaned_data["email"]
            if form.cleaned_data.get("phone_number"):
                user.userprofile.nickname = form.cleaned_data["phone_number"]  # type: ignore

            if form.cleaned_data.get("birthday"):
                user.userprofile.nickname = form.cleaned_data["birthday"]  # type: ignore

            user.userprofile.save()  # type: ignore
            user.save()
            return redirect(reverse("user:settings_profile"))
        else:
            messages.error(request, "Oops... Something wrong")

    context = {
        "form": SettingsProfile(
            {
                "nickname": request.user.userprofile.nickname,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "location": None,
                "email": request.user.email,
                "phone_number": None,
                "birthday": None,
            }
        )
    }
    return render(request, "user/settings_profile.html", context=context)


@login_required
def settings_security_user(request):
    if request.method == "POST":
        change_password_form = ChangePassword(request.POST)

        if change_password_form.is_valid():
            current_password = change_password_form.cleaned_data["current_password"]
            new_password = change_password_form.cleaned_data["new_password"]
            confirm_password = change_password_form.cleaned_data["confirm_password"]

            if User.objects.filter(pk=request.user.pk).exists():
                user = User.objects.get(pk=request.user.pk)
                if user.check_password(current_password):
                    if (
                        new_password == confirm_password
                        and current_password != new_password
                    ):
                        user.set_password(new_password)
                        user.save()
                        messages.success(request, "Password successfully changed")
                        return redirect(reverse("user:login"))
                    elif current_password == new_password == confirm_password:
                        messages.error(request, "This password is already in use")
                    else:
                        messages.error(request, "Passwords do not match")
                else:
                    messages.error(request, "Incorrect current password")
        else:
            messages.error(request, "Oops... Something wrong")
    context = {"change_password_form": ChangePassword()}
    return render(request, "user/settings_security.html", context=context)


@login_required
def settings_notifications_user(request):
    context = {}
    return render(request, "user/settings_notifications.html", context=context)


@login_required
def settings_billing_user(request):
    context = {}
    return render(request, "user/settings_billing.html", context=context)


def send_email_reset_password(request, to_email):
    user = User.objects.get(email=to_email)
    context = {
        "user": user.username,
        "domain": get_current_site(request).domain,
        "pk": urlsafe_base64_encode(force_bytes(user.pk)),
        "email": urlsafe_base64_encode(force_bytes(user.email)),
        "token": account_activation_token.make_token(user),
        "protocol": "https" if request.is_secure() else "http",
    }
    message = render_to_string("template_reset_password.html", context=context)
    email = EmailMessage("Reset password", message, to=[to_email])
    if email.send():
        messages.success(
            request,
            "Email send",
        )

    else:
        messages.error(
            request,
            f"Problem sending reset password to {to_email}, check if you typed it correctly.",
        )


def reset_password_user(
    request, pk, email, token
):  # FIXME added error masseg if email invalid
    try:
        pk = force_str(urlsafe_base64_decode(pk))
        email = force_str(urlsafe_base64_decode(email))
        user = User.objects.get(pk=pk, email=email)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, AttributeError):
        user = None
        messages.error(request, "Oops... Something wrong")
        return redirect(reverse("library:home"))

    if request.method == "POST":
        if user is not None and account_activation_token.check_token(user, token):
            form = ResetPassword(request.POST)
            if form.is_valid():
                if (
                    form.cleaned_data["new_password"]
                    == form.cleaned_data["confirm_password"]
                ):
                    if not user.check_password(form.cleaned_data["new_password"]):
                        user.set_password(form.cleaned_data["new_password"])
                        user.save()
                        messages.success(request, "Password successfully changed")
                        return redirect(reverse("user:login"))

                    else:
                        messages.error(request, "This password is already in use")
                else:
                    messages.error(request, "Passwords do not match")
        else:
            messages.error(request, "Oops... Something wrong")
            return redirect(reverse("user:login"))

    context = {"form": ResetPassword()}
    return render(request, "user/reset_password_user.html", context=context)


def reset_password_user_request_to_email(request):
    context = {}

    if request.method == "POST":
        form = ResetPasswordEmail(request.POST)
        if form.is_valid():
            send_email_reset_password(
                request=request, to_email=form.cleaned_data["email"]
            )
    else:
        form = ResetPasswordEmail()

    context |= {"form": form}
    return render(request, "user/reset_password_user_email.html", context=context)
