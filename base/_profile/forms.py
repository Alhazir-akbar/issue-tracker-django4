from django import forms
from django.contrib.auth.forms import UserCreationForm

from bug.models import Ticket
from .models import UserProfile, User

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserProfile.USER_ROLES, label="Pilih Peran")

    class Meta:
        model = User
        fields = ['username', 'first_name','password1', 'password2', 'role','groups']
        # fields = '__all__'

