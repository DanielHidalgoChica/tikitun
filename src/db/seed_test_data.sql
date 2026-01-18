-- =====================================================
-- SCRIPT DE DATOS DE PRUEBA PARA TIKITUN
-- =====================================================
-- Este script llena la base de datos con datos realistas
-- para pruebas. Ejecutar DESPUÉS de init.sql
-- =====================================================

-- =====================================================
-- USUARIOS (15 usuarios con contraseñas conocidas)
-- =====================================================
-- NOTA: Las contraseñas cumplen requisitos (8-15 chars, mayús, minús, especiales)
-- Para login usar: usuario / contraseña en texto plano

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
  'Juan García Pérez',
  'Juan#2025',
  40.4530,
  -3.6883,
  25.0,
  350.00,
  4.7,
  0
);

-- Usuario: maria / Maria$456
INSERT INTO Usuario VALUES (
  'maria',
  'maria@gmail.com',
  'María López Fernández',
  'Maria$456',
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
  'Carlos Martínez Ruiz',
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
  'Ana Sánchez Torres',
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
  'Pedro Hernández Gómez',
  'Pedro#321',
  43.2630,
  -2.9350,
  12.0,
  75.50,
  3.9,
  0
);

-- Usuario: laura / Laura$2025
INSERT INTO Usuario VALUES (
  'laura',
  'laura@gmail.com',
  'Laura Díaz Moreno',
  'Laura$2025',
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
  'David Jiménez Navarro',
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
  'Miguel Álvarez Prieto',
  'Miguel#55',
  28.4636,
  -16.2518,
  40.0,
  95.00,
  3.5,
  0
);

-- Usuario: sofia / Sofia$123
INSERT INTO Usuario VALUES (
  'sofia',
  'sofia@icloud.com',
  'Sofía Muñoz Ortega',
  'Sofia$123',
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
  'Pablo Gutiérrez Serrano',
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
  'Lucía Vega Ramos',
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

-- Usuario eliminado para probar funcionalidad
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
  1
);

-- =====================================================
-- PRODUCTOS (40+ productos variados)
-- =====================================================

-- === TECNOLOGÍA ===
INSERT INTO Producto VALUES (101, 'juan', 'Tecnología', 'iPhone 14 Pro Max', 'iPhone 14 Pro Max 256GB, color morado oscuro. Estado impecable, con caja original y todos los accesorios.', 899.00, NULL, 3, 45, 1);
INSERT INTO Producto VALUES (102, 'maria', 'Tecnología', 'MacBook Air M2', 'MacBook Air con chip M2, 8GB RAM, 256GB SSD. Color medianoche. Comprado hace 6 meses.', 1050.00, NULL, 2, 32, 1);
INSERT INTO Producto VALUES (103, 'carlos', 'Tecnología', 'PlayStation 5', 'PS5 edición disco con 2 mandos y 3 juegos. Poco uso, perfecta para gaming.', 450.00, NULL, NULL, 28, 1);
INSERT INTO Producto VALUES (104, 'ana', 'Tecnología', 'Samsung Galaxy S23 Ultra', 'Galaxy S23 Ultra 512GB negro. Incluye funda y protector de pantalla.', 780.00, NULL, 1, 19, 1);
INSERT INTO Producto VALUES (105, 'pedro', 'Tecnología', 'Nintendo Switch OLED', 'Switch OLED blanca con 5 juegos físicos y funda de transporte.', 280.00, NULL, NULL, 41, 1);
INSERT INTO Producto VALUES (106, 'laura', 'Tecnología', 'iPad Pro 12.9"', 'iPad Pro 2022 con Magic Keyboard y Apple Pencil 2. Ideal para diseño.', 1200.00, NULL, 2, 15, 1);
INSERT INTO Producto VALUES (107, 'david', 'Tecnología', 'Auriculares Sony WH-1000XM5', 'Los mejores auriculares con cancelación de ruido. Negros, como nuevos.', 280.00, NULL, NULL, 22, 1);
INSERT INTO Producto VALUES (108, 'elena', 'Tecnología', 'Monitor Gaming 27" 144Hz', 'Monitor curvo Samsung Odyssey G5. Resolución 2K, 1ms respuesta.', 220.00, NULL, 1, 8, 1);

