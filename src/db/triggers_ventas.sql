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