# APLICACIÓN DE TIENDA ONLINE CON MONGODB
## Documentación de Uso

---

## 📋 Descripción General

Esta es una aplicación de tienda en línea desarrollada en Python que utiliza **MongoDB** como base de datos documental. Permite a los usuarios realizar compras, gestionar un carrito de compras y mantener un historial de pedidos.

---

## 🎯 Funcionalidades Principales

### 1. **Ver Todos los Productos**
- Muestra el catálogo completo de productos disponibles
- Información: ID, nombre, precio y stock

### 2. **Buscar Productos por Categoría**
- Filtra productos según su categoría
- Categorías disponibles: Electrónica, Accesorios, Monitores, Audio, Almacenamiento, Componentes

### 3. **Buscar Productos por Nombre**
- Búsqueda por término de texto en nombre o descripción
- Búsqueda insensible a mayúsculas

### 4. **Carrito de Compras**
- Ver contenido del carrito con detalles de cada producto
- Agregar productos (con verificación de stock)
- Eliminar productos del carrito
- Vaciar carrito automáticamente después de compra

### 5. **Realizar Compra**
- Procesar pedido desde el carrito
- Verificar disponibilidad de stock
- Registrar pedido con número único
- Actualizar inventario automáticamente

### 6. **Historial de Compras**
- Ver todos los pedidos realizados
- Información: número de pedido, fecha, total y estado

### 7. **Autenticación de Usuarios**
- Registrar nuevos usuarios
- Iniciar sesión con email y contraseña
- Contraseñas encriptadas con SHA-256
- Cada usuario tiene su propio carrito e historial

---

## 🗄️ Estructura de Base de Datos

### Colecciones MongoDB

#### 1. **usuarios**
Almacena información de usuarios registrados
```json
{
  "_id": "user_001",
  "nombre": "Juan Pérez",
  "email": "juan@email.com",
  "contraseña": "hash_sha256",
  "fecha_registro": "2026-05-24T10:30:00Z",
  "historial_compras": ["PED_00001"],
  "estado": "activo"
}
```

#### 2. **productos**
Catálogo de productos disponibles
```json
{
  "_id": "prod_001",
  "nombre": "Laptop Dell XPS 13",
  "categoria": "Electrónica",
  "precio": 1200.00,
  "stock": 15,
  "descripcion": "Laptop ultraportátil de 13 pulgadas",
  "imagen": "laptop_dell.jpg",
  "valoracion": 4.8,
  "fecha_creacion": "2026-05-24T10:30:00Z"
}
```

#### 3. **carritos**
Carrito de compras de cada usuario
```json
{
  "_id": "user_001",
  "usuario_id": "user_001",
  "productos": [
    {
      "producto_id": "prod_001",
      "cantidad": 1,
      "precio_unitario": 1200.00,
      "subtotal": 1200.00,
      "fecha_agregado": "2026-05-24T10:50:00Z"
    }
  ],
  "fecha_creacion": "2026-05-24T10:30:00Z",
  "fecha_actualizacion": "2026-05-24T11:00:00Z",
  "total": 1200.00
}
```

#### 4. **pedidos**
Histórico de compras completadas
```json
{
  "_id": "PED_00001",
  "usuario_id": "user_001",
  "productos": [...],
  "total": 1200.00,
  "estado": "completado",
  "fecha_pedido": "2026-05-24T11:05:00Z",
  "fecha_entrega_estimada": "2026-05-30T11:05:00Z",
  "metodo_pago": "efectivo"
}
```

---

## ⚙️ Requisitos Técnicos

### Dependencias
- **Python 3.8+**
- **MongoDB 4.0+**
- **pymongo 4.6.0**
- **CustomTkinter**

### Instalación de Dependencias

```bash
# Instalar pymongo
pip install -r requirements.txt
```
```bash
# Instalar CustomTkinter
pip install customtkinter
```

O directamente:
```bash
pip install pymongo==4.6.0
```

---

## 🚀 Instalación y Ejecución

### 1. Asegurar que MongoDB esté ejecutándose

**En Windows:**
```bash
# Si MongoDB está instalado como servicio
net start MongoDB

# O si está en la carpeta de instalación
"C:\Program Files\MongoDB\Server\[VERSION]\bin\mongod.exe"
```

**En Linux/Mac:**
```bash
# Usando Homebrew (Mac)
brew services start mongodb-community

# O manualmente
mongod
```

