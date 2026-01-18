CREATE OR REPLACE TRIGGER trg_check_user_deletion
BEFORE DELETE ON Usuario
FOR EACH ROW
DECLARE
    active_sales INT;
    active_offers INT;
BEGIN
    -- Check for active sales
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
END;