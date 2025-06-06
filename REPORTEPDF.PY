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

def generar_reporte_pdf():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.nombre AS producto, i.fecha, SUM(i.cantidad) AS total_litros
            FROM inventario i
            JOIN productos p ON i.productoid = p.id
            GROUP BY p.nombre, i.fecha
            ORDER BY p.nombre, i.fecha;
        """)
        datos = cursor.fetchall()

        c = canvas.Canvas("reporte_inventario.pdf", pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, "Reporte de Inventario por Producto y Fecha")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(1*inch, height - 1.5*inch, "Producto")
        c.drawString(3*inch, height - 1.5*inch, "Fecha")
        c.drawString(5*inch, height - 1.5*inch, "Total Litros")

        y = height - 1.8*inch
        c.setFont("Helvetica", 10)

        for producto, fecha, total_litros in datos:
            if y < 1*inch:
                c.showPage()
                y = height - 1*inch
                c.setFont("Helvetica-Bold", 12)
                c.drawString(1*inch, height - 1*inch, "Reporte de Inventario por Producto y Fecha")
                c.drawString(1*inch, height - 1.5*inch, "Producto")
                c.drawString(3*inch, height - 1.5*inch, "Fecha")
                c.drawString(5*inch, height - 1.5*inch, "Total Litros")
                y -= 0.3*inch
                c.setFont("Helvetica", 10)

            c.drawString(1*inch, y, str(producto))
            c.drawString(3*inch, y, fecha.strftime("%Y-%m-%d"))
            c.drawRightString(6*inch, y, f"{total_litros:.2f}")
            y -= 0.3*inch

        c.save()
        print("✅ Reporte PDF generado: reporte_inventario.pdf")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")

# Llama esta función en tu flujo principal cuando quieras generar el reporte
generar_reporte_pdf()

