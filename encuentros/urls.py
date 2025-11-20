from django.urls import path
from . import views

app_name = 'encuentros'

urlpatterns = [
    path('', views.lista_encuentros, name='lista_encuentros'),
    path('detalle/<int:encuentro_id>/', views.detalle_encuentro, name='detalle_encuentro'),
    path('programar/', views.programar_encuentro, name='programar_encuentro'),
]