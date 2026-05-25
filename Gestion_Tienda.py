# ============================================================
# APLICACIÓN DE TIENDA ONLINE CON MONGODB
# Desarrolladores: Equipo Bases de Datos
# Asignatura: Bases de Datos - Actividad 8
# ============================================================

import sys
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import hashlib
import json

# ============================================================
# CONFIGURACIÓN DE CONEXIÓN
# ============================================================

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
        # Crear colecciones si no existen
        if "usuarios" not in self.db.list_collection_names():
            self._crear_coleccion_usuarios()
        
        if "productos" not in self.db.list_collection_names():
            self._crear_coleccion_productos()
        
        if "carritos" not in self.db.list_collection_names():
            self._crear_coleccion_carritos()
        
        if "pedidos" not in self.db.list_collection_names():
            self._crear_coleccion_pedidos()
    
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
        """Crea la colección de pedidos"""
        self.db.pedidos.create_index([("usuario_id", 1)])
        print("  ✓ Colección 'pedidos' creada")
    
    @staticmethod
    def _hash_contraseña(contraseña):
        """Genera hash SHA-256 de la contraseña"""
        return hashlib.sha256(contraseña.encode()).hexdigest()


# ============================================================
# SISTEMA DE AUTENTICACIÓN
# ============================================================

class SistemaAutenticacion:
    """Maneja la autenticación de usuarios"""
    
    def __init__(self, db):
        self.db = db
        self.usuario_actual = None
    
    def registrar_usuario(self, nombre, email, contraseña):
        """Registra un nuevo usuario"""
        # Verificar si el email ya existe
        if self.db.usuarios.find_one({"email": email}):
            return False, "El email ya está registrado"
        
        usuario_id = f"user_{self.db.usuarios.count_documents({}) + 1:03d}"
        nuevo_usuario = {
            "_id": usuario_id,
            "nombre": nombre,
            "email": email,
            "contraseña": ConexionMongoDB._hash_contraseña(contraseña),
            "fecha_registro": datetime.now(),
            "historial_compras": [],
            "estado": "activo"
        }
        
        self.db.usuarios.insert_one(nuevo_usuario)
        # Crear carrito para el nuevo usuario
        self.db.carritos.insert_one({
            "_id": usuario_id,
            "usuario_id": usuario_id,
            "productos": [],
            "fecha_creacion": datetime.now(),
            "fecha_actualizacion": datetime.now(),
            "total": 0.0
        })
        return True, f"Usuario registrado exitosamente. ID: {usuario_id}"
    
    def iniciar_sesion(self, email, contraseña):
        """Inicia sesión de un usuario"""
        usuario = self.db.usuarios.find_one({"email": email})
        
        if not usuario:
            return False, "Usuario no encontrado"
        
        if usuario["contraseña"] != ConexionMongoDB._hash_contraseña(contraseña):
            return False, "Contraseña incorrecta"
        
        self.usuario_actual = usuario
        return True, f"Bienvenido {usuario['nombre']}!"
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        self.usuario_actual = None
        return True, "Sesión cerrada"
    
    def obtener_usuario_actual(self):
        """Retorna el usuario autenticado"""
        return self.usuario_actual


# ============================================================
# GESTIÓN DE PRODUCTOS
# ============================================================

class GestorProductos:
    """Maneja operaciones CRUD de productos"""
    
    def __init__(self, db):
        self.db = db
    
    def obtener_todos_productos(self):
        """Obtiene todos los productos disponibles"""
        return list(self.db.productos.find())
    
    def obtener_productos_por_categoria(self, categoria):
        """Busca productos por categoría"""
        return list(self.db.productos.find({"categoria": categoria}))
    
    def obtener_categorias(self):
        """Obtiene lista de categorías únicas"""
        return self.db.productos.distinct("categoria")
    
    def obtener_producto_por_id(self, producto_id):
        """Obtiene un producto específico por ID"""
        return self.db.productos.find_one({"_id": producto_id})
    
    def buscar_productos(self, termino):
        """Busca productos por nombre o descripción"""
        return list(self.db.productos.find({
            "$or": [
                {"nombre": {"$regex": termino, "$options": "i"}},
                {"descripcion": {"$regex": termino, "$options": "i"}}
            ]
        }))
    
    def actualizar_stock(self, producto_id, cantidad):
        """Actualiza el stock de un producto"""
        self.db.productos.update_one(
            {"_id": producto_id},
            {"$inc": {"stock": -cantidad}}
        )
    
    def obtener_stock(self, producto_id):
        """Obtiene el stock actual de un producto"""
        producto = self.db.productos.find_one({"_id": producto_id})
        return producto["stock"] if producto else 0


