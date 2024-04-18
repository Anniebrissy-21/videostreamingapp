from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from myapp.models import UserProfile,Video


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","username","email","password1","password2"]


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2 shadow-none"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mt-2 shadow-none"}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["dob","profile_pic","gender","address","phone"]

class VideoForm(forms.ModelForm):
    class Meta:
        model=Video
        fields=["title","video_url","description"]