-- === MODA ===
INSERT INTO Producto VALUES (201, 'maria', 'Moda', 'Bolso Louis Vuitton Neverfull', 'Bolso LV original con ticket de compra. Tamaño MM, canvas monogram.', 950.00, NULL, 3, 67, 1);
INSERT INTO Producto VALUES (202, 'ana', 'Moda', 'Zapatillas Nike Air Jordan 1', 'Jordan 1 Retro High OG "Chicago". Talla 43, deadstock con caja.', 320.00, NULL, 2, 89, 1);
INSERT INTO Producto VALUES (203, 'laura', 'Moda', 'Vestido Zara nuevo', 'Vestido largo de fiesta, color verde esmeralda. Talla M, etiqueta puesta.', 45.00, NULL, NULL, 12, 1);
INSERT INTO Producto VALUES (204, 'sofia', 'Moda', 'Reloj Casio G-Shock', 'G-Shock GA-2100 "CasiOak" negro. Resistente al agua 200m.', 85.00, NULL, NULL, 34, 1);
INSERT INTO Producto VALUES (205, 'lucia', 'Moda', 'Chaqueta North Face', 'Chaqueta de plumas 700 fill power. Talla L, color azul marino.', 180.00, NULL, 1, 23, 1);
INSERT INTO Producto VALUES (206, 'elena', 'Moda', 'Gafas Ray-Ban Aviator', 'Ray-Ban originales con cristales polarizados. Montura dorada.', 95.00, NULL, NULL, 41, 1);
INSERT INTO Producto VALUES (207, 'maria', 'Moda', 'Sudadera Champion vintage', 'Sudadera Champion años 90, logo bordado. Talla XL, perfecta oversize.', 55.00, NULL, NULL, 18, 1);

-- === DEPORTES ===
INSERT INTO Producto VALUES (301, 'carlos', 'Deportes', 'Bicicleta montaña Specialized', 'Specialized Rockhopper 29". Cuadro aluminio, frenos hidráulicos.', 650.00, NULL, 2, 14, 1);
INSERT INTO Producto VALUES (302, 'pedro', 'Deportes', 'Raqueta tenis Wilson Pro Staff', 'Raqueta profesional Roger Federer. Incluye funda y 3 overgrips.', 120.00, NULL, NULL, 7, 1);
INSERT INTO Producto VALUES (303, 'david', 'Deportes', 'Balón fútbol oficial LaLiga', 'Balón Puma Orbita oficial temporada 23/24. Sin usar.', 35.00, NULL, NULL, 29, 1);
INSERT INTO Producto VALUES (304, 'miguel', 'Deportes', 'Tabla surf 6"2', 'Shortboard Channel Islands. Incluye quillas FCS y funda.', 380.00, NULL, 1, 5, 1);
INSERT INTO Producto VALUES (305, 'pablo', 'Deportes', 'Pesas ajustables 40kg', 'Set de mancuernas ajustables Bowflex. De 2 a 20kg cada una.', 250.00, NULL, NULL, 16, 1);
INSERT INTO Producto VALUES (306, 'juan', 'Deportes', 'Cinta de correr BH Fitness', 'Cinta plegable con inclinación automática. Poco uso, como nueva.', 450.00, NULL, 2, 3, 1);
INSERT INTO Producto VALUES (307, 'ana', 'Deportes', 'Patines en línea Rollerblade', 'Patines Rollerblade Zetrablade talla 42. Perfectos para iniciación.', 75.00, NULL, NULL, 11, 1);

