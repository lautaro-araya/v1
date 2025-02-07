from .models import Camiones, Propietario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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

class PropietarioRegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(max_length=255)
    apellidos = forms.CharField(max_length=255)
    direccion = forms.CharField(max_length=255)
    telefono_contacto = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nombre', 'apellidos', 'direccion', 'telefono_contacto']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # Asegurar que NO sea staff
        if commit:
            user.save()
            propietario = Propietario.objects.create(
                usuario=user,
                nombre=self.cleaned_data['nombre'],
                apellidos=self.cleaned_data['apellidos'],
                direccion=self.cleaned_data['direccion'],
                telefono_contacto=self.cleaned_data['telefono_contacto']
            )
        return user