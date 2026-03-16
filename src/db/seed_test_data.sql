-- =====================================================
-- SCRIPT DE DATOS DE PRUEBA PARA TIKITUN
-- =====================================================
-- Este script llena la base de datos con datos realistas
-- para pruebas. Ejecutar DESPUES de init.sql
-- =====================================================
-- NOTA: Adaptado a los triggers y restricciones:
--   - Titulos ≤ 80 caracteres (RS2.5)
--   - Descripciones ≤ 500 caracteres (RS2.6)
--   - num_favs = 0 (los triggers lo incrementan automaticamente)
--   - Contraofertas solo de usuarios que NO son duenos del producto
--   - Usuarios eliminados se crean DESPUES de sus operaciones
--   - No hay chats reflexivos (comprador ≠ vendedor)
-- =====================================================

-- =====================================================
-- USUARIOS (15 usuarios con contrasenas conocidas)
-- =====================================================
-- NOTA: Las contrasenas cumplen requisitos (8-15 chars, mayus, minus, especiales)
-- Para login usar: usuario / contrasena en texto plano

-- Usuario: admin / Admin@123
INSERT INTO Usuario VALUES (
  'admin',
  'admin@tikitun.com',
  'Administrador Sistema',
  'Admin@123',
  40.4168,
  -3.7038,
  50.0,
  10000.00,
  5.0,
  0
);

-- Usuario: juan / Juan#2025
INSERT INTO Usuario VALUES (
  'juan',
  'juan@gmail.com',
  'Juan Garcia Perez',
  'Juan#2025',
  40.4530,
  -3.6883,
  25.0,
  350.00,
  4.7,
  0
);

-- Usuario: maria / Maria\$456
INSERT INTO Usuario VALUES (
  'maria',
  'maria@gmail.com',
  'Maria Lopez Fernandez',
  'Maria\$456',
  41.3851,
  2.1734,
  30.0,
  520.00,
  4.9,
  0
);

-- Usuario: carlos / Carlos!789
INSERT INTO Usuario VALUES (
  'carlos',
  'carlos@outlook.com',
  'Carlos Martinez Ruiz',
  'Carlos!789',
  37.3891,
  -5.9845,
  15.0,
  180.00,
  4.2,
  0
);

-- Usuario: ana / Ana@Pass1
INSERT INTO Usuario VALUES (
  'ana',
  'ana@yahoo.es',
  'Ana Sanchez Torres',
  'Ana@Pass1',
  39.4699,
  -0.3763,
  20.0,
  890.00,
  4.8,
  0
);

-- Usuario: pedro / Pedro#321
INSERT INTO Usuario VALUES (
  'pedro',
  'pedro@hotmail.com',
  'Pedro Hernandez Gomez',
  'Pedro#321',
  43.2630,
  -2.9350,
  12.0,
  75.50,
  3.9,
  0
);

-- Usuario: laura / Laura\$2025
INSERT INTO Usuario VALUES (
  'laura',
  'laura@gmail.com',
  'Laura Diaz Moreno',
  'Laura\$2025',
  36.7213,
  -4.4214,
  18.0,
  1250.00,
  4.6,
  0
);

-- Usuario: david / David!Pass
INSERT INTO Usuario VALUES (
  'david',
  'david@gmail.com',
  'David Jimenez Navarro',
  'David!Pass',
  41.6488,
  -0.8891,
  22.0,
  430.00,
  4.4,
  0
);

-- Usuario: elena / Elena@987
INSERT INTO Usuario VALUES (
  'elena',
  'elena@outlook.es',
  'Elena Romero Castro',
  'Elena@987',
  42.8782,
  -8.5448,
  35.0,
  2100.00,
  4.95,
  0
);

-- Usuario: miguel / Miguel#55
INSERT INTO Usuario VALUES (
  'miguel',
  'miguel@gmail.com',
  'Miguel Alvarez Prieto',
  'Miguel#55',
  28.4636,
  -16.2518,
  40.0,
  95.00,
  3.5,
  0
);