-- === HOGAR ===
INSERT INTO Producto VALUES (401, 'laura', 'Hogar', 'Sofá 3 plazas IKEA', 'Sofá KIVIK gris oscuro. 2 años, perfecto estado. Fundas lavables.', 350.00, NULL, 1, 8, 1);
INSERT INTO Producto VALUES (402, 'elena', 'Hogar', 'Robot aspirador Roomba i7+', 'Roomba con base autovaciado. Mapeo inteligente, control por app.', 420.00, NULL, 2, 21, 1);
INSERT INTO Producto VALUES (403, 'sofia', 'Hogar', 'Cafetera Nespresso Vertuo', 'Cafetera Vertuo Plus con espumador de leche. 50 cápsulas incluidas.', 95.00, NULL, NULL, 37, 1);
INSERT INTO Producto VALUES (404, 'lucia', 'Hogar', 'Mesa comedor extensible', 'Mesa roble macizo 140-220cm. 6-10 comensales. Estilo nórdico.', 280.00, NULL, 1, 4, 1);
INSERT INTO Producto VALUES (405, 'pablo', 'Hogar', 'Colchón viscoelástico 150x190', 'Colchón Emma Original. 2 años con funda protectora siempre.', 200.00, NULL, NULL, 9, 1);
INSERT INTO Producto VALUES (406, 'miguel', 'Hogar', 'Lámpara pie diseño', 'Lámpara Arco estilo Castiglioni. Base mármol, arco cromado.', 120.00, NULL, NULL, 13, 1);
INSERT INTO Producto VALUES (407, 'carlos', 'Hogar', 'Thermomix TM6', 'Thermomix último modelo con Cook-Key. Recetario completo incluido.', 950.00, NULL, 3, 56, 1);

-- === LIBROS ===
INSERT INTO Producto VALUES (501, 'juan', 'Libros', 'Colección Harry Potter completa', '7 libros tapa dura edición especial 20 aniversario. Como nuevos.', 85.00, NULL, 1, 42, 1);
INSERT INTO Producto VALUES (502, 'maria', 'Libros', 'Kindle Paperwhite 2023', 'Kindle último modelo con luz cálida ajustable. 16GB, sin publicidad.', 140.00, NULL, NULL, 28, 1);
INSERT INTO Producto VALUES (503, 'david', 'Libros', 'Lote 20 novelas bestsellers', 'Novelas variadas: thriller, romance, ciencia ficción. Buen estado.', 40.00, NULL, NULL, 6, 1);
INSERT INTO Producto VALUES (504, 'elena', 'Libros', 'Enciclopedia Espasa completa', '100 tomos encuadernación lujo. Edición 1990, perfecto estado.', 300.00, NULL, 2, 2, 1);
INSERT INTO Producto VALUES (505, 'lucia', 'Libros', 'Libros universidad Ingeniería', 'Lote cálculo, física, álgebra. Autores: Stewart, Serway, Grossman.', 60.00, NULL, NULL, 15, 1);
INSERT INTO Producto VALUES (506, 'pedro', 'Libros', 'Cómics Marvel vintage', 'Colección años 80-90. Spiderman, X-Men, Vengadores. 50 ejemplares.', 150.00, NULL, 1, 19, 1);

-- === VEHÍCULOS ===
INSERT INTO Producto VALUES (601, 'carlos', 'Vehículos', 'Vespa Primavera 125', 'Vespa 2020, 8000km. Color azul cielo, maletero incluido.', 2800.00, NULL, 3, 31, 1);
INSERT INTO Producto VALUES (602, 'ana', 'Vehículos', 'Bicicleta eléctrica plegable', 'E-bike Xiaomi Mi Smart. 25km/h, autonomía 45km. Plegable.', 550.00, NULL, 2, 24, 1);
INSERT INTO Producto VALUES (603, 'pablo', 'Vehículos', 'Patinete Xiaomi Pro 2', 'Patinete eléctrico 25km/h. Batería nueva, ruedas antipinchazos.', 320.00, NULL, 1, 47, 1);
INSERT INTO Producto VALUES (604, 'miguel', 'Vehículos', 'Casco moto Shoei', 'Casco integral Shoei NXR2 talla M. Homologado ECE 22.06.', 380.00, NULL, NULL, 8, 1);

