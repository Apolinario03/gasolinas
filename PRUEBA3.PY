import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import os
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

# Configuración de rutas
RUTA_BASE_EXCEL = r'C:\Users\sistemas\Desktop\gasolinas'

# Crear la base de datos y las tablas
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

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Base de datos y tablas preparadas correctamente.")
    except mysql.connector.Error as err:
        print(f"❌ Error al crear la base de datos: {err}")

# Obtener todas las estaciones de la base de datos
def obtener_estaciones():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nombre FROM estacion")
        estaciones = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return estaciones
    except mysql.connector.Error as err:
        print(f"❌ Error al obtener estaciones: {err}")
        return []

# Cargar inventario para una estación específica
def cargar_inventario_estacion(estacion_id, nombre_estacion):
    try:
        # Construir ruta del archivo Excel para esta estación
        archivo_excel = os.path.join(RUTA_BASE_EXCEL, f"{estacion_id}.xlsx")
        
        # Verificar si existe el archivo
        if not os.path.exists(archivo_excel):
            print(f"⚠️ Archivo no encontrado para estación '{nombre_estacion}': {archivo_excel}")
            return False
        
        print(f"📊 Procesando estación: {nombre_estacion} (ID: {estacion_id})")
        print(f"📁 Archivo: {archivo_excel}")
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Leer el archivo Excel
        xls = pd.ExcelFile(archivo_excel)
        registros_procesados = 0
        
        for nombre_hoja in xls.sheet_names:
            print(f"  📄 Procesando hoja: {nombre_hoja}")
            
            try:
                # Leer datos de la hoja
                df = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=5, nrows=8,
                                   usecols=[0, 14], header=None)
                df.columns = ['producto', 'cantidad']
                df['FECHA'] = pd.to_datetime(nombre_hoja, dayfirst=True, errors='coerce')

                # Convertir a numérico, descartar no válidos
                df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
                df = df.dropna(subset=['cantidad', 'producto', 'FECHA'])

                # Procesar cada fila de datos
                for _, fila in df.iterrows():
                    producto = str(fila['producto']).strip()
                    cantidad = float(fila['cantidad'])
                    fecha = fila['FECHA'].date()

                    # Verificar si el producto existe
                    cursor.execute("SELECT id FROM productos WHERE nombre = %s", (producto,))
                    prod = cursor.fetchone()
                    if prod:
                        producto_id = prod[0]
                    else:
                        # Crear nuevo producto
                        cursor.execute("INSERT INTO productos (nombre, descripcion) VALUES (%s, '')", (producto,))
                        producto_id = cursor.lastrowid
                        print(f"    ➕ Nuevo producto creado: {producto}")

                    # Insertar registro de inventario
                    cursor.execute("""
                        INSERT INTO inventario (productoid, estacionid, fecha, cantidad)
                        VALUES (%s, %s, %s, %s)
                    """, (producto_id, estacion_id, fecha, cantidad))
                    
                    registros_procesados += 1

            except Exception as e:
                print(f"    ❌ Error procesando hoja '{nombre_hoja}': {e}")
                continue

        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"  ✅ Estación procesada exitosamente. Registros: {registros_procesados}")
        return True
        
    except Exception as e:
        print(f"❌ Error procesando estación '{nombre_estacion}': {e}")
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
        return False

# Función principal para procesar todas las estaciones
def procesar_todas_las_estaciones():
    print("🚀 Iniciando procesamiento de todas las estaciones...")
    
    # Obtener lista de estaciones
    estaciones = obtener_estaciones()
    
    if not estaciones:
        print("❌ No se encontraron estaciones en la base de datos.")
        return
    
    print(f"📋 Se encontraron {len(estaciones)} estaciones para procesar.")
    
    # Contadores de resultados
    exitosas = 0
    fallidas = 0
    
    # Procesar cada estación
    for estacion_id, nombre_estacion in estaciones:
        print(f"\n{'='*60}")
        resultado = cargar_inventario_estacion(estacion_id, nombre_estacion)
        
        if resultado:
            exitosas += 1
        else:
            fallidas += 1
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN DEL PROCESAMIENTO:")
    print(f"✅ Estaciones procesadas exitosamente: {exitosas}")
    print(f"❌ Estaciones con errores: {fallidas}")
    print(f"📈 Total de estaciones: {len(estaciones)}")
    print("🏁 Procesamiento completado.")

# Función para agregar estaciones de ejemplo (opcional)
def agregar_estaciones_ejemplo():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        estaciones_ejemplo = [
            (1, 'La Rinconada', 'Av. Principal s/n', 'Gasolinera'),
            (2, 'America Soler', 'Calle Soler 123', 'Gasolinera'),
            (3, 'Centro Norte', 'Av. Norte 456', 'Gasolinera'),
            (4, 'Plaza Mayor', 'Plaza Principal', 'Gasolinera')
        ]
        
        for estacion_id, nombre, direccion, tipo in estaciones_ejemplo:
            cursor.execute("""
                INSERT IGNORE INTO estacion (id, nombre, direccion, tipoestacion)
                VALUES (%s, %s, %s, %s)
            """, (estacion_id, nombre, direccion, tipo))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Estaciones de ejemplo agregadas.")
        
    except mysql.connector.Error as err:
        print(f"❌ Error agregando estaciones: {err}")

# Ejecutar el programa
if __name__ == "__main__":
    print("🔧 Preparando base de datos...")
    crear_esquema()
    
    # Descomentar la siguiente línea si necesitas agregar estaciones de ejemplo
    # agregar_estaciones_ejemplo()
    
    print("\n🔄 Iniciando procesamiento...")
    procesar_todas_las_estaciones()