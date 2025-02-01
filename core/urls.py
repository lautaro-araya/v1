from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view, name='login'),
    path('crear_formulario',views.crear_formulario, name='crear_formulario'),
    path('ver_formulario/<int:formulario_id>/', views.ver_formulario, name='ver_formulario'),
    path('lista-formularios/', views.lista_formularios, name='lista_formularios'),
    path('lista-camiones/', views.listar_camiones, name='lista_camiones'),
    path('ver-camion/<int:camion_id>/', views.ver_camion, name='ver_camion'),
    path('editar-camion/<int:camion_id>/', views.editar_camion, name='editar_camion'),
    path('ingresar-camion/', views.ingresar_camion, name='ingresar_camion'),
    path('logout/', views.logout_view, name='logout'),
]