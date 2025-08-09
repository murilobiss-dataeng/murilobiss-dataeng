#!/usr/bin/env python3
"""
Script para fazer JOIN automático de todas as tabelas de gaming
e gerar um arquivo CSV consolidado para uso no Tableau.
"""

import pandas as pd
import os

def load_csv_files():
    """Carrega todos os arquivos CSV da pasta atual"""
    print("📁 Carregando arquivos CSV...")
    
    # Carregar cada arquivo CSV
    matches = pd.read_csv('matches.csv')
    match_details = pd.read_csv('match_details.csv')
    medals = pd.read_csv('medals.csv')
    medals_matches_players = pd.read_csv('medals_matches_players.csv')
    players = pd.read_csv('players.csv')
    
    print(f"✅ matches.csv: {len(matches)} registros")
    print(f"✅ match_details.csv: {len(match_details)} registros")
    print(f"✅ medals.csv: {len(medals)} registros")
    print(f"✅ medals_matches_players.csv: {len(medals_matches_players)} registros")
    print(f"✅ players.csv: {len(players)} registros")
    
    return matches, match_details, medals, medals_matches_players, players

def perform_joins(matches, match_details, medals, medals_matches_players, players):
    """Executa todos os JOINs necessários"""
    print("\n🔗 Executando JOINs...")
    
    # 1. JOIN matches + match_details
    print("1️⃣ JOIN: matches + match_details")
    matches_with_details = pd.merge(
        matches, 
        match_details, 
        on='match_id', 
        how='left',
        suffixes=('_match', '_detail')
    )
    print(f"   Resultado: {len(matches_with_details)} registros")
    
    # 2. JOIN com medals_matches_players
    print("2️⃣ JOIN: + medals_matches_players")
    matches_with_medals = pd.merge(
        matches_with_details,
        medals_matches_players,
        on=['match_id', 'player_id'],
        how='left',
        suffixes=('', '_medal_match')
    )
    print(f"   Resultado: {len(matches_with_medals)} registros")
    
    # 3. JOIN com medals
    print("3️⃣ JOIN: + medals")
    matches_with_medal_info = pd.merge(
        matches_with_medals,
        medals,
        on='medal_id',
        how='left',
        suffixes=('', '_medal')
    )
    print(f"   Resultado: {len(matches_with_medal_info)} registros")
    
    # 4. JOIN com players (informações completas do jogador)
    print("4️⃣ JOIN: + players")
    final_dataset = pd.merge(
        matches_with_medal_info,
        players,
        on='player_id',
        how='left',
        suffixes=('', '_player')
    )
    print(f"   Resultado: {len(final_dataset)} registros")
    
    return final_dataset

def clean_and_organize_columns(final_dataset):
    """Organiza e limpa as colunas do dataset final"""
    print("\n🧹 Organizando e limpando colunas...")
    
    # Lista de colunas para manter (sem duplicatas)
    columns_to_keep = [
        # Match Info
        'match_id', 'match_date', 'match_time', 'duration', 'playlist', 
        'map_name', 'mode', 'player_count', 'winner_team',
        
        # Player Info
        'player_id', 'player_name', 'team', 'email', 'registration_date', 
        'last_login', 'player_level',
        
        # Performance Metrics
        'kills', 'deaths', 'assists', 'score', 'accuracy', 'headshots',
        
        # Achievement Info
        'medal_id', 'medal_name', 'medal_type', 'description', 'points', 
        'rarity', 'earned_at', 'match_time_medal_match', 'context',
        
        # Player Stats (totais)
        'total_matches', 'total_kills', 'total_deaths', 'total_score'
    ]
    
    # Filtrar apenas colunas que existem no dataset
    existing_columns = [col for col in columns_to_keep if col in final_dataset.columns]
    
    # Reorganizar colunas de forma lógica
    final_dataset = final_dataset[existing_columns]
    
    # Renomear algumas colunas para clareza
    column_rename = {
        'match_time_medal_match': 'medal_earned_time',
        'total_matches': 'player_total_matches',
        'total_kills': 'player_total_kills',
        'total_deaths': 'player_total_deaths',
        'total_score': 'player_total_score'
    }
    
    final_dataset = final_dataset.rename(columns=column_rename)
    
    print(f"✅ Dataset final com {len(final_dataset)} registros e {len(final_dataset.columns)} colunas")
    
    return final_dataset

