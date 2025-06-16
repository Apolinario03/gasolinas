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

def generar_reporte_mensual(anio, mes):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Consulta totales por producto en un mes y año específicos
        cursor.execute("""
            SELECT p.nombre, SUM(i.cantidad) AS total_litros
            FROM inventario i
            JOIN productos p ON i.productoid = p.id
            WHERE YEAR(i.fecha) = %s AND MONTH(i.fecha) = %s
            GROUP BY p.nombre
            ORDER BY p.nombre;
        """, (anio, mes))
        datos = cursor.fetchall()

        if not datos:
            print(f"⚠️ No se encontraron datos para {anio}-{mes:02d}.")
            return

        c = canvas.Canvas(f"reporte_mensual_{anio}_{mes:02d}.pdf", pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, f"Reporte Mensual por Producto - {anio}-{mes:02d}")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(1*inch, height - 1.5*inch, "Producto")
        c.drawString(5*inch, height - 1.5*inch, "Total Litros")

        y = height - 1.8*inch
        c.setFont("Helvetica", 10)

        for producto, total_litros in datos:
            if y < 1*inch:
                c.showPage()
                y = height - 1*inch
                c.setFont("Helvetica-Bold", 16)
                c.drawString(1*inch, height - 1*inch, f"Reporte Mensual por Producto - {anio}-{mes:02d}")
                c.setFont("Helvetica-Bold", 12)
                c.drawString(1*inch, height - 1.5*inch, "Producto")
                c.drawString(5*inch, height - 1.5*inch, "Total Litros")
                y -= 0.3*inch
                c.setFont("Helvetica", 10)

            c.drawString(1*inch, y, producto)
            c.drawRightString(6*inch, y, f"{total_litros:.2f}")
            y -= 0.3*inch

        c.save()
        print(f"✅ Reporte PDF generado: reporte_mensual_{anio}_{mes:02d}.pdf")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")

# Ejemplo de uso:
generar_reporte_mensual(2025, 5)  # Reporte para marzo 2020
