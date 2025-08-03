#!/usr/bin/env python3
"""
Script para verificar dados do dashboard
========================================

Verifica se há dados nas tabelas e testa os cálculos.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import after adding to path
try:
    from database.database import DatabaseManager
    from config.config import Config
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    print("💡 Execute: python3 -m src.database.database")
    sys.exit(1)

def check_dashboard_data():
    """Verifica os dados das tabelas para o dashboard."""
    
    print("🔍 Verificando dados do dashboard...")
    print("=" * 50)
    
    # Carregar configuração
    try:
        config = Config()
        db = DatabaseManager(config)
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        return
    
    try:
        # Conectar ao banco
        db.connect()
        print("✅ Conexão com Supabase estabelecida")
        
        # Verificar tabela students
        print("\n📊 Tabela 'students':")
        students_query = "SELECT COUNT(*) as total FROM students"
        result = db.execute_query(students_query)
        total_students = result[0]['total'] if result else 0
        print(f"   Total de alunos: {total_students}")
        
        if total_students > 0:
            # Verificar dados detalhados
            students_detail = db.execute_query("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN status = 'Ativo' THEN 1 END) as ativos,
                    COUNT(CASE WHEN status = 'Inativo' THEN 1 END) as inativos,
                    COUNT(CASE WHEN gender = 'Masculino' THEN 1 END) as masculino,
                    COUNT(CASE WHEN gender = 'Feminino' THEN 1 END) as feminino,
                    COUNT(CASE WHEN plan IS NOT NULL THEN 1 END) as com_plano,
                    SUM(CASE WHEN status = 'Ativo' THEN monthly_fee ELSE 0 END) as receita_mensal
                FROM students
            """)
            
            if students_detail:
                data = students_detail[0]
                print(f"   Alunos ativos: {data['ativos']}")
                print(f"   Alunos inativos: {data['inativos']}")
                print(f"   Masculino: {data['masculino']}")
                print(f"   Feminino: {data['feminino']}")
                print(f"   Com plano: {data['com_plano']}")
                print(f"   Receita mensal: R$ {data['receita_mensal']:,.2f}")
            
            # Verificar planos
            plans_query = "SELECT plan, COUNT(*) as count FROM students WHERE plan IS NOT NULL GROUP BY plan ORDER BY count DESC"
            plans_result = db.execute_query(plans_query)
            print(f"\n   Planos:")
            for plan in plans_result:
                print(f"     {plan['plan']}: {plan['count']}")
            
            # Verificar bairros
            neighborhoods_query = "SELECT neighborhood, COUNT(*) as count FROM students WHERE neighborhood IS NOT NULL GROUP BY neighborhood ORDER BY count DESC LIMIT 10"
            neighborhoods_result = db.execute_query(neighborhoods_query)
            print(f"\n   Top 10 Bairros:")
            for neighborhood in neighborhoods_result:
                print(f"     {neighborhood['neighborhood']}: {neighborhood['count']}")
        
        # Verificar tabela instagram_posts
        print("\n📱 Tabela 'instagram_posts':")
        posts_query = "SELECT COUNT(*) as total FROM instagram_posts"
        posts_result = db.execute_query(posts_query)
        total_posts = posts_result[0]['total'] if posts_result else 0
        print(f"   Total de posts: {total_posts}")
        
        if total_posts > 0:
            posts_detail = db.execute_query("""
                SELECT 
                    COUNT(*) as total,
                    SUM(likes) as total_likes,
                    SUM(comments) as total_comments,
                    SUM(saves) as total_saves,
                    AVG(likes) as avg_likes,
                    AVG(comments) as avg_comments,
                    AVG(saves) as avg_saves
                FROM instagram_posts
            """)
            
            if posts_detail:
                data = posts_detail[0]
                print(f"   Total de likes: {data['total_likes']}")
                print(f"   Total de comments: {data['total_comments']}")
                print(f"   Total de saves: {data['total_saves']}")
                print(f"   Média de likes: {data['avg_likes']:.1f}")
                print(f"   Média de comments: {data['avg_comments']:.1f}")
                print(f"   Média de saves: {data['avg_saves']:.1f}")
        
        # Verificar tabela analytics
        print("\n📈 Tabela 'analytics':")
        analytics_query = "SELECT COUNT(*) as total FROM analytics"
        analytics_result = db.execute_query(analytics_query)
        total_analytics = analytics_result[0]['total'] if analytics_result else 0
        print(f"   Total de analytics: {total_analytics}")
        
        if total_analytics > 0:
            analytics_detail = db.execute_query("""
                SELECT 
                    COUNT(*) as total,
                    AVG(engagement_rate) as avg_engagement,
                    AVG(correlation_score) as avg_correlation,
                    MAX(created_at) as last_update
                FROM analytics
            """)
            
            if analytics_detail:
                data = analytics_detail[0]
                print(f"   Engajamento médio: {data['avg_engagement']:.2f}%")
                print(f"   Correlação média: {data['avg_correlation']:.2f}")
                print(f"   Última atualização: {data['last_update']}")
        
        # Verificar se há dados suficientes
        print("\n🎯 Status dos dados:")
        if total_students > 0:
            print("✅ Dados de alunos disponíveis")
        else:
            print("❌ Nenhum aluno encontrado")
            
        if total_posts > 0:
            print("✅ Dados do Instagram disponíveis")
        else:
            print("❌ Nenhum post do Instagram encontrado")
            
        if total_analytics > 0:
            print("✅ Dados de analytics disponíveis")
        else:
            print("❌ Nenhum analytics encontrado")
        
        # Sugestões
        print("\n💡 Sugestões:")
        if total_students == 0:
            print("   - Execute o pipeline ETL para carregar dados de alunos")
        if total_posts == 0:
            print("   - Execute o pipeline ETL para carregar dados do Instagram")
        if total_analytics == 0:
            print("   - Execute o pipeline ETL para gerar analytics")
        
        if total_students > 0 and total_posts > 0 and total_analytics > 0:
            print("   - Todos os dados estão disponíveis! O dashboard deve funcionar corretamente.")
        
    except Exception as e:
        print(f"❌ Erro ao verificar dados: {e}")
    finally:
        try:
            db.close()
        except:
            pass

if __name__ == "__main__":
    check_dashboard_data() 