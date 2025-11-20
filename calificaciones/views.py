from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CalificacionForm
from .models import CalificacionSQLite
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import pytz


# Conexion a MongoDB Atlas
MONGODB_URI = settings.MONGODB_URI if hasattr(settings, 'MONGODB_URI') else "mongodb+srv://admin_triage:Cyb3rN3t78**@sistema-triage.f1qgnh7.mongodb.net/?retryWrites=true&w=majority&appName=sistema-triage"


def normalizar_fecha(fecha):
    """
    Convierte cualquier fecha a timezone-aware usando la zona horaria de Django
    """
    if fecha is None:
        return timezone.now()
    
    # Si ya tiene timezone, devolverla tal cual
    if timezone.is_aware(fecha):
        return fecha
    
    # Si no tiene timezone, hacerla timezone-aware
    return timezone.make_aware(fecha)


# VISTAS BASADAS EN FUNCIONES


def crear_calificacion(request):
    """Vista FBV para crear calificación con soporte SQLite y MongoDB"""
    bd_actual = getattr(settings, 'TIPO_BASE_DATOS', 'sqlite')
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        tipo_bd_seleccionado = request.POST.get('tipo_base_datos', bd_actual)
        
        print("=== DEBUG FORMULARIO ===")
        print(f"Form is valid: {form.is_valid()}")
        print(f"Tipo BD seleccionado: {tipo_bd_seleccionado}")
        
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        
        if form.is_valid():
            try:
                nombre = form.cleaned_data['nombre']
                comentario = form.cleaned_data['comentario']
                calificacion_val = form.cleaned_data['calificacion']
                
                print(f"Datos a guardar: {nombre}, {calificacion_val}, {comentario}")
                
                if tipo_bd_seleccionado == 'mongodb':
                    try:
                        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
                        client.admin.command('ping')
                        print("✅ Conectado a MongoDB Atlas")
                        
                        db = client['sistema_triage']
                        collection = db['calificaciones']

                        # Obtener timezone de Colombia
                        colombia_tz = pytz.timezone('America/Bogota')

                        # Crear fecha en UTC (lo que Django usa internamente)
                        fecha_utc = timezone.now()
        
                        # Convertir a hora de Colombia para display
                        fecha_colombia = fecha_utc.astimezone(colombia_tz)
        
                        documento = {
                            'nombre': nombre,
                            'comentario': comentario,
                            'calificacion': calificacion_val,
                            'fecha_creacion': fecha_utc,  # Guardar en UTC
                            'fecha_creacion_display': fecha_colombia.strftime('%Y-%m-%d %H:%M:%S')  # Para mostrar
                        }
        
                        resultado = collection.insert_one(documento)
                        print(f"✅ Guardado en MongoDB Atlas con ID: {resultado.inserted_id}")
                        print(f"🕐 Hora UTC: {fecha_utc}")
                        print(f"🕐 Hora Colombia: {fecha_colombia}")
                        
                        documento = {
                            'nombre': nombre,
                            'comentario': comentario,
                            'calificacion': calificacion_val,
                            'fecha_creacion': timezone.now()
                        }
                        
                        
                        client.close()
                        
                        messages.success(request, '✅ Calificación guardada exitosamente en MongoDB Atlas!')
                    except Exception as mongo_error:
                        print(f"❌ Error de MongoDB: {mongo_error}")
                        messages.error(request, f'❌ Error al conectar con MongoDB Atlas: {str(mongo_error)}')
                        return render(request, 'calificaciones/crear_calificacion.html', {
                            'form': form,
                            'bd_actual': bd_actual
                        })
                else:
                    calificacion_obj = CalificacionSQLite(
                        nombre=nombre,
                        comentario=comentario,
                        calificacion=calificacion_val
                    )
                    calificacion_obj.save()
                    print("✅ Guardado en SQLite")
                    
                    messages.success(request, '✅ Calificación guardada exitosamente en SQLite!')
                
                return redirect('calificaciones:lista_calificaciones')
                
            except Exception as e:
                messages.error(request, f'❌ Error al guardar: {str(e)}')
                print(f"❌ Error general al guardar: {e}")
                import traceback
                traceback.print_exc()
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'❌ {error}')
    else:
        form = CalificacionForm()
    
    return render(request, 'calificaciones/crear_calificacion.html', {
        'form': form,
        'bd_actual': bd_actual
    })


def lista_calificaciones(request):
    """Vista FBV para listar calificaciones de ambas bases de datos"""
    bd_actual = getattr(settings, 'TIPO_BASE_DATOS', 'sqlite')
    
    # Obtener calificaciones de SQLite
    calificaciones_sqlite = []
    try:
        calificaciones_sql = CalificacionSQLite.objects.all().order_by('-fecha_creacion')
        for cal in calificaciones_sql:
            calificaciones_sqlite.append({
                'id': str(cal.id),
                'nombre': cal.nombre,
                'comentario': cal.comentario,
                'calificacion': cal.calificacion,
                'fecha_creacion': normalizar_fecha(cal.fecha_creacion),
                'origen': 'SQLite'
            })
    except Exception as e:
        print(f"Error al obtener calificaciones de SQLite: {e}")
    
    # Obtener calificaciones de MongoDB Atlas
    calificaciones_mongodb = []
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        db = client['sistema_triage']
        collection = db['calificaciones']
        
        for doc in collection.find().sort('fecha_creacion', -1):
            fecha = doc.get('fecha_creacion', None)
            calificaciones_mongodb.append({
                'id': str(doc['_id']),
                'nombre': doc.get('nombre', ''),
                'comentario': doc.get('comentario', ''),
                'calificacion': doc.get('calificacion', 0),
                'fecha_creacion': normalizar_fecha(fecha),
                'origen': 'MongoDB Atlas'
            })
        
        client.close()
        print(f"✅ Obtenidas {len(calificaciones_mongodb)} calificaciones de MongoDB Atlas")
    except Exception as e:
        print(f"⚠️ No se pudieron obtener calificaciones de MongoDB Atlas: {e}")
    
    # Combinar todas las calificaciones
    todas_calificaciones = calificaciones_sqlite + calificaciones_mongodb
    
    # Ordenar por fecha
    todas_calificaciones.sort(
        key=lambda x: x.get('fecha_creacion', timezone.now()),
        reverse=True
    )
    
    # Calcular estadísticas
    total_calificaciones = len(todas_calificaciones)
    if total_calificaciones > 0:
        promedio = sum(c['calificacion'] for c in todas_calificaciones) / total_calificaciones
        promedio = round(promedio, 1)
    else:
        promedio = 0
    
    total_sqlite = len(calificaciones_sqlite)
    total_mongodb = len(calificaciones_mongodb)
    
    return render(request, 'calificaciones/lista_calificaciones.html', {
        'calificaciones': todas_calificaciones,
        'total_calificaciones': total_calificaciones,
        'promedio': promedio,
        'bd_actual': bd_actual,
        'total_sqlite': total_sqlite,
        'total_mongodb': total_mongodb
    })


def cambiar_base_datos(request):
    """Vista FBV para cambiar entre SQLite y MongoDB"""
    if request.method == 'POST':
        nueva_bd = request.POST.get('nueva_base_datos')
        if nueva_bd in ['sqlite', 'mongodb']:
            request.session['tipo_base_datos'] = nueva_bd
            messages.info(request, f'✅ Base de datos cambiada a: {nueva_bd.upper()}')
        return redirect('calificaciones:crear_calificacion')
    
    return redirect('calificaciones:crear_calificacion')


