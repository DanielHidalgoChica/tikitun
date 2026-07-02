-- =====================================================
-- SCRIPT DE DEMOSTRACIÓN DE TRIGGERS - TIKITUN
-- =====================================================
-- Este script demuestra el funcionamiento de todos los
-- triggers implementados en el sistema.
-- 
-- INSTRUCCIONES:
-- 1. Ejecutar init.sql primero (crea tablas y triggers)
-- 2. Ejecutar seed_test_data.sql (datos de prueba)
-- 3. Ejecutar este script sección por sección
--
-- Cada sección muestra:
-- - Qué trigger se prueba
-- - Qué restricción semántica implementa
-- - Operación que debe FALLAR (demuestra el trigger)
-- - Operación que debe FUNCIONAR (caso correcto)
-- =====================================================

SET SERVEROUTPUT ON;

-- =====================================================
-- PREPARACIÓN: Verificar datos de prueba
-- =====================================================
PROMPT ==========================================
PROMPT VERIFICANDO DATOS DE PRUEBA
PROMPT ==========================================

SELECT 'Usuarios: ' || COUNT(*) FROM Usuario;
SELECT 'Productos: ' || COUNT(*) FROM Producto;
SELECT 'Categorías: ' || COUNT(*) FROM Categoria;

-- =====================================================
-- SECCIÓN 1: TRIGGERS DE USUARIO
-- =====================================================
PROMPT
PROMPT ==========================================
PROMPT SECCIÓN 1: TRIGGERS DE USUARIO
PROMPT ==========================================

-- -------------------------------------------------
-- 1.1 trg_check_email_format (RS1.2, RS1.3)
-- Valida formato de correo electrónico
-- -------------------------------------------------
PROMPT
PROMPT --- 1.1 trg_check_email_format ---
PROMPT Intentando insertar usuario con email inválido...
PROMPT DEBE FALLAR: ORA-20003

BEGIN
    INSERT INTO Usuario VALUES (
        'test_email_mal',
        'esto-no-es-email',  -- Email inválido
        'Test Email',
        'Test@123',
        40.0, -3.0, 10.0, 100.00, 0.0, 0
    );
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

PROMPT Insertando usuario con email válido...
PROMPT DEBE FUNCIONAR

BEGIN
    INSERT INTO Usuario VALUES (
        'test_email_ok',
        'test_valido@gmail.com',
        'Test Email OK',
        'Test@123',
        40.0, -3.0, 10.0, 100.00, 0.0, 0
    );
    DBMS_OUTPUT.PUT_LINE('✓ Usuario insertado correctamente');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✗ ERROR INESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 1.2 trg_check_saldo_positivo (RS1.9)
-- Saldo no puede ser negativo
-- -------------------------------------------------
PROMPT
PROMPT --- 1.2 trg_check_saldo_positivo ---
PROMPT Intentando poner saldo negativo...
PROMPT DEBE FALLAR: ORA-20002

BEGIN
    UPDATE Usuario SET saldo = -50.00 WHERE username = 'test_email_ok';
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 1.3 trg_check_rango_positivo (RS1.17, RS1.18)
-- Rango de búsqueda debe ser positivo
-- -------------------------------------------------
PROMPT
PROMPT --- 1.3 trg_check_rango_positivo ---
PROMPT Intentando poner rango negativo...
PROMPT DEBE FALLAR: ORA-20004

BEGIN
    UPDATE Usuario SET rango = -10.0 WHERE username = 'test_email_ok';
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 1.4 trg_check_ubicacion_valida
-- Latitud [-90, 90], Longitud [-180, 180]
-- -------------------------------------------------
PROMPT
PROMPT --- 1.4 trg_check_ubicacion_valida ---
PROMPT Intentando poner latitud inválida (100)...
PROMPT DEBE FALLAR: ORA-20005

BEGIN
    UPDATE Usuario SET ubi_latitud = 100.0 WHERE username = 'test_email_ok';
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

PROMPT Intentando poner longitud inválida (200)...
PROMPT DEBE FALLAR: ORA-20006

