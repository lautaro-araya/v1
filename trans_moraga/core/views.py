from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import login_required
from .models import FormularioInspeccion, Componente, Camiones
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    errors = {}
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        
        # Validaciones automáticas de AuthenticationForm
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contraseña = form.cleaned_data.get("password")
            user = authenticate(username=nombre_usuario, password=contraseña)
            if user is not None:
                login(request, user)
                return redirect('')
            else:
                errors['autenticación'] = "*Usuario o contraseña incorrectos."
        else:
            errors['autenticación'] = "Usuario o contraseña incorrectos."

    form = AuthenticationForm()

    return render(request, "core/login.html", {
        "form": form,
        "errors": errors,
    })


#@login_required
def crear_formulario(request):
    if request.method == 'POST':
        # Obtener datos generales del formulario
        propietario = request.POST.get('propietario')
        encuestador_id = request.POST.get('encuestador')
        camion_id = request.POST.get('camion')

        encuestador = User.objects.get(id=encuestador_id)
        camion = Camiones.objects.get(id=camion_id)

        # Crear el formulario de inspección
        formulario = FormularioInspeccion.objects.create(
            propietario=propietario,
            encuestador=encuestador,
            camion=camion
        )

        # Procesar componentes por categoría
        categorias = ['externos', 'motor', 'electrico']
        for categoria in categorias:
            componentes = request.POST.getlist(f'components[{categoria}][0][componente]')
            inspecciones = request.POST.getlist(f'components[{categoria}][0][inspeccion]')
            observaciones = request.POST.getlist(f'components[{categoria}][0][observacion]')

            # Crear los componentes asociados al formulario
            for componente, inspeccion, observacion in zip(componentes, inspecciones, observaciones):
                Componente.objects.create(
                    formulario=formulario,
                    categoria=categoria.capitalize(),
                    componente=componente,
                    inspeccion=inspeccion,
                    observacion=observacion
                )

        # Redirigir al usuario a una página de éxito o lista
        return redirect('lista_formularios')

    # Obtener los usuarios y camiones disponibles
    encuestadores = User.objects.all()
    camiones = Camiones.objects.all()

    return render(request, 'core/crear_formulario.html', {
        'encuestadores': encuestadores,
        'camiones': camiones
    })

