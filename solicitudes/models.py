from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class CategoriaProblema(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría de Problema"
        verbose_name_plural = "Categorías de Problemas"

class Sintoma(models.Model):
    categoria = models.ForeignKey(CategoriaProblema, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria.nombre})"
    
    class Meta:
        verbose_name = "Síntoma"
        verbose_name_plural = "Síntomas"

class SolicitudAyuda(models.Model):
    URGENCIA_CHOICES = [
        ('baja', 'Baja - Agendar'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('crisis', 'Crisis - Intervención Inmediata'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de revisión'),
        ('evaluando', 'En evaluación'),
        ('atencion_inmediata', 'Atención Inmediata'),
        ('programado', 'Encuentro programado'),
        ('completado', 'Completado'),
        ('remitido', 'Remitido a otra entidad'),
    ]
    
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro'),
        ('prefiero_no_decir', 'Prefiero no decir'),
    ]
    
    GRUPO_RAIZAL_CHOICES = [
        ('ninguno', 'No pertenezco a ningún grupo raizal'),
        ('indigena', 'Indígena'),
        ('afrodescendiente', 'Afrodescendiente'),
        ('raizal', 'Raizal'),
        ('palenquero', 'Palenquero'),
        ('gitano', 'Gitano/Rom'),
        ('otro', 'Otro grupo étnico'),
    ]
    
    DISCAPACIDAD_CHOICES = [
        ('ninguna', 'No tengo discapacidad'),
        ('fisica', 'Discapacidad física'),
        ('visual', 'Discapacidad visual'),
        ('auditiva', 'Discapacidad auditiva'),
        ('intelectual', 'Discapacidad intelectual'),
        ('psicosocial', 'Discapacidad psicosocial'),
        ('multiple', 'Discapacidad múltiple'),
        ('otra', 'Otra discapacidad'),
    ]
    
    # Información Personal
    nombre_completo = models.CharField(
        null=True, 
        blank=True, 
        max_length=200, 
        verbose_name="Nombre completo"
    )
    cedula = models.CharField(
        max_length=20, 
        unique=False, 
        null=True, 
        blank=True, 
        verbose_name="Cédula de ciudadanía"
    )
    edad = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name="Edad",
        null=True,  
        blank=True  
    )
    celular = models.CharField(
        max_length=15, 
        default="0000000000",
        verbose_name="Número de celular"
    )
    correo_electronico = models.EmailField(
        default="temp@example.com", 
        verbose_name="Correo electrónico"
    )
    direccion = models.TextField(
        null=True, 
        blank=True, 
        verbose_name="Dirección de residencia"
    )
    genero = models.CharField(
        max_length=20, 
        choices=GENERO_CHOICES, 
        verbose_name="Género",
        null=True,  
        blank=True  
    )
    
    # Información Demográfica
    grupo_raizal = models.CharField(
        max_length=20, 
        choices=GRUPO_RAIZAL_CHOICES, 
        default='ninguno',
        verbose_name="Pertenencia a grupo raizal o étnico"
    )
    discapacidad = models.CharField(
        max_length=20, 
        choices=DISCAPACIDAD_CHOICES, 
        default='ninguna',
        verbose_name="Discapacidad"
    )
    descripcion_discapacidad = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Describa su discapacidad (si aplica)"
    )

    # Información de la Solicitud
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    urgencia = models.CharField(
        max_length=20, 
        choices=URGENCIA_CHOICES, 
        default='media'
    )
    descripcion_problema = models.TextField(
        verbose_name="Descripción del problema"
    )
    categoria_problema = models.ForeignKey(
        CategoriaProblema, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    sintomas_seleccionados = models.ManyToManyField(
        Sintoma, 
        blank=True
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='pendiente'
    )
    requiere_ayuda_basica = models.BooleanField(
        default=False, 
        verbose_name="Requiere ayuda básica"
    )
    informacion_adicional = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Información adicional"
    )
    sesiones_completadas = models.IntegerField(default=0)
    max_sesiones = models.IntegerField(default=6)
    remitido_otra_entidad = models.BooleanField(default=False)
    entidad_remision = models.CharField(
        max_length=200, 
        blank=True, 
        null=True
    )
    
    # Términos y Condiciones - CAMPOS NUEVOS
    acepta_terminos = models.BooleanField(
        default=False,
        verbose_name="Acepta términos y condiciones"
    )
    acepta_tratamiento_datos = models.BooleanField(
        default=False,
        verbose_name="Acepta tratamiento de datos personales"
    )
    
    
    def __str__(self):
        return f"Solicitud #{self.id} - {self.nombre_completo} - {self.urgencia}"
    
    def sesiones_restantes(self):
        """Retorna el número de sesiones restantes"""
        return self.max_sesiones - self.sesiones_completadas
    
    def puede_agendar_sesion(self):
        """Retorna True si puede agendar más sesiones"""
        return self.sesiones_completadas < self.max_sesiones and not self.remitido_otra_entidad
    
    def porcentaje_sesiones(self):
        """Retorna el porcentaje de sesiones completadas"""
        if self.max_sesiones == 0:
            return 0
        return int((self.sesiones_completadas / self.max_sesiones) * 100)
    
    class Meta:
        verbose_name = "Solicitud de Ayuda"
        verbose_name_plural = "Solicitudes de Ayuda"
        ordering = ['-fecha_creacion']
    
    class Meta:
        verbose_name = "Solicitud de Ayuda"
        verbose_name_plural = "Solicitudes de Ayuda"
        ordering = ['-fecha_creacion']