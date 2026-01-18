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

-- Trigger para validar el número de categorías preferidas (máximo 6)
CREATE OR REPLACE TRIGGER trg_check_num_categorias
AFTER INSERT ON Preferidos
FOR EACH ROW
DECLARE
    num_cats INT;
BEGIN
    SELECT COUNT(*) INTO num_cats
    FROM Preferidos
    WHERE username = :NEW.username;
    
    IF num_cats > 6 THEN
        RAISE_APPLICATION_ERROR(-20008, 'Un usuario no puede tener más de 6 categorías preferidas.');
    END IF;
END;
/

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