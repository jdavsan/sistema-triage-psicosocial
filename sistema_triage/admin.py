from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Avg
from solicitudes.models import SolicitudAyuda
from encuentros.models import EncuentroVirtual
from calificaciones.models import CalificacionSQLite

class CustomAdminSite(AdminSite):
    site_header = "🏥 Sistema de Triage Psicosocial"
    site_title = "Admin - Triage"
    index_title = "Panel de Administración"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('estadisticas/', self.admin_view(self.estadisticas_view), name='estadisticas'),
        ]
        return custom_urls + urls
    
    def estadisticas_view(self, request):
        """Vista personalizada de estadísticas"""
        context = {
            **self.each_context(request),
            'title': 'Estadísticas del Sistema',
            'total_solicitudes': SolicitudAyuda.objects.count(),
            'solicitudes_pendientes': SolicitudAyuda.objects.filter(estado='pendiente').count(),
            'solicitudes_completadas': SolicitudAyuda.objects.filter(estado='completado').count(),
            'total_encuentros': EncuentroVirtual.objects.count(),
            'encuentros_programados': EncuentroVirtual.objects.filter(estado='programado').count(),
            'total_calificaciones': CalificacionSQLite.objects.count(),
            'promedio_calificaciones': CalificacionSQLite.objects.aggregate(Avg('calificacion'))['calificacion__avg'],
        }
        return render(request, 'admin/estadisticas.html', context)

# Crear instancia del admin personalizado
admin_site = CustomAdminSite(name='custom_admin')