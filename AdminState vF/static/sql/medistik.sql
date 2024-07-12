-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 23-07-2021 a las 01:23:23
-- Versión del servidor: 5.7.27-log
-- Versión de PHP: 7.3.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `medistik`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contenido`
--

CREATE TABLE `contenido` (
  `IdContenido` int(11) NOT NULL,
  `IdReporte` int(11) NOT NULL,
  `Contenedor` varchar(100) NOT NULL,
  `Articulo` varchar(100) NOT NULL,
  `Descripcion` varchar(100) NOT NULL,
  `Ubicacion` varchar(100) NOT NULL,
  `Lote` varchar(100) NOT NULL,
  `Qty` varchar(100) NOT NULL,
  `UM` varchar(100) NOT NULL,
  `Caducidad` varchar(30) NOT NULL,
  `Temperatura` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `contenido`
--

INSERT INTO `contenido` (`IdContenido`, `IdReporte`, `Contenedor`, `Articulo`, `Descripcion`, `Ubicacion`, `Lote`, `Qty`, `UM`, `Caducidad`, `Temperatura`) VALUES
(1, 76, '1276704', '004D1803', 'AR PEPTUM200', '079C', '1056858', '1', 'PI', '2050-12-31', 'Ambiente'),
(2, 76, '1277213', '007C1503', 'ARC VESSELS', 'HRS045F', '602020', '3', 'PI', '2050-12-31', 'Ambiente'),
(3, 77, '5127711', '006C3727', 'REACTIVOC/100', '9EAD86C', '22037BE00', '16', 'PI', '2021-07-06', 'Refri'),
(4, 78, '1265546', '075G2201', 'HBDSGABGAL', '9EAD084B', '21546', '15', 'PI', '2021-08-12', 'Refri');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleadoal`
--

CREATE TABLE `empleadoal` (
  `IdEmpleadoA` int(11) NOT NULL,
  `NombreUs` varchar(100) NOT NULL,
  `UsAlmacen` varchar(100) NOT NULL,
  `PuestoA` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `empleadoal`
--

INSERT INTO `empleadoal` (`IdEmpleadoA`, `NombreUs`, `UsAlmacen`, `PuestoA`, `Password`) VALUES
(1, 'BRANDON STEVE SANTELIZ', 'steve', 'Almacen', '$2b$12$2eHCCbQgazCgQ3Tj8mcsA.ZHdkhFf4CYbmrzmq4wfCnEY.V3QhfWO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleadolo`
--

CREATE TABLE `empleadolo` (
  `IdEmpleado` int(11) NOT NULL,
  `NombreT` varchar(100) COLLATE utf8_spanish_ci NOT NULL,
  `UsTrabajador` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `PuestoT` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `ClaveT` varchar(100) COLLATE utf8_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `empleadolo`
--

INSERT INTO `empleadolo` (`IdEmpleado`, `NombreT`, `UsTrabajador`, `PuestoT`, `ClaveT`) VALUES
(1, 'BRANDON STEVE', 'SteveSan', 'logistica', '$2b$12$uXQNnVu0IHhZZsa1.Bzg6uaHyEFEYKwukixfmptutyFbFAaR5aowS'),
(3, 'NANCY SANTELIZ', 'NancyTest', 'Logistica', '$2b$12$O61RSvksvYIWfTHKD6Mv3OsL3GZO0Z7yWH/WAS9s1S7DAN6gqQ3aC'),
(4, 'BRANDON STEVE SOLIS SANTELIZ', 'Steve1', 'Logistica', '$2b$12$Car4/gxfMkAkraVqi0YGeOGNVLYz0VbO0Xp9sb5p48LtolDfhO5J.'),
(5, 'NANCY SANTELIZ', 'nancy', 'Logistica', '$2b$12$KdcNSp0XpLxTWyZOTtt7FOdxElaicHyLrCwROpWPu9TMThpvJKt4u'),
(6, 'NANCY SANTELIZ', 'nancy', 'Logistica', '$2b$12$GGeQbyihGw7RV579KeSIJ.R7NiuSCN03gaf8udtXg8MY1sisVMhyu'),
(7, 'NANCY SANTELIZ', 'NANCY', 'Logistica', '$2b$12$nCor.2nt.h1s8lTLPZ9QGOg1aVrihPBCgmICqF2qHmQgeowzI8sbi');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reporte`
--

CREATE TABLE `reporte` (
  `IdReporte` int(11) NOT NULL,
  `SerClienteF` varchar(100) NOT NULL,
  `clienteF` varchar(100) NOT NULL,
  `TServicioF` varchar(100) NOT NULL,
  `DestinoF` varchar(100) NOT NULL,
  `VentanaF` varchar(100) NOT NULL,
  `FechaF` varchar(30) NOT NULL,
  `Estatus` varchar(100) NOT NULL,
  `Prioridad` varchar(100) NOT NULL,
  `Transportista` varchar(100) NOT NULL,
  `Comentarios` varchar(300) NOT NULL,
  `Termino` varchar(50) NOT NULL,
  `Revision` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `reporte`
--

INSERT INTO `reporte` (`IdReporte`, `SerClienteF`, `clienteF`, `TServicioF`, `DestinoF`, `VentanaF`, `FechaF`, `Estatus`, `Prioridad`, `Transportista`, `Comentarios`, `Termino`, `Revision`) VALUES
(76, 'steve santeliz', 'Cardinal Health', 'A-Mensajería Express', 'ACAPULCO', '6:00 am', '2021-06-29', 'Escoge una opcion ...', '1', 'Andrade', '', 'Iniciado', 'Error en delivery'),
(77, 'steve santeliz', 'Pfizer', 'B-Distribuidor Foraneo (Intercentro)', 'ACAPULCO', '6:00 am', '2021-06-29', 'Escoge una opcion ...', '3', 'Andrade', '', 'Terminado a tiempo', ''),
(78, 'steve santeliz', 'Bayer', 'B-Distribuidor Foraneo (Intercentro)', 'ACAPULCO', '6:00 am', '2021-06-29', '', '1', 'Andrade', 'Mal empacado', 'Iniciado', 'Error de empaque');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `contenido`
--
ALTER TABLE `contenido`
  ADD PRIMARY KEY (`IdContenido`),
  ADD KEY `IdReporte` (`IdReporte`);

--
-- Indices de la tabla `empleadoal`
--
ALTER TABLE `empleadoal`
  ADD PRIMARY KEY (`IdEmpleadoA`);

--
-- Indices de la tabla `empleadolo`
--
ALTER TABLE `empleadolo`
  ADD PRIMARY KEY (`IdEmpleado`);

--
-- Indices de la tabla `reporte`
--
ALTER TABLE `reporte`
  ADD PRIMARY KEY (`IdReporte`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `contenido`
--
ALTER TABLE `contenido`
  MODIFY `IdContenido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `empleadoal`
--
ALTER TABLE `empleadoal`
  MODIFY `IdEmpleadoA` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `empleadolo`
--
ALTER TABLE `empleadolo`
  MODIFY `IdEmpleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `reporte`
--
ALTER TABLE `reporte`
  MODIFY `IdReporte` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `contenido`
--
ALTER TABLE `contenido`
  ADD CONSTRAINT `contenido_ibfk_1` FOREIGN KEY (`IdReporte`) REFERENCES `reporte` (`IdReporte`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
