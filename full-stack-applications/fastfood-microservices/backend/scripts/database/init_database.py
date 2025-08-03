#!/usr/bin/env python3
"""
Database Initialization Script
Combines Alembic migrations and data population
Uses environment variables from Render
"""
import os
import sys
import time
import uuid
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from sqlalchemy import create_engine, text
from alembic.config import Config
from alembic import command

def get_database_url():
    """Get DATABASE_URL from environment"""
    return os.getenv("DATABASE_URL")

def wait_for_database(max_retries=30, delay=2):
    """Wait for database to be ready"""
    print("🔄 Aguardando banco de dados ficar disponível...")
    
    database_url = get_database_url()
    if not database_url:
        print("❌ DATABASE_URL não configurada")
        return False
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(database_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Banco de dados disponível!")
            return True
        except Exception as e:
            print(f"⏳ Tentativa {attempt + 1}/{max_retries}: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    
    print("❌ Banco de dados não ficou disponível")
    return False

def check_table_exists(engine, table_name):
    """Check if a table exists in the database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table_name}'
                )
            """))
            return result.scalar()
    except Exception:
        return False

def check_migration_status():
    """Check if migrations have already been applied"""
    print("🔍 Verificando status das migrações...")
    
    try:
        database_url = get_database_url()
        if not database_url:
            print("❌ DATABASE_URL não configurada")
            return False
            
        engine = create_engine(database_url)
        
        # Check if alembic_version table exists
        if not check_table_exists(engine, 'alembic_version'):
            print("📋 Tabela alembic_version não existe - primeira execução")
            return False
        
        # Check if main tables exist
        main_tables = ['tb_produtos', 'tb_clientes', 'tb_pedidos']
        existing_tables = []
        
        for table in main_tables:
            if check_table_exists(engine, table):
                existing_tables.append(table)
        
        if existing_tables:
            print(f"✅ Tabelas existentes encontradas: {', '.join(existing_tables)}")
            return True
        else:
            print("📋 Nenhuma tabela principal encontrada")
            return False
            
    except Exception as e:
        print(f"⚠️ Erro ao verificar status: {e}")
        return False

def run_migrations():
    """Run Alembic migrations only if needed"""
    print("🔄 Verificando necessidade de migrações...")
    
    # Check if migrations are already applied
    if check_migration_status():
        print("✅ Migrações já aplicadas, pulando...")
        return True
    
    print("🔄 Executando migrações Alembic...")
    
    try:
        # Get the alembic.ini path from the config directory
        alembic_cfg = Config(str(Path(__file__).parent.parent.parent / "config" / "alembic.ini"))
        
        # Run migrations
        command.upgrade(alembic_cfg, "head")
        print("✅ Migrações executadas com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao executar migrações: {e}")
        return False

def check_products_exist():
    """Check if products already exist in the database"""
    try:
        database_url = get_database_url()
        if not database_url:
            return False
            
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM tb_produtos"))
            count = result.scalar()
            return count is not None and count > 0
    except Exception:
        return False

