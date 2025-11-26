import logging

from django import forms
from django.core.exceptions import ValidationError

from app.models import User, Profile


logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    login = forms.CharField(label="Login")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def clean_login(self):
        login = self.cleaned_data["login"]

        if len(login) < 3:
            raise ValidationError("Login >= 3 chars")

        return login

    def clean_password(self):
        password = self.cleaned_data["password"]

        # TODO: Исправить ограничение
        if len(password) < 4:
            raise ValidationError("Password >= 8 chars")

        return password
    

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Login")
    email = forms.EmailField(label="Email")
    nickname = forms.CharField(label="Nickname")
    avatar = forms.ImageField(label="Upload avatar", required=False)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    repeat_password = forms.CharField(label="Repeat password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")


    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists")
        
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]

        if len(password) < 8:
            raise ValidationError("Password >= 8 chars")

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data["password"]
        repeated_password = cleaned_data["repeat_password"]

        if password != repeated_password:
            raise ValidationError("Passwords should equal")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password"])
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            Profile.objects.create(
                user=user,
                avatar=self.cleaned_data.get("avatar"), # Именно через get, так как avatar не обязателен
                nickname=self.cleaned_data["nickname"],
            )

        return user