from django import forms

from .models import Result
from users.models import User



class ResultImageForm(forms.ModelForm):
    image=forms.ImageField(label='Image')
    class Meta:
        model = Result
        fields = ('image',)