-- Usuario: sofia / Sofia\$123
INSERT INTO Usuario VALUES (
  'sofia',
  'sofia@icloud.com',
  'Sofia Munoz Ortega',
  'Sofia\$123',
  37.9922,
  -1.1307,
  10.0,
  780.00,
  4.3,
  0
);

-- Usuario: pablo / Pablo!2025
INSERT INTO Usuario VALUES (
  'pablo',
  'pablo@gmail.com',
  'Pablo Gutierrez Serrano',
  'Pablo!2025',
  39.8628,
  -4.0273,
  28.0,
  320.00,
  4.1,
  0
);

-- Usuario: lucia / Lucia@Pass
INSERT INTO Usuario VALUES (
  'lucia',
  'lucia@yahoo.es',
  'Lucia Vega Ramos',
  'Lucia@Pass',
  40.9701,
  -5.6635,
  16.0,
  1500.00,
  4.85,
  0
);

-- Usuario: test / Test#1234
INSERT INTO Usuario VALUES (
  'test',
  'test@test.com',
  'Usuario Test',
  'Test#1234',
  40.4168,
  -3.7038,
  100.0,
  999.99,
  4.0,
  0
);

-- Usuario para eliminar (se marca eliminado AL FINAL del script)
INSERT INTO Usuario VALUES (
  'deleted_user',
  'deleted@mail.com',
  'Usuario Eliminado',
  'Deleted@99',
  40.0,
  -3.0,
  10.0,
  0.00,
  0.0,
  0
);

-- =====================================================
-- PRODUCTOS (40+ productos variados)
-- =====================================================
-- NOTA: 
--   - Titulos ≤ 80 caracteres
--   - num_favs = 0 (los triggers lo incrementaran)
--   - promocion entre 0 y 1

