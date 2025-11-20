from django.urls import path
from . import views

app_name = 'solicitudes'

urlpatterns = [
    path('', views.pagina_principal, name='inicio'),
    path('crear/', views.crear_solicitud, name='crear_solicitud'), #ruta estáttica
    path('<int:solicitud_id>/', views.detalle_solicitud, name='detalle_solicitud'), #ruta dinamica "captutra de directorio"
    path('<int:solicitud_id>/evaluacion/', views.evaluacion_sintomas, name='evaluacion_sintomas'),
    path('<int:solicitud_id>/crisis/', views.atencion_inmediata, name='atencion_inmediata'),
    path('<int:solicitud_id>/confirmacion/', views.confirmacion_solicitud, name='confirmacion_solicitud'),
    # Rutas dinámicas con múltiples parámetros
    path('solicitud/<int:solicitud_id>/seguimiento/<int:sesion_numero>/', 
         views.seguimiento_sesion, name='seguimiento_sesion'),
    
    # Rutas con slug
    path('categoria/<slug:categoria_slug>/solicitudes/', 
         views.solicitudes_por_categoria, name='solicitudes_por_categoria'),
    
    # Rutas con filtros múltiples
    path('buscar/<str:estado>/<str:urgencia>/', 
         views.buscar_solicitudes, name='buscar_solicitudes'),
    
    # Rutas con parámetros opcionales usando query params
    path('reporte/', views.generar_reporte, name='generar_reporte'),
]
