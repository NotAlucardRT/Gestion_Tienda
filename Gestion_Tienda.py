# ============================================================
# APLICACIÓN DE TIENDA ONLINE CON MONGODB
# Desarrolladores: Equipo Bases de Datos
# Asignatura: Bases de Datos - Actividad 8
# ============================================================

from tkinter import messagebox
from ui.aplicacion import Aplicacion


# Punto de Entrada

if __name__ == "__main__":
    try:
        app = Aplicacion()
        app.mainloop()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        messagebox.showerror("Error inesperado", str(e))