# ============================================================
# GESTIÓN DE CARRITO
# ============================================================

class GestorCarrito:
    """Maneja el carrito de compras del usuario"""
    
    def __init__(self, db):
        self.db = db
    
    def obtener_carrito(self, usuario_id):
        """Obtiene el carrito del usuario"""
        return self.db.carritos.find_one({"_id": usuario_id})
    
    def agregar_producto(self, usuario_id, producto_id, cantidad, precio_unitario):
        """Agrega un producto al carrito"""
        carrito = self.obtener_carrito(usuario_id)
        
        # Buscar si el producto ya existe en el carrito
        producto_existe = False
        for item in carrito["productos"]:
            if item["producto_id"] == producto_id:
                item["cantidad"] += cantidad
                item["subtotal"] = item["cantidad"] * item["precio_unitario"]
                producto_existe = True
                break
        
        if not producto_existe:
            carrito["productos"].append({
                "producto_id": producto_id,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "subtotal": cantidad * precio_unitario,
                "fecha_agregado": datetime.now()
            })
        
        # Actualizar total
        carrito["total"] = sum(item["subtotal"] for item in carrito["productos"])
        carrito["fecha_actualizacion"] = datetime.now()
        
        self.db.carritos.replace_one({"_id": usuario_id}, carrito)
        return True, f"Producto agregado al carrito. Total: ${carrito['total']:.2f}"
    
    def eliminar_producto(self, usuario_id, producto_id):
        """Elimina un producto del carrito"""
        carrito = self.obtener_carrito(usuario_id)
        carrito["productos"] = [
            item for item in carrito["productos"]
            if item["producto_id"] != producto_id
        ]
        
        carrito["total"] = sum(item["subtotal"] for item in carrito["productos"])
        carrito["fecha_actualizacion"] = datetime.now()
        
        self.db.carritos.replace_one({"_id": usuario_id}, carrito)
        return True, "Producto eliminado del carrito"
    
    def vaciar_carrito(self, usuario_id):
        """Vacía completamente el carrito"""
        self.db.carritos.update_one(
            {"_id": usuario_id},
            {
                "$set": {
                    "productos": [],
                    "total": 0.0,
                    "fecha_actualizacion": datetime.now()
                }
            }
        )
        return True, "Carrito vaciado"
    
    def obtener_total_carrito(self, usuario_id):
        """Obtiene el total del carrito"""
        carrito = self.obtener_carrito(usuario_id)
        return carrito["total"] if carrito else 0.0


# ============================================================
# GESTIÓN DE PEDIDOS
# ============================================================

class GestorPedidos:
    """Maneja los pedidos y compras"""
    
    def __init__(self, db):
        self.db = db
    
    def crear_pedido(self, usuario_id):
        """Crea un pedido a partir del carrito"""
        carrito = self.db.carritos.find_one({"_id": usuario_id})
        
        if not carrito or len(carrito["productos"]) == 0:
            return False, "El carrito está vacío"
        
        # Verificar stock disponible
        for item in carrito["productos"]:
            producto = self.db.productos.find_one({"_id": item["producto_id"]})
            if not producto or producto["stock"] < item["cantidad"]:
                return False, f"Stock insuficiente para {item['producto_id']}"
        
        # Crear pedido
        numero_pedido = f"PED_{self.db.pedidos.count_documents({}) + 1:05d}"
        pedido = {
            "_id": numero_pedido,
            "usuario_id": usuario_id,
            "productos": carrito["productos"],
            "total": carrito["total"],
            "estado": "completado",
            "fecha_pedido": datetime.now(),
            "fecha_entrega_estimada": datetime.now(),
            "metodo_pago": "efectivo"
        }
        
        # Insertar pedido
        self.db.pedidos.insert_one(pedido)
        
        # Actualizar stock de productos
        for item in carrito["productos"]:
            self.db.productos.update_one(
                {"_id": item["producto_id"]},
                {"$inc": {"stock": -item["cantidad"]}}
            )
        
        # Agregar a historial de compras del usuario
        self.db.usuarios.update_one(
            {"_id": usuario_id},
            {"$push": {"historial_compras": numero_pedido}}
        )
        
        # Vaciar carrito
        self.db.carritos.update_one(
            {"_id": usuario_id},
            {
                "$set": {
                    "productos": [],
                    "total": 0.0,
                    "fecha_actualizacion": datetime.now()
                }
            }
        )
        
        return True, f"Compra realizada exitosamente. Número de pedido: {numero_pedido}"
    
    def obtener_historial_pedidos(self, usuario_id):
        """Obtiene el historial de pedidos del usuario"""
        return list(self.db.pedidos.find({"usuario_id": usuario_id}))
    
    def obtener_detalles_pedido(self, numero_pedido):
        """Obtiene los detalles de un pedido específico"""
        return self.db.pedidos.find_one({"_id": numero_pedido})


