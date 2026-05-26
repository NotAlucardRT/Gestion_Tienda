# ============================================================
# GESTIÓN DE PEDIDOS
# ============================================================

from datetime import datetime, timedelta


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