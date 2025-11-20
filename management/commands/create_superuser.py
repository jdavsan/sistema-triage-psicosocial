from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Crea un superusuario si no existe'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ejemplo.com',
                password='Admin123!'
            )
            self.stdout.write(self.style.SUCCESS('✅ Superusuario creado: admin / Admin123!'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ El superusuario ya existe'))