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

def generar_reporte_producto(nombre_producto):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Consulta para un solo producto
        cursor.execute("""
            SELECT i.fecha, SUM(i.cantidad) AS total_litros
            FROM inventario i
            JOIN productos p ON i.productoid = p.id
            WHERE p.nombre = %s
            GROUP BY i.fecha
            ORDER BY i.fecha;
        """, (nombre_producto,))
        datos = cursor.fetchall()

        if not datos:
            print(f"⚠️ No se encontraron datos para el producto '{nombre_producto}'.")
            return

        # Crear PDF
        c = canvas.Canvas(f"reporte_{nombre_producto}.pdf", pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, f"Reporte de Inventario para Producto: {nombre_producto}")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(1*inch, height - 1.5*inch, "Fecha")
        c.drawString(3*inch, height - 1.5*inch, "Total Litros")

        y = height - 1.8*inch
        c.setFont("Helvetica", 10)

        for fecha, total_litros in datos:
            if y < 1*inch:
                c.showPage()
                y = height - 1*inch
                c.setFont("Helvetica-Bold", 16)
                c.drawString(1*inch, height - 1*inch, f"Reporte de Inventario para Producto: {nombre_producto}")
                c.setFont("Helvetica-Bold", 12)
                c.drawString(1*inch, height - 1.5*inch, "Fecha")
                c.drawString(3*inch, height - 1.5*inch, "Total Litros")
                y -= 0.3*inch
                c.setFont("Helvetica", 10)

            c.drawString(1*inch, y, fecha.strftime("%Y-%m-%d"))
            c.drawRightString(4*inch, y, f"{total_litros:.2f}")
            y -= 0.3*inch

        c.save()
        print(f"✅ Reporte PDF generado: reporte_{nombre_producto}.pdf")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")

# Ejemplo de uso:
generar_reporte_producto("PREMIUM")
