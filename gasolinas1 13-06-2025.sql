-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         11.6.2-MariaDB-log - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para gasolinas1
CREATE DATABASE IF NOT EXISTS `gasolinas1` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `gasolinas1`;

-- Volcando estructura para tabla gasolinas1.archivos_procesados
CREATE TABLE IF NOT EXISTS `archivos_procesados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_archivo` varchar(255) DEFAULT NULL,
  `hash` varchar(64) DEFAULT NULL,
  `fecha_procesado` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gasolinas1.archivos_procesados: ~0 rows (aproximadamente)

-- Volcando estructura para tabla gasolinas1.estacion
CREATE TABLE IF NOT EXISTS `estacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `tipoestacion` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gasolinas1.estacion: ~4 rows (aproximadamente)
INSERT INTO `estacion` (`id`, `nombre`, `direccion`, `tipoestacion`) VALUES
	(1, 'La Rinconada', 'Av. Principal s/n', 'Lima'),
	(2, 'America Soler', 'Av. Bolognesi s/n', 'trujillo'),
	(3, 'America Soler', 'Av. bolognesi s/n', 'trujillo'),
	(4, 'El Porvenir', 'Av. porvenir s/n', 'trujillo');

-- Volcando estructura para tabla gasolinas1.inventario
CREATE TABLE IF NOT EXISTS `inventario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productoid` int(11) NOT NULL,
  `estacionid` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `precio_venta` decimal(10,3) DEFAULT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `venta_soles` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `productoid` (`productoid`),
  KEY `idx_estacionid` (`estacionid`),
  CONSTRAINT `fk_estacionid_final` FOREIGN KEY (`estacionid`) REFERENCES `estacion` (`id`),
  CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`productoid`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3352 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gasolinas1.inventario: ~16 rows (aproximadamente)
INSERT INTO `inventario` (`id`, `productoid`, `estacionid`, `fecha`, `precio_venta`, `cantidad`, `venta_soles`) VALUES
	(3336, 1, 1, '2025-05-01', 4.996, 576.90, 2882.17),
	(3337, 2, 1, '2025-05-01', 12.780, 49.48, 632.40),
	(3338, 3, 1, '2025-05-01', 12.580, 7.62, 95.80),
	(3339, 4, 1, '2025-05-01', 12.180, 371.56, 4525.66),
	(3340, 1, 1, '2025-05-02', 4.996, 536.06, 2678.14),
	(3341, 2, 1, '2025-05-02', 12.780, 65.49, 837.01),
	(3342, 3, 1, '2025-05-02', 12.580, 8.35, 105.00),
	(3343, 4, 1, '2025-05-02', 12.180, 366.57, 4464.77),
	(3344, 1, 3, '2025-05-01', 6.990, 185.78, 1298.58),
	(3345, 2, 3, '2025-05-01', 15.750, 61.49, 968.51),
	(3346, 3, 3, '2025-05-01', 13.990, 65.44, 915.54),
	(3347, 4, 3, '2025-05-01', 13.990, 134.97, 1888.18),
	(3348, 1, 3, '2025-05-02', 6.990, 236.02, 1649.77),
	(3349, 2, 3, '2025-05-02', 15.750, 85.15, 1341.12),
	(3350, 3, 3, '2025-05-02', 13.990, 132.80, 1857.94),
	(3351, 4, 3, '2025-05-02', 13.990, 251.49, 3518.37);

-- Volcando estructura para tabla gasolinas1.precio
CREATE TABLE IF NOT EXISTS `precio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productoid` int(11) NOT NULL,
  `estacionid` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `fechacambio` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `productoid` (`productoid`),
  KEY `estacionid` (`estacionid`),
  CONSTRAINT `precio_ibfk_1` FOREIGN KEY (`productoid`) REFERENCES `productos` (`id`),
  CONSTRAINT `precio_ibfk_2` FOREIGN KEY (`estacionid`) REFERENCES `estacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gasolinas1.precio: ~0 rows (aproximadamente)

-- Volcando estructura para tabla gasolinas1.productos
CREATE TABLE IF NOT EXISTS `productos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gasolinas1.productos: ~4 rows (aproximadamente)
INSERT INTO `productos` (`id`, `nombre`, `descripcion`) VALUES
	(1, 'GLP', NULL),
	(2, 'PREMIUM', NULL),
	(3, 'REGULAR', NULL),
	(4, 'DB5', NULL);

-- Volcando estructura para tabla gasolinas1.ventas
CREATE TABLE IF NOT EXISTS `ventas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productoid` int(11) NOT NULL,
  `estacionid` int(11) NOT NULL,
  `dia_venta` date NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `productoid` (`productoid`),
  KEY `estacionid` (`estacionid`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`productoid`) REFERENCES `productos` (`id`),
  CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`estacionid`) REFERENCES `estacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gasolinas1.ventas: ~0 rows (aproximadamente)

