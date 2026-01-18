-- =====================================================
-- SCRIPT PARA ELIMINAR TODA LA BASE DE DATOS TIKITUN
-- =====================================================
-- Ejecutar este script para hacer un DROP completo
-- El orden es importante por las foreign keys
-- =====================================================

-- Primero las tablas con dependencias (hijas)
DROP TABLE Vendido;
DROP TABLE Preferidos;
DROP TABLE Contraoferta;
DROP TABLE Favorito;
DROP TABLE Mensaje;
DROP TABLE Chat;
DROP TABLE Producto;

-- Después las tablas maestras (padres)
DROP TABLE Categoria;
DROP TABLE Usuario;

COMMIT;

-- =====================================================
-- NOTA: Si alguna tabla no existe, Oracle dará error
-- Para ignorar errores, usar en SQLcl/SQL*Plus:
--   SET DEFINE OFF
--   WHENEVER SQLERROR CONTINUE
-- =====================================================
