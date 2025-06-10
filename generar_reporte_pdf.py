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

# Función PDF simple
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
        # Encabezados
        col_width = self.w / (len(df.columns) + 1)
        for col in df.columns:
            self.cell(col_width, 10, str(col), border=1)
        self.ln()
        # Filas
        for i in range(len(df)):
            for item in df.iloc[i]:
                self.cell(col_width, 10, str(item), border=1)
            self.ln()
        self.ln(5)

# Función de conexión
def get_df(query, params=None):
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

# Generar PDF con reporte
def generar_pdf(nombre_archivo, titulo, secciones):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.title = titulo
    for subtitulo, df in secciones:
        pdf.chapter_title(subtitulo)
        pdf.chapter_body(df)
    pdf.output(nombre_archivo)
    print(f"✅ PDF generado: {nombre_archivo}")

# Reporte diario
def reporte_diario(estacion, fecha_str):
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
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

# Reporte mensual
def reporte_mensual(estacion, anio, mes):
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

# Reporte por producto (total general por estación)
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

# Reporte general de las tres estaciones
def reporte_general_resumido(anio, mes=None):
    if mes:
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

# ============================
# EJEMPLOS DE USO
# ============================

# reporte_diario("America Soler", "2025-05-10")
# reporte_mensual("La Rinconada", 2025, 5)
# reporte_por_producto()
# reporte_general_resumido(2025, 5)
