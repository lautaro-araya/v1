from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view, name='login'),
    path('crear_formulario',views.crear_formulario, name='crear_formulario'),
     path('ver_formulario/<int:formulario_id>/', views.ver_formulario, name='ver_formulario'),
     path('formularios/', views.lista_formularios, name='lista_formularios'),
]