from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import login_required
from .models import FormularioInspeccion, Componente, Camiones
from django.contrib.auth.models import User

def crear_formulario(request):
    if request.method == 'POST':
        # Obtener datos generales del formulario
        propietario = request.POST.get('propietario')
        encuestador_id = request.POST.get('encuestador')
        encuestador = User.objects.get(id=encuestador_id)

        # Crear el formulario de inspección
        formulario = FormularioInspeccion.objects.create(
            propietario=propietario,
            encuestador=encuestador
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
                    categoria=categoria.capitalize(),  # Ejemplo: Externos, Motor, Eléctrico
                    componente=componente,
                    inspeccion=inspeccion,
                    observacion=observacion
                )

        # Redirigir al usuario a una página de éxito o lista
        return redirect('lista_formularios')

    # Obtener los usuarios que pueden ser encuestadores
    encuestadores = User.objects.all()

    return render(request, 'core/crear_formulario.html', {'encuestadores': encuestadores})

