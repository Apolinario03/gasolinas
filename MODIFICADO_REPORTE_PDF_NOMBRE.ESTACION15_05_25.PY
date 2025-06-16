import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sistemas321',
    'database': 'gasolinas1',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

def obtener_nombre_estacion(estacion_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM estacion WHERE id = %s", (estacion_id,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado[0] if resultado else f"Estación ID {estacion_id}"
    except:
        return f"Estación ID {estacion_id}"

def generar_reporte_producto(producto, estacion_id, fecha_inicio, fecha_fin):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.fecha, i.cantidad, i.precio_venta, i.venta_soles
            FROM inventario i
            JOIN productos p ON i.productoid = p.id
            WHERE p.nombre = %s AND i.estacionid = %s AND i.fecha BETWEEN %s AND %s
            ORDER BY i.fecha;
        """, (producto, estacion_id, fecha_inicio, fecha_fin))
        datos = cursor.fetchall()

        if not datos:
            print(f"⚠️ No se encontraron datos para el producto '{producto}' en la estación {estacion_id}.")
            return

        nombre_estacion = obtener_nombre_estacion(estacion_id)

        # Crear PDF
        nombre_pdf = f"reporte_{producto}_{nombre_estacion.replace(' ', '_')}.pdf"
        c = canvas.Canvas(nombre_pdf, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, f"Estación: {nombre_estacion}")
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
                c.drawString(1*inch, height - 1*inch, f"Estación: {nombre_estacion}")
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

        # Total
        c.setFont("Helvetica-Bold", 11)
        y -= 0.2*inch
        c.drawString(1*inch, y, "Total Venta S/:")
        c.drawRightString(7.4*inch, y, f"{total_venta:.2f}")

        c.save()
        print(f"✅ PDF generado correctamente: {nombre_pdf}")

    except Exception as e:
        print(f"❌ Error al generar el reporte: {e}")

# Llamada directa
if __name__ == "__main__":
    generar_reporte_producto(
        producto="GLP",
        estacion_id=3,
        fecha_inicio="2025-05-01",
        fecha_fin="2025-05-20"
    )




