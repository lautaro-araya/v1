from .models import Camiones, Propietario
from django import forms

class CamionForm(forms.ModelForm):
    class Meta:
        model = Camiones
        fields = ['patente', 'modelo', 'year', 'tipo_camion', 'marca', 'sigla_base']

class CamionesForm(forms.ModelForm):
    class Meta:
        model = Camiones
        fields = ['patente', 'modelo', 'year', 'tipo_camion', 'marca', 'sigla_base']
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_camion': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla_base': forms.TextInput(attrs={'class': 'form-control'}),
        }



class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = ['nombre', 'apellidos', 'direccion', 'telefono_contacto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control'}),
        }