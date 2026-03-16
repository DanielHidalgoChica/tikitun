CREATE TABLE Usuario(
    username VARCHAR2(128) PRIMARY KEY,
    correo VARCHAR2(128) UNIQUE,
    nombre_completo VARCHAR2(128),
    contrasenia VARCHAR2(128),
    ubi_latitud FLOAT(6),
    ubi_longitud FLOAT(6),
    rango FLOAT(6),
    saldo FLOAT(10),
    valoracion_media FLOAT(3),
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
    precio FLOAT(10) NOT NULL,
    imagen BLOB,
    promocion FLOAT(2),
    num_favs INT,
    disponible INT,
    CONSTRAINT FK_ProductoVendedor FOREIGN KEY (username) REFERENCES Usuario(username),
    CONSTRAINT FK_ProductoCategoria FOREIGN KEY (nombre_categoria) REFERENCES Categoria(nombre)
);

CREATE TABLE Chat(
    id_chat INT PRIMARY KEY,
    id_producto INT,
    username VARCHAR2(128),
    archivado INT, 
    CONSTRAINT PK_UsernameIDProd UNIQUE (id_producto, username)
);

CREATE TABLE Mensaje(
    id_chat INT NOT NULL,
    fecha TIMESTAMP(6) NOT NULL,
    username VARCHAR2(128) NOT NULL,
    texto VARCHAR2(512),
    adjunto BLOB,
    leido INT,
    CONSTRAINT PK_Mensaje PRIMARY KEY (id_chat,fecha),
    CONSTRAINT FK_MensajeEmisor FOREIGN KEY (username) REFERENCES Usuario(username),
    CONSTRAINT FK_MensajeID_chat FOREIGN KEY (id_chat) REFERENCES Chat(id_chat),
    CONSTRAINT NotNull_Texto_Or_Adjunto CHECK (texto IS NOT NULL OR adjunto IS NOT NULL)
);

CREATE TABLE Favorito(
    id_producto INT,
    username VARCHAR2(128),
    CONSTRAINT PK_Favorito PRIMARY KEY (id_producto, username),
    CONSTRAINT FK_FavoritoProducto FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    CONSTRAINT FK_FavoritoUsuario FOREIGN KEY (username) REFERENCES Usuario(username)
);

CREATE TABLE Contraoferta(
    id_producto INT,
    username VARCHAR2(128),
    precio FLOAT(10) NOT NULL,
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
    precio_final FLOAT(10),
    valoracion INT,
    CONSTRAINT FK_VendidoProducto FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    CONSTRAINT FK_VendidoComprador FOREIGN KEY (username) REFERENCES Usuario(username)
);

-- Categorías maestras del sistema
INSERT INTO Categoria VALUES ('Vehiculos');
INSERT INTO Categoria VALUES ('Moda');
INSERT INTO Categoria VALUES ('Tecnologia');
INSERT INTO Categoria VALUES ('Deportes');
INSERT INTO Categoria VALUES ('Hogar');
INSERT INTO Categoria VALUES ('Libros');



--=====================================TRIGGERS:===============================================================


--FAVORITOS (DANIEL HIDALGO CHICA)

/**
 * TRIGGERS PARA MANTENER SINCRONIZADO EL CONTADOR DE FAVORITOS
 * Responsable: Daniel Hidalgo
 * 
 * Sistema de triggers que mantiene actualizado el campo num_favs en la tabla Producto.
 * 
 * Triggers implementados:
 * 1. TR_Favorito_InsertDisponible: Valida que el producto esté disponible
 * 2. TR_Favorito_InsertUsuarioActivo: Valida que el usuario no está eliminado
 * 3. TR_Favorito_Insert: Incrementa num_favs cuando se añade un favorito
 * 4. TR_Favorito_Delete: Decrementa num_favs cuando se elimina un favorito
 * 5. TR_Usuario_SoftDelete: Borra favoritos de usuarios eliminados y ajusta contadores
 */

