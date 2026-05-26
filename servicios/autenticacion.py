# ============================================================
# SISTEMA DE AUTENTICACIÓN
# ============================================================

from datetime import datetime
from pymongo.errors import OperationFailure
from db.conexion import ConexionMongoDB


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