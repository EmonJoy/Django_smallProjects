from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully. Please login.",
            )

            return redirect("register")

    else:
        form = UserRegistrationForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "accounts/register.html",
        context,
    )

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def login_view(request):

    # Already logged-in users should not access login page
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                login(request, user)

                messages.success(
                    request,
                    f"Welcome back, {user.username}!",
                )

                return redirect("dashboard")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )

@login_required
def dashboard(request):
    return render(
        request,
        "accounts/dashboard.html",
    )

def logout_view(request):
    logout(request)

    messages.success(
        request, "logged out!"
    )

    return redirect('login')