# ============================================================
# INTERFAZ DE CONSOLA
# ============================================================

class Aplicacion:
    """Interfaz principal de la aplicación"""
    
    def __init__(self):
        self.conexion = ConexionMongoDB()
        self.conexion.inicializar_bd()
        self.autenticacion = SistemaAutenticacion(self.conexion.db)
        self.gestor_productos = GestorProductos(self.conexion.db)
        self.gestor_carrito = GestorCarrito(self.conexion.db)
        self.gestor_pedidos = GestorPedidos(self.conexion.db)
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        self.limpiar_pantalla()
        print("=" * 60)
        print("        BIENVENIDO A LA TIENDA ONLINE".center(60))
        print("=" * 60)
        print("\n1. Iniciar sesión")
        print("2. Registrar nuevo usuario")
        print("3. Salir")
        print("\n" + "-" * 60)
    
    def mostrar_menu_tienda(self):
        """Muestra el menú de la tienda"""
        self.limpiar_pantalla()
        usuario = self.autenticacion.obtener_usuario_actual()
        print("=" * 60)
        print(f"        TIENDA ONLINE - Usuario: {usuario['nombre']}".center(60))
        print("=" * 60)
        print("\n1. Ver todos los productos")
        print("2. Buscar productos por categoría")
        print("3. Buscar producto por nombre")
        print("4. Ver carrito de compras")
        print("5. Agregar producto al carrito")
        print("6. Eliminar producto del carrito")
        print("7. Realizar compra")
        print("8. Ver historial de compras")
        print("9. Cerrar sesión")
        print("\n" + "-" * 60)
    
    def mostrar_productos(self, productos):
        """Muestra una lista de productos formateada"""
        if not productos:
            print("\nNo se encontraron productos.")
            return
        
        print("\n" + "-" * 60)
        print(f"{'ID':<12} {'Nombre':<25} {'Precio':<12} {'Stock':<8}")
        print("-" * 60)
        for p in productos:
            print(f"{p['_id']:<12} {p['nombre']:<25} ${p['precio']:<11.2f} {p['stock']:<8}")
        print("-" * 60)
    
    def mostrar_detalles_producto(self, producto):
        """Muestra los detalles completos de un producto"""
        if not producto:
            print("\nProducto no encontrado.")
            return
        
        print("\n" + "=" * 60)
        print(f"Producto: {producto['nombre']}")
        print("=" * 60)
        print(f"ID:            {producto['_id']}")
        print(f"Categoría:     {producto['categoria']}")
        print(f"Precio:        ${producto['precio']:.2f}")
        print(f"Stock:         {producto['stock']} unidades")
        print(f"Descripción:   {producto['descripcion']}")
        print(f"Valoración:    {producto['valoracion']}/5 ⭐")
        print("=" * 60)
    
    def mostrar_carrito(self, usuario_id):
        """Muestra el contenido del carrito"""
        carrito = self.gestor_carrito.obtener_carrito(usuario_id)
        
        if not carrito or len(carrito["productos"]) == 0:
            print("\nEl carrito está vacío.")
            return
        
        print("\n" + "=" * 60)
        print("CARRITO DE COMPRAS".center(60))
        print("=" * 60)
        print(f"{'Producto':<20} {'Cantidad':<10} {'P.Unitario':<12} {'Subtotal':<12}")
        print("-" * 60)
        
        for item in carrito["productos"]:
            producto = self.gestor_productos.obtener_producto_por_id(item["producto_id"])
            print(f"{producto['nombre']:<20} {item['cantidad']:<10} "
                  f"${item['precio_unitario']:<11.2f} ${item['subtotal']:<11.2f}")
        
        print("-" * 60)
        print(f"TOTAL: ${carrito['total']:.2f}".rjust(60))
        print("=" * 60)
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        while True:
            if not self.autenticacion.obtener_usuario_actual():
                self.mostrar_menu_principal()
                opcion = input("Seleccione una opción: ").strip()
                
                if opcion == "1":
                    self.limpiar_pantalla()
                    email = input("Email: ").strip()
                    contraseña = input("Contraseña: ").strip()
                    exito, mensaje = self.autenticacion.iniciar_sesion(email, contraseña)
                    print(f"\n{'✓' if exito else '✗'} {mensaje}")
                    if not exito:
                        input("\nPresione Enter para continuar...")
                
                elif opcion == "2":
                    self.limpiar_pantalla()
                    nombre = input("Nombre completo: ").strip()
                    email = input("Email: ").strip()
                    contraseña = input("Contraseña: ").strip()
                    exito, mensaje = self.autenticacion.registrar_usuario(nombre, email, contraseña)
                    print(f"\n{'✓' if exito else '✗'} {mensaje}")
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "3":
                    print("\n¡Hasta luego!")
                    break
            
            else:
                usuario = self.autenticacion.obtener_usuario_actual()
                self.mostrar_menu_tienda()
                opcion = input("Seleccione una opción: ").strip()
                
                if opcion == "1":
                    self.limpiar_pantalla()
                    productos = self.gestor_productos.obtener_todos_productos()
                    self.mostrar_productos(productos)
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "2":
                    self.limpiar_pantalla()
                    categorias = self.gestor_productos.obtener_categorias()
                    print("\nCategorías disponibles:")
                    for i, cat in enumerate(categorias, 1):
                        print(f"{i}. {cat}")
                    
                    try:
                        idx = int(input("Seleccione categoría: ")) - 1
                        if 0 <= idx < len(categorias):
                            productos = self.gestor_productos.obtener_productos_por_categoria(categorias[idx])
                            self.mostrar_productos(productos)
                        else:
                            print("Opción inválida")
                    except ValueError:
                        print("Entrada inválida")
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "3":
                    self.limpiar_pantalla()
                    termino = input("Buscar producto: ").strip()
                    productos = self.gestor_productos.buscar_productos(termino)
                    self.mostrar_productos(productos)
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "4":
                    self.limpiar_pantalla()
                    self.mostrar_carrito(usuario["_id"])
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "5":
                    self.limpiar_pantalla()
                    producto_id = input("ID del producto: ").strip()
                    producto = self.gestor_productos.obtener_producto_por_id(producto_id)
                    
                    if producto:
                        self.mostrar_detalles_producto(producto)
                        try:
                            cantidad = int(input("Cantidad: "))
                            if cantidad > 0 and cantidad <= producto["stock"]:
                                exito, mensaje = self.gestor_carrito.agregar_producto(
                                    usuario["_id"], producto_id, cantidad, producto["precio"]
                                )
                                print(f"\n✓ {mensaje}")
                            else:
                                print(f"\n✗ Cantidad inválida o stock insuficiente")
                        except ValueError:
                            print("\n✗ Entrada inválida")
                    else:
                        print("\n✗ Producto no encontrado")
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "6":
                    self.limpiar_pantalla()
                    self.mostrar_carrito(usuario["_id"])
                    producto_id = input("\nID del producto a eliminar: ").strip()
                    exito, mensaje = self.gestor_carrito.eliminar_producto(usuario["_id"], producto_id)
                    print(f"\n{'✓' if exito else '✗'} {mensaje}")
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "7":
                    self.limpiar_pantalla()
                    self.mostrar_carrito(usuario["_id"])
                    confirmacion = input("\n¿Confirma la compra? (s/n): ").strip().lower()
                    
                    if confirmacion == 's':
                        exito, mensaje = self.gestor_pedidos.crear_pedido(usuario["_id"])
                        print(f"\n{'✓' if exito else '✗'} {mensaje}")
                    else:
                        print("\nCompra cancelada")
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "8":
                    self.limpiar_pantalla()
                    pedidos = self.gestor_pedidos.obtener_historial_pedidos(usuario["_id"])
                    
                    if pedidos:
                        print("\n" + "=" * 60)
                        print("HISTORIAL DE COMPRAS".center(60))
                        print("=" * 60)
                        for pedido in pedidos:
                            print(f"\nPedido: {pedido['_id']}")
                            print(f"Fecha: {pedido['fecha_pedido']}")
                            print(f"Total: ${pedido['total']:.2f}")
                            print(f"Estado: {pedido['estado']}")
                            print("-" * 60)
                    else:
                        print("\nNo tiene compras registradas.")
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "9":
                    self.autenticacion.cerrar_sesion()
                    print("\nSesión cerrada.")
                    input("Presione Enter para continuar...")


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    try:
        app = Aplicacion()
        app.ejecutar()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
    except Exception as e:
        print(f"\nError: {e}")
        input("Presione Enter para salir...")
