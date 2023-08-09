from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User,Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model= User
        fields=['username','email','password1','password2']

class OrganizerRegisterForm(UserCreationForm):
    MY_CHOICES = (
    ('1', 'Organizer'),
    ('0', 'Player'),
)
    email = forms.EmailField()
    account = forms.ChoiceField(choices=MY_CHOICES)

    class Meta:
        model= User
        fields=['username','email','password1','password2','account']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields= ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']
