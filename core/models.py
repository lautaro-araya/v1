from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Encuestador(models.Model):
    nombre =  models.CharField(max_length=255, null=True, blank=True)
    apellidos =  models.CharField(max_length=255, null=True, blank=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='encuestador')
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20, null=True, blank=True)
    firma = models.ImageField(upload_to="firmas",verbose_name="Firma",null=True , default='Sin Firma' )


class Propietario(models.Model):
    nombre =  models.CharField(max_length=255, null=True, blank=True)
    apellidos =  models.CharField(max_length=255, null=True, blank=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='propietario')
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20, null=True, blank=True)
    firma = models.ImageField(upload_to="firmas",verbose_name="Firma",null=True , default='Sin Firma' )

    
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

    
    def __str__(self):
        return self.sigla_base

#categoria componente
class Cat_com(models.Model):
    nombre =models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
    

class Componente(models.Model):
    categoria = models.ForeignKey(Cat_com,on_delete=models.CASCADE)
    componente = models.CharField(max_length=255)  # Ejemplo: "Neumáticos Direccionales"
    
    def __str__(self):
        return self.componente

class FormularioInspeccion(models.Model):
    propietario = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    encuestador = models.ForeignKey(Encuestador,on_delete=models.CASCADE)
    camion = models.ForeignKey(Camiones,on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ubicacion = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Formulario de {self.propietario},{self.fecha_creacion}"

class InspeccionComponente(models.Model):
    formulario = models.ForeignKey('FormularioInspeccion', on_delete=models.CASCADE)
    componente = models.ForeignKey('Componente', on_delete=models.CASCADE)
    inspeccion = models.CharField(max_length=1, choices=[('M', 'Malo'), ('R', 'Regular'), ('B', 'Bueno')])
    observacion = models.TextField(blank=True, null=True)

