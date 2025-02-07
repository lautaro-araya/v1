from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from collections import defaultdict
import datetime
from .models import FormularioInspeccion, Encuestador, Camiones, Componente, Cat_com, InspeccionComponente, Propietario
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CamionesForm, CamionForm, PropietarioForm, PropietarioRegistroForm

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    errors = {}
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contraseña = form.cleaned_data.get("password")
            user = authenticate(username=nombre_usuario, password=contraseña)
            if user is not None:
                login(request, user)
                if hasattr(user, 'propietario'):
                    return redirect('crear_formulario')
                elif hasattr(user, 'encuestador'):
                    return redirect('lista_formularios')
                else:
                    return redirect('default_home')
            else:
                errors['autenticación'] = "*Usuario o contraseña incorrectos."
        else:
            errors['autenticación'] = "*Usuario o contraseña incorrectos."
    form = AuthenticationForm()
    return render(request, "core/login.html", {
        "form": form,
        "errors": errors,
    })

from django.contrib.auth.decorators import user_passes_test

# Verifica si el usuario es propietario
def es_propietario(user):
    return hasattr(user, 'propietario')

# Verifica si el usuario es encuestador
def es_encuestador(user):
    return hasattr(user, 'encuestador')

@login_required
@user_passes_test(es_propietario)
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
        return redirect('crear_formulario')

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


@login_required
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

@login_required
@user_passes_test(es_encuestador)
def lista_formularios(request):
    query = request.GET.get('q', '')  # Captura la búsqueda
    formularios = FormularioInspeccion.objects.all().order_by('-fecha_creacion')

    if query:
        # Intentar convertir la búsqueda en una fecha válida
        try:
            fecha_formateada = datetime.datetime.strptime(query, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            fecha_formateada = None  # No es una fecha válida

        # Filtrar por diferentes campos
        formularios = formularios.filter(
            Q(ubicacion__icontains=query) |  
            Q(encuestador__nombre__icontains=query) |  
            Q(propietario__username__icontains=query) |  
            Q(camion__patente__icontains=query) |  
            Q(camion__sigla_base__icontains=query) |
            (Q(fecha_creacion__date=fecha_formateada) if fecha_formateada else Q())  # Buscar por fecha
        )

    paginator = Paginator(formularios, 6)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    context = {
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'core/lista_formularios.html', context)

@login_required
def ver_camion(request, camion_id):
    camion = get_object_or_404(Camiones, id=camion_id)  # Busca el camión por ID o devuelve 404
    return render(request, 'core/ver_camion.html', {'camion': camion})

@login_required
def editar_camion(request, camion_id):
    camion = get_object_or_404(Camiones, id=camion_id)  # Busca el camión o devuelve 404

    if request.method == 'POST':
        form = CamionForm(request.POST, instance=camion)  # Formulario con los datos del camión
        if form.is_valid():
            form.save()  # Guarda los cambios
            return redirect('ver_camion', camion_id=camion.id)  # Redirige al detalle del camión
    else:
        form = CamionForm(instance=camion)  # Muestra el formulario prellenado

    return render(request, 'core/editar_camion.html', {'form': form, 'camion': camion})

@login_required
def listar_camiones(request): 
    query = request.GET.get('q', '')
    camiones = Camiones.objects.all() 
    if query:
        # Filtrar por diferentes campos
        camiones = camiones.filter(
            Q(patente__icontains=query) |  
            Q(modelo__icontains=query) |  
            Q(marca__icontains=query) |  
            Q(year__icontains=query) |  
            Q(tipo_camion__icontains=query) |  
            Q(sigla_base__icontains=query)
        )

    paginator = Paginator(camiones, 6)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    context = {
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'core/lista_camiones.html', context)

@login_required
def ingresar_camion(request):
    if request.method == 'POST':
        form = CamionesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_camiones')  # Cambia esto por la URL donde quieres redirigir al guardar
    else:
        form = CamionesForm()
    return render(request, 'core/ingresar_camion.html', {'form': form})

@login_required
@login_required
def editar_propietario(request, propietario_id):
    propietario = get_object_or_404(Propietario, id=propietario_id)

    if request.method == 'POST':
        form = PropietarioForm(request.POST, instance=propietario)
        if form.is_valid():
            form.save()
            return redirect('listar_propietarios')
    else:
        form = PropietarioForm(instance=propietario)

    return render(request, 'core/editar_propietario.html', {'form': form, 'propietario': propietario})

@login_required
def listar_propietarios(request): 
    query = request.GET.get('q', '')
    propietarios = Propietario.objects.all()

    if query:
        propietarios = propietarios.filter(
            Q(nombre__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(usuario__username__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono_contacto__icontains=query)
        )

    paginator = Paginator(propietarios, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'core/lista_propietarios.html', context)

@login_required
def ingresar_propietario(request):
    if request.method == 'POST':
        form = PropietarioRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('listar_propietarios')  # Cambia 'inicio' por la vista a la que quieres redirigir
    else:
        form = PropietarioRegistroForm()
    return render(request, 'core/ingresar_propietario.html', {'form': form})