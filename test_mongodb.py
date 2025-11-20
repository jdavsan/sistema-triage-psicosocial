from pymongo import MongoClient
from decouple import config

# Leer MongoDB URI desde .env
MONGODB_URI = config('MONGODB_URI')

print("🔄 Probando conexión a MongoDB Atlas...")
print(f"URI: {MONGODB_URI[:50]}...")

try:
    # Conectar
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Hacer ping
    client.admin.command('ping')
    print("✅ Conexión exitosa a MongoDB Atlas!")
    
    # Listar bases de datos
    print("\n📊 Bases de datos disponibles:")
    for db_name in client.list_database_names():
        print(f"  - {db_name}")
    
    # Probar base de datos del proyecto
    db = client['sistema_triage']
    print(f"\n📁 Colecciones en 'sistema_triage':")
    for collection_name in db.list_collection_names():
        count = db[collection_name].count_documents({})
        print(f"  - {collection_name}: {count} documentos")
    
    # Cerrar conexión
    client.close()
    print("\n✅ Todas las pruebas pasaron correctamente!")
    
except Exception as e:
    print(f"\n❌ Error al conectar con MongoDB Atlas:")
    print(f"   {str(e)}")
    print("\n💡 Verifica:")
    print("   1. Tu URI de MongoDB Atlas es correcta")
    print("   2. Tu IP está en la whitelist de MongoDB Atlas")
    print("   3. Tu usuario y contraseña son correctos")
    print("   4. El archivo .env tiene la variable MONGODB_URI")