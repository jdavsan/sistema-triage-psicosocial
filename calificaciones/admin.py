from django.contrib import admin
from django.utils.html import format_html
from .models import CalificacionSQLite

@admin.register(CalificacionSQLite)
class CalificacionSQLiteAdmin(admin.ModelAdmin):
    """Admin para calificaciones en SQLite"""
    
    # Configuración de la lista
    list_display = [
        'nombre', 
        'mostrar_calificacion', 
        'comentario_corto', 
        'fecha_creacion',
        'acciones_personalizadas'
    ]
    
    list_filter = ['calificacion', 'fecha_creacion']
    search_fields = ['nombre', 'comentario']
    list_per_page = 20
    ordering = ['-fecha_creacion']
    
    # Campos de solo lectura
    readonly_fields = ['fecha_creacion', 'calificacion_estrellas']
    
    # Agrupamiento de campos en el formulario de edición
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre',),
        }),
        ('Evaluación', {
            'fields': ('calificacion', 'calificacion_estrellas'),
            'description': 'Calificación del servicio (1-5 estrellas)'
        }),
        ('Comentario', {
            'fields': ('comentario',),
            'description': 'Comentarios adicionales del usuario'
        }),
        ('Metadata', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )
    
    # Métodos personalizados para display
    def mostrar_calificacion(self, obj):
        """Muestra la calificación con colores según el valor"""
        if obj.calificacion <= 2:
            color = '#e74c3c'  # Rojo
        elif obj.calificacion <= 3:
            color = '#f39c12'  # Naranja
        else:
            color = '#27ae60'  # Verde
        
        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 1.1em;">⭐ {}/5</span>',
            color, obj.calificacion
        )
    mostrar_calificacion.short_description = '⭐ Calificación'
    mostrar_calificacion.admin_order_field = 'calificacion'
    
    def comentario_corto(self, obj):
        """Muestra un preview del comentario"""
        if obj.comentario:
            if len(obj.comentario) > 60:
                return obj.comentario[:60] + '...'
            return obj.comentario
        return format_html('<span style="color: #999;">Sin comentario</span>')
    comentario_corto.short_description = '💬 Comentario'
    
    def calificacion_estrellas(self, obj):
        """Muestra estrellas según la calificación"""
        estrellas_llenas = '⭐' * obj.calificacion
        estrellas_vacias = '☆' * (5 - obj.calificacion)
        
        return format_html(
            '<div style="font-size: 1.3em; letter-spacing: 2px;">{}{}</div>',
            estrellas_llenas,
            estrellas_vacias
        )
    calificacion_estrellas.short_description = '⭐ Vista de estrellas'
    
    def acciones_personalizadas(self, obj):
        """Botones de acción personalizados"""
        return format_html(
            '''
            <div style="display: flex; gap: 5px;">
                <a href="/admin/calificaciones/calificacionsqlite/{}/change/" 
                   class="button" 
                   style="padding: 3px 8px; background: #3498db; color: white; text-decoration: none; border-radius: 3px; font-size: 0.9em;">
                   ✏️ Editar
                </a>
                <a href="/admin/calificaciones/calificacionsqlite/{}/delete/" 
                   class="button" 
                   style="padding: 3px 8px; background: #e74c3c; color: white; text-decoration: none; border-radius: 3px; font-size: 0.9em;">
                   🗑️ Eliminar
                </a>
            </div>
            ''',
            obj.id, obj.id
        )
    acciones_personalizadas.short_description = '🔧 Acciones'
    
    # Acciones personalizadas en lote
    actions = ['marcar_como_excelente', 'exportar_calificaciones']
    
    def marcar_como_excelente(self, request, queryset):
        """Acción para marcar calificaciones como excelentes (5 estrellas)"""
        updated_count = queryset.update(calificacion=5)
        
        self.message_user(
            request, 
            f'✅ {updated_count} calificación(es) actualizada(s) a 5 estrellas.',
            level='success'
        )
    marcar_como_excelente.short_description = '⭐ Cambiar a 5 estrellas (excelente)'
    
    def exportar_calificaciones(self, request, queryset):
        """Acción para exportar calificaciones seleccionadas"""
        total = queryset.count()
        promedio = sum(q.calificacion for q in queryset) / total if total > 0 else 0
        
        self.message_user(
            request,
            f'📊 {total} calificación(es) seleccionada(s). Promedio: {promedio:.1f}/5',
            level='info'
        )
    exportar_calificaciones.short_description = '📊 Ver estadísticas de selección'
    
    # Personalización del formulario
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Personalizar el widget de calificación
        if 'calificacion' in form.base_fields:
            form.base_fields['calificacion'].help_text = '⭐ Selecciona de 1 a 5 estrellas'
        
        if 'comentario' in form.base_fields:
            form.base_fields['comentario'].help_text = '💬 Comentarios adicionales del usuario (opcional)'
        
        return form
    
    # Estadísticas en el changelist
    def changelist_view(self, request, extra_context=None):
        """Agregar estadísticas al listado"""
        extra_context = extra_context or {}
        
        # Calcular estadísticas
        queryset = self.get_queryset(request)
        total = queryset.count()
        
        if total > 0:
            promedio = sum(q.calificacion for q in queryset) / total
            excelentes = queryset.filter(calificacion=5).count()
            buenas = queryset.filter(calificacion=4).count()
            regulares = queryset.filter(calificacion=3).count()
            malas = queryset.filter(calificacion__lte=2).count()
            
            extra_context['estadisticas'] = {
                'total': total,
                'promedio': round(promedio, 2),
                'excelentes': excelentes,
                'buenas': buenas,
                'regulares': regulares,
                'malas': malas,
            }
        
        return super().changelist_view(request, extra_context=extra_context)


# Personalización del sitio de administración
admin.site.site_header = "🌟 Sistema de Calificaciones - Panel de Administración"
admin.site.site_title = "Calificaciones Admin"
admin.site.index_title = "Bienvenido al Panel de Gestión de Calificaciones"