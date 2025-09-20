from django import forms
from . import models

class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Post #from models.py
        fields = ['title','body','slug','banner']
