from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view, name='login'),
    path('crear_formulario',views.crear_formulario, name='crear_formulario'),
]