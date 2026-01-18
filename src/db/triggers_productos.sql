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
