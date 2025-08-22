# cupones/forms.py
from django import forms
from django.forms import inlineformset_factory
from infrastructure.models.couponcollectiondb import CouponCollectionsDB
from infrastructure.models.couponsdb import CouponsDB
from infrastructure.models.rulescouponsrelation import CouponRuleRelation

class CuponForm(forms.ModelForm):
    class Meta:
        model = CouponsDB
        fields = '__all__'
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'datetime-local'}),
            'valid_to': forms.DateInput(attrs={'type': 'datetime-local'}),
            'one_use_only': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'same_price_and_discount': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'exceed_maximum_discount': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

class CouponRuleRelationForm(forms.ModelForm):
    class Meta:
        model = CouponRuleRelation
        fields = ["rule", "min_value", "max_value"]
        widgets = {
            "rule": forms.Select(attrs={"class": "form-select"}),
            "min_value": forms.NumberInput(attrs={"class": "form-control"}),
            "max_value": forms.NumberInput(attrs={"class": "form-control"}),
        }

# Inline formset para reglas asociadas a un cupón
CouponRuleRelationFormSet = inlineformset_factory(
    CouponsDB,
    CouponRuleRelation,
    form=CouponRuleRelationForm,
    extra=1,          # cuántas filas vacías mostrar por defecto
    can_delete=True   # permitir eliminar relaciones
)

class CouponCollectionsForm(forms.ModelForm):
    class Meta:
        model = CouponCollectionsDB
        fields = ['collection']
        widgets = {
            'collection': forms.Select(attrs={'class': 'form-select'}),
        }

# Inline formset para colecciones asociadas a un cupón
CouponCollectionsFormSet = inlineformset_factory(
    CouponsDB,
    CouponCollectionsDB,
    form=CouponCollectionsForm,
    extra=1,
    can_delete=True
)