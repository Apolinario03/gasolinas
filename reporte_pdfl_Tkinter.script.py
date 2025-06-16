import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime


# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sistemas321',
    'database': 'gasolinas1',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# ===================== FUNCIONES BASE DE DATOS =====================

def obtener_productos():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM productos ORDER BY nombre")
        productos = [fila[0] for fila in cursor.fetchall()]
        cursor.close()
        conn.close()
        return productos
    except Exception as e:
        print(f"Error obteniendo productos: {e}")
        return []

def obtener_estaciones():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM estacion ORDER BY nombre")
        estaciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return estaciones
    except Exception as e:
        print(f"Error obteniendo estaciones: {e}")
        return []

# ===================== REPORTE PDF =====================

def generar_reporte_pdf(producto, estacion_id, estacion_nombre, fecha_inicio, fecha_fin):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.fecha, i.cantidad, i.precio_venta, i.venta_soles
            FROM inventario i
            JOIN productos p ON i.productoid = p.id
            WHERE p.nombre = %s AND i.estacionid = %s AND i.fecha BETWEEN %s AND %s
            ORDER BY i.fecha
        """, (producto, estacion_id, fecha_inicio, fecha_fin))
        datos = cursor.fetchall()
        cursor.close()
        conn.close()

        if not datos:
            messagebox.showwarning("Sin datos", "No se encontraron registros para ese rango.")
            return

        # Crear PDF
        nombre_pdf = f"reporte_{producto}_{estacion_nombre.replace(' ', '_')}.pdf"
        c = canvas.Canvas(nombre_pdf, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, f"Estación: {estacion_nombre}")
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 1.4*inch, f"Producto: {producto}")
        c.drawString(1*inch, height - 1.7*inch, f"Desde: {fecha_inicio}  Hasta: {fecha_fin}")

        c.setFont("Helvetica-Bold", 11)
        c.drawString(1*inch, height - 2.1*inch, "Fecha")
        c.drawString(2.5*inch, height - 2.1*inch, "Cantidad (gal)")
        c.drawString(4.2*inch, height - 2.1*inch, "Precio Venta")
        c.drawString(5.8*inch, height - 2.1*inch, "Venta S/")

        y = height - 2.4*inch
        total_venta = 0

        c.setFont("Helvetica", 10)
        for fecha, cantidad, precio, venta in datos:
            if y < 1*inch:
                c.showPage()
                y = height - 1*inch
                c.setFont("Helvetica-Bold", 16)
                c.drawString(1*inch, height - 1*inch, f"Estación: {estacion_nombre}")
                c.setFont("Helvetica-Bold", 11)
                c.drawString(1*inch, height - 1.5*inch, "Fecha")
                c.drawString(2.5*inch, height - 1.5*inch, "Cantidad (gal)")
                c.drawString(4.2*inch, height - 1.5*inch, "Precio Venta")
                c.drawString(5.8*inch, height - 1.5*inch, "Venta S/")
                y = height - 1.8*inch
                c.setFont("Helvetica", 10)

            c.drawString(1*inch, y, fecha.strftime("%Y-%m-%d"))
            c.drawRightString(3.9*inch, y, f"{cantidad:.2f}")
            c.drawRightString(5.4*inch, y, f"{precio:.2f}")
            c.drawRightString(7.4*inch, y, f"{venta:.2f}")
            total_venta += venta
            y -= 0.25*inch

        c.setFont("Helvetica-Bold", 11)
        y -= 0.2*inch
        c.drawString(1*inch, y, "Total Venta S/:")
        c.drawRightString(7.4*inch, y, f"{total_venta:.2f}")

        c.save()
        messagebox.showinfo("Éxito", f"PDF generado: {nombre_pdf}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")

# ===================== INTERFAZ =====================

def crear_interfaz():
    root = tk.Tk()
    root.title("Generar Reporte PDF")
    root.geometry("450x300")

    # === Productos ===
    tk.Label(root, text="Producto:").pack(pady=5)
    producto_cb = ttk.Combobox(root, values=obtener_productos(), state="readonly")
    producto_cb.pack()

    # === Estaciones ===
    tk.Label(root, text="Estación:").pack(pady=5)
    estaciones = obtener_estaciones()
    estacion_dict = {nombre: id_ for id_, nombre in estaciones}
    estacion_cb = ttk.Combobox(root, values=list(estacion_dict.keys()), state="readonly")
    estacion_cb.pack()

    # === Fechas ===
    tk.Label(root, text="Fecha Inicio:").pack(pady=5)
    fecha_inicio = DateEntry(root, width=15, date_pattern='yyyy-mm-dd')
    fecha_inicio.set_date(datetime.date.today())
    fecha_inicio.pack()

    tk.Label(root, text="Fecha Fin:").pack(pady=5)
    fecha_fin = DateEntry(root, width=15, date_pattern='yyyy-mm-dd')
    fecha_fin.set_date(datetime.date.today())
    fecha_fin.pack()

    # === Botón generar ===
    def generar():
        producto = producto_cb.get()
        estacion_nombre = estacion_cb.get()
        estacion_id = estacion_dict.get(estacion_nombre)
        f_ini = fecha_inicio.get_date().strftime("%Y-%m-%d")
        f_fin = fecha_fin.get_date().strftime("%Y-%m-%d")

        if not producto or not estacion_id:
            messagebox.showwarning("Campos vacíos", "Selecciona todos los campos.")
            return

        generar_reporte_pdf(producto, estacion_id, estacion_nombre, f_ini, f_fin)

    tk.Button(root, text="Generar PDF", command=generar, bg="#4CAF50", fg="white").pack(pady=15)

    root.mainloop()

# === Ejecutar
if __name__ == "__main__":
    crear_interfaz()
