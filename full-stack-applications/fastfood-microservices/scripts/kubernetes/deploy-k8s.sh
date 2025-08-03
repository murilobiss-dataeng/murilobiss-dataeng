#!/bin/bash

# 🚀 FastFood Kubernetes Deploy Script
# Script para fazer deploy completo no Kubernetes

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

echo "🍔 FastFood Kubernetes Deploy"
echo "=============================="

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl não está instalado. Instale primeiro."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "k8s/kustomization.yaml" ]; then
    print_error "Execute este script na raiz do projeto FastFood"
    exit 1
fi

# Build Docker image
print_info "🔨 Construindo imagem Docker..."
docker build -f backend/deploy/Dockerfile -t fastfood-api:latest backend/

print_success "Imagem Docker construída!"

# Apply Kubernetes resources
print_info "🚀 Aplicando recursos Kubernetes..."

# Create namespace first
kubectl apply -f k8s/namespace.yaml

# Apply all resources
kubectl apply -k k8s/

print_success "Recursos Kubernetes aplicados!"

# Wait for pods to be ready
print_info "⏳ Aguardando pods ficarem prontos..."
kubectl wait --for=condition=ready pod -l app=fastfood-api -n fastfood --timeout=300s

print_success "Pods prontos!"

# Show status
print_info "📊 Status do deploy:"
kubectl get pods -n fastfood
kubectl get services -n fastfood
kubectl get ingress -n fastfood

# Show logs from init container
print_info "📋 Logs do container de inicialização:"
kubectl logs -n fastfood -l app=fastfood-api -c init-database --tail=50

print_success "✅ Deploy concluído com sucesso!"
print_info "🌐 Acesse: http://fastfood-api.local"
print_info "📚 Documentação: http://fastfood-api.local/docs" 