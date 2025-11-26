import logging

from django import forms
from django.core.exceptions import ValidationError
from app.models import User, Profile


logger = logging.getLogger(__name__)
    

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")

        labels = {
            "username": "Login",
            "email": "Email",
        }

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Email in use")
        
        return email
    
    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Login in use")
        
        return username


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("nickname", "avatar")

        labels = {
            "nickname": "Nickname",
            "avatar": "Upload avatar"
        }