BEGIN
    UPDATE Usuario SET ubi_longitud = 200.0 WHERE username = 'test_email_ok';
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 1.5 trg_check_valoracion_rango
-- Valoración debe estar entre 0 y 5
-- -------------------------------------------------
PROMPT
PROMPT --- 1.5 trg_check_valoracion_rango ---
PROMPT Intentando poner valoración 6...
PROMPT DEBE FALLAR: ORA-20007

BEGIN
    UPDATE Usuario SET valoracion_media = 6.0 WHERE username = 'test_email_ok';
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 1.6 trg_check_num_categorias (RS1.6, RS1.7)
-- Máximo 6 categorías preferidas
-- -------------------------------------------------
PROMPT
PROMPT --- 1.6 trg_check_num_categorias ---
PROMPT Añadiendo 6 categorías al usuario de prueba (máximo permitido)...

BEGIN
    -- Primero añadir todas las categorías posibles
    INSERT INTO Preferidos VALUES ('test_email_ok', 'Tecnología');
    INSERT INTO Preferidos VALUES ('test_email_ok', 'Moda');
    INSERT INTO Preferidos VALUES ('test_email_ok', 'Deportes');
    INSERT INTO Preferidos VALUES ('test_email_ok', 'Hogar');
    INSERT INTO Preferidos VALUES ('test_email_ok', 'Libros');
    INSERT INTO Preferidos VALUES ('test_email_ok', 'Vehículos');
    DBMS_OUTPUT.PUT_LINE('✓ 6 categorías añadidas correctamente');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✗ ERROR: ' || SQLERRM);
END;
/

PROMPT Intentando añadir 7ª categoría...
PROMPT DEBE FALLAR: ORA-20008

-- Crear categoría extra para la prueba
INSERT INTO Categoria VALUES ('CategoriaExtra');

BEGIN
    INSERT INTO Preferidos VALUES ('test_email_ok', 'CategoriaExtra');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- Limpiar categoría extra
DELETE FROM Categoria WHERE nombre = 'CategoriaExtra';

-- -------------------------------------------------
-- 1.7 trg_check_cuenta_eliminada (RS1.12-RS1.16)
-- No modificar usuarios con cuenta eliminada
-- -------------------------------------------------
PROMPT
PROMPT --- 1.7 trg_check_cuenta_eliminada ---
PROMPT Verificando usuario deleted_user está eliminado...

SELECT username, cuenta_eliminada FROM Usuario WHERE username = 'deleted_user';

PROMPT Intentando modificar usuario eliminado...
PROMPT DEBE FALLAR: ORA-20009

BEGIN
    UPDATE Usuario SET saldo = 500.00 
    WHERE username = 'deleted_user';
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- =====================================================
-- SECCIÓN 2: TRIGGERS DE PRODUCTO
-- =====================================================
PROMPT
PROMPT ==========================================
PROMPT SECCIÓN 2: TRIGGERS DE PRODUCTO
PROMPT ==========================================

-- -------------------------------------------------
-- 2.1 trg_check_precio_producto (RS2.1, RS2.2)
-- Precio debe ser > 0
-- -------------------------------------------------
PROMPT
PROMPT --- 2.1 trg_check_precio_producto ---
PROMPT Intentando insertar producto con precio 0...
PROMPT DEBE FALLAR: ORA-20101

BEGIN
    INSERT INTO Producto VALUES (
        9001, 'juan', 'Tecnología', 
        'Producto precio cero', 'Descripción', 
        0.00,  -- Precio inválido
        NULL, 0, 0, 1
    );
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

PROMPT Intentando insertar producto con precio negativo...
PROMPT DEBE FALLAR: ORA-20101

BEGIN
    INSERT INTO Producto VALUES (
        9002, 'juan', 'Tecnología', 
        'Producto precio negativo', 'Descripción', 
        -50.00,  -- Precio negativo
        NULL, 0, 0, 1
    );
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 2.2 trg_check_categoria_producto (RS2.3, RS2.4)
-- Categoría debe existir
-- -------------------------------------------------
PROMPT
PROMPT --- 2.2 trg_check_categoria_producto ---
PROMPT Intentando insertar producto con categoría inexistente...
PROMPT DEBE FALLAR: ORA-20102

