/**
 * TRIGGERS PARA MANTENER SINCRONIZADO EL CONTADOR DE FAVORITOS
 * Responsable: Daniel Hidalgo
 * 
 * Sistema de triggers que mantiene actualizado el campo num_favs en la tabla Producto.
 * 
 * Triggers implementados:
 * 1. TR_Favorito_Insert: Incrementa num_favs cuando se añade un favorito
 * 2. TR_Favorito_Delete: Decrementa num_favs cuando se elimina un favorito
 * 3. TR_Usuario_SoftDelete: Borra favoritos de usuarios eliminados y ajusta contadores
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
-- TRIGGER 1: TR_Favorito_Insert
-- ============================================================================
-- Incrementa num_favs cuando alguien marca un producto como favorito.
-- 
-- Dispara: AFTER INSERT ON Favorito
-- Acción: UPDATE Producto SET num_favs = num_favs + 1
--
-- Nota: La validación de que el usuario no está eliminado se hace en la app
-- antes de insertar en la tabla Favorito.

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
-- TRIGGER 2: TR_Favorito_Delete
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
-- TRIGGER 3: TR_Usuario_SoftDelete
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