### 2. Verificar conexión a MongoDB

```bash
# Abre MongoDB Compass o una terminal
mongosh
# o
mongo

# Verifica que puedas conectarte a localhost:27017
```

### 3. Ejecutar la aplicación

```bash
python Gestion_Tienda.py
```

---

## 👤 Usuarios de Prueba

La aplicación crea 3 usuarios automáticamente:

| Usuario | Email | Contraseña |
|---------|-------|-----------|
| Juan Pérez | juan@email.com | 123456 |
| María García | maria@email.com | 123456 |
| Carlos López | carlos@email.com | 123456 |

También puedes registrar nuevos usuarios desde el menú de inicio.

---

## 📖 Guía de Uso

### Flujo Principal

1. **Inicio**: El programa te pide iniciar sesión o registrarse
2. **Tienda**: Accede al menú principal para navegar productos
3. **Compra**: Agrega productos al carrito y realiza la compra
4. **Historial**: Visualiza tus pedidos anteriores

### Operaciones CRUD Implementadas

| Operación | Dónde | Método |
|-----------|-------|--------|
| **CREATE** (Crear) | usuarios, productos, carritos, pedidos | registrar_usuario(), crear_pedido() |
| **READ** (Leer) | usuarios, productos, carritos, pedidos | obtener_todos_productos(), obtener_carrito() |
| **UPDATE** (Actualizar) | productos, carritos, usuarios | actualizar_stock(), agregar_producto() |
| **DELETE** (Eliminar) | carritos, pedidos | vaciar_carrito(), eliminar_producto() |

---

## 🔐 Características de Seguridad

- **Contraseñas Encriptadas**: Se almacenan con hash SHA-256
- **Validación de Stock**: No permite vender más de lo disponible
- **Carritos Independientes**: Cada usuario tiene su propio carrito
- **Historial Inmutable**: Los pedidos no se pueden modificar (solo lectura)

---

## 🔗 Relaciones entre Colecciones

```
usuarios (1) ───────── (muchos) pedidos
   │
   └───────────────────────── (1) carritos

productos (muchos) ───────── (muchos) carritos.productos[]
     │
     └───────────────────── (muchos) pedidos.productos[]
```

---

## 📊 Datos de Ejemplo

### 8 Productos Precargados:
1. **Laptop Dell XPS 13** - $1200.00 - 15 en stock
2. **Mouse Logitech MX Master** - $99.99 - 45 en stock
3. **Teclado Mecánico Corsair K95** - $199.99 - 20 en stock
4. **Monitor LG UltraWide** - $599.99 - 8 en stock
5. **Webcam Logitech C920** - $79.99 - 30 en stock
6. **Audífonos Sony WH-1000XM5** - $399.99 - 12 en stock
7. **SSD Samsung 980 Pro** - $249.99 - 50 en stock
8. **Memoria RAM Corsair Vengeance** - $89.99 - 35 en stock

---

## 🐛 Solución de Problemas

### Error: "No se puede conectar a MongoDB"
- Verifica que MongoDB esté ejecutándose
- Comprueba que escucha en localhost:27017
- Usa `mongosh` o `mongo` para verificar la conexión

### Error: "El email ya está registrado"
- El usuario ya existe en la base de datos
- Intenta con otro email

### Error: "Stock insuficiente"
- No hay suficientes unidades del producto
- Ajusta la cantidad o intenta con otro producto

---

## 📝 Notas Importantes

- La aplicación no persiste sesiones (se cierra al salir)
- Los datos se guardan en MongoDB (permanente)
- El carrito se vacía automáticamente después de una compra exitosa
- Los precios son en dólares USD

---

## 👨‍💻 Clases Principales

### ConexionMongoDB
Gestiona la conexión e inicialización de la base de datos

### SistemaAutenticacion
Maneja registro e inicio de sesión de usuarios

### GestorProductos
CRUD de productos y búsquedas

### GestorCarrito
Agregar, eliminar y actualizar carrito

### GestorPedidos
Crear pedidos y gestionar historial

### Aplicacion
Interfaz de consola interactiva

---

## 📞 Contacto y Soporte

Para preguntas o problemas, consulta la documentación técnica en `Esquema_Tienda.json`

---

**Versión**: 1.0  
**Fecha**: Mayo 2026  
**Desarrolladores**: Equipo Bases de Datos - Quinto Semestre
