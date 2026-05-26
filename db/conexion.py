# ============================================================
# CONFIGURACIÓN DE CONEXIÓN
# ============================================================

import sys
import hashlib
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class ConexionMongoDB:
    """Clase para manejar la conexión a MongoDB"""

    def __init__(self, uri="mongodb://localhost:27017/"):
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Verificar conexión
            self.client.admin.command('ping')
            self.db = self.client["Tienda_Online"]
            print("✓ Conexión exitosa a MongoDB")
        except ConnectionFailure:
            print("✗ Error: No se puede conectar a MongoDB")
            print("  Asegúrese de que MongoDB está ejecutándose en localhost:27017")
            sys.exit(1)

    def inicializar_bd(self):
        """Inicializa las colecciones y datos de ejemplo"""
        colecciones_existentes = self.db.list_collection_names()

        # Crear colecciones si no existen
        if "usuarios" not in colecciones_existentes:
            self._crear_coleccion_usuarios()

        if "productos" not in colecciones_existentes:
            self._crear_coleccion_productos()

        if "carritos" not in colecciones_existentes:
            self._crear_coleccion_carritos()

        if "pedidos" not in colecciones_existentes:
            self._crear_coleccion_pedidos()

        # Crear índices necesarios
        self._crear_indices()

    def _crear_coleccion_usuarios(self):
        """Crea la colección de usuarios con datos de ejemplo"""
        usuarios = [
            {
                "_id": "user_001",
                "nombre": "Juan Pérez",
                "email": "juan@email.com",
                "contraseña": self._hash_contraseña("123456"),
                "fecha_registro": datetime.now(),
                "historial_compras": [],
                "estado": "activo"
            },
            {
                "_id": "user_002",
                "nombre": "María García",
                "email": "maria@email.com",
                "contraseña": self._hash_contraseña("123456"),
                "fecha_registro": datetime.now(),
                "historial_compras": [],
                "estado": "activo"
            },
            {
                "_id": "user_003",
                "nombre": "Carlos López",
                "email": "carlos@email.com",
                "contraseña": self._hash_contraseña("123456"),
                "fecha_registro": datetime.now(),
                "historial_compras": [],
                "estado": "activo"
            }
        ]
        self.db.usuarios.insert_many(usuarios)
        print("  ✓ Colección 'usuarios' creada con datos de ejemplo")

    def _crear_coleccion_productos(self):
        """Crea la colección de productos con datos de ejemplo"""
        productos = [
            {
                "_id": "prod_001",
                "nombre": "Laptop Dell XPS 13",
                "categoria": "Electrónica",
                "precio": 1200.00,
                "stock": 15,
                "descripcion": "Laptop ultraportátil de 13 pulgadas con procesador Intel i7",
                "imagen": "laptop_dell.jpg",
                "valoracion": 4.8,
                "fecha_creacion": datetime.now()
            },
            {
                "_id": "prod_002",
                "nombre": "Mouse Logitech MX Master",
                "categoria": "Accesorios",
                "precio": 99.99,
                "stock": 45,
                "descripcion": "Mouse inalámbrico de precisión para profesionales",
                "imagen": "mouse_logitech.jpg",
                "valoracion": 4.7,
                "fecha_creacion": datetime.now()
            },
            {
                "_id": "prod_003",
                "nombre": "Teclado Mecánico Corsair K95",
                "categoria": "Accesorios",
                "precio": 199.99,
                "stock": 20,
                "descripcion": "Teclado mecánico RGB para gaming",
                "imagen": "teclado_corsair.jpg",
                "valoracion": 4.9,
                "fecha_creacion": datetime.now()
            },
            {
                "_id": "prod_004",
                "nombre": "Monitor LG UltraWide",
                "categoria": "Monitores",
                "precio": 599.99,
                "stock": 8,
                "descripcion": "Monitor ultraancho de 34 pulgadas con resolución 3440x1440",
                "imagen": "monitor_lg.jpg",
                "valoracion": 4.6,
                "fecha_creacion": datetime.now()
            },
            {
                "_id": "prod_005",
                "nombre": "Webcam Logitech C920",
                "categoria": "Accesorios",
                "precio": 79.99,
                "stock": 30,
                "descripcion": "Cámara web Full HD con enfoque automático",
                "imagen": "webcam_logitech.jpg",
                "valoracion": 4.5,
                "fecha_creacion": datetime.now()
            },
            {
                "_id": "prod_006",
                "nombre": "Audífonos Sony WH-1000XM5",
                "categoria": "Audio",
                "precio": 399.99,
                "stock": 12,
                "descripcion": "Audífonos con cancelación de ruido de clase mundial",
                "imagen": "audifonos_sony.jpg",
                "valoracion": 4.9,
                "fecha_creacion": datetime.now()
            },
            {
                "_id": "prod_007",
                "nombre": "SSD Samsung 980 Pro",
                "categoria": "Almacenamiento",
                "precio": 249.99,
                "stock": 50,
                "descripcion": "Disco duro SSD NVMe de 1TB con velocidades ultra rápidas",
                "imagen": "ssd_samsung.jpg",
                "valoracion": 4.8,
                "fecha_creacion": datetime.now()
            },
            {
                "_id": "prod_008",
                "nombre": "Memoria RAM Corsair Vengeance",
                "categoria": "Componentes",
                "precio": 89.99,
                "stock": 35,
                "descripcion": "Memoria RAM DDR4 de 16GB a 3600MHz",
                "imagen": "ram_corsair.jpg",
                "valoracion": 4.7,
                "fecha_creacion": datetime.now()
            }
        ]
        self.db.productos.insert_many(productos)
        print("  ✓ Colección 'productos' creada con datos de ejemplo")

    def _crear_coleccion_carritos(self):
        """Crea la colección de carritos"""
        carritos = [
            {
                "_id": "user_001",
                "usuario_id": "user_001",
                "productos": [],
                "fecha_creacion": datetime.now(),
                "fecha_actualizacion": datetime.now(),
                "total": 0.0
            },
            {
                "_id": "user_002",
                "usuario_id": "user_002",
                "productos": [],
                "fecha_creacion": datetime.now(),
                "fecha_actualizacion": datetime.now(),
                "total": 0.0
            },
            {
                "_id": "user_003",
                "usuario_id": "user_003",
                "productos": [],
                "fecha_creacion": datetime.now(),
                "fecha_actualizacion": datetime.now(),
                "total": 0.0
            }
        ]
        self.db.carritos.insert_many(carritos)
        print("  ✓ Colección 'carritos' creada")

    def _crear_coleccion_pedidos(self):
        """Crea la colección de pedidos vacía (los documentos se insertan al realizar compras)"""
        # Inserta un documento temporal para forzar la creación de la colección y lo elimina de inmediato
        resultado = self.db.pedidos.insert_one({"_init": True})
        self.db.pedidos.delete_one({"_id": resultado.inserted_id})
        print("  ✓ Colección 'pedidos' creada")

    def _crear_indices(self):
        """Crea los índices necesarios en todas las colecciones"""
        # usuarios: índice único sobre email para evitar duplicados y agilizar el login
        self.db.usuarios.create_index([("email", 1)], unique=True, name="idx_usuarios_email")

        # productos: índice sobre categoría para las búsquedas por categoría
        self.db.productos.create_index([("categoria", 1)], name="idx_productos_categoria")

        # productos: índice de texto sobre nombre y descripción para búsquedas full-text
        self.db.productos.create_index(
            [("nombre", "text"), ("descripcion", "text")],
            name="idx_productos_texto"
        )

        # pedidos: índice sobre usuario_id para consultar el historial por usuario
        self.db.pedidos.create_index([("usuario_id", 1)], name="idx_pedidos_usuario_id")

    @staticmethod
    def _hash_contraseña(contraseña):
        """Genera hash SHA-256 de la contraseña"""
        return hashlib.sha256(contraseña.encode()).hexdigest()