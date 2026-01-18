
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
