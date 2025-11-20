from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class CalificacionBase(models.Model):
    nombre = models.CharField(max_length=100)
    comentario = models.TextField(blank=True)
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

class CalificacionSQLite(CalificacionBase):
    def __str__(self):
        return f"{self.nombre} - {self.calificacion}/5"
    
    class Meta:
        db_table = 'calificaciones_calificacion'
        ordering = ['-fecha_creacion']


def get_calificacion_model():
    """Retorna el modelo según la configuración"""
    tipo_bd = getattr(settings, 'TIPO_BASE_DATOS', 'sqlite')
    return CalificacionSQLite