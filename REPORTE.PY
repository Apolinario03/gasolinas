import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sistemas321',
    'database': 'gasolinas1',
    'charset': 'utf8mb4',  # Importante para evitar errores de codificación
    'collation': 'utf8mb4_general_ci'
}

ARCHIVO_EXCEL = r'C:\Users\sistemas\Desktop\gasolinas\INVENTARIO_MARZO_2020.xlsx'

def crear_esquema():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS gasolinas1 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
        conn.database = 'gasolinas1'

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estacion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                direccion VARCHAR(255),
                tipoestacion VARCHAR(50)
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                productoid INT,
                estacionid INT,
                fecha DATE,
                cantidad DECIMAL(10,2),
                FOREIGN KEY (productoid) REFERENCES productos(id),
                FOREIGN KEY (estacionid) REFERENCES estacion(id)
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
        """)

        cursor.execute("SELECT id FROM estacion WHERE nombre = 'La Rinconada'")
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO estacion (nombre, direccion, tipoestacion)
                VALUES ('La Rinconada', 'Av. Principal s/n', 'Gasolinera')
            """)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Base de datos y tablas preparadas correctamente.")
    except mysql.connector.Error as err:
        print(f"❌ Error al crear la base de datos: {err}")

def cargar_inventario():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM estacion WHERE nombre = 'La Rinconada'")
        estacion_id = cursor.fetchone()[0]

        xls = pd.ExcelFile(ARCHIVO_EXCEL)
        for nombre_hoja in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=5, nrows=8,
                               usecols=[0, 14], header=None)
            df.columns = ['producto', 'cantidad']
            df['FECHA'] = pd.to_datetime(nombre_hoja, dayfirst=True, errors='coerce')
            df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
            df = df.dropna(subset=['cantidad', 'producto', 'FECHA'])

            for _, fila in df.iterrows():
                producto = str(fila['producto']).strip()
                cantidad = float(fila['cantidad'])
                fecha = fila['FECHA'].date()

                cursor.execute("SELECT id FROM productos WHERE nombre = %s", (producto,))
                prod = cursor.fetchone()
                if prod:
                    producto_id = prod[0]
                else:
                    cursor.execute("INSERT INTO productos (nombre, descripcion) VALUES (%s, '')", (producto,))
                    producto_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO inventario (productoid, estacionid, fecha, cantidad)
                    VALUES (%s, %s, %s, %s)
                """, (producto_id, estacion_id, fecha, cantidad))

        conn.commit()
        print("✅ Inventario cargado correctamente.")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def generar_reporte_resumen():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.nombre AS producto, i.fecha, SUM(i.cantidad) AS total_litros
            FROM inventario i
            JOIN productos p ON i.productoid = p.id
            GROUP BY p.nombre, i.fecha
            ORDER BY i.fecha, p.nombre;
        """)

        print("\n📋 RESUMEN DE INVENTARIO POR PRODUCTO Y FECHA:")
        print("----------------------------------------------------")
        for (producto, fecha, total_litros) in cursor.fetchall():
            print(f"{fecha} | {producto:<20} | {total_litros:.2f} litros")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"❌ Error al generar el reporte: {err}")

# Ejecutar todo
crear_esquema()
cargar_inventario()
generar_reporte_resumen()
