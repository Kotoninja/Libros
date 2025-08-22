from django.shortcuts import render


def login(request):
    return render(request,"user/login.html")

def registration(request):
    return render(request,"user/registration.html")


def logout(request):
    pass