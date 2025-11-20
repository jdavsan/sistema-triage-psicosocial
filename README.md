Sistema de Triage - Trabajo Social

Sistema web para gestión de solicitudes de ayuda psicosocial con clasificación por urgencia.

Características

- Sistema de triage automático por urgencia
- Gestión de solicitudes de ayuda
- Programación de encuentros virtuales
- Sistema de calificaciones con doble almacenamiento (SQLite + MongoDB)
- Panel de administración personalizado
- Responsive design

Requisitos

- Python 3.12+
- Django 5.2.8
- MongoDB Atlas (opcional)

Instalación

1. Clonar el repositorio:
bash
git clone https://github.com/tu-usuario/sistema-triage.git
cd sistema-triage


2. Crear entorno virtual:
bash
python -m venv psicosocial
Windows:
psicosocial\Scripts\activate
Linux/Mac:
source psicosocial/bin/activate


3. Instalar dependencias:
bash
pip install -r requirements.txt


4. Configurar variables de entorno:
Crear archivo `.env` en la raíz con:

5. Ejecutar migraciones:
bash
python manage.py migrate


6. Crear superusuario:
bash
python manage.py createsuperuser


7. Ejecutar servidor:
bash
python manage.py runserver


Ejecutar Tests
bash
python manage.py test


Estructura del Proyecto
sistema_triage/
├── calificaciones/      # App de calificaciones
├── encuentros/          # App de encuentros virtuales
├── solicitudes/         # App principal de solicitudes
├── usuarios/            # App de usuarios
├── sistema_triage/      # Configuración del proyecto
│   └── templates/       # Templates globales
├── manage.py
└── requirements.txt

## 👥 Autor

- Juan Cortés

## 📄 Licencia

Este proyecto es para fines académicos.
