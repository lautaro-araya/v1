from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import FormularioInspeccion, Encuestador, Camiones, Componente, Cat_com, InspeccionComponente
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
                return redirect('lista_formularios')
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
        # Procesar el formulario enviado
        propietario = request.user  # Usuario actual
        encuestador_id = request.POST.get('encuestador')
        camion_id = request.POST.get('camion')
        ubicacion = request.POST.get('ubicacion')

        encuestador = Encuestador.objects.get(id=encuestador_id)
        camion = Camiones.objects.get(id=camion_id)

        # Crear formulario de inspección
        formulario = FormularioInspeccion.objects.create(
            propietario=propietario,
            encuestador=encuestador,
            camion=camion,
            ubicacion=ubicacion
        )

        # Procesar inspecciones de componentes
        for key, value in request.POST.items():
            if key.startswith('components'):  # Filtrar las claves que pertenecen a componentes
                # Extraer los datos del formato 'components[categoria][indice][campo]'
                parts = key.split('[')
                if len(parts) == 4:
                    categoria = parts[1].strip(']')
                    indice = parts[2].strip(']')
                    campo = parts[3].strip(']')

                    # Buscar valores asociados a esta clave
                    componente_id = request.POST.get(f'components[{categoria}][{indice}][componente]')
                    inspeccion = request.POST.get(f'components[{categoria}][{indice}][inspeccion]')
                    observacion = request.POST.get(f'components[{categoria}][{indice}][observacion]', '')

                    if componente_id and inspeccion:
                        componente = Componente.objects.get(id=componente_id)
                        
                        # Verificar si ya existe una inspección para este componente y formulario
                        if not InspeccionComponente.objects.filter(formulario=formulario, componente=componente).exists():
                            InspeccionComponente.objects.create(
                                formulario=formulario,
                                componente=componente,
                                inspeccion=inspeccion,
                                observacion=observacion
                            )
        return redirect('lista_formularios')

    # Preparar datos para el formulario
    encuestadores = Encuestador.objects.all()
    camiones = Camiones.objects.all()

    categorias = {
        categoria.nombre: Componente.objects.filter(categoria=categoria)
        for categoria in Cat_com.objects.all()
    }

    return render(request, 'core/crear_formulario.html', {
        'encuestadores': encuestadores,
        'camiones': camiones,
        'categorias': categorias
    })


def ver_formulario(request, formulario_id):
    formulario = FormularioInspeccion.objects.get(id=formulario_id)
    inspecciones = InspeccionComponente.objects.filter(formulario=formulario).select_related('componente__categoria')

    # Agrupar inspecciones por categoría
    inspecciones_por_categoria = defaultdict(list)
    for inspeccion in inspecciones:
        categoria = inspeccion.componente.categoria.nombre
        inspecciones_por_categoria[categoria].append(inspeccion)

    context = {
        'formulario': formulario,
        'inspecciones_por_categoria': dict(inspecciones_por_categoria)
    }
    return render(request, 'core/ver_formulario.html', context)

def lista_formularios(request):
    # Obtener todos los formularios ordenados por fecha de creación
    formularios = FormularioInspeccion.objects.all().order_by('-fecha_creacion')
    context = {
        'formularios': formularios,
    }
    return render(request, 'core/lista_formularios.html', context)