-- ============================================================================
-- RECALCULAR CONTADORES INICIALES (ejecución única)
-- ============================================================================
-- Esta actualización recalcula el número de favoritos para cada producto.
-- Solo cuenta favoritos de usuarios con cuenta activa (cuenta_eliminada = 0)
--
-- NOTA: Esta sentencia se ejecuta una sola vez al instalar los triggers.
-- Los triggers posteriores mantendrán los contadores actualizados automáticamente.

UPDATE Producto 
SET num_favs = (
    SELECT COUNT(*) 
    FROM Favorito f
    JOIN Usuario u ON f.username = u.username
    WHERE f.id_producto = Producto.id_producto 
      AND u.cuenta_eliminada = 0
);

-- ============================================================================
-- TRIGGER 1: TR_Favorito_InsertDisponible
-- ============================================================================
-- Valida que el producto esté disponible antes de permitir la adición a favoritos.
-- Previene race conditions: si otro proceso vende el producto entre la validación
-- en Python y el INSERT, este trigger lo detiene.
--
-- Dispara: BEFORE INSERT ON Favorito
-- Acción: Lanza error si disponible = 0

CREATE OR REPLACE TRIGGER TR_Favorito_InsertDisponible
    BEFORE INSERT ON Favorito
    FOR EACH ROW
DECLARE
    disponible_flag Producto.disponible%TYPE;
BEGIN
    -- Obtener estado disponible del producto
    SELECT disponible INTO disponible_flag FROM Producto
    WHERE id_producto = :NEW.id_producto;
    
    -- Validar que está disponible
    IF disponible_flag = 0 THEN
        RAISE_APPLICATION_ERROR(-20010, 
            'No se puede añadir a favoritos un producto no disponible');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20011, 'El producto no existe');
END;
/

-- ============================================================================
-- TRIGGER 2: TR_Favorito_InsertUsuarioActivo
-- ============================================================================
-- Valida que el usuario que intenta marcar como favorito no tiene cuenta eliminada.
-- Previene que usuarios eliminados modifiquen sus favoritos.
--
-- Dispara: BEFORE INSERT ON Favorito
-- Acción: Lanza error si cuenta_eliminada = 1

CREATE OR REPLACE TRIGGER TR_Favorito_InsertUsuarioActivo
    BEFORE INSERT ON Favorito
    FOR EACH ROW
DECLARE
    cuenta_eliminada_flag Usuario.cuenta_eliminada%TYPE;
BEGIN
    -- Obtener estado de eliminación del usuario
    SELECT cuenta_eliminada INTO cuenta_eliminada_flag FROM Usuario
    WHERE username = :NEW.username;
    
    -- Validar que la cuenta está activa
    IF cuenta_eliminada_flag = 1 THEN
        RAISE_APPLICATION_ERROR(-20013, 
            'No puedes realizar esta acción con una cuenta eliminada');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20014, 'El usuario no existe');
END;
/

-- ============================================================================
-- TRIGGER 3: TR_Favorito_Insert
-- ============================================================================
-- Incrementa num_favs cuando alguien marca un producto como favorito.
-- 
-- Dispara: AFTER INSERT ON Favorito
-- Acción: UPDATE Producto SET num_favs = num_favs + 1
--
-- Nota: Los triggers BEFORE (1 y 2) garantizan que el usuario y producto
-- son válidos antes de ejecutarse este trigger.

CREATE OR REPLACE TRIGGER TR_Favorito_Insert
AFTER INSERT ON Favorito
FOR EACH ROW
BEGIN
  UPDATE Producto 
  SET num_favs = num_favs + 1 
  WHERE id_producto = :NEW.id_producto;
END;
/

-- ============================================================================
-- TRIGGER 4: TR_Favorito_Delete
-- ============================================================================
-- Decrementa num_favs cuando alguien quita un producto de favoritos.
--
-- Dispara: AFTER DELETE ON Favorito
-- Acción: UPDATE Producto SET num_favs = GREATEST(num_favs - 1, 0)
--
-- GREATEST se usa para evitar valores negativos (defensa contra inconsistencias).

CREATE OR REPLACE TRIGGER TR_Favorito_Delete
AFTER DELETE ON Favorito
FOR EACH ROW
BEGIN
  UPDATE Producto 
  SET num_favs = GREATEST(num_favs - 1, 0) 
  WHERE id_producto = :OLD.id_producto;
