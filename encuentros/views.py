from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from solicitudes.models import SolicitudAyuda
from .models import EncuentroVirtual, TrabajadorSocial

def programar_encuentro(request, solicitud_id):
    """Vista para programar un encuentro virtual"""
    solicitud = get_object_or_404(SolicitudAyuda, id=solicitud_id)
    trabajadores = TrabajadorSocial.objects.filter(disponible=True)
    
    if request.method == 'POST':
        try:
            trabajador_id = request.POST.get('trabajador_social')
            fecha_programada = request.POST.get('fecha_programada')
            duracion = request.POST.get('duracion_estimada', 60)
            
            trabajador = get_object_or_404(TrabajadorSocial, id=trabajador_id)
            
            # Crear el encuentro
            encuentro = EncuentroVirtual.objects.create(
                trabajador_social=trabajador,
                fecha_programada=fecha_programada,
                duracion_estimada=duracion,
                estado='programado'
            )
            
            # Actualizar estado de la solicitud
            solicitud.estado = 'programado'
            solicitud.save()
            
            messages.success(request, f'✅ Encuentro programado exitosamente para el {fecha_programada}')
            return redirect('encuentros:detalle_encuentro', encuentro_id=encuentro.id)
            
        except Exception as e:
            messages.error(request, f'❌ Error al programar encuentro: {str(e)}')
    
    return render(request, 'encuentros/programar_encuentro.html', {
        'solicitud': solicitud,
        'trabajadores': trabajadores,
        'hoy': timezone.now().date()
    })

def detalle_encuentro(request, encuentro_id):
    """Vista para ver detalle de un encuentro"""
    encuentro = get_object_or_404(EncuentroVirtual, id=encuentro_id)
    
    return render(request, 'encuentros/detalle_encuentro.html', {
        'encuentro': encuentro
    })

def lista_encuentros(request):
    """Vista para listar todos los encuentros"""
    encuentros = EncuentroVirtual.objects.all().order_by('-fecha_programada')
    
    return render(request, 'encuentros/lista_encuentros.html', {
        'encuentros': encuentros
    })