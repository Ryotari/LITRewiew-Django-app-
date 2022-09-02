from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'image')

class FollowForm(forms.Form):
    followed_user = forms.CharField(
        required=None,
        label=False,
        widget=forms.TextInput(attrs={"type": "hidden"}),
        #widget=forms.TextInput(attrs={"placeholder": "Utilisateur"})
    )

class FollowFormUsername(forms.Form):
    followed_user = forms.CharField(
        required=None,
        label=False,
        #widget=forms.TextInput(attrs={"type": "hidden"}),
        widget=forms.TextInput(attrs={"placeholder": "Utilisateur"})
    )