END;
/

-- ============================================================================
-- TRIGGER 5: TR_Usuario_SoftDelete
-- ============================================================================
-- Cuando se marca un usuario como eliminado (soft-delete, cuenta_eliminada = 1),
-- se eliminan automáticamente todos sus favoritos.
--
-- Dispara: AFTER UPDATE ON Usuario
-- Condición: OLD.cuenta_eliminada = 0 AND NEW.cuenta_eliminada = 1
-- Acción: DELETE FROM Favorito WHERE username = :NEW.username
--
-- Nota: El DELETE disparará automáticamente TR_Favorito_Delete para cada
-- fila eliminada, ajustando correctamente los contadores de los productos.

CREATE OR REPLACE TRIGGER TR_Usuario_SoftDelete
AFTER UPDATE ON Usuario
FOR EACH ROW
WHEN (OLD.cuenta_eliminada = 0 AND NEW.cuenta_eliminada = 1)
BEGIN
  DELETE FROM Favorito WHERE username = :NEW.username;
END;
/

-- ============================================================================
-- FIN DE TRIGGERS FAVORITOS
-- ============================================================================


-- MENSAJES Y CHATS (AITOR DE LA IGLESIA GARCÍA)


-- =====================================================
-- TRIGGERS PARA GESTIÓN DE CHATS Y ARCHIVADO AUTOMÁTICO
-- (Aitor de la Iglesia García)
-- =====================================================
-- Implementación de restricciones semánticas RS5.1 - RS5.4
-- =====================================================

-- =====================================================
-- RS3.1: Al confirmar la recepción de un producto,
-- se deben archivar todos los chats asociados a ese producto
-- =====================================================
CREATE OR REPLACE TRIGGER TR_Archivado_Al_Confirmar_Recepcion
AFTER UPDATE OF recepcion_confirmada
ON Vendido
FOR EACH ROW
WHEN (NEW.recepcion_confirmada = 1 AND OLD.recepcion_confirmada <> 1)
BEGIN
    UPDATE Chat
    SET archivado = 1
    WHERE id_producto = :NEW.id_producto;
END;
/

-- =====================================================
-- RS3.2: Al marcar un producto como no disponible,
-- se deben archivar los chats de los usuarios que
-- NO lo hayan comprado
-- =====================================================
CREATE OR REPLACE TRIGGER TR_Archivado_Al_No_Estar_Disponible_Si_No_Lo_Compraste
AFTER UPDATE OF disponible
ON Producto
FOR EACH ROW
WHEN (NEW.disponible = 0 AND OLD.disponible <> 0)
BEGIN
    UPDATE Chat c
    SET c.archivado = 1
    WHERE c.id_producto = :NEW.id_producto
      AND c.username NOT IN (
          SELECT v.username
          FROM Vendido v
          WHERE v.id_producto = :NEW.id_producto
      );
END;
/

-- =====================================================
-- RS3.3: Al eliminar (marcar como eliminada) una cuenta,
-- se deben archivar todos los chats donde participe
-- ese usuario, como comprador o como vendedor
-- =====================================================
CREATE OR REPLACE TRIGGER TR_Archivado_Al_Eliminar_Usuario
AFTER UPDATE OF cuenta_eliminada
ON Usuario
FOR EACH ROW
WHEN (NEW.cuenta_eliminada = 1 AND OLD.cuenta_eliminada <> 1)
BEGIN
    UPDATE Chat c
    SET c.archivado = 1
    WHERE c.id_chat IN (
        SELECT c.id_chat
        FROM Chat c 
        JOIN Producto p ON p.id_producto = c.id_producto
        WHERE p.username = :NEW.username 
           OR c.username = :NEW.username
    );
END;
/

-- =====================================================
-- RS3.4: No se puede crear un chat reflexivo:
-- un usuario no puede abrir un chat sobre su propio producto
-- =====================================================
CREATE OR REPLACE TRIGGER TR_No_Chat_Reflexivo
BEFORE INSERT 
ON Chat
FOR EACH ROW
DECLARE
    vendedor Producto.username%TYPE;
