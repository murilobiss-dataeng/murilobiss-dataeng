#!/bin/bash

# 🚀 FastFood Complete Deploy Script
# Script para fazer deploy completo em todos os ambientes

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

echo "🍔 FastFood Complete Deploy"
echo "==========================="

# Check if we're in the right directory
if [ ! -f "deploy/render.yaml" ]; then
    print_error "Execute este script na raiz do projeto FastFood"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
print_info "🔍 Verificando pré-requisitos..."

if ! command_exists git; then
    print_error "git não está instalado"
    exit 1
fi

if ! command_exists curl; then
    print_error "curl não está instalado"
    exit 1
fi

print_success "Pré-requisitos verificados!"

# Check git status
print_info "📋 Verificando status do Git..."
if [ -n "$(git status --porcelain)" ]; then
    print_warning "Há mudanças não commitadas. Deseja continuar? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_info "Deploy cancelado"
        exit 0
    fi
fi

# Push to repository
print_info "📤 Fazendo push para o repositório..."
git add .
git commit -m "deploy: atualização automática $(date)" || true
git push

print_success "Push realizado!"

# Wait for deployments
print_info "⏳ Aguardando deploys..."
print_info "Render (Backend): ~2-3 minutos"
print_info "Vercel (Frontend): ~1-2 minutos"

sleep 30

# Verify deployments
print_info "🔍 Verificando deploys..."
./scripts/verify/verify-deploy.sh

print_success "✅ Deploy completo realizado!"
print_info "🌐 URLs de produção:"
print_info "   Frontend: https://fastfood-murex.vercel.app"
print_info "   Backend: https://fastfood-api.onrender.com"
print_info "   API Docs: https://fastfood-api.onrender.com/docs" 