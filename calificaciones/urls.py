from django.urls import path
from . import views

app_name = 'calificaciones'

urlpatterns = [
    # RUTAS VISTAS BASADAS EN FUNCIONES
    path('crear/', views.crear_calificacion, name='crear_calificacion'),
    path('lista/', views.lista_calificaciones, name='lista_calificaciones'),
    path('detalle/<str:id>/', views.detalle_calificacion, name='detalle_calificacion'),
    path('cambiar-bd/', views.cambiar_base_datos, name='cambiar_base_datos'),
    
    # RUTAS VISTAS GENÉRICAS
    path('cbv/lista/', views.CalificacionListView.as_view(), name='lista_calificaciones_cbv'),
    path('cbv/detalle/<int:pk>/', views.CalificacionDetailView.as_view(), name='detalle_calificacion_cbv'),
    path('cbv/crear/', views.CalificacionCreateView.as_view(), name='crear_calificacion_cbv'),
    path('cbv/editar/<int:pk>/', views.CalificacionUpdateView.as_view(), name='editar_calificacion_cbv'),
    path('cbv/eliminar/<int:pk>/', views.CalificacionDeleteView.as_view(), name='eliminar_calificacion_cbv'),
    path('estadisticas/', views.estadisticas_calificaciones, name='estadisticas'),

]