BEGIN
    -- Obtener el dueño del producto (solo si está disponible)
    SELECT username 
    INTO vendedor 
    FROM Producto
    WHERE id_producto = :NEW.id_producto 
      AND disponible = 1;

    -- Comparar comprador con vendedor
    IF vendedor = :NEW.username THEN
        RAISE_APPLICATION_ERROR(-20051, 'No puedes hablar contigo mismo');
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20052, 'El producto no existe o no está disponible');
END;
/

COMMIT;

-- =====================================================
-- RESUMEN DE TRIGGERS CREADOS
-- =====================================================
-- 
-- | Trigger                                      | RS   | Descripción                                             |
-- |----------------------------------------------|------|---------------------------------------------------------|
-- | TR_Archivado_Al_Confirmar_Recepcion          | RS3.1| Archiva chats al confirmar recepción                    |
-- | TR_Archivado_Al_No_Estar_Disponible_Si_No_Lo_Compraste | RS3.2| Archiva chats de no compradores al retirar producto     |
-- | TR_Archivado_Al_Eliminar_Usuario             | RS3.3| Archiva chats al eliminar una cuenta                    |
-- | TR_No_Chat_Reflexivo                         | RS3.4| Impide crear chats sobre productos propios o no diponibles        |
--
-- =====================================================


-- TRIGGERS PARA GESTIÓN DE USUARIOS (ELSA RODRÍGUEZ MACMICHAEL)

-- RS1.11: Un usuario no puede eliminar su cuenta si tiene ventas activas en curso.
-- Trigger para validar antes de eliminar lógicamente un usuario
-- Se activa cuando se intenta marcar cuenta_eliminada = 1
CREATE OR REPLACE TRIGGER trg_check_user_soft_deletion
BEFORE UPDATE OF cuenta_eliminada ON Usuario
FOR EACH ROW
DECLARE
    active_sales INT;
    active_offers INT;
BEGIN
    -- Solo validar cuando se está eliminando la cuenta (pasando de 0 a 1)
    IF :OLD.cuenta_eliminada = 0 AND :NEW.cuenta_eliminada = 1 THEN
        -- Check for active sales (como vendedor o comprador)
        SELECT COUNT(*) INTO active_sales
        FROM Vendido
        WHERE (Vendido.username = :OLD.username AND recepcion_confirmada = 0)
           OR (Vendido.id_producto IN (
                SELECT id_producto
                FROM Producto
                WHERE username = :OLD.username
              ) AND recepcion_confirmada = 0);

        -- Check for active counteroffers
        SELECT COUNT(*) INTO active_offers
        FROM Contraoferta
        WHERE username = :OLD.username;

        -- Raise an error if there are active sales or counteroffers
        IF active_sales > 0 OR active_offers > 0 THEN
            RAISE_APPLICATION_ERROR(-20001, 'No se puede eliminar el usuario porque tiene ventas activas o contraofertas pendientes.');
        END IF;
    END IF;
END;
/

-- RS1.9: La cantidad a transferir debe estar comprendida entre 0 y el saldo disponible.
-- Trigger para validar que el saldo no sea negativo al actualizar
CREATE OR REPLACE TRIGGER trg_check_saldo_positivo
BEFORE UPDATE OF saldo ON Usuario
FOR EACH ROW
BEGIN
    IF :NEW.saldo < 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'El saldo del monedero no puede ser negativo.');
    END IF;
END;
/

-- RS1.2, RS1.3: El correo electrónico debe tener formato válido y ser único.
-- Trigger para validar el formato del correo electrónico
CREATE OR REPLACE TRIGGER trg_check_email_format
BEFORE INSERT OR UPDATE OF correo ON Usuario
FOR EACH ROW
BEGIN
    IF :NEW.correo IS NOT NULL AND NOT REGEXP_LIKE(:NEW.correo, '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$') THEN
        RAISE_APPLICATION_ERROR(-20003, 'El formato del correo electrónico no es válido.');
    END IF;
END;
/