def add_calculated_fields(final_dataset):
    """Adiciona campos calculados úteis para análise"""
    print("\n🧮 Adicionando campos calculados...")
    
    # K/D Ratio
    final_dataset['kd_ratio'] = final_dataset.apply(
        lambda row: round(row['kills'] / row['deaths'], 2) if row['deaths'] > 0 else row['kills'],
        axis=1
    )
    
    # Performance Score (fórmula personalizada)
    final_dataset['performance_score'] = final_dataset.apply(
        lambda row: (row['kills'] * 100) + (row['assists'] * 50) + (row['score'] * 10),
        axis=1
    )
    
    # Match Result (Win/Loss)
    final_dataset['match_result'] = final_dataset.apply(
        lambda row: 'Win' if row['team'] == row['winner_team'] else 'Loss',
        axis=1
    )
    
    # Headshot Percentage
    final_dataset['headshot_percentage'] = final_dataset.apply(
        lambda row: round((row['headshots'] / row['kills']) * 100, 1) if row['kills'] > 0 else 0,
        axis=1
    )
    
    # Efficiency Score
    final_dataset['efficiency_score'] = final_dataset.apply(
        lambda row: round((row['kills'] + row['assists']) / (row['deaths'] + 1), 2),
        axis=1
    )
    
    print("✅ Campos calculados adicionados:")
    print("   - K/D Ratio")
    print("   - Performance Score")
    print("   - Match Result")
    print("   - Headshot Percentage")
    print("   - Efficiency Score")
    
    return final_dataset

def save_consolidated_dataset(final_dataset):
    """Salva o dataset consolidado em CSV"""
    print("\n💾 Salvando dataset consolidado...")
    
    # Nome do arquivo
    output_filename = 'gaming_consolidated_dataset.csv'
    
    # Salvar CSV
    final_dataset.to_csv(output_filename, index=False, encoding='utf-8')
    
    print(f"✅ Dataset salvo como: {output_filename}")
    print(f"📊 Tamanho: {len(final_dataset)} registros x {len(final_dataset.columns)} colunas")
    
    # Mostrar primeiras linhas
    print("\n📋 Primeiras 3 linhas do dataset:")
    print(final_dataset.head(3).to_string())
    
    # Mostrar informações do dataset
    print(f"\n📈 Informações do dataset:")
    print(f"   - Total de registros: {len(final_dataset)}")
    print(f"   - Total de colunas: {len(final_dataset.columns)}")
    print(f"   - Jogadores únicos: {final_dataset['player_id'].nunique()}")
    print(f"   - Partidas únicas: {final_dataset['match_id'].nunique()}")
    print(f"   - Medalhas únicas: {final_dataset['medal_id'].nunique()}")
    
    return output_filename

def main():
    """Função principal"""
    print("🎮 GAMING DATASET CONSOLIDATOR")
    print("=" * 50)
    
    try:
        # 1. Carregar arquivos CSV
        matches, match_details, medals, medals_matches_players, players = load_csv_files()
        
        # 2. Executar JOINs
        final_dataset = perform_joins(matches, match_details, medals, medals_matches_players, players)
        
        # 3. Organizar e limpar colunas
        final_dataset = clean_and_organize_columns(final_dataset)
        
        # 4. Adicionar campos calculados
        final_dataset = add_calculated_fields(final_dataset)
        
        # 5. Salvar dataset consolidado
        output_file = save_consolidated_dataset(final_dataset)
        
        print("\n🎉 CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"📁 Arquivo gerado: {output_file}")
        print("\n💡 Agora você pode:")
        print("   1. Abrir este arquivo diretamente no Tableau")
        print("   2. Usar para análise em Python/R")
        print("   3. Importar em outras ferramentas de BI")
        
    except FileNotFoundError as e:
        print(f"❌ Erro: Arquivo não encontrado - {e}")
        print("   Certifique-se de que todos os arquivos CSV estão na mesma pasta")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("   Verifique se os arquivos CSV estão no formato correto")

if __name__ == "__main__":
    main()