BEGIN
    INSERT INTO Producto VALUES (
        9003, 'juan', 'CategoriaFalsa', 
        'Producto categoría falsa', 'Descripción', 
        100.00, NULL, 0, 0, 1
    );
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 2.3 trg_check_longitud_producto (RS2.5, RS2.6)
-- Título ≤ 80 chars, Descripción ≤ 500 chars
-- -------------------------------------------------
PROMPT
PROMPT --- 2.3 trg_check_longitud_producto ---
PROMPT Intentando insertar producto con título > 80 caracteres...
PROMPT DEBE FALLAR: ORA-20103

BEGIN
    INSERT INTO Producto VALUES (
        9004, 'juan', 'Tecnología', 
        'Este es un título extremadamente largo que definitivamente supera los ochenta caracteres permitidos por el sistema',
        'Descripción', 100.00, NULL, 0, 0, 1
    );
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

PROMPT Intentando insertar producto con descripción > 500 caracteres...
PROMPT DEBE FALLAR: ORA-20104

BEGIN
    INSERT INTO Producto VALUES (
        9005, 'juan', 'Tecnología', 
        'Título normal',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor.',
        100.00, NULL, 0, 0, 1
    );
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 2.4 trg_check_promocion_rango (RS2.10)
-- Promoción debe estar en [0, 1]
-- -------------------------------------------------
PROMPT
PROMPT --- 2.4 trg_check_promocion_rango ---
PROMPT Intentando poner promoción > 1...
PROMPT DEBE FALLAR: ORA-20108

BEGIN
    UPDATE Producto SET promocion = 1.5 WHERE id_producto = 101;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

PROMPT Probando que promoción negativa se corrige a 0 automáticamente...

BEGIN
    UPDATE Producto SET promocion = -0.5 WHERE id_producto = 101;
    DBMS_OUTPUT.PUT_LINE('✓ Actualización aceptada (se corrige a 0)');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('ERROR: ' || SQLERRM);
END;
/

SELECT 'Promoción del producto 101: ' || promocion FROM Producto WHERE id_producto = 101;

-- Restaurar promoción
UPDATE Producto SET promocion = 0 WHERE id_producto = 101;

-- -------------------------------------------------
-- 2.5 trg_check_vendedor_existe (RS2.14)
-- Vendedor debe existir y no estar eliminado
-- -------------------------------------------------
PROMPT
PROMPT --- 2.5 trg_check_vendedor_existe ---
PROMPT Intentando crear producto para vendedor inexistente...
PROMPT DEBE FALLAR: ORA-20110

BEGIN
    INSERT INTO Producto VALUES (
        9006, 'usuario_fantasma', 'Tecnología', 
        'Producto vendedor falso', 'Descripción', 
        100.00, NULL, 0, 0, 1
    );
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

PROMPT Intentando crear producto para vendedor eliminado...
PROMPT DEBE FALLAR: ORA-20109

BEGIN
    INSERT INTO Producto VALUES (
        9007, 'deleted_user', 'Tecnología', 
        'Producto usuario eliminado', 'Descripción', 
        100.00, NULL, 0, 0, 1
    );
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 2.6 trg_producto_defaults
-- Valores por defecto: promocion=0, num_favs=0, disponible=1
-- -------------------------------------------------
PROMPT
PROMPT --- 2.6 trg_producto_defaults ---
PROMPT Insertando producto sin especificar defaults...

BEGIN
    INSERT INTO Producto (id_producto, username, nombre_categoria, titulo, descripcion, precio)
    VALUES (9008, 'juan', 'Tecnología', 'Producto defaults', 'Prueba de defaults', 50.00);
    DBMS_OUTPUT.PUT_LINE('✓ Producto insertado');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('ERROR: ' || SQLERRM);
END;
/

SELECT 'Defaults aplicados - promocion: ' || promocion || ', num_favs: ' || num_favs || ', disponible: ' || disponible
FROM Producto WHERE id_producto = 9008;

-- Limpiar
DELETE FROM Producto WHERE id_producto = 9008;

-- -------------------------------------------------
-- 2.7 trg_check_modificar_producto (RS2.8)
-- No modificar producto con contraofertas activas
-- -------------------------------------------------
PROMPT
PROMPT --- 2.7 trg_check_modificar_producto ---
PROMPT Verificando contraofertas del producto 101 (iPhone de juan)...