-- === PRODUCTOS NO DISPONIBLES (vendidos) ===
INSERT INTO Producto VALUES (701, 'juan', 'Tecnología', 'AirPods Pro 2 (VENDIDO)', 'AirPods Pro segunda generación. Ya no disponibles.', 200.00, NULL, NULL, 55, 0);
INSERT INTO Producto VALUES (702, 'maria', 'Moda', 'Bolso Gucci (VENDIDO)', 'Bolso GG Marmont pequeño. Vendido.', 800.00, NULL, 2, 78, 0);

-- =====================================================
-- FAVORITOS
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
-- Chat 101: maria interesada en iPhone de juan
INSERT INTO Mensaje VALUES (101, TIMESTAMP '2025-01-10 10:00:00', 'maria', 'Hola! Sigue disponible el iPhone?', NULL, 1);
INSERT INTO Mensaje VALUES (101, TIMESTAMP '2025-01-10 10:15:00', 'juan', 'Sí! Está en perfecto estado', NULL, 1);
INSERT INTO Mensaje VALUES (101, TIMESTAMP '2025-01-10 10:16:00', 'maria', 'Harías algún descuento si quedamos hoy?', NULL, 1);
INSERT INTO Mensaje VALUES (101, TIMESTAMP '2025-01-10 10:20:00', 'juan', 'Podría dejártelo en 850€', NULL, 0);

-- Chat 102: carlos también interesado en iPhone
INSERT INTO Mensaje VALUES (102, TIMESTAMP '2025-01-10 11:00:00', 'carlos', 'Buenas, aceptas 800 por el iPhone?', NULL, 1);
INSERT INTO Mensaje VALUES (102, TIMESTAMP '2025-01-10 12:30:00', 'juan', 'Lo mínimo sería 850, lo siento', NULL, 0);

-- Chat 103: juan interesado en MacBook de maria
INSERT INTO Mensaje VALUES (103, TIMESTAMP '2025-01-11 09:00:00', 'juan', 'Buenos días! El MacBook tiene algún rasguño?', NULL, 1);
INSERT INTO Mensaje VALUES (103, TIMESTAMP '2025-01-11 09:05:00', 'maria', 'Ninguno, lo he usado siempre con funda', NULL, 1);
INSERT INTO Mensaje VALUES (103, TIMESTAMP '2025-01-11 09:06:00', 'juan', 'Genial! Podemos quedar este finde?', NULL, 1);
INSERT INTO Mensaje VALUES (103, TIMESTAMP '2025-01-11 09:10:00', 'maria', 'El sábado me viene bien, mañana o tarde?', NULL, 0);

-- Chat 104: ana pregunta por bolso LV de maria
INSERT INTO Mensaje VALUES (104, TIMESTAMP '2025-01-12 14:00:00', 'ana', 'Hola! El bolso es original 100%?', NULL, 1);
INSERT INTO Mensaje VALUES (104, TIMESTAMP '2025-01-12 14:02:00', 'maria', 'Sí, tengo ticket de El Corte Inglés', NULL, 1);
INSERT INTO Mensaje VALUES (104, TIMESTAMP '2025-01-12 14:03:00', 'ana', 'Perfecto, me interesa mucho', NULL, 0);

-- Chat 106: miguel pregunta por bici de carlos
INSERT INTO Mensaje VALUES (106, TIMESTAMP '2025-01-13 18:00:00', 'miguel', 'Qué talla es el cuadro de la bici?', NULL, 1);
INSERT INTO Mensaje VALUES (106, TIMESTAMP '2025-01-13 18:30:00', 'carlos', 'Es talla L, para personas de 175-185cm', NULL, 1);
INSERT INTO Mensaje VALUES (106, TIMESTAMP '2025-01-13 18:31:00', 'miguel', 'Me queda perfecto, la compro!', NULL, 0);

