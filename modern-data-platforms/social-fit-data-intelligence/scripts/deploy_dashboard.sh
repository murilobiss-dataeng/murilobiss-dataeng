#!/bin/bash

# 🚀 Script de Deploy do Dashboard Social FIT
# ===========================================

set -e

echo "🏋️ Social FIT Dashboard Deploy"
echo "================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar se estamos no diretório correto
if [ ! -f "index.html" ]; then
    log_error "index.html não encontrado! Execute este script na raiz do projeto."
    exit 1
fi

# Verificar se o git está configurado
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "Não é um repositório git!"
    exit 1
fi

# Verificar se há mudanças não commitadas
if [ -n "$(git status --porcelain)" ]; then
    log_warning "Há mudanças não commitadas:"
    git status --short
    echo
    read -p "Deseja continuar mesmo assim? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Deploy cancelado."
        exit 0
    fi
fi

# Verificar se as credenciais do Supabase estão configuradas
if ! grep -q "SUPABASE_URL.*https://" index.html; then
    log_warning "Credenciais do Supabase não configuradas!"
    log_info "Execute: python dashboard/setup_dashboard.py"
    exit 1
fi

log_info "Iniciando deploy..."

# Fazer commit das mudanças (se houver)
if [ -n "$(git status --porcelain)" ]; then
    log_info "Fazendo commit das mudanças..."
    git add .
    git commit -m "🔄 Update dashboard - $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Fazer push para o GitHub
log_info "Fazendo push para GitHub..."
if git push origin main; then
    log_success "Push realizado com sucesso!"
else
    log_error "Erro no push para GitHub!"
    exit 1
fi

# Aguardar um pouco para o GitHub processar
log_info "Aguardando processamento do GitHub..."
sleep 5

# Mostrar informações do deploy
echo
log_success "Deploy iniciado com sucesso!"
echo
echo "🌐 URLs do Dashboard:"
echo "   Principal: https://murilobiss-dataeng.github.io/social_fit/"
echo "   Dashboard: https://murilobiss-dataeng.github.io/social_fit/dashboard/dashboard.html"
echo "   Index:     https://murilobiss-dataeng.github.io/social_fit/index.html"
echo
echo "⏱️  Tempo estimado para deploy: 2-5 minutos"
echo
echo "📊 Para verificar o status:"
echo "   1. GitHub Actions: https://github.com/murilobiss-dataeng/social_fit/actions"
echo "   2. GitHub Pages: https://github.com/murilobiss-dataeng/social_fit/settings/pages"
echo
echo "🔧 Para ativar GitHub Pages manualmente:"
echo "   1. Vá para Settings > Pages"
echo "   2. Source: Deploy from a branch"
echo "   3. Branch: main"
echo "   4. Folder: / (root)"
echo "   5. Save"
echo

# Verificar se o GitHub Pages está ativo
log_info "Verificando status do GitHub Pages..."
if curl -s -o /dev/null -w "%{http_code}" "https://murilobiss-dataeng.github.io/social_fit/" | grep -q "200\|404"; then
    log_success "GitHub Pages está respondendo!"
else
    log_warning "GitHub Pages pode não estar ativo ainda."
    log_info "Verifique: https://github.com/murilobiss-dataeng/social_fit/settings/pages"
fi

echo
log_success "🎉 Deploy concluído! O dashboard estará disponível em alguns minutos." 