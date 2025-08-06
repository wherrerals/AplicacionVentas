# forms.py
from django import forms
from uploadApp.models.imgdb import ImagenDB

class ImagenForm(forms.ModelForm):
    class Meta:
        model = ImagenDB
        fields = ['nombre', 'archivo']
