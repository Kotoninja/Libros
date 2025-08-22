from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login,logout

def login_user(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data["username"],password = form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("library:home")
            else:
                context |= {"auth_errors":"Incorrect username or password. Please submit the form again."}
        else:
            context |= {"errors": form.errors}
    else:
        form = LoginForm()

    context |= {"form":form}

    return render(request,"user/login.html",context=context)

def registration(request):
    return render(request,"user/registration.html")

def profile(request):
    # return HttpResponse(request.user.username)
    return render(request,"user/profile.html")

def logout_user(request):
    logout(request)
    return redirect("library:home")