-- RS1.17, RS1.18: El rango de interés debe ser positivo.
-- Trigger para validar que el rango de búsqueda sea positivo
CREATE OR REPLACE TRIGGER trg_check_rango_positivo
BEFORE INSERT OR UPDATE OF rango ON Usuario
FOR EACH ROW
BEGIN
    IF :NEW.rango IS NOT NULL AND :NEW.rango < 0 THEN
        RAISE_APPLICATION_ERROR(-20004, 'El rango de búsqueda debe ser un valor positivo.');
    END IF;
END;
/

-- Trigger para validar las coordenadas de ubicación
CREATE OR REPLACE TRIGGER trg_check_ubicacion_valida
BEFORE INSERT OR UPDATE ON Usuario
FOR EACH ROW
BEGIN
    -- Validar latitud (entre -90 y 90)
    IF :NEW.ubi_latitud IS NOT NULL AND (:NEW.ubi_latitud < -90 OR :NEW.ubi_latitud > 90) THEN
        RAISE_APPLICATION_ERROR(-20005, 'La latitud debe estar entre -90 y 90 grados.');
    END IF;
    
    -- Validar longitud (entre -180 y 180)
    IF :NEW.ubi_longitud IS NOT NULL AND (:NEW.ubi_longitud < -180 OR :NEW.ubi_longitud > 180) THEN
        RAISE_APPLICATION_ERROR(-20006, 'La longitud debe estar entre -180 y 180 grados.');
    END IF;
END;
/

-- Trigger para validar la valoración media (entre 0 y 5)
CREATE OR REPLACE TRIGGER trg_check_valoracion_rango
BEFORE INSERT OR UPDATE OF valoracion_media ON Usuario
FOR EACH ROW
BEGIN
    IF :NEW.valoracion_media IS NOT NULL AND (:NEW.valoracion_media < 0 OR :NEW.valoracion_media > 5) THEN
        RAISE_APPLICATION_ERROR(-20007, 'La valoración media debe estar entre 0 y 5.');
    END IF;
END;
/

-- RS1.6, RS1.7: Un usuario no puede tener menos de 1 ni más de 6 categorías de preferencia.
-- Compound trigger para evitar error de tabla mutante (ORA-04091)
CREATE OR REPLACE TRIGGER trg_check_num_categorias
FOR INSERT ON Preferidos
COMPOUND TRIGGER
    -- Colección para almacenar los usuarios afectados
    TYPE t_usernames IS TABLE OF Preferidos.username%TYPE INDEX BY PLS_INTEGER;
    v_usernames t_usernames;
    v_index PLS_INTEGER := 0;

AFTER EACH ROW IS
BEGIN
    -- Guardar el username para verificar después
    v_index := v_index + 1;
    v_usernames(v_index) := :NEW.username;
END AFTER EACH ROW;

AFTER STATEMENT IS
    num_cats INT;
BEGIN
    -- Verificar cada usuario afectado
    FOR i IN 1..v_usernames.COUNT LOOP
        SELECT COUNT(*) INTO num_cats
        FROM Preferidos
        WHERE username = v_usernames(i);
        
        IF num_cats > 6 THEN
            RAISE_APPLICATION_ERROR(-20008, 'Un usuario no puede tener más de 6 categorías preferidas.');
        END IF;
    END LOOP;
END AFTER STATEMENT;
END trg_check_num_categorias;
/

-- RS1.12 a RS1.16: Ninguna operación de gestión de perfil podrá ejecutarse si el usuario ha sido eliminado.
-- Trigger para evitar modificar usuarios eliminados
CREATE OR REPLACE TRIGGER trg_check_cuenta_eliminada
BEFORE UPDATE ON Usuario
FOR EACH ROW
BEGIN
    -- Si la cuenta está eliminada, solo permitir cambios en cuenta_eliminada (para reactivar)
    IF :OLD.cuenta_eliminada = 1 AND :NEW.cuenta_eliminada = 1 THEN
        RAISE_APPLICATION_ERROR(-20009, 'No se puede modificar una cuenta que ha sido eliminada.');
    END IF;
END;
/

--TRIGGERS PARA GESTIÓN DE PRODUCTOS (ROBERTO GONZALEZ LUGO)
-- =====================================================
-- TRIGGERS PARA GESTIÓN DE PRODUCTOS (Roberto González)
-- =====================================================
-- Implementación de restricciones semánticas RS2.1 - RS2.15
-- =====================================================

