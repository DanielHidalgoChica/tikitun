
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
        FROM Chat c JOIN Producto p ON p.id_producto = c.id_producto
        WHERE p.username = :NEW.username OR c.username = :NEW.username
    );
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
    WHERE id_producto = :new.id_producto AND disponible=1;
    -- Comparar comprador con vendedor
    IF vendedor = :new.username THEN
        RAISE_APPLICATION_ERROR(-20051, 'No puedes hablar contigo mismo');
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20052, 'El producto no existe');
END;
/

