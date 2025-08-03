#!/usr/bin/env python3
"""
Dashboard Configuration
======================

Configuration management for the Social FIT HTML Dashboard.
"""

import os
from pathlib import Path

class DashboardConfig:
    """Configuration class for the dashboard."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.dashboard_file = self.project_root / "dashboard" / "dashboard.html"
        self.env_file = self.project_root / ".env"
    
    def get_supabase_credentials(self):
        """Get Supabase credentials from environment or .env file."""
        # Try environment variables first
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        # If not in environment, try .env file
        if not supabase_url or not supabase_key:
            if self.env_file.exists():
                with open(self.env_file, 'r') as f:
                    for line in f:
                        if line.startswith('SUPABASE_URL='):
                            supabase_url = line.split('=', 1)[1].strip()
                        elif line.startswith('SUPABASE_ANON_KEY='):
                            supabase_key = line.split('=', 1)[1].strip()
        
        return supabase_url, supabase_key
    
    def update_dashboard_credentials(self, supabase_url, supabase_key):
        """Update the dashboard HTML with Supabase credentials."""
        if not self.dashboard_file.exists():
            raise FileNotFoundError(f"Dashboard file not found: {self.dashboard_file}")
        
        # Read the HTML file
        with open(self.dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace credentials
        import re
        content = re.sub(
            r"const SUPABASE_URL = '[^']*';",
            f"const SUPABASE_URL = '{supabase_url}';",
            content
        )
        
        content = re.sub(
            r"const SUPABASE_KEY = '[^']*';",
            f"const SUPABASE_KEY = '{supabase_key}';",
            content
        )
        
        # Write back to file
        with open(self.dashboard_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    def validate_credentials(self, supabase_url, supabase_key):
        """Validate Supabase credentials."""
        if not supabase_url or not supabase_key:
            return False, "Credenciais não fornecidas"
        
        if not supabase_url.startswith('https://'):
            return False, "URL do Supabase deve começar com https://"
        
        if not supabase_key.startswith('eyJ'):
            return False, "Chave do Supabase parece inválida"
        
        return True, "Credenciais válidas"
    
    def get_dashboard_url(self):
        """Get the dashboard URL for GitHub Pages."""
        # This would be the actual GitHub Pages URL
        return "https://seu-usuario.github.io/social_fit/dashboard/dashboard.html" 