def populate_products():
    """Populate products table only if empty"""
    print("🔄 Verificando produtos existentes...")
    
    if check_products_exist():
        print("✅ Produtos já existem, pulando população...")
        return True
    
    print("🔄 Populando tabela de produtos...")
    
    try:
        database_url = get_database_url()
        if not database_url:
            print("❌ DATABASE_URL não configurada")
            return False
            
        engine = create_engine(database_url)
        
        # Verificar se a constraint única existe
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT COUNT(*) FROM information_schema.table_constraints 
                WHERE table_name = 'tb_produtos' 
                AND constraint_name = 'uq_produto_nome' 
                AND constraint_type = 'UNIQUE'
            """))
            has_unique_constraint = result.scalar() > 0
        
        # SQL para inserir produtos (com ou sem ON CONFLICT baseado na constraint)
        if has_unique_constraint:
            print("✅ Constraint única encontrada, usando ON CONFLICT")
            produtos_sql = f"""
            INSERT INTO tb_produtos (id, nome, categoria, preco) VALUES
            ('{uuid.uuid4()}', 'Hambúrguer Clássico', 'burgers', 15.90),
            ('{uuid.uuid4()}', 'Hambúrguer Duplo', 'burgers', 22.50),
            ('{uuid.uuid4()}', 'X-Bacon', 'burgers', 18.90),
            ('{uuid.uuid4()}', 'X-Salada', 'burgers', 16.90),
            ('{uuid.uuid4()}', 'X-Frango', 'burgers', 17.90),
            ('{uuid.uuid4()}', 'Refrigerante Cola', 'drinks', 5.00),
            ('{uuid.uuid4()}', 'Suco Natural', 'drinks', 6.50),
            ('{uuid.uuid4()}', 'Água Mineral', 'drinks', 3.50),
            ('{uuid.uuid4()}', 'Batata Frita', 'sides', 8.50),
            ('{uuid.uuid4()}', 'Onion Rings', 'sides', 7.90),
            ('{uuid.uuid4()}', 'Nuggets', 'sides', 9.90),
            ('{uuid.uuid4()}', 'Sorvete de Chocolate', 'desserts', 4.50),
            ('{uuid.uuid4()}', 'Pudim', 'desserts', 5.90),
            ('{uuid.uuid4()}', 'Milk Shake', 'desserts', 12.90)
            ON CONFLICT (nome) DO NOTHING;
            """
        else:
            print("⚠️ Constraint única não encontrada, inserindo sem ON CONFLICT")
            produtos_sql = f"""
            INSERT INTO tb_produtos (id, nome, categoria, preco) VALUES
            ('{uuid.uuid4()}', 'Hambúrguer Clássico', 'burgers', 15.90),
            ('{uuid.uuid4()}', 'Hambúrguer Duplo', 'burgers', 22.50),
            ('{uuid.uuid4()}', 'X-Bacon', 'burgers', 18.90),
            ('{uuid.uuid4()}', 'X-Salada', 'burgers', 16.90),
            ('{uuid.uuid4()}', 'X-Frango', 'burgers', 17.90),
            ('{uuid.uuid4()}', 'Refrigerante Cola', 'drinks', 5.00),
            ('{uuid.uuid4()}', 'Suco Natural', 'drinks', 6.50),
            ('{uuid.uuid4()}', 'Água Mineral', 'drinks', 3.50),
            ('{uuid.uuid4()}', 'Batata Frita', 'sides', 8.50),
            ('{uuid.uuid4()}', 'Onion Rings', 'sides', 7.90),
            ('{uuid.uuid4()}', 'Nuggets', 'sides', 9.90),
            ('{uuid.uuid4()}', 'Sorvete de Chocolate', 'desserts', 4.50),
            ('{uuid.uuid4()}', 'Pudim', 'desserts', 5.90),
            ('{uuid.uuid4()}', 'Milk Shake', 'desserts', 12.90);
            """
        
        with engine.connect() as conn:
            conn.execute(text(produtos_sql))
            conn.commit()
        
        # Verify insertion
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM tb_produtos"))
            count = result.scalar()
            print(f"✅ {count} produtos inseridos com sucesso!")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao popular produtos: {e}")
        return False

def verify_database():
    """Verify database setup"""
    print("🔍 Verificando configuração do banco...")
    
    try:
        database_url = get_database_url()
        if not database_url:
            print("❌ DATABASE_URL não configurada")
            return False
            
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check tables (usando nomes corretos com prefixo tb_)
            tables = ['tb_produtos', 'tb_categorias', 'tb_clientes', 'tb_pedidos', 'tb_pagamentos']
            for table in tables:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"📊 Tabela {table}: {count} registros")
                except Exception as e:
                    print(f"⚠️ Tabela {table}: {e}")
        
        print("✅ Verificação concluída!")
        return True
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

def main():
    """Main initialization function"""
    print("🚀 Iniciando configuração do banco de dados...")
    
    database_url = get_database_url()
    if database_url:
        print(f"📡 Conectando em: {database_url}")
    else:
        print("❌ DATABASE_URL não configurada")
        sys.exit(1)
    
    # Step 1: Wait for database
    if not wait_for_database():
        sys.exit(1)
    
    # Step 2: Run migrations (only if needed)
    if not run_migrations():
        sys.exit(1)
    
    # Step 3: Populate products (only if needed)
    if not populate_products():
        sys.exit(1)
    
    # Step 4: Verify setup
    if not verify_database():
        sys.exit(1)
    
    print("🎉 Configuração do banco concluída com sucesso!")

if __name__ == "__main__":
    main() 