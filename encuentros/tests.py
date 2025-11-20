from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import TrabajadorSocial, EncuentroVirtual
from solicitudes.models import SolicitudAyuda
from django.utils import timezone

class TrabajadorSocialTestCase(TestCase):
    """Tests para el modelo TrabajadorSocial"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user = User.objects.create_user(
            username='trabajador1',
            first_name='Juan',
            last_name='Pérez',
            password='testpass123'
        )
        self.trabajador = TrabajadorSocial.objects.create(
            user=self.user,
            telefono='3001234567',
            especialidad='Terapia Familiar',
            disponible=True
        )
    
    def test_trabajador_creado(self):
        """Test: Verificar que el trabajador social se creó"""
        self.assertEqual(self.trabajador.especialidad, 'Terapia Familiar')
        self.assertTrue(self.trabajador.disponible)
    
    def test_trabajador_str(self):
        """Test: Verificar método __str__"""
        self.assertEqual(str(self.trabajador), "Juan Pérez")


class EncuentroVirtualTestCase(TestCase):
    """Tests para el modelo EncuentroVirtual"""
    
    def setUp(self):
        """Configuración inicial"""
        # Crear usuario y trabajador social
        self.user = User.objects.create_user(
            username='trabajador1',
            first_name='María',
            last_name='González',
            password='testpass123'
        )
        self.trabajador = TrabajadorSocial.objects.create(
            user=self.user,
            telefono='3009876543',
            especialidad='Intervención en Crisis',
            disponible=True
        )
        
        # Crear solicitud
        self.solicitud = SolicitudAyuda.objects.create(
            nombre_completo="Test Usuario",
            cedula="123456789",
            edad=30,
            celular="3001234567",
            correo_electronico="test@ejemplo.com",
            direccion="Calle Test 123",
            genero="femenino",
            urgencia="alta",
            descripcion_problema="Problema de prueba",
            acepta_terminos=True,
            acepta_tratamiento_datos=True
        )
        
        # Crear encuentro
        self.encuentro = EncuentroVirtual.objects.create(
            solicitud=self.solicitud,
            trabajador_social=self.trabajador,
            fecha_programada=timezone.now() + timezone.timedelta(days=1),
            duracion_estimada=60,
            estado='programado'
        )
    
    def test_encuentro_creado(self):
        """Test: Verificar que el encuentro se creó"""
        self.assertEqual(self.encuentro.estado, 'programado')
        self.assertEqual(self.encuentro.duracion_estimada, 60)
    
    def test_encuentro_tiene_solicitud(self):
        """Test: Verificar relación con solicitud"""
        self.assertEqual(self.encuentro.solicitud.nombre_completo, "Test Usuario")
    
    def test_encuentro_tiene_trabajador(self):
        """Test: Verificar relación con trabajador social"""
        self.assertEqual(self.encuentro.trabajador_social.especialidad, 'Intervención en Crisis')


class EncuentrosViewTestCase(TestCase):
    """Tests para las vistas de encuentros"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
    
    def test_url_lista_encuentros(self):
        """Test: Verificar que la lista de encuentros carga"""
        response = self.client.get(reverse('encuentros:lista_encuentros'))
        self.assertEqual(response.status_code, 200)
    
    def test_lista_encuentros_sin_encuentros(self):
        """Test: Verificar mensaje cuando no hay encuentros"""
        response = self.client.get(reverse('encuentros:lista_encuentros'))
        self.assertContains(response, 'No hay encuentros')