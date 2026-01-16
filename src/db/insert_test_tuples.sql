INSERT INTO Usuario VALUES (
  'alice',
  'alice@mail.com',
  'Alice García',
  'hash_alice',
  40.4168,
  -3.7038,
  10.0,
  120.50,
  4.5,
  0
);

INSERT INTO Usuario VALUES (
  'bob',
  'bob@mail.com',
  'Bob Martínez',
  'hash_bob',
  41.3874,
  2.1686,
  15.0,
  80.00,
  4.0,
  0
);

INSERT INTO Usuario VALUES (
  'carol',
  'carol@mail.com',
  'Carol López',
  'hash_carol',
  37.3891,
  -5.9845,
  8.0,
  200.00,
  4.8,
  0
);

INSERT INTO Categoria VALUES ('Electrónica');
INSERT INTO Categoria VALUES ('Libros');
INSERT INTO Categoria VALUES ('Hogar');

INSERT INTO Producto VALUES (
  1,
  'alice',
  'Electrónica',
  'Auriculares Bluetooth',
  'Auriculares inalámbricos con cancelación de ruido',
  59.99,
  NULL,
  10.00,
  1
);

INSERT INTO Producto VALUES (
  2,
  'bob',
  'Libros',
  'Libro de Álgebra',
  'Álgebra lineal para universitarios',
  25.00,
  NULL,
  NULL,
  1
);

INSERT INTO Producto VALUES (
  11,
  'bob',
  'Libros',
  'Libro de Topología',
  'Munkres: 2019',
  25.00,
  NULL,
  NULL,
  1
);

INSERT INTO Producto VALUES (
  3,
  'alice',
  'Hogar',
  'Lámpara de escritorio',
  'Lámpara LED regulable',
  18.50,
  NULL,
  5.00,
  1
);

INSERT INTO Chat VALUES (
  1,
  1,
  'bob',
  0
);

INSERT INTO Chat VALUES (
  2,
  2,
  'carol',
  0
);

INSERT INTO Mensaje VALUES (
  1,
  TIMESTAMP '2025-01-01 10:00:00',
  'bob',
  'Hola, ¿siguen disponibles los auriculares?',
  NULL,
  1
);

INSERT INTO Mensaje VALUES (
  1,
  TIMESTAMP '2025-01-01 10:05:00',
  'alice',
  'Sí, están disponibles.',
  NULL,
  1
);

INSERT INTO Mensaje VALUES (
  2,
  TIMESTAMP '2025-01-02 12:00:00',
  'carol',
  '¿El libro está en buen estado?',
  NULL,
  0
);

INSERT INTO Favorito VALUES (1, 'bob');
INSERT INTO Favorito VALUES (3, 'carol');

INSERT INTO Contraoferta VALUES (
  1,
  'bob',
  50.00
);

INSERT INTO Contraoferta VALUES (
  2,
  'carol',
  20.00
);

INSERT INTO Preferidos VALUES ('alice', 'Electrónica');
INSERT INTO Preferidos VALUES ('bob', 'Libros');
INSERT INTO Preferidos VALUES ('carol', 'Hogar');

INSERT INTO Vendido VALUES (
  2,
  'carol',
  1,
  22.00,
  5
);

COMMIT;
