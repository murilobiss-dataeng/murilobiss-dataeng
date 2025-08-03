-- Script para resetar completamente o banco de dados
-- ATENÇÃO: Este script irá deletar TODOS os dados e estruturas!

-- Desabilitar verificação de chaves estrangeiras temporariamente
SET session_replication_role = replica;

-- Deletar todas as tabelas na ordem correta (respeitando dependências)
DROP TABLE IF EXISTS tb_pagamentos CASCADE;
DROP TABLE IF EXISTS tb_itens_pedido CASCADE;
DROP TABLE IF EXISTS tb_pedidos CASCADE;
DROP TABLE IF EXISTS tb_produtos CASCADE;
DROP TABLE IF EXISTS tb_fila_pedidos CASCADE;
DROP TABLE IF EXISTS tb_clientes CASCADE;
DROP TABLE IF EXISTS tb_categorias CASCADE;

-- Deletar tabela de controle do Alembic
DROP TABLE IF EXISTS alembic_version CASCADE;

-- Deletar todas as sequences (se existirem)
DROP SEQUENCE IF EXISTS tb_produtos_id_seq CASCADE;
DROP SEQUENCE IF EXISTS tb_clientes_id_seq CASCADE;
DROP SEQUENCE IF EXISTS tb_pedidos_id_seq CASCADE;
DROP SEQUENCE IF EXISTS tb_pagamentos_id_seq CASCADE;
DROP SEQUENCE IF EXISTS tb_categorias_id_seq CASCADE;
DROP SEQUENCE IF EXISTS tb_fila_pedidos_id_seq CASCADE;

-- Deletar todas as views (se existirem)
DROP VIEW IF EXISTS vw_produtos_categorias CASCADE;
DROP VIEW IF EXISTS vw_pedidos_completos CASCADE;
DROP VIEW IF EXISTS vw_pagamentos_pendentes CASCADE;

-- Deletar todas as functions (se existirem)
DROP FUNCTION IF EXISTS fn_calcular_total_pedido(UUID) CASCADE;
DROP FUNCTION IF EXISTS fn_atualizar_status_pedido(UUID, VARCHAR) CASCADE;
DROP FUNCTION IF EXISTS fn_verificar_produto_disponivel(UUID) CASCADE;

-- Deletar todos os triggers (se existirem)
DROP TRIGGER IF EXISTS tr_audit_pedidos ON tb_pedidos CASCADE;
DROP TRIGGER IF EXISTS tr_audit_produtos ON tb_produtos CASCADE;
DROP TRIGGER IF EXISTS tr_audit_pagamentos ON tb_pagamentos CASCADE;

-- Deletar todas as constraints customizadas (se existirem)
-- (Constraints específicas seriam listadas aqui se existissem)

-- Deletar todos os índices customizados (se existirem)
DROP INDEX IF EXISTS idx_produtos_categoria CASCADE;
DROP INDEX IF EXISTS idx_pedidos_cliente_data CASCADE;
DROP INDEX IF EXISTS idx_pagamentos_status CASCADE;
DROP INDEX IF EXISTS idx_clientes_email CASCADE;
DROP INDEX IF EXISTS idx_clientes_cpf CASCADE;

-- Deletar todos os tipos customizados (se existirem)
DROP TYPE IF EXISTS status_pedido_enum CASCADE;
DROP TYPE IF EXISTS status_pagamento_enum CASCADE;
DROP TYPE IF EXISTS categoria_produto_enum CASCADE;

-- Reabilitar verificação de chaves estrangeiras
SET session_replication_role = DEFAULT;

-- Verificar se tudo foi deletado
DO $$
DECLARE
    table_count INTEGER;
    function_count INTEGER;
    view_count INTEGER;
    sequence_count INTEGER;
BEGIN
    -- Contar tabelas restantes
    SELECT COUNT(*) INTO table_count 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE';
    
    -- Contar functions restantes
    SELECT COUNT(*) INTO function_count 
    FROM information_schema.routines 
    WHERE routine_schema = 'public' 
    AND routine_type = 'FUNCTION';
    
    -- Contar views restantes
    SELECT COUNT(*) INTO view_count 
    FROM information_schema.views 
    WHERE table_schema = 'public';
    
    -- Contar sequences restantes
    SELECT COUNT(*) INTO sequence_count 
    FROM information_schema.sequences 
    WHERE sequence_schema = 'public';
    
    RAISE NOTICE 'Reset concluído! Objetos restantes:';
    RAISE NOTICE '- Tabelas: %', table_count;
    RAISE NOTICE '- Functions: %', function_count;
    RAISE NOTICE '- Views: %', view_count;
    RAISE NOTICE '- Sequences: %', sequence_count;
    
    IF table_count = 0 AND function_count = 0 AND view_count = 0 AND sequence_count = 0 THEN
        RAISE NOTICE '✅ Banco de dados completamente limpo!';
    ELSE
        RAISE NOTICE '⚠️ Alguns objetos ainda existem no banco.';
    END IF;
END $$;

-- Comentário final
COMMENT ON DATABASE current_database() IS 'Banco resetado em ' || current_timestamp; 