-- =====================================================
-- RS2.1 / RS2.2: El precio debe ser mayor que 0
-- Aplica a INSERT y UPDATE en Producto
-- =====================================================
CREATE OR REPLACE TRIGGER trg_check_precio_producto
BEFORE INSERT OR UPDATE OF precio ON Producto
FOR EACH ROW
BEGIN
    IF :NEW.precio IS NULL OR :NEW.precio <= 0 THEN
        RAISE_APPLICATION_ERROR(-20101, 'El precio del producto debe ser mayor que 0.');
    END IF;
END;
/

-- =====================================================
-- RS2.3 / RS2.4: La categoría debe existir en el sistema
-- Esto ya está garantizado por la FK, pero añadimos
-- mensaje de error más descriptivo
-- =====================================================
CREATE OR REPLACE TRIGGER trg_check_categoria_producto
BEFORE INSERT OR UPDATE OF nombre_categoria ON Producto
FOR EACH ROW
DECLARE
    v_count INT;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM Categoria
    WHERE nombre = :NEW.nombre_categoria;
    
    IF v_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20102, 'La categoría seleccionada no existe en el sistema.');
    END IF;
END;
/

-- =====================================================
-- RS2.5 / RS2.6: Longitudes máximas de título (80) y descripción (500)
-- =====================================================
CREATE OR REPLACE TRIGGER trg_check_longitud_producto
BEFORE INSERT OR UPDATE ON Producto
FOR EACH ROW
BEGIN
    -- Verificar longitud del título (máximo 80 caracteres)
    IF :NEW.titulo IS NOT NULL AND LENGTH(:NEW.titulo) > 80 THEN
        RAISE_APPLICATION_ERROR(-20103, 'El título no puede exceder los 80 caracteres.');
    END IF;
    
    -- Verificar longitud de la descripción (máximo 500 caracteres)
    IF :NEW.descripcion IS NOT NULL AND LENGTH(:NEW.descripcion) > 500 THEN
        RAISE_APPLICATION_ERROR(-20104, 'La descripción no puede exceder los 500 caracteres.');
    END IF;
END;
/

-- =====================================================
-- RS2.8: Solo se puede modificar un producto disponible
-- y sin contraofertas activas
-- =====================================================
CREATE OR REPLACE TRIGGER trg_check_modificar_producto
BEFORE UPDATE ON Producto
FOR EACH ROW
DECLARE
    v_contraofertas INT;
BEGIN
    -- Solo aplicar si se están modificando campos de contenido (no promoción ni num_favs)
    IF :OLD.titulo != :NEW.titulo 
       OR :OLD.descripcion != :NEW.descripcion 
       OR :OLD.precio != :NEW.precio 
       OR :OLD.nombre_categoria != :NEW.nombre_categoria 
       OR (:OLD.imagen IS NULL AND :NEW.imagen IS NOT NULL)
       OR (:OLD.imagen IS NOT NULL AND :NEW.imagen IS NULL) THEN
        
        -- Verificar que el producto esté disponible
        IF :OLD.disponible = 0 THEN
            RAISE_APPLICATION_ERROR(-20105, 'No se puede modificar un producto que no está disponible.');
        END IF;
        
        -- Verificar que no tenga contraofertas activas
        SELECT COUNT(*) INTO v_contraofertas
        FROM Contraoferta
        WHERE id_producto = :OLD.id_producto;
        
        IF v_contraofertas > 0 THEN
            RAISE_APPLICATION_ERROR(-20106, 'No se puede modificar un producto con contraofertas activas.');
        END IF;
    END IF;
END;
/

-- =====================================================
-- RS2.9: Solo se puede eliminar (marcar no disponible)
-- un producto disponible sin contraofertas activas
-- =====================================================
CREATE OR REPLACE TRIGGER trg_check_eliminar_producto
BEFORE UPDATE OF disponible ON Producto
FOR EACH ROW
DECLARE
    v_contraofertas INT;
