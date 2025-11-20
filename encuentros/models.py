from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator 
from solicitudes.models import SolicitudAyuda  # AGREGAR ESTA LÍNEA

class TrabajadorSocial(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    disponible = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "Trabajador Social"
        verbose_name_plural = "Trabajadores Sociales"

class EncuentroVirtual(models.Model):
    ESTADO_CHOICES = [
        ('programado', 'Programado'),
        ('en_curso', 'En Curso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),  # AGREGAR ESTA OPCIÓN
    ]
    
    # AGREGAR ESTA LÍNEA - Relación con la solicitud
    solicitud = models.ForeignKey(
        SolicitudAyuda, 
        on_delete=models.CASCADE,
        related_name='encuentros',
        null=True,
        blank=True
    )
    
    trabajador_social = models.ForeignKey(TrabajadorSocial, on_delete=models.CASCADE)
    fecha_programada = models.DateTimeField()
    duracion_estimada = models.IntegerField(help_text="Duración en minutos")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programado')
    
    def __str__(self):
        return f"Encuentro {self.id}"

# Relación OneToOne: Un encuentro tiene UNA evaluación
class EvaluacionEncuentro(models.Model):
    encuentro = models.OneToOneField(
        EncuentroVirtual, 
        on_delete=models.CASCADE,
        related_name='evaluacion'
    )
    calidad_atencion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentarios = models.TextField(blank=True)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Evaluación del Encuentro {self.encuentro.id}"
    
    class Meta:
        verbose_name = "Evaluación de Encuentro"
        verbose_name_plural = "Evaluaciones de Encuentros"

# Relación ForeignKey: Múltiples notas por encuentro
class NotaEncuentro(models.Model):
    encuentro = models.ForeignKey(
        EncuentroVirtual,
        on_delete=models.CASCADE,
        related_name='notas'
    )
    trabajador_social = models.ForeignKey(
        TrabajadorSocial,
        on_delete=models.CASCADE
    )
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    privada = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Nota de Encuentro"
        verbose_name_plural = "Notas de Encuentros"
    
    def __str__(self):
        return f"Nota - Encuentro {self.encuentro.id}"

# Relación ManyToMany: Múltiples recursos pueden usarse en múltiples encuentros
class RecursoTerapeutico(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, choices=[
        ('documento', 'Documento'),
        ('video', 'Video'),
        ('ejercicio', 'Ejercicio'),
        ('enlace', 'Enlace externo'),
    ])
    url = models.URLField(blank=True, null=True)
    encuentros = models.ManyToManyField(
        EncuentroVirtual,
        related_name='recursos',
        blank=True
    )
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Recurso Terapéutico"
        verbose_name_plural = "Recursos Terapéuticos"