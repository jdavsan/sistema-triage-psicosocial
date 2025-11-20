from django.contrib import admin
from django.utils.html import format_html
from sistema_triage.admin import admin_site
from .models import SolicitudAyuda, CategoriaProblema, Sintoma

@admin.register(SolicitudAyuda)
class SolicitudAyudaAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'nombre_completo', 'cedula', 'mostrar_urgencia', 
        'estado', 'fecha_creacion', 'acciones_rapidas'
    ]
    
    list_filter = ['urgencia', 'estado', 'fecha_creacion', 'requiere_ayuda_basica']
    search_fields = ['nombre_completo', 'cedula', 'descripcion_problema']
    list_per_page = 25
    date_hierarchy = 'fecha_creacion'
    
    # Campos de solo lectura
    readonly_fields = ['fecha_creacion', 'informacion_completa']
    
    # Configuración de campos en el formulario de edición
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'nombre_completo', 'cedula', 'edad', 'celular',
                'correo_electronico', 'direccion', 'genero'
            )
        }),
        ('Información de la Solicitud', {
            'fields': (
                'urgencia', 'descripcion_problema', 'categoria_problema',
                'sintomas_seleccionados', 'requiere_ayuda_basica', 'estado'
            )
        }),
        ('Seguimiento y Análisis', {
            'fields': ('informacion_adicional', 'informacion_completa'),
            'classes': ('collapse',)
        }),
    )
    
    # Filtros laterales avanzados
    class UrgenciaFilter(admin.SimpleListFilter):
        title = 'Nivel de Urgencia'
        parameter_name = 'urgencia'
        
        def lookups(self, request, model_admin):
            return [
                ('crisis', 'Crisis (Alta Prioridad)'),
                ('alta', 'Alta Urgencia'),
                ('media_baja', 'Media/Baja Urgencia'),
            ]
        
        def queryset(self, request, queryset):
            if self.value() == 'crisis':
                return queryset.filter(urgencia='crisis')
            elif self.value() == 'alta':
                return queryset.filter(urgencia='alta')
            elif self.value() == 'media_baja':
                return queryset.filter(urgencia__in=['media', 'baja'])
    
    list_filter = [UrgenciaFilter, 'estado', 'fecha_creacion']
    
    # Métodos personalizados
    def mostrar_urgencia(self, obj):
        """Muestra la urgencia con colores"""
        colors = {
            'crisis': '#e74c3c',
            'alta': '#e67e22', 
            'media': '#f39c12',
            'baja': '#27ae60'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.urgencia, '#333'),
            obj.get_urgencia_display()
        )
    mostrar_urgencia.short_description = 'Urgencia'
    
    def informacion_completa(self, obj):
        """Muestra información resumida de la solicitud"""
        return format_html(
            '''
            <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                <strong>Resumen:</strong><br>
                <strong>Edad:</strong> {} años<br>
                <strong>Contacto:</strong> {} | {}<br>
                <strong>Síntomas:</strong> {}<br>
                <strong>Ayuda Básica:</strong> {}
            </div>
            ''',
            obj.edad,
            obj.celular,
            obj.correo_electronico,
            ", ".join([s.nombre for s in obj.sintomas_seleccionados.all()][:3]),
            "Sí" if obj.requiere_ayuda_basica else "No"
        )
    informacion_completa.short_description = 'Información Completa'
    
    def acciones_rapidas(self, obj):
        """Botones de acción rápida"""
        return format_html(
            '''
            <div>
                <a href="/admin/solicitudes/solicitudayuda/{}/change/" class="button" title="Editar">✏️</a>
                <a href="/solicitudes/{}/" class="button" title="Ver en sitio" target="_blank">👁️</a>
            </div>
            ''',
            obj.id, obj.id
        )
    acciones_rapidas.short_description = 'Acciones'
    
    # Acciones personalizadas
    actions = ['marcar_como_completadas', 'derivar_a_encuentro']
    
    def marcar_como_completadas(self, request, queryset):
        """Marca solicitudes como completadas"""
        updated = queryset.update(estado='completado')
        self.message_user(request, f'{updated} solicitudes marcadas como completadas.')
    marcar_como_completadas.short_description = '✅ Marcar como completadas'
    
    def derivar_a_encuentro(self, request, queryset):
        """Deriva solicitudes para encuentro virtual"""
        for solicitud in queryset.filter(estado='pendiente'):
            # Lógica para crear encuentro automáticamente
            solicitud.estado = 'programado'
            solicitud.save()
        self.message_user(request, f'{queryset.count()} solicitudes derivadas a encuentros.')
    derivar_a_encuentro.short_description = '👥 Derivar a encuentro virtual'

# Admin para Categorías y Síntomas
@admin.register(CategoriaProblema)
class CategoriaProblemaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cantidad_sintomas', 'descripcion_corta']
    search_fields = ['nombre', 'descripcion']
    
    def cantidad_sintomas(self, obj):
        return obj.sintoma_set.count()
    cantidad_sintomas.short_description = 'Síntomas'
    
    def descripcion_corta(self, obj):
        return obj.descripcion[:100] + '...' if len(obj.descripcion) > 100 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

@admin.register(Sintoma)
class SintomaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'descripcion_corta']
    list_filter = ['categoria']
    search_fields = ['nombre', 'descripcion']
    
    def descripcion_corta(self, obj):
        return obj.descripcion[:80] + '...' if len(obj.descripcion) > 80 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'



admin_site.register(SolicitudAyuda)
admin_site.register(CategoriaProblema)
admin_site.register(Sintoma)
