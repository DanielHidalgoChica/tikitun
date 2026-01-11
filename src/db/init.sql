CREATE TABLE Usuario(
    username VARCHAR2(128),
    correo VARCHAR2(128),
    nombre_completo VARCHAR2(128),
    contrasenia VARCHAR2(128),
    ubi_latitud FLOAT(2),
    ubi_longitud FLOAT(2),
    rango FLOAT(3),
    saldo FLOAT(2),
    valoracion_media FLOAT(1),
    cuenta_eliminada INT
);

CREATE TABLE Categoria(
    nombre VARCHAR2(128)
);

CREATE TABLE Producto(
    id_producto INT,
    username VARCHAR2(128),
    nombre_categoria VARCHAR2(128),
    titulo VARCHAR2(128),
    descripcion VARCHAR2(512),
    precio FLOAT(2),
    imagen BLOB,
    promocion FLOAT(2),
    disponible INT
);

CREATE TABLE Chat(
    id_chat INT,
    id_producto INT,
    username VARCHAR2(128),
    archivado INT
);

CREATE TABLE Mensaje(
    id_chat INT,
    fecha TIMESTAMP(6),
    username VARCHAR2(128),
    texto VARCHAR2(512),
    adjunto BLOB,
    leido INT
);

CREATE TABLE Favorito(
    id_producto INT,
    username VARCHAR2(128)
);

CREATE TABLE Contraoferta(
    id_producto INT,
    username VARCHAR2(128),
    precio FLOAT(2)
);

CREATE TABLE Preferidos(
    username VARCHAR(128),
    nombre VARCHAR2(128)
);

CREATE TABLE Vendido(
    id_producto INT,
    username VARCHAR2(128),
    recepcion_confirmada INT,
    precio_final FLOAT(2),
    valoracion INT
);