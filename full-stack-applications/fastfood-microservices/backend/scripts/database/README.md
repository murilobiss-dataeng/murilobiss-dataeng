# Scripts de Banco de Dados

Este diretório contém scripts para gerenciar o banco de dados do projeto FastFood.

## Scripts Disponíveis

### 1. `init_database.py`
**Propósito**: Inicializa o banco de dados de forma dinâmica
- ✅ Verifica se as tabelas já existem antes de executar migrações
- ✅ Verifica se os produtos já existem antes de popular
- ✅ Executa migrações Alembic apenas se necessário
- ✅ Popula dados iniciais apenas se a tabela estiver vazia

**Uso**:
```bash
cd backend/scripts/database
python init_database.py
```

### 2. `reset_database.sql`
**Propósito**: Script SQL para resetar completamente o banco
- 🗑️ Remove todas as tabelas
- 🗑️ Remove todas as constraints
- 🗑️ Remove todas as functions
- 🗑️ Remove todas as views
- 🗑️ Remove todas as sequences
- 🗑️ Remove tabela de controle do Alembic

**Uso**:
```bash
# Via psql
psql $DATABASE_URL -f reset_database.sql

# Ou via Python
python reset_database.py
```

### 3. `reset_database.py`
**Propósito**: Script Python para executar o reset de forma segura
- ⚠️ Solicita confirmação antes de executar
- 🚨 Detecta ambiente de produção e avisa
- 🔍 Verifica se o reset foi bem-sucedido
- 📊 Mostra relatório dos objetos restantes

**Uso**:
```bash
cd backend/scripts/database
python reset_database.py
```

### 4. `fresh_start.py`
**Propósito**: Combina reset + inicialização para um fresh start completo
- 🗑️ Reseta completamente o banco
- 🚀 Inicializa com migrações e dados
- ✅ Verifica se tudo funcionou

**Uso**:
```bash
cd backend/scripts/database
python fresh_start.py
```

## Variáveis de Ambiente

Todos os scripts requerem a variável `DATABASE_URL` configurada:

```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
```

## Cenários de Uso

### Desenvolvimento Local
```bash
# Primeira vez
python fresh_start.py

# Apenas inicializar (se tabelas já existem)
python init_database.py

# Reset completo
python reset_database.py
```

### Produção (Render)
```bash
# Apenas inicializar (recomendado)
python init_database.py

# Reset completo (CUIDADO!)
python reset_database.py
```

### Testes
```bash
# Fresh start para testes
python fresh_start.py
```

## Estrutura do Banco

### Tabelas Principais
- `tb_produtos` - Produtos do cardápio
- `tb_categorias` - Categorias de produtos
- `tb_clientes` - Dados dos clientes
- `tb_pedidos` - Pedidos realizados
- `tb_itens_pedido` - Itens de cada pedido
- `tb_pagamentos` - Informações de pagamento
- `tb_fila_pedidos` - Fila de processamento

### Dados Iniciais
- 14 produtos pré-cadastrados
- Categorias: burgers, drinks, sides, desserts
- Preços em formato brasileiro (vírgula decimal)

## Logs e Debugging

Os scripts fornecem logs detalhados:
- ✅ Sucesso
- ❌ Erro
- ⚠️ Aviso
- 🔄 Processando
- 📊 Estatísticas

## Segurança

- Scripts detectam ambiente de produção
- Confirmação obrigatória para reset
- Verificação de resultados
- Tratamento de erros robusto

## Troubleshooting

### Erro: "relation already exists"
- Use `init_database.py` que é dinâmico
- Ou execute `reset_database.py` primeiro

### Erro: "DATABASE_URL not configured"
- Configure a variável de ambiente
- Verifique se está no diretório correto

### Erro: "connection failed"
- Verifique se o banco está rodando
- Confirme as credenciais na DATABASE_URL 