import mysql.connector
import pandas as pd
from fpdf import FPDF

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
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Reporte Mensual de Ventas por Estación y Producto', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

def generar_pdf(data, archivo='reporte_mensual.pdf'):
    pdf = PDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    columnas = ['Estación', 'Producto', 'Mes', 'Galones', 'Total S/']
    anchos = [50, 40, 30, 30, 40]

    for i, col in enumerate(columnas):
        pdf.cell(anchos[i], 10, col, border=1, align='C')
    pdf.ln()

    for _, row in data.iterrows():
        pdf.cell(anchos[0], 10, row['estacion'], border=1)
        pdf.cell(anchos[1], 10, row['producto'], border=1)
        pdf.cell(anchos[2], 10, row['mes'], border=1)
        pdf.cell(anchos[3], 10, f"{row['total_galones']:.2f}", border=1, align='R')
        pdf.cell(anchos[4], 10, f"{row['total_ventas']:.2f}", border=1, align='R')
        pdf.ln()

    pdf.output(archivo)
    print(f"\n✅ PDF generado: {archivo}")

def main():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        query = """
            SELECT * FROM vista_ventas_mensuales_por_estacion
            ORDER BY mes DESC, estacion, producto
        """
        df = pd.read_sql(query, conn)
        conn.close()

        if not df.empty:
            generar_pdf(df)
        else:
            print("⚠️ No hay datos disponibles en la vista.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
