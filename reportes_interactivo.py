import mysql.connector
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sistemas321',
    'database': 'gasolinas1',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Clase PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, self.title, ln=True, align='C')
        self.ln(5)

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 11)
        self.cell(0, 10, label, ln=True)
        self.ln(2)

    def chapter_body(self, df: pd.DataFrame):
        self.set_font('Arial', '', 10)
        if df.empty:
            self.cell(0, 10, 'No hay datos disponibles.', ln=True)
            return
        col_width = self.w / (len(df.columns) + 1)
        for col in df.columns:
            self.cell(col_width, 10, str(col), border=1)
        self.ln()
        for i in range(len(df)):
            for item in df.iloc[i]:
                self.cell(col_width, 10, str(item), border=1)
            self.ln()
        self.ln(5)

# Función para consultar base de datos
def get_df(query, params=None):
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

# Generador de PDF (corregido con .title antes de add_page)
def generar_pdf(nombre_archivo, titulo, secciones):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.title = titulo  # Asignar antes de llamar header()
    pdf.add_page()
    for subtitulo, df in secciones:
        pdf.chapter_title(subtitulo)
        pdf.chapter_body(df)
    pdf.output(nombre_archivo)
    print(f"✅ PDF generado: {nombre_archivo}\n")

# Reportes
def reporte_diario():
    estacion = input("Nombre de la estación: ")
    fecha_str = input("Fecha (YYYY-MM-DD): ")
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        print("⚠️ Fecha inválida.")
        return

    query = """
        SELECT p.nombre AS producto, i.cantidad, i.fecha
        FROM inventario i
        JOIN productos p ON i.productoid = p.id
        JOIN estacion e ON i.estacionid = e.id
        WHERE e.nombre = %s AND i.fecha = %s
    """
    df = get_df(query, (estacion, fecha))
    generar_pdf(
        f"reporte_diario_{estacion}_{fecha}.pdf",
        f"Reporte Diario - {estacion} - {fecha}",
        [(f"Inventario del {fecha}", df)]
    )

def reporte_mensual():
    estacion = input("Nombre de la estación: ")
    anio = int(input("Año (YYYY): "))
    mes = int(input("Mes (1-12): "))

    query = """
        SELECT p.nombre AS producto, SUM(i.cantidad) AS total_cantidad
        FROM inventario i
        JOIN productos p ON i.productoid = p.id
        JOIN estacion e ON i.estacionid = e.id
        WHERE e.nombre = %s AND YEAR(i.fecha) = %s AND MONTH(i.fecha) = %s
        GROUP BY p.nombre
    """
    df = get_df(query, (estacion, anio, mes))
    generar_pdf(
        f"reporte_mensual_{estacion}_{anio}_{mes}.pdf",
        f"Reporte Mensual - {estacion} - {anio}-{mes:02d}",
        [(f"Totales del mes", df)]
    )

def reporte_por_producto():
    query = """
        SELECT e.nombre AS estacion, p.nombre AS producto, SUM(i.cantidad) AS total
        FROM inventario i
        JOIN productos p ON i.productoid = p.id
        JOIN estacion e ON i.estacionid = e.id
        GROUP BY e.nombre, p.nombre
    """
    df = get_df(query)
    generar_pdf(
        "reporte_total_productos.pdf",
        "Totales por Producto y Estación",
        [("Resumen General", df)]
    )

def reporte_general():
    anio = int(input("Año (YYYY): "))
    mes_opc = input("¿Quieres filtrar por mes? (s/n): ").strip().lower()

    if mes_opc == 's':
        mes = int(input("Mes (1-12): "))
        query = """
            SELECT e.nombre AS estacion, i.fecha, SUM(i.cantidad) AS total_combustible
            FROM inventario i
            JOIN estacion e ON i.estacionid = e.id
            WHERE YEAR(i.fecha) = %s AND MONTH(i.fecha) = %s
            GROUP BY e.nombre, i.fecha
            ORDER BY i.fecha
        """
        df = get_df(query, (anio, mes))
        titulo = f"Resumen de Estaciones - {anio}-{mes:02d}"
        archivo = f"reporte_estaciones_resumen_{anio}_{mes}.pdf"
    else:
        query = """
            SELECT e.nombre AS estacion, i.fecha, SUM(i.cantidad) AS total_combustible
            FROM inventario i
            JOIN estacion e ON i.estacionid = e.id
            WHERE YEAR(i.fecha) = %s
            GROUP BY e.nombre, i.fecha
            ORDER BY i.fecha
        """
        df = get_df(query, (anio,))
        titulo = f"Resumen de Estaciones - {anio}"
        archivo = f"reporte_estaciones_resumen_{anio}.pdf"

    generar_pdf(archivo, titulo, [("Resumen Total por Día", df)])

# Menú principal
def menu():
    while True:
        print("\n=== GENERADOR DE REPORTES ===")
        print("1. Reporte diario por estación")
        print("2. Reporte mensual por estación")
        print("3. Reporte total por producto")
        print("4. Reporte resumen de todas las estaciones")
        print("5. Salir")
        opcion = input("Elige una opción (1-5): ")

        if opcion == "1":
            reporte_diario()
        elif opcion == "2":
            reporte_mensual()
        elif opcion == "3":
            reporte_por_producto()
        elif opcion == "4":
            reporte_general()
        elif opcion == "5":
            print("👋 Saliendo del generador.")
            break
        else:
            print("⚠️ Opción inválida. Intenta de nuevo.")

# Ejecutar
if __name__ == "__main__":
    menu()
