import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import os

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sistemas321',
    'database': 'gasolinas1',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Diccionario de estaciones (nombre de archivo clave -> nombre real en BD y su ID esperado)
ESTACIONES = {
    'rinconada': {'nombre': 'La Rinconada', 'id': 1},
    'america': {'nombre': 'America Soler', 'id': 3},
    'porvenir': {'nombre': 'El Porvenir', 'id': 4}
}

# Carpeta donde están los archivos Excel
CARPETA_EXCEL = r'C:\Users\sistemas\Desktop\gasolinas'

# Crear la base de datos y las tablas si no existen
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
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT
            );
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
            );
        """)

        # Insertar estaciones si no existen
        for datos in ESTACIONES.values():
            cursor.execute("SELECT id FROM estacion WHERE nombre = %s", (datos['nombre'],))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO estacion (id, nombre, direccion, tipoestacion)
                    VALUES (%s, %s, %s, %s)
                """, (datos['id'], datos['nombre'], 'Dirección genérica', 'Gasolinera'))

        conn.commit()
        print("✅ Base de datos y tablas preparadas correctamente.")
    except mysql.connector.Error as err:
        print(f"❌ Error al crear la base de datos: {err}")
    finally:
        cursor.close()
        conn.close()

# Cargar los archivos Excel por estación
def cargar_inventarios():
    archivos = [f for f in os.listdir(CARPETA_EXCEL) if f.lower().endswith('.xlsx')]

    for archivo in archivos:
        ruta_completa = os.path.join(CARPETA_EXCEL, archivo)
        nombre_archivo = archivo.lower().replace(" ", "")  # 🔧 Eliminar espacios

        # Determinar estación por nombre de archivo
        estacion_encontrada = None
        for clave in ESTACIONES:
            if clave in nombre_archivo:
                estacion_encontrada = ESTACIONES[clave]
                print(f"🔍 Detectado archivo: {archivo} -> clave detectada: {clave}")
                break

        if not estacion_encontrada:
            print(f"⚠️ Archivo {archivo} no coincide con ninguna estación conocida. Saltando.")
            continue

        print(f"📂 Procesando archivo: {archivo} para estación: {estacion_encontrada['nombre']}")

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            estacion_id = estacion_encontrada['id']

            xls = pd.ExcelFile(ruta_completa)
            for nombre_hoja in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=5, nrows=5,
                                   usecols=[0, 13], header=None)
                df.columns = ['producto', 'cantidad']
                df['FECHA'] = pd.to_datetime(nombre_hoja, dayfirst=True, errors='coerce')
                df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
                df = df.dropna(subset=['cantidad', 'producto', 'FECHA' ])

                for _, fila in df.iterrows():
                    producto = str(fila['producto']).strip()
                    cantidad = float(fila['cantidad'])
                    fecha = fila['FECHA'].date()

                    # Obtener o insertar producto
                    cursor.execute("SELECT id FROM productos WHERE nombre = %s", (producto,))
                    prod = cursor.fetchone()
                    if prod:
                        producto_id = prod[0]
                    else:
                        cursor.execute("INSERT INTO productos (nombre, descripcion) VALUES (%s, '')", (producto,))
                        producto_id = cursor.lastrowid

                    # Insertar inventario
                    cursor.execute("""
                        INSERT INTO inventario (productoid, estacionid, fecha, cantidad)
                        VALUES (%s, %s, %s, %s)
                    """, (producto_id, estacion_id, fecha, cantidad))

            conn.commit()
            print(f"✅ Datos cargados para {estacion_encontrada['nombre']}")
        except Exception as e:
            print(f"❌ Error procesando {archivo}: {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

# Ejecutar todo
crear_esquema()
cargar_inventarios()
