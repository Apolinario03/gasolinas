import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sistemas321',
    'database': 'gasolinas1',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

def generar_reporte_producto_detallado(producto, estacion_id, fecha_inicio, fecha_fin):
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
        conn.close()

        if not datos:
            print(f"⚠️ No se encontraron datos para el producto '{producto}' entre {fecha_inicio} y {fecha_fin} en la estación ID {estacion_id}.")
            return

        archivo_pdf = f"Reporte_{producto}_{fecha_inicio}_a_{fecha_fin}.pdf"
        c = canvas.Canvas(archivo_pdf, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, f"Reporte Diario de Ventas - {producto}")
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 1.3*inch, f"Estación ID: {estacion_id}")
        c.drawString(1*inch, height - 1.6*inch, f"Del {fecha_inicio} al {fecha_fin}")

        c.setFont("Helvetica-Bold", 11)
        c.drawString(1*inch, height - 2*inch, "Fecha")
        c.drawString(2.5*inch, height - 2*inch, "Galones")
        c.drawString(4*inch, height - 2*inch, "Precio Venta")
        c.drawString(5.5*inch, height - 2*inch, "Venta S/")

        y = height - 2.3*inch
        total_cantidad = 0
        total_soles = 0

        for fecha, cantidad, precio, venta in datos:
            c.setFont("Helvetica", 10)
            c.drawString(1*inch, y, fecha.strftime("%Y-%m-%d"))
            c.drawRightString(3*inch, y, f"{cantidad:.2f}")
            c.drawRightString(4.8*inch, y, f"{precio:.2f}")
            c.drawRightString(6.5*inch, y, f"{venta:.2f}")
            y -= 0.25*inch
            total_cantidad += cantidad
            total_soles += venta

            if y < 1*inch:
                c.showPage()
                y = height - 1*inch

        # Totales
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1*inch, y - 0.2*inch, "TOTAL")
        c.drawRightString(3*inch, y - 0.2*inch, f"{total_cantidad:.2f}")
        c.drawRightString(6.5*inch, y - 0.2*inch, f"{total_soles:.2f}")

        c.save()
        print(f"✅ Reporte generado correctamente: {archivo_pdf}")

    except Exception as e:
        print(f"❌ Error al generar el reporte: {e}")

# Llamada directa
if __name__ == "__main__":
    generar_reporte_producto_detallado(
        producto='GLP',
        estacion_id=1,
        fecha_inicio='2025-05-01',
        fecha_fin='2025-05-20'
    )
