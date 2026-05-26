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