BEGIN
    -- Solo aplicar cuando se está marcando como no disponible
    IF :OLD.disponible = 1 AND :NEW.disponible = 0 THEN
        -- Verificar que no tenga contraofertas activas
        SELECT COUNT(*) INTO v_contraofertas
        FROM Contraoferta
        WHERE id_producto = :OLD.id_producto;
        
        IF v_contraofertas > 0 THEN
            RAISE_APPLICATION_ERROR(-20107, 'No se puede eliminar un producto con contraofertas activas.');
        END IF;
    END IF;
END;
/

-- =====================================================
-- RS2.10: El grado de promoción debe estar en [0, 1]
-- =====================================================
CREATE OR REPLACE TRIGGER trg_check_promocion_rango
BEFORE INSERT OR UPDATE OF promocion ON Producto
FOR EACH ROW
BEGIN
    IF :NEW.promocion IS NOT NULL THEN
        IF :NEW.promocion < 0 THEN
            :NEW.promocion := 0;
        ELSIF :NEW.promocion > 1 THEN
            RAISE_APPLICATION_ERROR(-20108, 'El grado de promoción debe estar entre 0 y 1.');
        END IF;
    END IF;
END;
/

-- =====================================================
-- RS2.11: Decaimiento automático de promoción
-- (0.1 cada 24 horas - se implementaría con un JOB)
-- Este trigger evitaría valores negativos
-- =====================================================
CREATE OR REPLACE TRIGGER trg_promocion_no_negativa
BEFORE UPDATE OF promocion ON Producto
FOR EACH ROW
BEGIN
    -- Asegurar que la promoción nunca sea negativa
    IF :NEW.promocion IS NOT NULL AND :NEW.promocion < 0 THEN
        :NEW.promocion := 0;
    END IF;
END;
/

-- =====================================================
-- RS2.12 / RS2.13: id_producto se genera automáticamente
-- y es único (implementado con secuencia)
-- =====================================================
CREATE SEQUENCE seq_producto_id
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

CREATE OR REPLACE TRIGGER trg_auto_id_producto
BEFORE INSERT ON Producto
FOR EACH ROW
BEGIN
    -- Asignar ID automático si no se proporciona o es nulo
    IF :NEW.id_producto IS NULL THEN
        SELECT seq_producto_id.NEXTVAL INTO :NEW.id_producto FROM DUAL;
    END IF;
END;
/

-- =====================================================
-- RS2.14: El vendedor debe existir y no estar eliminado
-- =====================================================
CREATE OR REPLACE TRIGGER trg_check_vendedor_existe
BEFORE INSERT ON Producto
FOR EACH ROW
DECLARE
    v_eliminado INT;
BEGIN
    SELECT cuenta_eliminada INTO v_eliminado
    FROM Usuario
    WHERE username = :NEW.username;
    
    IF v_eliminado = 1 THEN
        RAISE_APPLICATION_ERROR(-20109, 'No se puede crear un producto para un usuario con cuenta eliminada.');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20110, 'El vendedor especificado no existe.');
END;
/

-- =====================================================
-- Trigger adicional: Inicializar valores por defecto
-- =====================================================
CREATE OR REPLACE TRIGGER trg_producto_defaults
BEFORE INSERT ON Producto
FOR EACH ROW
BEGIN
    -- Promoción por defecto a 0 si es nula
    IF :NEW.promocion IS NULL THEN
        :NEW.promocion := 0;
    END IF;
    
    -- num_favs por defecto a 0 si es nulo
    IF :NEW.num_favs IS NULL THEN
        :NEW.num_favs := 0;
    END IF;
    
    -- disponible por defecto a 1 (disponible) si es nulo
    IF :NEW.disponible IS NULL THEN
        :NEW.disponible := 1;
    END IF;
END;
/

COMMIT;

