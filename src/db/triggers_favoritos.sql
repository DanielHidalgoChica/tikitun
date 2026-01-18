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
-- FIN DE TRIGGERS
-- ============================================================================