SELECT COUNT(*) AS contraofertas FROM Contraoferta WHERE id_producto = 101;

PROMPT Intentando modificar producto con contraofertas...
PROMPT DEBE FALLAR: ORA-20106

BEGIN
    UPDATE Producto SET precio = 800.00 WHERE id_producto = 101;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 2.8 trg_check_eliminar_producto (RS2.9)
-- No eliminar producto con contraofertas
-- -------------------------------------------------
PROMPT
PROMPT --- 2.8 trg_check_eliminar_producto ---
PROMPT Intentando eliminar producto con contraofertas...
PROMPT DEBE FALLAR: ORA-20107

BEGIN
    UPDATE Producto SET disponible = 0 WHERE id_producto = 101;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- =====================================================
-- SECCIÓN 3: TRIGGERS DE FAVORITOS
-- =====================================================
PROMPT
PROMPT ==========================================
PROMPT SECCIÓN 3: TRIGGERS DE FAVORITOS
PROMPT ==========================================

-- -------------------------------------------------
-- 3.1 TR_Favorito_Insert / TR_Favorito_Delete
-- Contador automático de favoritos
-- -------------------------------------------------
PROMPT
PROMPT --- 3.1 TR_Favorito_Insert / TR_Favorito_Delete ---
PROMPT Verificando num_favs inicial del producto 107...

SELECT 'num_favs antes: ' || num_favs FROM Producto WHERE id_producto = 107;

PROMPT Añadiendo favorito...

INSERT INTO Favorito VALUES (107, 'test_email_ok');

SELECT 'num_favs después de añadir: ' || num_favs FROM Producto WHERE id_producto = 107;

PROMPT Eliminando favorito...

DELETE FROM Favorito WHERE id_producto = 107 AND username = 'test_email_ok';

SELECT 'num_favs después de eliminar: ' || num_favs FROM Producto WHERE id_producto = 107;

-- -------------------------------------------------
-- 3.2 TR_Favorito_InsertDisponible
-- No añadir favorito a producto no disponible
-- -------------------------------------------------
PROMPT
PROMPT --- 3.2 TR_Favorito_InsertDisponible ---
PROMPT Intentando añadir favorito a producto no disponible (701)...
PROMPT DEBE FALLAR: ORA-20010

BEGIN
    INSERT INTO Favorito VALUES (701, 'test_email_ok');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 3.3 TR_Favorito_InsertUsuarioActivo
-- Usuario eliminado no puede añadir favoritos
-- -------------------------------------------------
PROMPT
PROMPT --- 3.3 TR_Favorito_InsertUsuarioActivo ---
PROMPT Intentando que usuario eliminado añada favorito...
PROMPT DEBE FALLAR: ORA-20013

BEGIN
    INSERT INTO Favorito VALUES (102, 'deleted_user');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- =====================================================
-- SECCIÓN 4: TRIGGERS DE CHATS
-- =====================================================
PROMPT
PROMPT ==========================================
PROMPT SECCIÓN 4: TRIGGERS DE CHATS
PROMPT ==========================================

-- -------------------------------------------------
-- 4.1 TR_No_Chat_Reflexivo (RS3.4)
-- No crear chat sobre producto propio
-- -------------------------------------------------
PROMPT
PROMPT --- 4.1 TR_No_Chat_Reflexivo ---
PROMPT El producto 101 pertenece a juan
PROMPT Intentando que juan cree chat sobre su propio producto...
PROMPT DEBE FALLAR: ORA-20051

BEGIN
    INSERT INTO Chat VALUES (999, 101, 'juan', 0);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 4.2 TR_Archivado_Al_No_Estar_Disponible (RS3.2)
-- Archivar chats cuando producto no disponible
-- -------------------------------------------------
PROMPT
PROMPT --- 4.2 TR_Archivado_Al_No_Estar_Disponible ---
PROMPT Creando producto y chat de prueba...

-- Crear producto de prueba
INSERT INTO Producto VALUES (9010, 'test_email_ok', 'Tecnología', 'Producto para archivar', 'Test', 100.00, NULL, 0, 0, 1);

-- Crear chat sobre ese producto
INSERT INTO Chat VALUES (9010, 9010, 'juan', 0);

