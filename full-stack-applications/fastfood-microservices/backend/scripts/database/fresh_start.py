#!/usr/bin/env python3
"""
Fresh Start Script
Combina reset completo do banco + inicialização
Útil para desenvolvimento e testes
"""
import os
import sys
import subprocess
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n🔄 {description}...")
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"❌ Script não encontrado: {script_path}")
        return False
    
    try:
        # Run the script
        result = subprocess.run([
            sys.executable, str(script_path)
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} concluído!")
            return True
        else:
            print(f"❌ {description} falhou!")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar {script_name}: {e}")
        return False

def main():
    """Main fresh start function"""
    print("🔄 Script de Fresh Start - Reset + Inicialização")
    print("=" * 60)
    
    # Check if DATABASE_URL is set
    if not os.getenv("DATABASE_URL"):
        print("❌ DATABASE_URL não configurada")
        print("Configure a variável de ambiente DATABASE_URL")
        sys.exit(1)
    
    print("📋 Este script irá:")
    print("   1. Resetar completamente o banco de dados")
    print("   2. Executar migrações Alembic")
    print("   3. Popular dados iniciais")
    print("   4. Verificar a configuração")
    print()
    
    response = input("Continuar? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Operação cancelada")
        sys.exit(0)
    
    # Step 1: Reset database
    if not run_script("reset_database.py", "Resetando banco de dados"):
        print("❌ Falha no reset do banco")
        sys.exit(1)
    
    # Step 2: Initialize database
    if not run_script("init_database.py", "Inicializando banco de dados"):
        print("❌ Falha na inicialização do banco")
        sys.exit(1)
    
    print("\n🎉 Fresh start concluído com sucesso!")
    print("✅ Banco de dados resetado e inicializado")
    print("🚀 Aplicação pronta para uso!")

if __name__ == "__main__":
    main() 