def detalle_calificacion(request, id):
    """Vista FBV para ver detalle de calificación"""
    # Intentar buscar en SQLite (si el ID es numérico)
    try:
        id_numerico = int(id)
        calificacion = CalificacionSQLite.objects.get(id=id_numerico)
        calificacion_data = {
            'id': calificacion.id,
            'nombre': calificacion.nombre,
            'comentario': calificacion.comentario,
            'calificacion': calificacion.calificacion,
            'fecha_creacion': calificacion.fecha_creacion,
            'origen': 'SQLite'
        }
        return render(request, 'calificaciones/detalle_calificacion.html', {
            'calificacion': calificacion_data
        })
    except (ValueError, CalificacionSQLite.DoesNotExist):
        pass
    
    # Si no está en SQLite, buscar en MongoDB Atlas
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        db = client['sistema_triage']
        collection = db['calificaciones']
        
        try:
            documento = collection.find_one({'_id': ObjectId(id)})
        except:
            documento = collection.find_one({'_id': id})
        
        client.close()
        
        if documento:
            calificacion_data = {
                'id': str(documento['_id']),
                'nombre': documento.get('nombre', ''),
                'comentario': documento.get('comentario', ''),
                'calificacion': documento.get('calificacion', 0),
                'fecha_creacion': documento.get('fecha_creacion', None),
                'origen': 'MongoDB Atlas'
            }
            return render(request, 'calificaciones/detalle_calificacion.html', {
                'calificacion': calificacion_data
            })
    except Exception as e:
        print(f"Error al buscar en MongoDB Atlas: {e}")
    
    messages.error(request, '❌ La calificación no existe en ninguna base de datos')
    return redirect('calificaciones:lista_calificaciones')


# VISTAS GENÉRICAS


class CalificacionListView(ListView):
    """
    Vista genérica CBV para listar calificaciones (solo SQLite)
    URL: /calificaciones/cbv/lista/
    """
    model = CalificacionSQLite
    template_name = 'calificaciones/lista_calificaciones_cbv.html'
    context_object_name = 'calificaciones'
    paginate_by = 10
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        """Obtener calificaciones ordenadas por fecha"""
        return CalificacionSQLite.objects.all().order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        """Agregar estadísticas al contexto"""
        context = super().get_context_data(**kwargs)
        calificaciones = CalificacionSQLite.objects.all()
        
        context['total_calificaciones'] = calificaciones.count()
        
        if calificaciones.exists():
            promedio = sum(c.calificacion for c in calificaciones) / calificaciones.count()
            context['promedio'] = round(promedio, 1)
            
            # Estadísticas por estrella
            context['estadisticas'] = {
                'excelentes': calificaciones.filter(calificacion=5).count(),
                'buenas': calificaciones.filter(calificacion=4).count(),
                'regulares': calificaciones.filter(calificacion=3).count(),
                'malas': calificaciones.filter(calificacion__lte=2).count(),
            }
        else:
            context['promedio'] = 0
            context['estadisticas'] = {
                'excelentes': 0,
                'buenas': 0,
                'regulares': 0,
                'malas': 0,
            }
        
        return context


class CalificacionDetailView(DetailView):
    """
    Vista genérica CBV para ver detalle de calificación
    URL: /calificaciones/cbv/detalle/<int:pk>/
    """
    model = CalificacionSQLite
    template_name = 'calificaciones/detalle_calificacion_cbv.html'
    context_object_name = 'calificacion'
    
    def get_context_data(self, **kwargs):
        """Agregar información adicional al contexto"""
        context = super().get_context_data(**kwargs)
        context['origen'] = 'SQLite'
        
        # Obtener calificaciones relacionadas
        calificacion_actual = self.object
        context['calificaciones_similares'] = CalificacionSQLite.objects.filter(
            calificacion=calificacion_actual.calificacion
        ).exclude(id=calificacion_actual.id)[:3]
        
        return context


