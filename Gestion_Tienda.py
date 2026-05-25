# ============================================================
# APLICACIÓN DE TIENDA ONLINE CON MONGODB
# Desarrolladores: Equipo Bases de Datos
# Asignatura: Bases de Datos - Actividad 8
# ============================================================

import sys
import threading
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import hashlib
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
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
        #Inserta un documento temporal para forzar la creación de la colección y lo elimina de una vez, dejando la colección vaçia
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
        
        # Generar ID secuencial basado en el mayor ID existente
        ultimo = self.db.usuarios.find_one(sort=[("_id", -1)])
        if ultimo:
            try:
                ultimo_num = int(ultimo["_id"].split("_")[1])
            except (IndexError, ValueError):
                ultimo_num = self.db.usuarios.count_documents({})
        else:
            ultimo_num = 0
        usuario_id = f"user_{ultimo_num + 1:03d}"
        
        nuevo_usuario = {
            "_id": usuario_id,
            "nombre": nombre,
            "email": email,
            "contraseña": ConexionMongoDB._hash_contraseña(contraseña),
            "fecha_registro": datetime.now(),
            "historial_compras": [],
            "estado": "activo"
        }
        
        try:
            self.db.usuarios.insert_one(nuevo_usuario)
        except OperationFailure:
            return False, "El email ya está registrado"
        
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
        
        if not carrito:
            return False, "No se encontró el carrito del usuario"
        
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
        
        if not carrito:
            return False, "No se encontró el carrito del usuario"
        
        productos_originales = len(carrito["productos"])
        carrito["productos"] = [
            item for item in carrito["productos"]
            if item["producto_id"] != producto_id
        ]
        
        if len(carrito["productos"]) == productos_originales:
            return False, "El producto no se encontró en el carrito"
        
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
            if not producto:
                return False, f"El producto '{item['producto_id']}' ya no existe en el catálogo"
            if producto["stock"] < item["cantidad"]:
                return False, f"Stock insuficiente para '{producto['nombre']}' (disponible: {producto['stock']})"
        
        # Generar número de pedido basado en el mayor existente
        ultimo_pedido = self.db.pedidos.find_one(sort=[("_id", -1)])
        if ultimo_pedido:
            try:
                ultimo_num = int(ultimo_pedido["_id"].split("_")[1])
            except (IndexError, ValueError):
                ultimo_num = self.db.pedidos.count_documents({})
        else:
            ultimo_num = 0
        numero_pedido = f"PED_{ultimo_num + 1:05d}"
        
        from datetime import timedelta
        pedido = {
            "_id": numero_pedido,
            "usuario_id": usuario_id,
            "productos": carrito["productos"],
            "total": carrito["total"],
            "estado": "completado",
            "fecha_pedido": datetime.now(),
            "fecha_entrega_estimada": datetime.now() + timedelta(days=6),
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
        
        # Vaciar carrito después de comprar
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
# INTERFAZ GRÁFICA
# ============================================================

# Ventana de Login y Registro

class VentanaAuth(ctk.CTkToplevel):
    """Ventana de inicio de sesión y registro"""

    def __init__(self, parent, autenticacion, on_login_exitoso):
        super().__init__(parent)
        self.autenticacion = autenticacion
        self.on_login_exitoso = on_login_exitoso

        self.title("Tienda Online — Acceso")
        self.geometry("420x520")
        self.resizable(False, False)
        self.grab_set()
        self.focus()

        # Centrar en pantalla
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 210
        y = (self.winfo_screenheight() // 2) - 260
        self.geometry(f"+{x}+{y}")

        self._construir_ui()

    def _construir_ui(self):
        # Título
        ctk.CTkLabel(
            self, text="🛒  Tienda Online",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=(36, 4))

        ctk.CTkLabel(
            self, text="Inicia sesión o regístrate para continuar",
            font=ctk.CTkFont(size=13), text_color="gray"
        ).pack(pady=(0, 24))

        # Tabs login / registro
        self.tabview = ctk.CTkTabview(self, width=360)
        self.tabview.pack(padx=28, pady=0, fill="x")

        self.tabview.add("Iniciar sesión")
        self.tabview.add("Registrarse")

        self._tab_login(self.tabview.tab("Iniciar sesión"))
        self._tab_registro(self.tabview.tab("Registrarse"))

    def _tab_login(self, tab):
        ctk.CTkLabel(tab, text="Correo electrónico", anchor="w").pack(fill="x", pady=(12, 2))
        self.login_email = ctk.CTkEntry(tab, placeholder_text="usuario@email.com", width=340)
        self.login_email.pack(fill="x")

        ctk.CTkLabel(tab, text="Contraseña", anchor="w").pack(fill="x", pady=(12, 2))
        self.login_pass = ctk.CTkEntry(tab, placeholder_text="••••••", show="•", width=340)
        self.login_pass.pack(fill="x")
        self.login_pass.bind("<Return>", lambda e: self._iniciar_sesion())

        self.login_msg = ctk.CTkLabel(tab, text="", text_color="#e05555", font=ctk.CTkFont(size=12))
        self.login_msg.pack(pady=(8, 0))

        ctk.CTkButton(
            tab, text="Iniciar sesión", height=40,
            command=self._iniciar_sesion
        ).pack(fill="x", pady=(10, 12))

    def _tab_registro(self, tab):
        ctk.CTkLabel(tab, text="Nombre completo", anchor="w").pack(fill="x", pady=(12, 2))
        self.reg_nombre = ctk.CTkEntry(tab, placeholder_text="Juan Pérez", width=340)
        self.reg_nombre.pack(fill="x")

        ctk.CTkLabel(tab, text="Correo electrónico", anchor="w").pack(fill="x", pady=(10, 2))
        self.reg_email = ctk.CTkEntry(tab, placeholder_text="usuario@email.com", width=340)
        self.reg_email.pack(fill="x")

        ctk.CTkLabel(tab, text="Contraseña", anchor="w").pack(fill="x", pady=(10, 2))
        self.reg_pass = ctk.CTkEntry(tab, placeholder_text="••••••", show="•", width=340)
        self.reg_pass.pack(fill="x")
        self.reg_pass.bind("<Return>", lambda e: self._registrar())

        self.reg_msg = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(size=12))
        self.reg_msg.pack(pady=(8, 0))

        ctk.CTkButton(
            tab, text="Crear cuenta", height=40,
            command=self._registrar
        ).pack(fill="x", pady=(10, 12))

    def _iniciar_sesion(self):
        email = self.login_email.get().strip()
        contraseña = self.login_pass.get().strip()
        if not email or not contraseña:
            self.login_msg.configure(text="Completa todos los campos.", text_color="#e05555")
            return
        exito, mensaje = self.autenticacion.iniciar_sesion(email, contraseña)
        if exito:
            self.destroy()
            self.on_login_exitoso()
        else:
            self.login_msg.configure(text=mensaje, text_color="#e05555")

    def _registrar(self):
        nombre = self.reg_nombre.get().strip()
        email = self.reg_email.get().strip()
        contraseña = self.reg_pass.get().strip()
        if not nombre or not email or not contraseña:
            self.reg_msg.configure(text="Completa todos los campos.", text_color="#e05555")
            return
        exito, mensaje = self.autenticacion.registrar_usuario(nombre, email, contraseña)
        if exito:
            self.reg_msg.configure(text="¡Cuenta creada! Inicia sesión.", text_color="#4caf50")
            self.tabview.set("Iniciar sesión")
            self.reg_nombre.delete(0, "end")
            self.reg_email.delete(0, "end")
            self.reg_pass.delete(0, "end")
        else:
            self.reg_msg.configure(text=mensaje, text_color="#e05555")


# Ventana Principal de la tienda

class Aplicacion(ctk.CTk):
    """Ventana principal de la aplicación de tienda"""

    # Colores de acento
    COLOR_ACENTO   = "#1f6feb"
    COLOR_PELIGRO  = "#d93025"
    COLOR_EXITO    = "#2ea043"
    COLOR_TABLA_H  = "#1a1a2e"
    COLOR_FILA_PAR = "#1e1e2e"

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Tienda Online")
        self.geometry("1050x680")
        self.minsize(900, 580)

        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 525
        y = (self.winfo_screenheight() // 2) - 340
        self.geometry(f"+{x}+{y}")

        # Inicializar backend
        self.conexion = ConexionMongoDB()
        self.conexion.inicializar_bd()
        self.autenticacion = SistemaAutenticacion(self.conexion.db)
        self.gestor_productos = GestorProductos(self.conexion.db)
        self.gestor_carrito = GestorCarrito(self.conexion.db)
        self.gestor_pedidos = GestorPedidos(self.conexion.db)

        # Variable de estado: sección activa
        self._seccion_activa = None

        # Construir estructura base (navbar + contenido)
        self._construir_layout()

        # Mostrar pantalla de login al iniciar
        self.withdraw()
        self.after(100, self._mostrar_login)

    # Layout

    def _construir_layout(self):
        """Construye navbar lateral + área de contenido"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar, text="🛒 Tienda",
            font=ctk.CTkFont(size=20, weight="bold"), pady=10
        ).grid(row=0, column=0, padx=16, pady=(24, 4), sticky="w")

        self.lbl_usuario_nav = ctk.CTkLabel(
            self.sidebar, text="", font=ctk.CTkFont(size=11),
            text_color="gray", wraplength=170
        )
        self.lbl_usuario_nav.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="w")

        ctk.CTkLabel(self.sidebar, text="CATÁLOGO", font=ctk.CTkFont(size=10),
                     text_color="gray").grid(row=2, column=0, padx=16, pady=(4, 2), sticky="w")

        self._nav_btns = {}
        nav_items = [
            ("todos",     "📦  Todos los productos",    3),
            ("categoria", "🔖  Por categoría",           4),
            ("buscar",    "🔍  Buscar producto",         5),
            ("carrito",   "🛒  Carrito de compras",      6),
            ("historial", "📋  Historial de compras",    7),
        ]
        for key, label, row in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                fg_color="transparent", hover_color=("#2a2d3e", "#2a2d3e"),
                font=ctk.CTkFont(size=13),
                command=lambda k=key: self._navegar(k)
            )
            btn.grid(row=row, column=0, padx=8, pady=2, sticky="ew")
            self._nav_btns[key] = btn

        # Botón cerrar sesión al fondo
        ctk.CTkButton(
            self.sidebar, text="↩  Cerrar sesión",
            fg_color="transparent", hover_color="#3a1a1a",
            text_color="#e05555", anchor="w",
            command=self._cerrar_sesion
        ).grid(row=11, column=0, padx=8, pady=(0, 20), sticky="ew")

        # Área de contenido principal
        self.contenido = ctk.CTkFrame(self, fg_color="transparent")
        self.contenido.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.contenido.grid_columnconfigure(0, weight=1)
        self.contenido.grid_rowconfigure(1, weight=1)

        # Barra superior (título de sección)
        self.barra_top = ctk.CTkFrame(self.contenido, height=56, corner_radius=0,
                                       fg_color=("#1a1a2e", "#1a1a2e"))
        self.barra_top.grid(row=0, column=0, sticky="ew")
        self.lbl_seccion = ctk.CTkLabel(
            self.barra_top, text="",
            font=ctk.CTkFont(size=17, weight="bold")
        )
        self.lbl_seccion.place(relx=0.03, rely=0.5, anchor="w")

        # Frame de contenido dinámico
        self.frame_contenido = ctk.CTkScrollableFrame(
            self.contenido, fg_color="transparent"
        )
        self.frame_contenido.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)
        self.frame_contenido.grid_columnconfigure(0, weight=1)

    # Navegación

    def _navegar(self, seccion):
        """Cambia la sección activa del contenido"""
        self._seccion_activa = seccion

        # Resaltar botón activo
        for key, btn in self._nav_btns.items():
            if key == seccion:
                btn.configure(fg_color=self.COLOR_ACENTO)
            else:
                btn.configure(fg_color="transparent")

        # Limpiar contenido actual
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        secciones = {
            "todos":     (self._vista_todos_productos,   "📦  Todos los productos"),
            "categoria": (self._vista_por_categoria,     "🔖  Buscar por categoría"),
            "buscar":    (self._vista_buscar,            "🔍  Buscar producto"),
            "carrito":   (self._vista_carrito,           "🛒  Carrito de compras"),
            "historial": (self._vista_historial,         "📋  Historial de compras"),
        }
        if seccion in secciones:
            fn, titulo = secciones[seccion]
            self.lbl_seccion.configure(text=titulo)
            fn()

    # Helpers Visuales

    def _tabla_header(self, parent, columnas, pesos):
        """Dibuja fila de encabezados de tabla"""
        fila = ctk.CTkFrame(parent, fg_color=self.COLOR_TABLA_H, corner_radius=6)
        fila.pack(fill="x", pady=(0, 2))
        for i, (col, peso) in enumerate(zip(columnas, pesos)):
            fila.grid_columnconfigure(i, weight=peso)
            ctk.CTkLabel(
                fila, text=col, font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w", padx=8, pady=6
            ).grid(row=0, column=i, sticky="ew")
        return fila

    def _tabla_fila(self, parent, valores, pesos, par=True, botones=None):
        """Dibuja una fila de datos en la tabla"""
        color = self.COLOR_FILA_PAR if par else "#16213e"
        fila = ctk.CTkFrame(parent, fg_color=color, corner_radius=4)
        fila.pack(fill="x", pady=1)
        total_cols = len(valores) + (len(botones) if botones else 0)
        for i in range(total_cols):
            peso = pesos[i] if i < len(pesos) else 1
            fila.grid_columnconfigure(i, weight=peso)

        for i, (val, peso) in enumerate(zip(valores, pesos)):
            ctk.CTkLabel(
                fila, text=val, anchor="w", padx=8, pady=5,
                font=ctk.CTkFont(size=12)
            ).grid(row=0, column=i, sticky="ew")

        if botones:
            for j, (label, color_btn, cmd) in enumerate(botones):
                ctk.CTkButton(
                    fila, text=label, width=90, height=26,
                    fg_color=color_btn, hover_color=color_btn,
                    font=ctk.CTkFont(size=11), command=cmd
                ).grid(row=0, column=len(valores) + j, padx=4, pady=3)
        return fila

    def _mensaje_vacio(self, parent, texto):
        ctk.CTkLabel(
            parent, text=texto,
            font=ctk.CTkFont(size=14), text_color="gray"
        ).pack(pady=40)

    # Vista de todos los productos

    def _vista_todos_productos(self):
        productos = self.gestor_productos.obtener_todos_productos()
        if not productos:
            self._mensaje_vacio(self.frame_contenido, "No hay productos disponibles.")
            return
        self._renderizar_tabla_productos(productos)

    # Vista de productos por categoría

    def _vista_por_categoria(self):
        categorias = self.gestor_productos.obtener_categorias()

        top = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        top.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(top, text="Categoría:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(0, 8))

        self._cat_var = ctk.StringVar(value=categorias[0] if categorias else "")
        menu = ctk.CTkOptionMenu(
            top, values=categorias, variable=self._cat_var,
            width=200, command=self._filtrar_por_categoria
        )
        menu.pack(side="left")

        self._frame_cat_resultados = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        self._frame_cat_resultados.pack(fill="both", expand=True)

        if categorias:
            self._filtrar_por_categoria(categorias[0])

    def _filtrar_por_categoria(self, categoria):
        for w in self._frame_cat_resultados.winfo_children():
            w.destroy()
        productos = self.gestor_productos.obtener_productos_por_categoria(categoria)
        if not productos:
            self._mensaje_vacio(self._frame_cat_resultados, "Sin productos en esta categoría.")
        else:
            self._renderizar_tabla_productos(productos, parent=self._frame_cat_resultados)

    # Vista de Buscar Producto

    def _vista_buscar(self):
        top = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        top.pack(fill="x", pady=(0, 16))

        self._buscar_entry = ctk.CTkEntry(
            top, placeholder_text="Escribe un nombre o descripción...", width=340
        )
        self._buscar_entry.pack(side="left", padx=(0, 8))
        self._buscar_entry.bind("<Return>", lambda e: self._ejecutar_busqueda())

        ctk.CTkButton(
            top, text="Buscar", width=100,
            command=self._ejecutar_busqueda
        ).pack(side="left")

        self._frame_buscar_resultados = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        self._frame_buscar_resultados.pack(fill="both", expand=True)

    def _ejecutar_busqueda(self):
        termino = self._buscar_entry.get().strip()
        for w in self._frame_buscar_resultados.winfo_children():
            w.destroy()
        if not termino:
            self._mensaje_vacio(self._frame_buscar_resultados, "Escribe un término para buscar.")
            return
        productos = self.gestor_productos.buscar_productos(termino)
        if not productos:
            self._mensaje_vacio(self._frame_buscar_resultados, f"Sin resultados para \"{termino}\".")
        else:
            self._renderizar_tabla_productos(productos, parent=self._frame_buscar_resultados)

    # Tabla de Productos

    def _renderizar_tabla_productos(self, productos, parent=None):
        if parent is None:
            parent = self.frame_contenido

        columnas = ["ID", "Nombre", "Categoría", "Precio", "Stock", "Val.", ""]
        pesos    = [2,    5,        3,            2,        1,       1,      2]
        self._tabla_header(parent, columnas, pesos)

        for i, p in enumerate(productos):
            self._tabla_fila(
                parent,
                valores=[
                    p["_id"],
                    p["nombre"],
                    p["categoria"],
                    f"${p['precio']:.2f}",
                    str(p["stock"]),
                    f"⭐ {p.get('valoracion', '-')}",
                ],
                pesos=pesos,
                par=(i % 2 == 0),
                botones=[
                    ("+ Agregar", self.COLOR_ACENTO, lambda pid=p["_id"]: self._dialogo_agregar(pid))
                ]
            )

    # Agregar al carrito

    def _dialogo_agregar(self, producto_id):
        producto = self.gestor_productos.obtener_producto_por_id(producto_id)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        dialogo = ctk.CTkToplevel(self)
        dialogo.title("Agregar al carrito")
        dialogo.geometry("380x300")
        dialogo.resizable(False, False)
        dialogo.grab_set()

        ctk.CTkLabel(
            dialogo, text=producto["nombre"],
            font=ctk.CTkFont(size=16, weight="bold"), wraplength=340
        ).pack(pady=(24, 4), padx=20)

        ctk.CTkLabel(
            dialogo,
            text=f"{producto['descripcion']}\n\nPrecio: ${producto['precio']:.2f}  |  Stock disponible: {producto['stock']}",
            font=ctk.CTkFont(size=12), text_color="gray", wraplength=340
        ).pack(padx=20)

        ctk.CTkLabel(dialogo, text="Cantidad:", anchor="w").pack(fill="x", padx=28, pady=(16, 2))
        entrada_cantidad = ctk.CTkEntry(dialogo, placeholder_text="1", width=120)
        entrada_cantidad.insert(0, "1")
        entrada_cantidad.pack(padx=28, anchor="w")

        msg = ctk.CTkLabel(dialogo, text="", text_color="#e05555", font=ctk.CTkFont(size=12))
        msg.pack(pady=6)

        def confirmar():
            try:
                cantidad = int(entrada_cantidad.get())
                if cantidad <= 0:
                    raise ValueError
            except ValueError:
                msg.configure(text="Ingresa una cantidad válida (número entero positivo).")
                return
            if cantidad > producto["stock"]:
                msg.configure(text=f"Stock insuficiente. Máximo disponible: {producto['stock']}")
                return
            usuario = self.autenticacion.obtener_usuario_actual()
            exito, mensaje = self.gestor_carrito.agregar_producto(
                usuario["_id"], producto_id, cantidad, producto["precio"]
            )
            dialogo.destroy()
            if exito:
                messagebox.showinfo("✓ Agregado", mensaje)
            else:
                messagebox.showerror("Error", mensaje)

        ctk.CTkButton(
            dialogo, text="Agregar al carrito", height=38, command=confirmar
        ).pack(padx=28, fill="x", pady=(4, 16))

    # Vista del carrito

    def _vista_carrito(self):
        usuario = self.autenticacion.obtener_usuario_actual()
        carrito = self.gestor_carrito.obtener_carrito(usuario["_id"])

        if not carrito or not carrito["productos"]:
            self._mensaje_vacio(self.frame_contenido, "Tu carrito está vacío.")
            return

        columnas = ["Producto", "P. Unitario", "Cantidad", "Subtotal", ""]
        pesos    = [5,          2,              2,          2,          2]
        self._tabla_header(self.frame_contenido, columnas, pesos)

        for i, item in enumerate(carrito["productos"]):
            prod = self.gestor_productos.obtener_producto_por_id(item["producto_id"])
            nombre = prod["nombre"] if prod else item["producto_id"]
            self._tabla_fila(
                self.frame_contenido,
                valores=[
                    nombre,
                    f"${item['precio_unitario']:.2f}",
                    str(item["cantidad"]),
                    f"${item['subtotal']:.2f}",
                ],
                pesos=pesos,
                par=(i % 2 == 0),
                botones=[
                    ("Eliminar", self.COLOR_PELIGRO,
                     lambda pid=item["producto_id"]: self._eliminar_del_carrito(pid))
                ]
            )

        # Totales y botón comprar
        sep = ctk.CTkFrame(self.frame_contenido, height=2, fg_color=self.COLOR_ACENTO)
        sep.pack(fill="x", pady=12)

        fila_total = ctk.CTkFrame(self.frame_contenido, fg_color="transparent")
        fila_total.pack(fill="x")

        ctk.CTkLabel(
            fila_total,
            text=f"TOTAL:  ${carrito['total']:.2f}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            fila_total, text="✅  Realizar compra", height=42, width=200,
            fg_color=self.COLOR_EXITO, hover_color="#256d34",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._confirmar_compra
        ).pack(side="right", padx=8)

    def _eliminar_del_carrito(self, producto_id):
        usuario = self.autenticacion.obtener_usuario_actual()
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este producto del carrito?"):
            exito, mensaje = self.gestor_carrito.eliminar_producto(usuario["_id"], producto_id)
            if exito:
                self._navegar("carrito")
            else:
                messagebox.showerror("Error", mensaje)

    def _confirmar_compra(self):
        usuario = self.autenticacion.obtener_usuario_actual()
        carrito = self.gestor_carrito.obtener_carrito(usuario["_id"])
        if not carrito or not carrito["productos"]:
            messagebox.showwarning("Carrito vacío", "No hay productos en el carrito.")
            return

        confirmado = messagebox.askyesno(
            "Confirmar compra",
            f"¿Confirmas la compra por un total de ${carrito['total']:.2f}?\n\n"
            "El pago se procesará en efectivo."
        )
        if confirmado:
            exito, mensaje = self.gestor_pedidos.crear_pedido(usuario["_id"])
            if exito:
                messagebox.showinfo("✓ Compra realizada", mensaje)
                self._navegar("historial")
            else:
                messagebox.showerror("Error al procesar", mensaje)

    # Vista del Historial

    def _vista_historial(self):
        usuario = self.autenticacion.obtener_usuario_actual()
        pedidos = self.gestor_pedidos.obtener_historial_pedidos(usuario["_id"])

        if not pedidos:
            self._mensaje_vacio(self.frame_contenido, "Aún no tienes compras registradas.")
            return

        columnas = ["N° Pedido", "Fecha", "Entrega estimada", "Total", "Estado"]
        pesos    = [3,           4,       4,                  2,       2]
        self._tabla_header(self.frame_contenido, columnas, pesos)

        for i, pedido in enumerate(reversed(pedidos)):
            fecha = pedido["fecha_pedido"]
            entrega = pedido.get("fecha_entrega_estimada", "—")
            fecha_str   = fecha.strftime("%d/%m/%Y %H:%M") if isinstance(fecha, datetime) else str(fecha)
            entrega_str = entrega.strftime("%d/%m/%Y") if isinstance(entrega, datetime) else str(entrega)

            self._tabla_fila(
                self.frame_contenido,
                valores=[
                    pedido["_id"],
                    fecha_str,
                    entrega_str,
                    f"${pedido['total']:.2f}",
                    pedido["estado"].capitalize(),
                ],
                pesos=pesos,
                par=(i % 2 == 0)
            )

    # Login

    def _mostrar_login(self):
        VentanaAuth(self, self.autenticacion, self._on_login_exitoso)

    def _on_login_exitoso(self):
        usuario = self.autenticacion.obtener_usuario_actual()
        self.lbl_usuario_nav.configure(text=f"👤 {usuario['nombre']}")
        self.deiconify()
        self._navegar("todos")

    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar tu sesión?"):
            self.autenticacion.cerrar_sesion()
            self.lbl_usuario_nav.configure(text="")
            self._seccion_activa = None
            for key, btn in self._nav_btns.items():
                btn.configure(fg_color="transparent")
            for widget in self.frame_contenido.winfo_children():
                widget.destroy()
            self.lbl_seccion.configure(text="")
            self.withdraw()
            self.after(100, self._mostrar_login)


# Punto de Entrada

if __name__ == "__main__":
    try:
        app = Aplicacion()
        app.mainloop()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        messagebox.showerror("Error inesperado", str(e))