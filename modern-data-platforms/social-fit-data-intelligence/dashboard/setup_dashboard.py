#!/usr/bin/env python3
"""
Setup Script for Social FIT HTML Dashboard
==========================================

Script to configure Supabase credentials in the HTML dashboard.
"""

import os
import re
from pathlib import Path

def get_supabase_credentials():
    """Get Supabase credentials from environment or .env file."""
    # Try to get from environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    # If not in environment, try to read from .env file
    if not supabase_url or not supabase_key:
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('SUPABASE_URL='):
                        supabase_url = line.split('=', 1)[1].strip()
                    elif line.startswith('SUPABASE_ANON_KEY='):
                        supabase_key = line.split('=', 1)[1].strip()
    
    return supabase_url, supabase_key

def update_dashboard_html(supabase_url, supabase_key):
    """Update the dashboard.html file with Supabase credentials."""
    dashboard_file = Path('dashboard.html')
    
    if not dashboard_file.exists():
        print("❌ dashboard.html não encontrado!")
        return False
    
    # Read the HTML file
    with open(dashboard_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the placeholder credentials
    content = re.sub(
        r"const SUPABASE_URL = 'YOUR_SUPABASE_URL';",
        f"const SUPABASE_URL = '{supabase_url}';",
        content
    )
    
    content = re.sub(
        r"const SUPABASE_KEY = 'YOUR_SUPABASE_ANON_KEY';",
        f"const SUPABASE_KEY = '{supabase_key}';",
        content
    )
    
    # Write back to file
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Main function to setup the dashboard."""
    print("🚀 Social FIT HTML Dashboard Setup")
    print("=" * 40)
    
    # Get Supabase credentials
    supabase_url, supabase_key = get_supabase_credentials()
    
    if not supabase_url or not supabase_key:
        print("❌ Credenciais do Supabase não encontradas!")
        print("💡 Certifique-se de que o arquivo .env existe com:")
        print("   SUPABASE_URL=sua_url_do_supabase")
        print("   SUPABASE_ANON_KEY=sua_chave_anonima")
        return
    
    print(f"✅ URL do Supabase: {supabase_url}")
    print(f"✅ Chave anônima: {supabase_key[:20]}...")
    
    # Update dashboard HTML
    if update_dashboard_html(supabase_url, supabase_key):
        print("✅ Dashboard HTML atualizado com sucesso!")
        print()
        print("🌐 Para usar o dashboard:")
        print("1. Abra o arquivo dashboard.html no navegador")
        print("2. Ou hospede no GitHub Pages:")
        print("   - Faça commit do dashboard.html")
        print("   - Vá em Settings > Pages")
        print("   - Selecione 'Deploy from a branch'")
        print("   - Escolha a branch main")
        print("   - Acesse: https://seu-usuario.github.io/social_fit/dashboard.html")
        print()
        print("📱 O dashboard será acessível publicamente!")
    else:
        print("❌ Erro ao atualizar o dashboard HTML")

if __name__ == "__main__":
    main() 