from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import LoginForm, RegisterForm
# Create your views here.


def register_user(request):
    form = RegisterForm(request.POST or None)
    message = None
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        try:
            new_user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                last_name=last_name)
            new_user.set_password(password)
            new_user.save()
            login(request, new_user)
        except IntegrityError as e:
            message = "Username already exists!"
        else:
            return redirect("orders:index")
    for i in form.non_field_errors().as_data():
        if i.code == "confirm_error":
            message = i.message
    context = {
        "form": form,
        "message": message
    }
    return render(request, "users/register.html", context)


def login_user(request):
    form = LoginForm(request.POST or None)
    message = None
    next_url = request.GET.get('next', None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        next_url = request.POST.get('next', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url and next_url != "None":
                return redirect(next_url)
            else:
                return redirect("orders:index")
        else:
            message = "Incorrect username and/or password!"
    context = {
        "form": form,
        "message": message,
        "next": next_url
    }
    return render(request, "users/login.html", context)


def logout_user(request):
    logout(request)
    return redirect("orders:index")
