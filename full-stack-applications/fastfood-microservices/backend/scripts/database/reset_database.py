#!/usr/bin/env python3
"""
Database Reset Script
Executa o script SQL para resetar completamente o banco de dados
ATENÇÃO: Este script irá deletar TODOS os dados!
"""
import os
import sys
import time
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from sqlalchemy import create_engine, text

def get_database_url():
    """Get DATABASE_URL from environment"""
    return os.getenv("DATABASE_URL")

def confirm_reset():
    """Ask for confirmation before resetting database"""
    print("⚠️  ATENÇÃO: Este script irá deletar TODOS os dados do banco!")
    print("📋 Isso inclui:")
    print("   - Todas as tabelas")
    print("   - Todos os dados")
    print("   - Todas as constraints")
    print("   - Todas as functions")
    print("   - Todas as views")
    print("   - Todas as sequences")
    print()
    
    # Check if running in production
    database_url = get_database_url()
    if database_url and "render.com" in database_url:
        print("🚨 PRODUÇÃO DETECTADA!")
        print("Você está prestes a resetar o banco de PRODUÇÃO!")
        print()
    
    response = input("Digite 'RESET' para confirmar: ")
    return response.strip().upper() == "RESET"

def read_sql_script():
    """Read the SQL reset script"""
    script_path = Path(__file__).parent / "reset_database.sql"
    
    if not script_path.exists():
        print(f"❌ Script SQL não encontrado: {script_path}")
        return None
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Erro ao ler script SQL: {e}")
        return None

def execute_reset():
    """Execute the database reset"""
    print("🚀 Iniciando reset do banco de dados...")
    
    database_url = get_database_url()
    if not database_url:
        print("❌ DATABASE_URL não configurada")
        return False
    
    print(f"📡 Conectando em: {database_url}")
    
    # Read SQL script
    sql_script = read_sql_script()
    if not sql_script:
        return False
    
    try:
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        print("✅ Conexão estabelecida!")
        
        # Execute reset script
        print("🔄 Executando script de reset...")
        with engine.connect() as conn:
            # Split script into individual statements
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
            
            for i, statement in enumerate(statements, 1):
                if statement and not statement.startswith('--'):
                    try:
                        print(f"   Executando statement {i}/{len(statements)}...")
                        conn.execute(text(statement))
                        conn.commit()
                    except Exception as e:
                        print(f"   ⚠️ Statement {i} falhou: {e}")
                        # Continue with other statements
        
        print("✅ Reset concluído!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante reset: {e}")
        return False

def verify_reset():
    """Verify that the reset was successful"""
    print("🔍 Verificando resultado do reset...")
    
    try:
        database_url = get_database_url()
        if not database_url:
            return False
            
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check if main tables are gone
            main_tables = ['tb_produtos', 'tb_clientes', 'tb_pedidos', 'tb_pagamentos', 'alembic_version']
            
            for table in main_tables:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    print(f"⚠️ Tabela {table} ainda existe com {count} registros")
                except Exception:
                    print(f"✅ Tabela {table} foi removida")
            
            # Check total tables in public schema
            result = conn.execute(text("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
            """))
            total_tables = result.scalar()
            print(f"📊 Total de tabelas restantes: {total_tables}")
        
        return True
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

def main():
    """Main reset function"""
    print("🗑️  Script de Reset do Banco de Dados")
    print("=" * 50)
    
    # Check if DATABASE_URL is set
    if not get_database_url():
        print("❌ DATABASE_URL não configurada")
        print("Configure a variável de ambiente DATABASE_URL")
        sys.exit(1)
    
    # Ask for confirmation
    if not confirm_reset():
        print("❌ Reset cancelado pelo usuário")
        sys.exit(0)
    
    # Execute reset
    if not execute_reset():
        print("❌ Falha no reset do banco")
        sys.exit(1)
    
    # Verify reset
    if not verify_reset():
        print("⚠️ Verificação do reset falhou")
        sys.exit(1)
    
    print("🎉 Reset do banco concluído com sucesso!")
    print("💡 Execute o script de inicialização para recriar as tabelas")

if __name__ == "__main__":
    main() 