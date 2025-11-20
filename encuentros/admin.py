from django.contrib import admin
from .models import TrabajadorSocial, EncuentroVirtual

@admin.register(TrabajadorSocial)
class TrabajadorSocialAdmin(admin.ModelAdmin):
    list_display = ['user', 'especialidad', 'telefono', 'disponible']
    list_filter = ['disponible', 'especialidad']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

@admin.register(EncuentroVirtual)
class EncuentroVirtualAdmin(admin.ModelAdmin):
    list_display = ['id', 'trabajador_social', 'fecha_programada', 'duracion_estimada', 'estado']
    list_filter = ['estado', 'fecha_programada']
    search_fields = ['trabajador_social__user__username']
    date_hierarchy = 'fecha_programada'