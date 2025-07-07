# cupones/forms.py
from django import forms
from datosLsApp.models.couponsdb import CouponsDB

class CuponForm(forms.ModelForm):
    class Meta:
        model = CouponsDB
        fields = '__all__'
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'datetime-local'}),
            'valid_to': forms.DateInput(attrs={'type': 'datetime-local'}),
            'one_use_only': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'same_price_and_discount': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }