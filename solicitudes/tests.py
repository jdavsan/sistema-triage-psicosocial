from django.test import TestCase, Client
from django.urls import reverse
from .models import SolicitudAyuda

class SolicitudAyudaTestCase(TestCase):
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = Client()
        self.solicitud = SolicitudAyuda.objects.create(
            nombre_completo="Test Usuario",
            cedula="123456789",
            edad=25,
            celular="3001234567",
            correo_electronico="test@ejemplo.com",
            direccion="Calle Test 123",
            genero="masculino",
            urgencia="media",
            descripcion_problema="Problema de prueba",
            acepta_terminos=True,
            acepta_tratamiento_datos=True
        )
    
    def test_solicitud_creada(self):
        """Test: Verificar que la solicitud se creó correctamente"""
        self.assertEqual(self.solicitud.nombre_completo, "Test Usuario")
        self.assertEqual(self.solicitud.urgencia, "media")
    
    def test_url_inicio_funciona(self):
        """Test: Verificar que la URL de inicio responde"""
        response = self.client.get(reverse('solicitudes:inicio'))
        self.assertEqual(response.status_code, 200)
    
    def test_crear_solicitud_get(self):
        """Test: Verificar que el formulario de crear solicitud carga"""
        response = self.client.get(reverse('solicitudes:crear_solicitud'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nueva Solicitud')
    
    def test_detalle_solicitud(self):
        """Test: Verificar que se puede ver el detalle de una solicitud"""
        response = self.client.get(
            reverse('solicitudes:detalle_solicitud', args=[self.solicitud.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Usuario")
    
    def test_sesiones_restantes(self):
        """Test: Verificar cálculo de sesiones restantes"""
        self.solicitud.sesiones_completadas = 2
        self.solicitud.max_sesiones = 6
        self.assertEqual(self.solicitud.sesiones_restantes(), 4)
    
    def test_puede_agendar_sesion(self):
        """Test: Verificar si puede agendar más sesiones"""
        self.solicitud.sesiones_completadas = 2
        self.solicitud.max_sesiones = 6
        self.assertTrue(self.solicitud.puede_agendar_sesion())
        
        self.solicitud.sesiones_completadas = 6
        self.assertFalse(self.solicitud.puede_agendar_sesion())
    
    def test_porcentaje_sesiones(self):
        """Test: Verificar cálculo de porcentaje de sesiones"""
        self.solicitud.sesiones_completadas = 3
        self.solicitud.max_sesiones = 6
        self.assertEqual(self.solicitud.porcentaje_sesiones(), 50)


class EncuentrosTestCase(TestCase):
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
    
    def test_url_lista_encuentros(self):
        """Test: Verificar que la lista de encuentros carga"""
        response = self.client.get(reverse('encuentros:lista_encuentros'))
        self.assertEqual(response.status_code, 200)