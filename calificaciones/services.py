from django.conf import settings
from .models import CalificacionSQLite, CalificacionMongoDB

class CalificacionService:
    """Servicio para manejar calificaciones en ambas bases de datos"""
    
    @staticmethod
    def guardar_calificacion(nombre, comentario, calificacion, tipo_bd=None):
        """Guarda en la base de datos especificada"""
        if tipo_bd is None:
            tipo_bd = settings.TIPO_BASE_DATOS
        
        if tipo_bd == 'sqlite':
            # Guardar en SQLite
            calificacion_obj = CalificacionSQLite(
                nombre=nombre,
                comentario=comentario,
                calificacion=calificacion
            )
            calificacion_obj.save()
            return calificacion_obj
            
        elif tipo_bd == 'mongodb':
            # Guardar en MongoDB
            calificacion_obj = CalificacionMongoDB(
                nombre=nombre,
                comentario=comentario, 
                calificacion=calificacion
            )
            calificacion_obj.save()
            return calificacion_obj
    
    @staticmethod
    def obtener_calificaciones(tipo_bd=None):
        """Obtiene calificaciones de la base de datos especificada"""
        if tipo_bd is None:
            tipo_bd = settings.TIPO_BASE_DATOS
        
        if tipo_bd == 'sqlite':
            return CalificacionSQLite.objects.all().order_by('-fecha_creacion')
        elif tipo_bd == 'mongodb':
            return CalificacionMongoDB.objects.using('mongodb').all().order_by('-fecha_creacion')
    
    @staticmethod
    def cambiar_base_datos(nueva_bd):
        """Cambia la base de datos global"""
        if nueva_bd in ['sqlite', 'mongodb']:
            from django.conf import settings
            settings.TIPO_BASE_DATOS = nueva_bd
            return True
        return False