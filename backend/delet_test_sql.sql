DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Opcional: restaurar as permissões padrão do postgres
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;