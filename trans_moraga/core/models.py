from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Encuestador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20, null=True, blank=True)
    firma = models.ImageField(upload_to="firmas",verbose_name="Firma",null=True , default='Sin Firma' )

    def __str__(self):
        return f"Encuestador: {self.usuario.username}"

class Propietario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20, null=True, blank=True)
    firma = models.ImageField(upload_to="firmas",verbose_name="Firma",null=True , default='Sin Firma' )

    def __str__(self):
        return f"Propietario: {self.usuario.username}" 
    
class Camiones(models.Model):
    patente = models.CharField(max_length=8)
    modelo = models.CharField(max_length=255)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1970),
            MaxValueValidator(datetime.date.today().year)
        ]
    )
    tipo_camion = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    sigla_base = models.CharField(max_length=10)


class FormularioInspeccion(models.Model):
    propietario = models.CharField(max_length=255)
    encuestador = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Componente(models.Model):
    formulario = models.ForeignKey(FormularioInspeccion, on_delete=models.CASCADE, related_name='componentes')
    categoria = models.CharField(max_length=255)  # Ejemplo: "Componentes Externos", "Motor"
    componente = models.CharField(max_length=255)  # Ejemplo: "Neumáticos Direccionales"
    inspeccion = models.CharField(max_length=1, choices=[('M', 'Malo'), ('R', 'Regular'), ('B', 'Bueno')])
    observacion = models.TextField(blank=True, null=True)