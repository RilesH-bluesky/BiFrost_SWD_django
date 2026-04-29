from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    """Registration form extending Django's built-in UserCreationForm."""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "class": "form-control", "placeholder": "you@example.com"
    }))
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "First name"
    }))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Last name"
    }))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Choose a username"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Create password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm password"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user)
        return user


class ProfileEditForm(forms.ModelForm):
    """Form for editing the UserProfile model fields."""
    class Meta:
        model = UserProfile
        fields = ["bio", "home_city", "preferred_currency", "avatar_url"]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Tell us about your travel interests..."}),
            "home_city": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Nashville, TN"}),
            "preferred_currency": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. USD, EUR"}),
            "avatar_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
        }


class UserEditForm(forms.ModelForm):
    """Form for editing core Django User fields."""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class BiFrostPasswordChangeForm(PasswordChangeForm):
    """Styled wrapper around Django's built-in PasswordChangeForm."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})