class CalificacionCreateView(CreateView):
    """
    Vista genérica CBV para crear calificación
    URL: /calificaciones/cbv/crear/
    """
    model = CalificacionSQLite
    fields = ['nombre', 'comentario', 'calificacion']
    template_name = 'calificaciones/crear_calificacion_cbv.html'
    success_url = reverse_lazy('calificaciones:lista_calificaciones_cbv')
    
    def form_valid(self, form):
        """Ejecutar cuando el formulario es válido"""
        messages.success(
            self.request, 
            f'✅ Calificación de {form.cleaned_data["nombre"]} creada exitosamente con {form.cleaned_data["calificacion"]}⭐'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Ejecutar cuando el formulario tiene errores"""
        messages.error(self.request, '❌ Por favor corrige los errores en el formulario')
        return super().form_invalid(form)


class CalificacionUpdateView(UpdateView):
    """
    Vista genérica CBV para actualizar calificación
    URL: /calificaciones/cbv/editar/<int:pk>/
    """
    model = CalificacionSQLite
    fields = ['nombre', 'comentario', 'calificacion']
    template_name = 'calificaciones/editar_calificacion.html'
    success_url = reverse_lazy('calificaciones:lista_calificaciones_cbv')
    context_object_name = 'calificacion'
    
    def form_valid(self, form):
        """Ejecutar cuando el formulario es válido"""
        messages.success(
            self.request, 
            f'✅ Calificación actualizada exitosamente'
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Agregar información al contexto"""
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Editar'
        return context


class CalificacionDeleteView(DeleteView):
    """
    Vista genérica CBV para eliminar calificación
    URL: /calificaciones/cbv/eliminar/<int:pk>/
    """
    model = CalificacionSQLite
    template_name = 'calificaciones/confirmar_eliminar.html'
    success_url = reverse_lazy('calificaciones:lista_calificaciones_cbv')
    context_object_name = 'calificacion'
    
    def delete(self, request, *args, **kwargs):
        """Ejecutar al confirmar eliminación"""
        calificacion = self.get_object()
        messages.success(
            request, 
            f'🗑️ Calificación de {calificacion.nombre} eliminada exitosamente'
        )
        return super().delete(request, *args, **kwargs)


# VISTAS ADICIONALES


def estadisticas_calificaciones(request):
    """Vista para mostrar estadísticas detalladas"""
    calificaciones_sqlite = CalificacionSQLite.objects.all()
    
    # Obtener también de MongoDB
    calificaciones_mongodb = []
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        db = client['sistema_triage']
        collection = db['calificaciones']
        calificaciones_mongodb = list(collection.find())
        client.close()
    except:
        pass
    
    # Calcular estadísticas combinadas
    total_sqlite = calificaciones_sqlite.count()
    total_mongodb = len(calificaciones_mongodb)
    total_general = total_sqlite + total_mongodb
    
    if total_general > 0:
        # Promedio SQLite
        if total_sqlite > 0:
            promedio_sqlite = sum(c.calificacion for c in calificaciones_sqlite) / total_sqlite
        else:
            promedio_sqlite = 0
        
        # Promedio MongoDB
        if total_mongodb > 0:
            promedio_mongodb = sum(c.get('calificacion', 0) for c in calificaciones_mongodb) / total_mongodb
        else:
            promedio_mongodb = 0
        
        # Promedio general
        suma_total = sum(c.calificacion for c in calificaciones_sqlite) + sum(c.get('calificacion', 0) for c in calificaciones_mongodb)
        promedio_general = suma_total / total_general
    else:
        promedio_sqlite = promedio_mongodb = promedio_general = 0
    
    context = {
        'total_sqlite': total_sqlite,
        'total_mongodb': total_mongodb,
        'total_general': total_general,
        'promedio_sqlite': round(promedio_sqlite, 2),
        'promedio_mongodb': round(promedio_mongodb, 2),
        'promedio_general': round(promedio_general, 2),
        'calificaciones_5_estrellas': calificaciones_sqlite.filter(calificacion=5).count(),
        'calificaciones_4_estrellas': calificaciones_sqlite.filter(calificacion=4).count(),
        'calificaciones_3_estrellas': calificaciones_sqlite.filter(calificacion=3).count(),
        'calificaciones_2_estrellas': calificaciones_sqlite.filter(calificacion=2).count(),
        'calificaciones_1_estrella': calificaciones_sqlite.filter(calificacion=1).count(),
    }
    
    return render(request, 'calificaciones/estadisticas.html', context)
    