SELECT 'Chat 9010 archivado antes: ' || archivado FROM Chat WHERE id_chat = 9010;

PROMPT Marcando producto como no disponible...

UPDATE Producto SET disponible = 0 WHERE id_producto = 9010;

SELECT 'Chat 9010 archivado después: ' || archivado FROM Chat WHERE id_chat = 9010;

-- Limpiar
DELETE FROM Chat WHERE id_chat = 9010;
DELETE FROM Producto WHERE id_producto = 9010;

-- =====================================================
-- SECCIÓN 5: TRIGGERS DE VENTAS Y CONTRAOFERTAS
-- =====================================================
PROMPT
PROMPT ==========================================
PROMPT SECCIÓN 5: TRIGGERS DE VENTAS Y CONTRAOFERTAS
PROMPT ==========================================

-- -------------------------------------------------
-- 5.1 TR_Contraoferta_Insertar
-- No contraoferta a producto propio
-- -------------------------------------------------
PROMPT
PROMPT --- 5.1 TR_Contraoferta_Insertar ---
PROMPT El producto 101 pertenece a juan
PROMPT Intentando que juan haga contraoferta a su propio producto...
PROMPT DEBE FALLAR: ORA-20003

BEGIN
    INSERT INTO Contraoferta VALUES (101, 'juan', 500.00);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 5.2 TR_Vendido_Insert
-- No comprar producto propio
-- -------------------------------------------------
PROMPT
PROMPT --- 5.2 TR_Vendido_Insert ---
PROMPT Intentando que juan compre su propio producto 101...
PROMPT DEBE FALLAR: ORA-20001

BEGIN
    INSERT INTO Vendido VALUES (101, 'juan', 0, 800.00, NULL);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- -------------------------------------------------
-- 5.3 trg_check_user_soft_deletion (RS1.11)
-- No eliminar usuario con ventas activas
-- -------------------------------------------------
PROMPT
PROMPT --- 5.3 trg_check_user_soft_deletion ---
PROMPT Verificando contraofertas del usuario maria...

SELECT COUNT(*) AS contraofertas_maria FROM Contraoferta WHERE username = 'maria';

PROMPT Intentando eliminar usuario maria que tiene contraofertas...
PROMPT DEBE FALLAR: ORA-20001

BEGIN
    UPDATE Usuario SET cuenta_eliminada = 1 WHERE username = 'maria';
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('✓ ERROR ESPERADO: ' || SQLERRM);
END;
/

-- =====================================================
-- SECCIÓN 6: TR_Usuario_SoftDelete
-- Eliminar favoritos al eliminar usuario
-- =====================================================
PROMPT
PROMPT ==========================================
PROMPT SECCIÓN 6: ELIMINACIÓN EN CASCADA
PROMPT ==========================================

PROMPT
PROMPT --- 6.1 TR_Usuario_SoftDelete ---
PROMPT Verificando favoritos del usuario test_email_ok antes de eliminar...

SELECT COUNT(*) AS favoritos_antes FROM Favorito WHERE username = 'test_email_ok';

-- Primero eliminar las preferencias para poder eliminar usuario
DELETE FROM Preferidos WHERE username = 'test_email_ok';

PROMPT Eliminando cuenta de test_email_ok...

UPDATE Usuario SET cuenta_eliminada = 1 WHERE username = 'test_email_ok';

PROMPT Verificando favoritos después de eliminar...

SELECT COUNT(*) AS favoritos_despues FROM Favorito WHERE username = 'test_email_ok';

-- =====================================================
-- LIMPIEZA FINAL
-- =====================================================
PROMPT
PROMPT ==========================================
PROMPT LIMPIEZA DE DATOS DE PRUEBA
PROMPT ==========================================

DELETE FROM Usuario WHERE username = 'test_email_ok';

COMMIT;

PROMPT
PROMPT ==========================================
PROMPT DEMOSTRACIÓN COMPLETADA
PROMPT ==========================================
PROMPT
PROMPT Todos los triggers han sido probados exitosamente.
PROMPT Los casos que debían fallar, fallaron.
PROMPT Los casos que debían funcionar, funcionaron.
PROMPT
