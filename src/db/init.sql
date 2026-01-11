CREATE TABLE Usuario(
    username VARCHAR2(128) PRIMARY KEY,
    correo VARCHAR2(128) UNIQUE,
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
    nombre VARCHAR2(128) PRIMARY KEY
);

CREATE TABLE Producto(
    id_producto INT PRIMARY KEY,
    username VARCHAR2(128),
    nombre_categoria VARCHAR2(128),
    titulo VARCHAR2(128) NOT NULL,
    descripcion VARCHAR2(512),
    precio FLOAT(2) NOT NULL,
    imagen BLOB,
    promocion FLOAT(2),
    disponible INT,
    CONSTRAINT FK_ProductoVendedor FOREIGN KEY (username) REFERENCES Usuario(username),
    CONSTRAINT FK_ProductoCategoria FOREIGN KEY (nombre_categoria) REFERENCES Categoria(nombre)
);

CREATE TABLE Chat(
    id_chat INT PRIMARY KEY,
    id_producto INT,
    username VARCHAR2(128),
    archivado INT
);

CREATE TABLE Mensaje(
    id_chat INT NOT NULL,
    fecha TIMESTAMP(6) NOT NULL,
    username VARCHAR2(128) NOT NULL,
    texto VARCHAR2(512) NOT NULL,
    adjunto BLOB,
    leido INT,
    CONSTRAINT PK_Mensaje PRIMARY KEY (id_chat,fecha),
    CONSTRAINT FK_MensajeEmisor FOREIGN KEY (username) REFERENCES Usuario(username),
    CONSTRAINT FK_MensajeID_chat FOREIGN KEY (id_chat) REFERENCES Chat(id_chat)
);

CREATE TABLE Favorito(
    id_producto INT,
    username VARCHAR2(128),
    CONSTRAINT FK_FavoritoProducto FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    CONSTRAINT FK_FavoritoUsuario FOREIGN KEY (username) REFERENCES Usuario(username)
);

CREATE TABLE Contraoferta(
    id_producto INT,
    username VARCHAR2(128),
    precio FLOAT(2) NOT NULL,
    CONSTRAINT PK_Contraoferta PRIMARY KEY (id_producto,username),
    CONSTRAINT FK_ContraofertaProducto FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    CONSTRAINT FK_ContraofertaContraofertante FOREIGN KEY (username) REFERENCES Usuario(username)
);

CREATE TABLE Preferidos(
    username VARCHAR(128),
    nombre VARCHAR2(128),
    CONSTRAINT PK_Preferidos PRIMARY KEY (username,nombre),
    CONSTRAINT FK_PreferidosUsuario FOREIGN KEY (username) REFERENCES Usuario(username),
    CONSTRAINT FK_PreferidosCategoria FOREIGN KEY (nombre) REFERENCES Categoria(nombre)
);

CREATE TABLE Vendido(
    id_producto INT PRIMARY KEY,
    username VARCHAR2(128),
    recepcion_confirmada INT,
    precio_final FLOAT(2),
    valoracion INT,
    CONSTRAINT FK_VendidoProducto FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    CONSTRAINT FK_VendidoComprador FOREIGN KEY (username) REFERENCES Usuario(username)
);

SELECT * FROM USER_TABLES;