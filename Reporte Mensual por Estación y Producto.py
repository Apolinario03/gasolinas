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

def generar_reporte_mensual_por_estacion(anio, mes):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Nueva consulta: total galones y total soles
        cursor.execute("""
            SELECT e.nombre AS estacion, p.nombre AS producto,
                   SUM(i.cantidad) AS total_galones,
                   SUM(i.venta_soles) AS total_soles
            FROM inventario i
            JOIN productos p ON i.productoid = p.id
            JOIN estacion e ON i.estacionid = e.id
            WHERE YEAR(i.fecha) = %s AND MONTH(i.fecha) = %s
            GROUP BY e.nombre, p.nombre
            ORDER BY e.nombre, p.nombre;
        """, (anio, mes))

        datos = cursor.fetchall()

        if not datos:
            print(f"⚠️ No se encontraron datos para {anio}-{mes:02d}.")
            return

        c = canvas.Canvas(f"reporte_mensual_estaciones_{anio}_{mes:02d}.pdf", pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, f"Reporte Mensual por Estación y Producto - {anio}-{mes:02d}")

        # Encabezado
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.6*inch, height - 1.5*inch, "Estación")
        c.drawString(2.8*inch, height - 1.5*inch, "Producto")
        c.drawString(4.5*inch, height - 1.5*inch, "Galones")
        c.drawString(6.0*inch, height - 1.5*inch, "Total S/.")

        y = height - 1.8*inch
        c.setFont("Helvetica", 10)

        for estacion, producto, total_galones, total_soles in datos:
            if y < 1*inch:
                c.showPage()
                y = height - 1*inch
                c.setFont("Helvetica-Bold", 16)
                c.drawString(1*inch, height - 1*inch, f"Reporte Mensual por Estación y Producto - {anio}-{mes:02d}")
                c.setFont("Helvetica-Bold", 12)
                c.drawString(0.6*inch, height - 1.5*inch, "Estación")
                c.drawString(2.8*inch, height - 1.5*inch, "Producto")
                c.drawString(4.5*inch, height - 1.5*inch, "Galones")
                c.drawString(6.0*inch, height - 1.5*inch, "Total S/.")
                y -= 0.3*inch
                c.setFont("Helvetica", 10)

            c.drawString(0.6*inch, y, estacion)
            c.drawString(2.8*inch, y, producto)
            c.drawRightString(5.8*inch, y, f"{total_galones:.2f}")
            c.drawRightString(7.5*inch, y, f"S/. {total_soles:.2f}")
            y -= 0.3*inch

        c.save()
        print(f"\n✅ PDF generado: reporte_mensual_estaciones_{anio}_{mes:02d}.pdf")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error generando el reporte: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    anio = int(input("📅 Ingrese el año del reporte (ej. 2025): "))
    mes = int(input("🗓️  Ingrese el número del mes (1-12): "))
    generar_reporte_mensual_por_estacion(anio, mes)



