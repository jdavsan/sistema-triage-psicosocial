from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from sistema_triage.admin import admin_site 

def redirigir_inicio(request):
    return redirect('solicitudes:inicio')

urlpatterns = [
    path('admin/', admin_site.urls), 
    path('', redirigir_inicio, name='inicio'),
    path('solicitudes/', include('solicitudes.urls')),
    path('encuentros/', include('encuentros.urls')),
    path('calificaciones/', include('calificaciones.urls')),
]

handler404 = 'sistema_triage.views.error_404'
handler500 = 'sistema_triage.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)