-- === TECNOLOGIA ===
INSERT INTO Producto VALUES (101, 'juan', 'Tecnologia', 'iPhone 14 Pro Max 256GB', 'iPhone 14 Pro Max 256GB, color morado oscuro. Estado impecable, con caja original y todos los accesorios.', 899.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (102, 'maria', 'Tecnologia', 'MacBook Air M2 8GB 256GB SSD', 'MacBook Air con chip M2, 8GB RAM, 256GB SSD. Color medianoche. Comprado hace 6 meses.', 1050.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (103, 'carlos', 'Tecnologia', 'PlayStation 5 con 2 mandos', 'PS5 edicion disco con 2 mandos y 3 juegos. Poco uso, perfecta para gaming.', 450.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (104, 'ana', 'Tecnologia', 'Samsung Galaxy S23 Ultra 512GB', 'Galaxy S23 Ultra 512GB negro. Incluye funda y protector de pantalla.', 780.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (105, 'pedro', 'Tecnologia', 'Nintendo Switch OLED blanca', 'Switch OLED blanca con 5 juegos fisicos y funda de transporte.', 280.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (106, 'laura', 'Tecnologia', 'iPad Pro 12.9 con Magic Keyboard', 'iPad Pro 2022 con Magic Keyboard y Apple Pencil 2. Ideal para diseno.', 1200.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (107, 'david', 'Tecnologia', 'Auriculares Sony WH-1000XM5', 'Los mejores auriculares con cancelacion de ruido. Negros, como nuevos.', 280.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (108, 'elena', 'Tecnologia', 'Monitor Gaming 27 pulgadas 144Hz', 'Monitor curvo Samsung Odyssey G5. Resolucion 2K, 1ms respuesta.', 220.00, NULL, 0, 0, 1);

-- === MODA ===
INSERT INTO Producto VALUES (201, 'maria', 'Moda', 'Bolso Louis Vuitton Neverfull MM', 'Bolso LV original con ticket de compra. Tamano MM, canvas monogram.', 950.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (202, 'ana', 'Moda', 'Nike Air Jordan 1 Retro Chicago', 'Jordan 1 Retro High OG Chicago. Talla 43, deadstock con caja.', 320.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (203, 'laura', 'Moda', 'Vestido Zara largo fiesta verde', 'Vestido largo de fiesta, color verde esmeralda. Talla M, etiqueta puesta.', 45.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (204, 'sofia', 'Moda', 'Reloj Casio G-Shock GA-2100', 'G-Shock GA-2100 CasiOak negro. Resistente al agua 200m.', 85.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (205, 'lucia', 'Moda', 'Chaqueta North Face plumas 700', 'Chaqueta de plumas 700 fill power. Talla L, color azul marino.', 180.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (206, 'elena', 'Moda', 'Gafas Ray-Ban Aviator polarizadas', 'Ray-Ban originales con cristales polarizados. Montura dorada.', 95.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (207, 'maria', 'Moda', 'Sudadera Champion vintage anos 90', 'Sudadera Champion anos 90, logo bordado. Talla XL, perfecta oversize.', 55.00, NULL, 0, 0, 1);

-- === DEPORTES ===
INSERT INTO Producto VALUES (301, 'carlos', 'Deportes', 'Bicicleta montana Specialized 29', 'Specialized Rockhopper 29. Cuadro aluminio, frenos hidraulicos.', 650.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (302, 'pedro', 'Deportes', 'Raqueta tenis Wilson Pro Staff', 'Raqueta profesional Roger Federer. Incluye funda y 3 overgrips.', 120.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (303, 'david', 'Deportes', 'Balon futbol oficial LaLiga 23/24', 'Balon Puma Orbita oficial temporada 23/24. Sin usar.', 35.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (304, 'miguel', 'Deportes', 'Tabla surf Channel Islands 6.2', 'Shortboard Channel Islands. Incluye quillas FCS y funda.', 380.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (305, 'pablo', 'Deportes', 'Pesas ajustables Bowflex 40kg', 'Set de mancuernas ajustables Bowflex. De 2 a 20kg cada una.', 250.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (306, 'juan', 'Deportes', 'Cinta de correr BH Fitness plegable', 'Cinta plegable con inclinacion automatica. Poco uso, como nueva.', 450.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (307, 'ana', 'Deportes', 'Patines Rollerblade Zetrablade 42', 'Patines Rollerblade Zetrablade talla 42. Perfectos para iniciacion.', 75.00, NULL, 0, 0, 1);

-- === HOGAR ===
INSERT INTO Producto VALUES (401, 'laura', 'Hogar', 'Sofa 3 plazas IKEA KIVIK gris', 'Sofa KIVIK gris oscuro. 2 anos, perfecto estado. Fundas lavables.', 350.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (402, 'elena', 'Hogar', 'Robot aspirador Roomba i7+', 'Roomba con base autovaciado. Mapeo inteligente, control por app.', 420.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (403, 'sofia', 'Hogar', 'Cafetera Nespresso Vertuo Plus', 'Cafetera Vertuo Plus con espumador de leche. 50 capsulas incluidas.', 95.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (404, 'lucia', 'Hogar', 'Mesa comedor extensible roble', 'Mesa roble macizo 140-220cm. 6-10 comensales. Estilo nordico.', 280.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (405, 'pablo', 'Hogar', 'Colchon viscoelastico Emma 150x190', 'Colchon Emma Original. 2 anos con funda protectora siempre.', 200.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (406, 'miguel', 'Hogar', 'Lampara pie diseno Arco', 'Lampara Arco estilo Castiglioni. Base marmol, arco cromado.', 120.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (407, 'carlos', 'Hogar', 'Thermomix TM6 con Cook-Key', 'Thermomix ultimo modelo con Cook-Key. Recetario completo incluido.', 950.00, NULL, 0, 0, 1);

-- === LIBROS ===
INSERT INTO Producto VALUES (501, 'juan', 'Libros', 'Coleccion Harry Potter 7 libros', '7 libros tapa dura edicion especial 20 aniversario. Como nuevos.', 85.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (502, 'maria', 'Libros', 'Kindle Paperwhite 2023 16GB', 'Kindle ultimo modelo con luz calida ajustable. 16GB, sin publicidad.', 140.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (503, 'david', 'Libros', 'Lote 20 novelas bestsellers', 'Novelas variadas: thriller, romance, ciencia ficcion. Buen estado.', 40.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (504, 'elena', 'Libros', 'Enciclopedia Espasa 100 tomos', '100 tomos encuadernacion lujo. Edicion 1990, perfecto estado.', 300.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (505, 'lucia', 'Libros', 'Libros universidad Ingenieria', 'Lote calculo, fisica, algebra. Autores: Stewart, Serway, Grossman.', 60.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (506, 'pedro', 'Libros', 'Comics Marvel vintage 50 unidades', 'Coleccion anos 80-90. Spiderman, X-Men, Vengadores. 50 ejemplares.', 150.00, NULL, 0, 0, 1);

-- === VEHICULOS ===
INSERT INTO Producto VALUES (601, 'carlos', 'Vehiculos', 'Vespa Primavera 125 azul cielo', 'Vespa 2020, 8000km. Color azul cielo, maletero incluido.', 2800.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (602, 'ana', 'Vehiculos', 'Bicicleta electrica Xiaomi plegable', 'E-bike Xiaomi Mi Smart. 25km/h, autonomia 45km. Plegable.', 550.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (603, 'pablo', 'Vehiculos', 'Patinete electrico Xiaomi Pro 2', 'Patinete electrico 25km/h. Bateria nueva, ruedas antipinchazos.', 320.00, NULL, 0, 0, 1);
INSERT INTO Producto VALUES (604, 'miguel', 'Vehiculos', 'Casco moto Shoei NXR2 talla M', 'Casco integral Shoei NXR2 talla M. Homologado ECE 22.06.', 380.00, NULL, 0, 0, 1);

-- === PRODUCTOS NO DISPONIBLES (vendidos) ===
INSERT INTO Producto VALUES (701, 'juan', 'Tecnologia', 'AirPods Pro 2 - VENDIDO', 'AirPods Pro segunda generacion. Ya no disponibles.', 200.00, NULL, 0, 0, 0);
INSERT INTO Producto VALUES (702, 'maria', 'Moda', 'Bolso Gucci GG Marmont - VENDIDO', 'Bolso GG Marmont pequeno. Vendido.', 800.00, NULL, 0, 0, 0);

-- =====================================================
-- FAVORITOS (los triggers incrementan num_favs)
-- =====================================================
INSERT INTO Favorito VALUES (101, 'maria');
INSERT INTO Favorito VALUES (101, 'carlos');
INSERT INTO Favorito VALUES (101, 'ana');
INSERT INTO Favorito VALUES (102, 'juan');
INSERT INTO Favorito VALUES (102, 'elena');
INSERT INTO Favorito VALUES (103, 'david');
INSERT INTO Favorito VALUES (103, 'miguel');
INSERT INTO Favorito VALUES (201, 'ana');
INSERT INTO Favorito VALUES (201, 'laura');
INSERT INTO Favorito VALUES (201, 'sofia');
INSERT INTO Favorito VALUES (202, 'carlos');
INSERT INTO Favorito VALUES (202, 'pedro');
INSERT INTO Favorito VALUES (301, 'miguel');
INSERT INTO Favorito VALUES (301, 'pablo');
INSERT INTO Favorito VALUES (401, 'lucia');
INSERT INTO Favorito VALUES (402, 'maria');
INSERT INTO Favorito VALUES (501, 'elena');
INSERT INTO Favorito VALUES (501, 'david');
INSERT INTO Favorito VALUES (601, 'ana');
INSERT INTO Favorito VALUES (603, 'juan');

-- =====================================================
-- CHATS
-- =====================================================
INSERT INTO Chat VALUES (101, 101, 'maria', 0);
INSERT INTO Chat VALUES (102, 101, 'carlos', 0);
INSERT INTO Chat VALUES (103, 102, 'juan', 0);
INSERT INTO Chat VALUES (104, 201, 'ana', 0);
INSERT INTO Chat VALUES (105, 201, 'sofia', 1);
INSERT INTO Chat VALUES (106, 301, 'miguel', 0);
INSERT INTO Chat VALUES (107, 103, 'david', 0);
INSERT INTO Chat VALUES (108, 401, 'maria', 0);
INSERT INTO Chat VALUES (109, 501, 'elena', 0);
INSERT INTO Chat VALUES (110, 601, 'pablo', 0);

-- =====================================================
-- MENSAJES
-- =====================================================
INSERT INTO Mensaje VALUES (101, TIMESTAMP '2025-01-10 10:00:00', 'maria', 'Hola! Sigue disponible el iPhone?', NULL, 1);
INSERT INTO Mensaje VALUES (101, TIMESTAMP '2025-01-10 10:15:00', 'juan', 'Si! Esta en perfecto estado', NULL, 1);
INSERT INTO Mensaje VALUES (101, TIMESTAMP '2025-01-10 10:16:00', 'maria', 'Harias algun descuento si quedamos hoy?', NULL, 1);
INSERT INTO Mensaje VALUES (101, TIMESTAMP '2025-01-10 10:20:00', 'juan', 'Podria dejartelo en 850', NULL, 0);

INSERT INTO Mensaje VALUES (102, TIMESTAMP '2025-01-10 11:00:00', 'carlos', 'Buenas, aceptas 800 por el iPhone?', NULL, 1);
INSERT INTO Mensaje VALUES (102, TIMESTAMP '2025-01-10 12:30:00', 'juan', 'Lo minimo seria 850, lo siento', NULL, 0);

INSERT INTO Mensaje VALUES (103, TIMESTAMP '2025-01-11 09:00:00', 'juan', 'Buenos dias! El MacBook tiene algun rasguno?', NULL, 1);
INSERT INTO Mensaje VALUES (103, TIMESTAMP '2025-01-11 09:05:00', 'maria', 'Ninguno, lo he usado siempre con funda', NULL, 1);
INSERT INTO Mensaje VALUES (103, TIMESTAMP '2025-01-11 09:06:00', 'juan', 'Genial! Podemos quedar este finde?', NULL, 1);
INSERT INTO Mensaje VALUES (103, TIMESTAMP '2025-01-11 09:10:00', 'maria', 'El sabado me viene bien, manana o tarde?', NULL, 0);

INSERT INTO Mensaje VALUES (104, TIMESTAMP '2025-01-12 14:00:00', 'ana', 'Hola! El bolso es original 100%?', NULL, 1);
INSERT INTO Mensaje VALUES (104, TIMESTAMP '2025-01-12 14:02:00', 'maria', 'Si, tengo ticket de El Corte Ingles', NULL, 1);
INSERT INTO Mensaje VALUES (104, TIMESTAMP '2025-01-12 14:03:00', 'ana', 'Perfecto, me interesa mucho', NULL, 0);

INSERT INTO Mensaje VALUES (106, TIMESTAMP '2025-01-13 18:00:00', 'miguel', 'Que talla es el cuadro de la bici?', NULL, 1);
INSERT INTO Mensaje VALUES (106, TIMESTAMP '2025-01-13 18:30:00', 'carlos', 'Es talla L, para personas de 175-185cm', NULL, 1);
INSERT INTO Mensaje VALUES (106, TIMESTAMP '2025-01-13 18:31:00', 'miguel', 'Me queda perfecto, la compro!', NULL, 0);

INSERT INTO Mensaje VALUES (107, TIMESTAMP '2025-01-14 20:00:00', 'david', 'Que juegos incluye la PS5?', NULL, 1);
INSERT INTO Mensaje VALUES (107, TIMESTAMP '2025-01-14 20:05:00', 'carlos', 'FIFA 24, Spider-Man 2 y God of War Ragnarok', NULL, 0);

-- =====================================================
-- CONTRAOFERTAS
-- =====================================================
INSERT INTO Contraoferta VALUES (101, 'maria', 850.00);
INSERT INTO Contraoferta VALUES (101, 'carlos', 800.00);
INSERT INTO Contraoferta VALUES (102, 'juan', 980.00);
INSERT INTO Contraoferta VALUES (201, 'ana', 900.00);
INSERT INTO Contraoferta VALUES (301, 'miguel', 600.00);
INSERT INTO Contraoferta VALUES (401, 'maria', 300.00);
INSERT INTO Contraoferta VALUES (603, 'juan', 280.00);

-- =====================================================
-- PREFERENCIAS DE CATEGORIAS
-- =====================================================
INSERT INTO Preferidos VALUES ('juan', 'Tecnologia');
INSERT INTO Preferidos VALUES ('juan', 'Deportes');
INSERT INTO Preferidos VALUES ('maria', 'Moda');
INSERT INTO Preferidos VALUES ('maria', 'Tecnologia');
INSERT INTO Preferidos VALUES ('carlos', 'Vehiculos');
INSERT INTO Preferidos VALUES ('carlos', 'Deportes');
INSERT INTO Preferidos VALUES ('ana', 'Moda');
INSERT INTO Preferidos VALUES ('ana', 'Hogar');
INSERT INTO Preferidos VALUES ('pedro', 'Deportes');
INSERT INTO Preferidos VALUES ('pedro', 'Libros');
INSERT INTO Preferidos VALUES ('laura', 'Hogar');
INSERT INTO Preferidos VALUES ('laura', 'Moda');
INSERT INTO Preferidos VALUES ('david', 'Tecnologia');
INSERT INTO Preferidos VALUES ('david', 'Libros');
INSERT INTO Preferidos VALUES ('elena', 'Libros');
INSERT INTO Preferidos VALUES ('elena', 'Hogar');
INSERT INTO Preferidos VALUES ('miguel', 'Deportes');
INSERT INTO Preferidos VALUES ('miguel', 'Vehiculos');
INSERT INTO Preferidos VALUES ('sofia', 'Moda');
INSERT INTO Preferidos VALUES ('sofia', 'Hogar');
INSERT INTO Preferidos VALUES ('pablo', 'Deportes');
INSERT INTO Preferidos VALUES ('pablo', 'Vehiculos');
INSERT INTO Preferidos VALUES ('lucia', 'Libros');
INSERT INTO Preferidos VALUES ('lucia', 'Hogar');
INSERT INTO Preferidos VALUES ('test', 'Tecnologia');
INSERT INTO Preferidos VALUES ('test', 'Moda');
INSERT INTO Preferidos VALUES ('admin', 'Tecnologia');
INSERT INTO Preferidos VALUES ('admin', 'Vehiculos');
INSERT INTO Preferidos VALUES ('deleted_user', 'Hogar');

-- =====================================================
-- VENTAS COMPLETADAS
-- =====================================================
INSERT INTO Vendido VALUES (701, 'maria', 1, 190.00, 5);
INSERT INTO Vendido VALUES (702, 'laura', 1, 750.00, 4);

-- =====================================================
-- MARCAR USUARIO COMO ELIMINADO (AL FINAL)
-- =====================================================
UPDATE Usuario SET cuenta_eliminada = 1 WHERE username = 'deleted_user';

COMMIT;

-- =====================================================
-- RESUMEN DE CREDENCIALES PARA TESTING
-- =====================================================
-- Todas las contrasenas cumplen: 8-15 chars, mayus, minus, especiales
-- 
-- | Usuario  | Contrasena  | Saldo    | Descripcion          |
-- |----------|-------------|----------|----------------------|
-- | admin    | Admin@123   | 10000.00 | Administrador        |
-- | juan     | Juan#2025   | 350.00   | Usuario vendedor     |
-- | maria    | Maria\$456   | 520.00   | Usuario activo       |
-- | carlos   | Carlosreboot  | 180.00   | Usuario vendedor     |
-- | ana      | Ana@Pass1   | 890.00   | Usuario comprador    |
-- | pedro    | Pedro#321   | 75.50    | Usuario bajo saldo   |
-- | laura    | Laura\$2025  | 1250.00  | Usuario premium      |
-- | david    | David!Pass  | 430.00   | Usuario normal       |
-- | elena    | Elena@987   | 2100.00  | Usuario top seller   |
-- | miguel   | Miguel#55   | 95.00    | Usuario bajo saldo   |
-- | sofia    | Sofia\$123   | 780.00   | Usuario activo       |
-- | pablo    | Pablo!2025  | 320.00   | Usuario normal       |
-- | lucia    | Lucia@Pass  | 1500.00  | Usuario premium      |
-- | test     | Test#1234   | 999.99   | Usuario para testing |
--
-- =====================================================
