
CREATE OR REPLACE TRIGGER TR_Archivado_Al_Finalizar
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

CREATE OR REPLACE TRIGGER TR_Archivado_Al_Eliminar_Producto
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

CREATE OR REPLACE TRIGGER TR_Archivado_Al_Eliminar_Usuario
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

CREATE OR REPLACE TRIGGER TR_No_Chat_Reflexivo
BEFORE INSERT 
ON Chat
FOR EACH ROW
DECLARE
    vendedor Producto.username%TYPE;
BEGIN
    -- Obtener dueño del producto
    SELECT username INTO vendedor FROM PRODUCTO
    WHERE id_producto = :new.id_producto;
    -- Comparar comprador con vendedor
    IF vendedor = :new.username THEN
        RAISE_APPLICATION_ERROR(-20051, 'No puedes hablar contigo mismo');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20052, 'El producto no existe');
END;
/