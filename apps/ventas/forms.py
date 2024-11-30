# apps/ventas/forms.py
from django import forms
from .models import Venta

class VentaForm(forms.Form):
    producto = forms.CharField(max_length=100)  # El producto lo seleccionamos manualmente
    cantidad = forms.IntegerField(min_value=1)
