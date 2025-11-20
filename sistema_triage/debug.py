import os
import sys
import django
from pathlib import Path

# Configura Django
project_root = Path(__file__).parent
sys.path.append(str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_triage.settings')

try:
    django.setup()
    
    from django.template.engine import Engine
    from django.conf import settings
    
    print("=== DEBUG TEMPLATES ===")
    print(f"Project root: {project_root}")
    print(f"Templates DIRS: {settings.TEMPLATES[0]['DIRS']}")
    
    # Verifica cada directorio de templates
    engine = Engine.get_default()
    for i, template_dir in enumerate(engine.dirs):
        print(f"\nTemplate dir {i+1}: {template_dir}")
        print(f"  Existe: {template_dir.exists()}")
        
        # Verifica si existe el template específico
        template_path = template_dir / 'solicitudes' / 'inicio.html'
        print(f"  ¿Puede encontrar inicio.html? {template_path.exists()}")
        if template_path.exists():
            print(f"  ✅ RUTA CORRECTA: {template_path}")
    
    # Verifica la estructura actual
    templates_root = project_root / 'templates'
    print(f"\n=== ESTRUCTURA ACTUAL ===")
    print(f"¿Existe templates/? {templates_root.exists()}")
    if templates_root.exists():
        for root, dirs, files in os.walk(templates_root):
            level = root.replace(str(templates_root), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
                
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()