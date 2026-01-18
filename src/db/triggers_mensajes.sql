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
-- | TR_No_Chat_Reflexivo                         | RS3.4| Impide crear chats sobre productos propios              |
--
-- =====================================================
