#!/bin/bash

# Ejecutar migraciones
python manage.py migrate --noinput

# Recolectar archivos estáticos
python manage.py collectstatic --noinput --clear

# Iniciar servidor
gunicorn sistema_triage.wsgi --log-file -
