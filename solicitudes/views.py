from django.shortcuts import render, get_object_or_404, redirect #SHORTCUTS
from django.http import Http404
from django.utils import timezone
from django.contrib import messages
from solicitudes.forms import SolicitudAyudaForm
from .models import SolicitudAyuda, CategoriaProblema, Sintoma
from encuentros.models import TrabajadorSocial, EncuentroVirtual
from django.contrib.auth.models import User

def pagina_principal(request):
    """Página principal"""
    return render(request, 'solicitudes/inicio.html')

def crear_solicitud(request):
    """Paso 2: Comentar su situación y razón del acompañamiento"""
    if request.method == 'POST':
        form = SolicitudAyudaForm(request.POST) 
        if form.is_valid():
            
            solicitud = form.save(commit=False) #crea automáticamente el objeto en la BD, pero no lo guarda inmediatamente
            solicitud.estado = 'pendiente'
            solicitud.save() #uardar en BD
            form.save_m2m()  # relaciones ManyToMany
            
            if solicitud.urgencia == 'crisis':
                return redirect('solicitudes:atencion_inmediata', solicitud_id=solicitud.id)
            else:
                return redirect('solicitudes:evaluacion_sintomas', solicitud_id=solicitud.id)
        else:
            
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = SolicitudAyudaForm()
    
    return render(request, 'solicitudes/crear_solicitud.html', {'form': form})


def evaluacion_sintomas(request, solicitud_id):
    """Paso 3: Evaluación de síntomas, causas y elementos clave"""
    solicitud = get_object_or_404(SolicitudAyuda, id=solicitud_id)
    
    if request.method == 'POST':
        sintomas = request.POST.getlist('sintomas')
        causas = request.POST.get('causas', '')
        elementos_clave = request.POST.get('elementos_clave', '')
        observaciones = request.POST.get('observaciones', '')
        
        solicitud.informacion_adicional = f"Causas: {causas}\nElementos clave: {elementos_clave}\nObservaciones: {observaciones}"
        solicitud.save()
        
        messages.success(request, 'Evaluación completada. Será contactado por un trabajador social.')
        
        return redirect('solicitudes:confirmacion_solicitud', solicitud_id=solicitud.id)
    
    return render(request, 'solicitudes/evaluacion_sintomas.html', {
        'solicitud': solicitud
    })

def atencion_inmediata(request, solicitud_id):
    """Paso 4: Intervención inmediata para crisis"""
    solicitud = get_object_or_404(SolicitudAyuda, id=solicitud_id)
    
    solicitud.urgencia = 'crisis'
    solicitud.estado = 'atencion_inmediata'
    solicitud.save()
    
    trabajadores_disponibles = TrabajadorSocial.objects.filter(disponible=True)
    
    return render(request, 'solicitudes/atencion_inmediata.html', {
        'solicitud': solicitud,
        'trabajadores_disponibles': trabajadores_disponibles
    })

def detalle_solicitud(request, solicitud_id):
    """Ver detalle de solicitud"""
    solicitud = get_object_or_404(SolicitudAyuda, id=solicitud_id)
    return render(request, 'solicitudes/detalle_solicitud.html', {'solicitud': solicitud})

def confirmacion_solicitud(request, solicitud_id):
    """Confirmación de que la solicitud fue recibida"""
    solicitud = get_object_or_404(SolicitudAyuda, id=solicitud_id)
    return render(request, 'solicitudes/confirmacion_solicitud.html', {'solicitud': solicitud})

def pagina_no_encontrada(request, exception):
    return render(request, '404.html', status=404)



def seguimiento_sesion(request, solicitud_id, sesion_numero):
    """Vista con múltiples parámetros dinámicos"""
    solicitud = get_object_or_404(SolicitudAyuda, id=solicitud_id)
    
    context = {
        'solicitud': solicitud,
        'sesion_numero': sesion_numero,
        'progreso': (sesion_numero / solicitud.max_sesiones) * 100
    }
    return render(request, 'solicitudes/seguimiento_sesion.html', context)

def solicitudes_por_categoria(request, categoria_slug):
    """Vista con slug parameter"""
    categoria = get_object_or_404(CategoriaProblema, nombre__iexact=categoria_slug.replace('-', ' '))
    solicitudes = SolicitudAyuda.objects.filter(categoria_problema=categoria)
    
    return render(request, 'solicitudes/por_categoria.html', {
        'categoria': categoria,
        'solicitudes': solicitudes
    })

def buscar_solicitudes(request, estado, urgencia):
    """Vista con múltiples filtros dinámicos"""
    solicitudes = SolicitudAyuda.objects.filter(
        estado=estado,
        urgencia=urgencia
    ).order_by('-fecha_creacion')
    
    return render(request, 'solicitudes/resultados_busqueda.html', {
        'solicitudes': solicitudes,
        'estado': estado,
        'urgencia': urgencia
    })

def generar_reporte(request):
    """Vista con parámetros de query string"""
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    categoria_id = request.GET.get('categoria')
    
    solicitudes = SolicitudAyuda.objects.all()
    
    if fecha_inicio:
        solicitudes = solicitudes.filter(fecha_creacion__gte=fecha_inicio)
    if fecha_fin:
        solicitudes = solicitudes.filter(fecha_creacion__lte=fecha_fin)
    if categoria_id:
        solicitudes = solicitudes.filter(categoria_problema_id=categoria_id)
    
    return render(request, 'solicitudes/reporte.html', {
        'solicitudes': solicitudes,
        'total': solicitudes.count()
    })


