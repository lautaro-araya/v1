from .models import Camiones
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