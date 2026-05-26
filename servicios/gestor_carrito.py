# ============================================================
# GESTIÓN DE CARRITO
# ============================================================

from datetime import datetime


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