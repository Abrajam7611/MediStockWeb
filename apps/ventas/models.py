# apps/ventas/models.py
from django.db import models

class Venta(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False  # Esto evita que Django intente crear o gestionar la tabla en SQLite.

    def __str__(self):
        return f"Venta {self.id} - {self.producto}"
