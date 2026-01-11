CREATE TABLE Usuario(
    username
    correo
    nombre_completo
    password
    ubicacion
    rango
    saldo
    valoracion_media
    cuenta_eliminada
);

CREATE TABLE Categoria(
    nombre
);

CREATE TABLE Producto(
    id_producto
    username
    nombre_categoria
    titulo
    descripcion
    precio
    imagen
    promocion
    disponible
);

CREATE TABLE Chat(
    id_chat
    id_producto
    username
    archivado
);

CREATE TABLE Mensaje(
    id_chat
    fecha
    username
    texto
    adjunto
    leido
);

CREATE TABLE Favorito(
    id_producto
    username
);

CREATE TABLE Contraoferta(
    id_producto
    username
    precio
);

CREATE TABLE Preferidos(
    username
    nombre
);

CREATE TABLE Vendido(
    id_producto
    username
    recepcion_confirmada
    precio_final
    valoracion
);