-- Volcando estructura para vista gasolinas1.vista_archivos_procesados
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `vista_archivos_procesados` (
	`nombre_archivo` VARCHAR(1) NULL COLLATE 'utf8mb4_general_ci',
	`hash` VARCHAR(1) NULL COLLATE 'utf8mb4_general_ci',
	`fecha` DATE NULL,
	`hora` TIME NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gasolinas1.vista_precios_promedio
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `vista_precios_promedio` (
	`estacion` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`producto` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`precio_promedio` DECIMAL(11,3) NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gasolinas1.vista_ranking_estaciones
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `vista_ranking_estaciones` (
	`estacion` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`total_ventas` DECIMAL(32,2) NULL,
	`total_galones` DECIMAL(32,2) NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gasolinas1.vista_resumen_diario
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `vista_resumen_diario` (
	`estacion` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`producto` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`fecha` DATE NOT NULL,
	`total_galones` DECIMAL(32,2) NULL,
	`total_soles` DECIMAL(32,2) NULL,
	`precio_promedio` DECIMAL(14,7) NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gasolinas1.vista_ventas_mensuales_por_estacion
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `vista_ventas_mensuales_por_estacion` (
	`estacion` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`producto` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`mes` VARCHAR(1) NULL COLLATE 'utf8mb4_uca1400_ai_ci',
	`total_galones` DECIMAL(32,2) NULL,
	`total_ventas` DECIMAL(32,2) NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gasolinas1.vista_ventas_por_producto
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `vista_ventas_por_producto` (
	`producto` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`total_galones` DECIMAL(32,2) NULL,
	`total_ventas` DECIMAL(32,2) NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gasolinas1.vista_ventas_por_producto_estacion
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `vista_ventas_por_producto_estacion` (
	`estacion` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`producto` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`total_galones` DECIMAL(32,2) NULL,
	`total_ventas` DECIMAL(32,2) NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gasolinas1.vista_ventas_por_producto_estacion_fecha
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `vista_ventas_por_producto_estacion_fecha` (
	`estacion` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`producto` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_general_ci',
	`fecha` DATE NOT NULL,
	`total_galones` DECIMAL(32,2) NULL,
	`total_ventas` DECIMAL(32,2) NULL
) ENGINE=MyISAM;

-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `vista_archivos_procesados`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vista_archivos_procesados` AS SELECT 
    nombre_archivo,
    hash,
    DATE(fecha_procesado) AS fecha,
    TIME(fecha_procesado) AS hora
FROM archivos_procesados
ORDER BY fecha_procesado DESC ;

-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `vista_precios_promedio`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vista_precios_promedio` AS SELECT 
    e.nombre AS estacion,
    p.nombre AS producto,
    ROUND(AVG(i.precio_venta), 3) AS precio_promedio
FROM inventario i
JOIN productos p ON i.productoid = p.id
JOIN estacion e ON i.estacionid = e.id
GROUP BY e.nombre, p.nombre ;

-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `vista_ranking_estaciones`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vista_ranking_estaciones` AS SELECT 
    e.nombre AS estacion,
    SUM(i.venta_soles) AS total_ventas,
    SUM(i.cantidad) AS total_galones
FROM inventario i
JOIN estacion e ON i.estacionid = e.id
GROUP BY e.nombre
ORDER BY total_ventas DESC ;

-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `vista_resumen_diario`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vista_resumen_diario` AS SELECT 
    e.nombre AS estacion,
    p.nombre AS producto,
    i.fecha,
    SUM(i.cantidad) AS total_galones,
    SUM(i.venta_soles) AS total_soles,
    AVG(i.precio_venta) AS precio_promedio
FROM inventario i
JOIN productos p ON i.productoid = p.id
JOIN estacion e ON i.estacionid = e.id
GROUP BY e.nombre, p.nombre, i.fecha ;

-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `vista_ventas_mensuales_por_estacion`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vista_ventas_mensuales_por_estacion` AS SELECT 
    e.nombre AS estacion,
    p.nombre AS producto,
    DATE_FORMAT(i.fecha, '%Y-%m') AS mes,  -- Formato AAAA-MM
    SUM(i.cantidad) AS total_galones,
    SUM(i.venta_soles) AS total_ventas
FROM inventario i
JOIN productos p ON i.productoid = p.id
JOIN estacion e ON i.estacionid = e.id
GROUP BY e.nombre, p.nombre, mes
ORDER BY mes DESC, e.nombre, p.nombre ;

-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `vista_ventas_por_producto`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vista_ventas_por_producto` AS SELECT 
    p.nombre AS producto,
    SUM(i.cantidad) AS total_galones,
    SUM(i.venta_soles) AS total_ventas
FROM inventario i
JOIN productos p ON i.productoid = p.id
GROUP BY p.nombre ;

-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `vista_ventas_por_producto_estacion`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vista_ventas_por_producto_estacion` AS SELECT 
    e.nombre AS estacion,
    p.nombre AS producto,
    SUM(i.cantidad) AS total_galones,
    SUM(i.venta_soles) AS total_ventas
FROM inventario i
JOIN productos p ON i.productoid = p.id
JOIN estacion e ON i.estacionid = e.id
GROUP BY e.nombre, p.nombre
ORDER BY e.nombre, total_ventas DESC ;

-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `vista_ventas_por_producto_estacion_fecha`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vista_ventas_por_producto_estacion_fecha` AS SELECT 
    e.nombre AS estacion,
    p.nombre AS producto,
    i.fecha,
    SUM(i.cantidad) AS total_galones,
    SUM(i.venta_soles) AS total_ventas
FROM inventario i
JOIN productos p ON i.productoid = p.id
JOIN estacion e ON i.estacionid = e.id
GROUP BY e.nombre, p.nombre, i.fecha
ORDER BY i.fecha DESC, e.nombre, p.nombre ;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
