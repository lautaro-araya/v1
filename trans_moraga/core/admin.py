from django.contrib import admin

from .models import Camiones, Propietario, Encuestador, FormularioInspeccion, Componente
# Register your models here.
admin.site.register(Camiones)
admin.site.register(Propietario)
admin.site.register(Encuestador)
admin.site.register(FormularioInspeccion)
admin.site.register(Componente)