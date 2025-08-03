#!/bin/bash

# 🔍 FastFood Deploy Verification Script
# Script para verificar se o deploy está funcionando

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

# URLs
BACKEND_URL="https://fastfood-api.onrender.com"
FRONTEND_URL="https://fastfood-murex.vercel.app"

echo "🔍 FastFood Deploy Verification"
echo "================================"

# Check if curl is available
if ! command -v curl &> /dev/null; then
    print_error "curl não está instalado. Instale curl para continuar."
    exit 1
fi

echo ""
print_info "🔧 Verificando Backend (Render)..."
echo ""

# Health Check
print_info "Testando Health Check..."
if curl -s -f "$BACKEND_URL/health" > /dev/null; then
    print_success "✅ Health Check: OK"
else
    print_error "❌ Health Check: FALHOU"
fi

# API Documentation
print_info "Testando API Documentation..."
if curl -s -f "$BACKEND_URL/docs" > /dev/null; then
    print_success "✅ API Docs: OK"
else
    print_error "❌ API Docs: FALHOU"
fi

# Products Endpoint
print_info "Testando Endpoint de Produtos..."
PRODUCTS_RESPONSE=$(curl -s "$BACKEND_URL/v1/api/public/produtos" 2>/dev/null || echo "ERROR")
if [[ "$PRODUCTS_RESPONSE" != "ERROR" ]] && [[ "$PRODUCTS_RESPONSE" != "" ]]; then
    PRODUCT_COUNT=$(echo "$PRODUCTS_RESPONSE" | grep -o '"id"' | wc -l)
    print_success "✅ Produtos: $PRODUCT_COUNT produtos encontrados"
else
    print_error "❌ Produtos: FALHOU"
fi

echo ""
print_info "🌐 Verificando Frontend (Vercel)..."
echo ""

# Frontend Check
print_info "Testando Frontend..."
if curl -s -f "$FRONTEND_URL" > /dev/null; then
    print_success "✅ Frontend: OK"
else
    print_error "❌ Frontend: FALHOU"
fi

echo ""
print_info "🔗 Verificando Integração..."
echo ""

# Check if frontend can access backend
print_info "Testando CORS..."
CORS_TEST=$(curl -s -I -H "Origin: $FRONTEND_URL" "$BACKEND_URL/v1/api/public/produtos" 2>/dev/null | grep -i "access-control-allow-origin" || echo "NO_CORS")
if [[ "$CORS_TEST" != "NO_CORS" ]]; then
    print_success "✅ CORS: Configurado corretamente"
else
    print_warning "⚠️ CORS: Não verificado (pode estar funcionando)"
fi

echo ""
print_info "📊 Resumo dos Testes:"
echo ""

# Summary
echo "🔗 URLs de Produção:"
echo "   Backend: $BACKEND_URL"
echo "   Frontend: $FRONTEND_URL"
echo "   API Docs: $BACKEND_URL/docs"
echo "   Health: $BACKEND_URL/health"
echo ""

echo "🎯 Próximos Passos:"
echo "   1. Acesse o frontend: $FRONTEND_URL"
echo "   2. Teste o carrinho de compras"
echo "   3. Faça um pedido de teste"
echo "   4. Verifique os logs no Render"
echo ""

print_success "✅ Verificação concluída!"
print_info "💡 Dica: Use 'curl -v' para ver detalhes das requisições" 