-- =====================================================
-- RESUMEN DE TRIGGERS CREADOS
-- =====================================================
-- 
-- | Trigger                       | RS     | Descripción                                |
-- |-------------------------------|--------|--------------------------------------------|
-- | trg_check_precio_producto     | RS2.1/2| Precio > 0                                 |
-- | trg_check_categoria_producto  | RS2.3/4| Categoría debe existir                     |
-- | trg_check_longitud_producto   | RS2.5/6| Título ≤80, Descripción ≤500               |
-- | trg_check_modificar_producto  | RS2.8  | No modificar si no disponible o con ofertas|
-- | trg_check_eliminar_producto   | RS2.9  | No eliminar si tiene contraofertas         |
-- | trg_check_promocion_rango     | RS2.10 | Promoción en [0, 1]                        |
-- | trg_promocion_no_negativa     | RS2.11 | Evita promoción negativa                   |
-- | trg_auto_id_producto          | RS2.12/13| ID automático y único                    |
-- | trg_check_vendedor_existe     | RS2.14 | Vendedor existe y no eliminado             |
-- | trg_producto_defaults         | -      | Valores por defecto                        |
--
-- =====================================================

--TRIGGERS PARA GESTIÓN DE VENTAS (JUAN MANUEL FERNÁNDEZ GARCÍA)
/**
 * TRIGGERS PARA MANTENER CONSISTENTES LAS TABLAS VENDIDO Y CONTRAOFERTA.
 * Responsable: Juanma Fernández
 * 
 * Sistema de triggers que evitan que se inserten tuplas inconsistentes en las tablas
 * Vendido y Contraoferta.
 * 
 * Triggers implementados:
 * 1. TR_Vendido_Insert: Evita que se inserten ventas en las que el comprador es el dueño del producto.
 * 2. TR_Contraoferta_Insertar: Evita que se inserten contraofertas en las que el comprador es el dueño
 * del producto.
 * 3. TR_Update_Contraofertas: Elimina las contraofertas no válidas asociadas a un producto cuando
 * se actualiza un producto en venta.
 */

-- ============================================================================
-- TRIGGER 1: TR_Vendido_Insert
-- ============================================================================
-- Evita que se inserte en la tabla VENDIDO una venta en la que el usuario comprador
-- es dueño de su propio producto.
-- 
-- Dispara: BEFORE INSERT ON VENDIDO
-- Acción: Comprobar que el usuario comprador no sea el dueño del producto que ha comprado
--
-- Nota: En el código que implementa la compra directa y la aceptación de contraofertas ya se
-- comprueba antes de realizar una consulta que el comprador no sea dueño del producto y que el
-- producto existe, por lo que este disparador no debería lanzar nunca ninguna excepción.

CREATE OR REPLACE TRIGGER TR_Vendido_Insert
    BEFORE
    INSERT ON Vendido
    FOR EACH ROW
DECLARE
    propietario Producto.username%TYPE;
BEGIN
    -- Obtener dueño del producto
    SELECT username INTO propietario FROM PRODUCTO
    WHERE id_producto = :new.id_producto;

    -- Comparar comprador con propietario
    IF propietario = :new.username THEN
        RAISE_APPLICATION_ERROR(-20001, 'No puedes comprar tu propio producto');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'El producto no existe');
END;
/

-- ============================================================================
-- TRIGGER 2: TR_Contraoferta_Insertar
-- ============================================================================
-- Evita que se inserte en la tabla CONTRAOFERTA una contraoferta en la que el
-- usuario comprador es dueño de su propio producto.
-- 
-- Dispara: BEFORE INSERT ON CONTRAOFERTA
-- Acción: Comprobar que el usuario comprador no sea el dueño del producto al que realiza la contraoferta
--
-- Nota: En el código que implementa la aceptación de contraofertas ya se comprueba antes de realizar
-- una consulta que el comprador no sea dueño del producto y que el producto existe, por lo que este disparador
-- no debería lanzar nunca ninguna excepción.

CREATE OR REPLACE TRIGGER TR_Contraoferta_Insertar
    BEFORE
    INSERT ON Contraoferta
    FOR EACH ROW
DECLARE
    propietario Producto.username%TYPE;
BEGIN
    -- Obtener dueño del producto
    SELECT username INTO propietario FROM PRODUCTO
    WHERE id_producto = :new.id_producto;

    -- Comparar comprador con propietario
    IF propietario = :new.username THEN
        RAISE_APPLICATION_ERROR(-20003, 'No puedes realizar contraofertas a tu propio producto');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'El producto no existe');
END;
/


-- ============================================================================
COMMIT;