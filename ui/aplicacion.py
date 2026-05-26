# ============================================================
# INTERFAZ GRÁFICA
# ============================================================

from datetime import datetime
from tkinter import messagebox
import customtkinter as ctk

from db.conexion import ConexionMongoDB
from servicios.autenticacion import SistemaAutenticacion
from servicios.gestor_productos import GestorProductos
from servicios.gestor_carrito import GestorCarrito
from servicios.gestor_pedidos import GestorPedidos


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
            self, text="Tienda Online",
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