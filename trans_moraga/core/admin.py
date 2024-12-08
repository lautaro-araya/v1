from django.contrib import admin
from .models import Encuestador, Propietario, Camiones, Componente, FormularioInspeccion
# Register your models here.
admin.site.register(Encuestador)
admin.site.register(Propietario)
admin.site.register(Camiones)
admin.site.register(Componente)
admin.site.register(FormularioInspeccion)

