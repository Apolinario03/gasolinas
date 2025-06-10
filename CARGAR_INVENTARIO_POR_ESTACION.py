import pandas as pd
import mysql.connector
from datetime import datetime

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sistemas321',
    'database': 'gasolinas1',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Estación objetivo y archivo Excel
ESTACION_OBJETIVO = 'America Soler'  # Cambiar si se carga otra estación
ARCHIVO_EXCEL = r'C:\Users\sistemas\Desktop\gasolinas\INVENTARIO_AMERICA_SOLER_ MAYO 2025.xlsx'

def cargar_inventario():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Obtener id de la estación
        cursor.execute("SELECT id FROM estacion WHERE nombre = %s", (ESTACION_OBJETIVO,))
        estacion_row = cursor.fetchone()
        if not estacion_row:
            raise ValueError(f"🚫 Estación '{ESTACION_OBJETIVO}' no encontrada.")
        estacion_id = estacion_row[0]

        xls = pd.ExcelFile(ARCHIVO_EXCEL)
        for nombre_hoja in xls.sheet_names:
            try:
                fecha = datetime.strptime(f'2025-05-{nombre_hoja.zfill(2)}', '%Y-%m-%d').date()
            except Exception:
                print(f"⚠️ Hoja '{nombre_hoja}' ignorada: no es un día válido.")
                continue

            df = pd.read_excel(xls, sheet_name=nombre_hoja, header=None, skiprows=5, nrows=8)

            for i in range(df.shape[0]):  # Leer todas las filas del bloque
                producto = str(df.iloc[i, 0]).strip()
                cantidad = pd.to_numeric(df.iloc[i, 14], errors='coerce')      # VENTA GLNS (columna O)
                venta_soles = pd.to_numeric(df.iloc[i, 16], errors='coerce')   # VENTA SOLES (columna P)

                # Mostrar para depuración
                print(f"{fecha} - Producto: '{producto}', GLNS: {cantidad}, SOLES: {venta_soles}")

                if not producto or pd.isna(cantidad) or cantidad == 0:
                    continue

                # Verificar o insertar producto
                cursor.execute("SELECT id FROM productos WHERE nombre = %s", (producto,))
                prod = cursor.fetchone()
                if prod:
                    producto_id = prod[0]
                else:
                    cursor.execute("INSERT INTO productos (nombre, descripcion) VALUES (%s, '')", (producto,))
                    producto_id = cursor.lastrowid

                # Insertar en inventario con venta_soles
                cursor.execute("""
                    INSERT INTO inventario (productoid, estacionid, fecha, cantidad, venta_soles)
                    VALUES (%s, %s, %s, %s, %s)
                """, (producto_id, estacion_id, fecha, cantidad, venta_soles))

        conn.commit()
        print(f"\n✅ Inventario de '{ESTACION_OBJETIVO}' cargado correctamente.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    cargar_inventario()