-- Chat 107: david interesado en PS5
INSERT INTO Mensaje VALUES (107, TIMESTAMP '2025-01-14 20:00:00', 'david', 'Qué juegos incluye la PS5?', NULL, 1);
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
-- PREFERENCIAS DE CATEGORÍAS
-- =====================================================
INSERT INTO Preferidos VALUES ('juan', 'Tecnología');
INSERT INTO Preferidos VALUES ('juan', 'Deportes');
INSERT INTO Preferidos VALUES ('maria', 'Moda');
INSERT INTO Preferidos VALUES ('maria', 'Tecnología');
INSERT INTO Preferidos VALUES ('carlos', 'Vehículos');
INSERT INTO Preferidos VALUES ('carlos', 'Deportes');
INSERT INTO Preferidos VALUES ('ana', 'Moda');
INSERT INTO Preferidos VALUES ('ana', 'Hogar');
INSERT INTO Preferidos VALUES ('pedro', 'Deportes');
INSERT INTO Preferidos VALUES ('pedro', 'Libros');
INSERT INTO Preferidos VALUES ('laura', 'Hogar');
INSERT INTO Preferidos VALUES ('laura', 'Moda');
INSERT INTO Preferidos VALUES ('david', 'Tecnología');
INSERT INTO Preferidos VALUES ('david', 'Libros');
INSERT INTO Preferidos VALUES ('elena', 'Libros');
INSERT INTO Preferidos VALUES ('elena', 'Hogar');
INSERT INTO Preferidos VALUES ('miguel', 'Deportes');
INSERT INTO Preferidos VALUES ('miguel', 'Vehículos');
INSERT INTO Preferidos VALUES ('sofia', 'Moda');
INSERT INTO Preferidos VALUES ('sofia', 'Hogar');
INSERT INTO Preferidos VALUES ('pablo', 'Deportes');
INSERT INTO Preferidos VALUES ('pablo', 'Vehículos');
INSERT INTO Preferidos VALUES ('lucia', 'Libros');
INSERT INTO Preferidos VALUES ('lucia', 'Hogar');
INSERT INTO Preferidos VALUES ('test', 'Tecnología');
INSERT INTO Preferidos VALUES ('test', 'Moda');
INSERT INTO Preferidos VALUES ('admin', 'Tecnología');
INSERT INTO Preferidos VALUES ('admin', 'Vehículos');
INSERT INTO Preferidos VALUES ('deleted_user', 'Hogar');

-- =====================================================
-- VENTAS COMPLETADAS
-- =====================================================
INSERT INTO Vendido VALUES (701, 'maria', 1, 190.00, 5);
INSERT INTO Vendido VALUES (702, 'laura', 1, 750.00, 4);

COMMIT;

-- =====================================================
-- RESUMEN DE CREDENCIALES PARA TESTING
-- =====================================================
-- Todas las contraseñas cumplen: 8-15 chars, mayús, minús, especiales
-- 
-- | Usuario  | Contraseña  | Saldo    | Descripción          |
-- |----------|-------------|----------|----------------------|
-- | admin    | Admin@123   | 10000.00 | Administrador        |
-- | juan     | Juan#2025   | 350.00   | Usuario vendedor     |
-- | maria    | Maria$456   | 520.00   | Usuario activo       |
-- | carlos   | Carlos!789  | 180.00   | Usuario vendedor     |
-- | ana      | Ana@Pass1   | 890.00   | Usuario comprador    |
-- | pedro    | Pedro#321   | 75.50    | Usuario bajo saldo   |
-- | laura    | Laura$2025  | 1250.00  | Usuario premium      |
-- | david    | David!Pass  | 430.00   | Usuario normal       |
-- | elena    | Elena@987   | 2100.00  | Usuario top seller   |
-- | miguel   | Miguel#55   | 95.00    | Usuario bajo saldo   |
-- | sofia    | Sofia$123   | 780.00   | Usuario activo       |
-- | pablo    | Pablo!2025  | 320.00   | Usuario normal       |
-- | lucia    | Lucia@Pass  | 1500.00  | Usuario premium      |
-- | test     | Test#1234   | 999.99   | Usuario para testing |
--
-- =====================================================
