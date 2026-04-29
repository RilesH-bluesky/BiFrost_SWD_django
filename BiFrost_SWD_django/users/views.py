from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import RegisterForm, ProfileEditForm, UserEditForm, BiFrostPasswordChangeForm
from .models import UserProfile

def register(request):
    """Handles new user sign-up and auto-login on success."""
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to BiFrost, {user.username}! Your account is ready.")
            return redirect("index")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})

class BiFrostLoginView(LoginView):
    """Custom login view that uses BiFrost's styled template."""
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return "/itinerary/"

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


def logout_view(request):
    """Logs out the current user and redirects to login."""
    logout(request)
    messages.info(request, "You've been logged out. Safe travels!")
    return redirect("login")


@login_required
def profile(request):
    """Displays the current user's profile page with trip summary."""
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    trips = request.user.itineraries.order_by("-created_at")[:5]
    return render(request, "users/profile.html", {
        "profile": profile_obj,
        "trips": trips,
    })


@login_required
def edit_profile(request):
    """Handles editing of both User and UserProfile fields."""
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile_obj)

    return render(request, "users/edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })


@login_required
def change_password(request):
    """Handles secure in-app password change."""
    if request.method == "POST":
        form = BiFrostPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Password updated successfully.")
            return redirect("profile")
    else:
        form = BiFrostPasswordChangeForm(request.user)

    return render(request, "users/change_password.html", {"form": form})