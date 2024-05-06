from django import forms
from .models import *

class PedidosForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['producto', 'numLinea', 'descuento', 'cantidad', 'totalNetoLinea', 'totalBrutoLinea',  'comentario', 'tipoObjetoDocBase', 'docEntryBase', 'numLineaBase', 'fechaEntrega', 'direccionEntrega', 'documento', 'tipoentrega', 'tipoobjetoSap']



