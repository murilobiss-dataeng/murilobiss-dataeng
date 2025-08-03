#!/bin/bash

# 🍔 FastFood - Script Principal
# Script centralizado para gerenciar o projeto

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

show_help() {
    echo "🍔 FastFood - Script Principal"
    echo "=============================="
    echo ""
    echo "Comandos disponíveis:"
    echo ""
    echo "  setup         - Configurar variáveis de ambiente"
    echo "  verify        - Verificar deploy"
    echo "  deploy        - Deploy completo"
    echo "  k8s           - Deploy Kubernetes"
    echo "  dev           - Desenvolvimento backend local"
    echo "  dev-frontend  - Desenvolvimento frontend local"
    echo "  test          - Executar testes"
    echo "  clean         - Limpar arquivos temporários"
    echo "  help          - Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  ./scripts/main.sh setup"
    echo "  ./scripts/main.sh verify"
    echo "  ./scripts/main.sh dev"
    echo "  ./scripts/main.sh dev-frontend"
}

run_setup() {
    print_info "Executando setup..."
    ./scripts/setup/setup-env.sh
}

run_verify() {
    print_info "Verificando deploy..."
    ./scripts/verify/verify-deploy.sh
}

run_deploy() {
    print_info "Executando deploy..."
    ./scripts/deploy/deploy.sh
}

run_k8s() {
    print_info "Deploy Kubernetes..."
    ./scripts/kubernetes/deploy-k8s.sh
}

run_dev() {
    print_info "Iniciando desenvolvimento local..."
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 não está instalado"
        exit 1
    fi
    
    # Check if pip is installed
    if ! command -v pip &> /dev/null; then
        print_error "pip não está instalado"
        exit 1
    fi
    
    cd backend
    
    # Install dependencies
    print_info "Instalando dependências..."
    pip install -r requirements.txt
    
    # Run database initialization
    print_info "Inicializando banco de dados..."
    python scripts/database/init_database.py
    
    # Start development server
    print_info "Iniciando servidor de desenvolvimento..."
    print_info "Backend: http://localhost:8000"
    print_info "API Docs: http://localhost:8000/docs"
    print_info "Health: http://localhost:8000/health"
    uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
}

run_dev_frontend() {
    print_info "Iniciando desenvolvimento do frontend..."
    
    cd frontend
    
    # Check if Python is available for simple server
    if command -v python3 &> /dev/null; then
        print_info "Iniciando servidor Python..."
        print_info "Frontend: http://localhost:3000"
        python3 -m http.server 3000
    elif command -v python &> /dev/null; then
        print_info "Iniciando servidor Python..."
        print_info "Frontend: http://localhost:3000"
        python -m http.server 3000
    elif command -v npx &> /dev/null; then
        print_info "Iniciando servidor Node.js..."
        print_info "Frontend: http://localhost:3000"
        npx serve . -p 3000
    else
        print_error "Nenhum servidor disponível. Instale Python ou Node.js"
        print_info "Ou abra o arquivo frontend/index.html diretamente no navegador"
        exit 1
    fi
}

run_test() {
    print_info "Executando testes..."
    
    cd backend
    
    # Check if pytest is installed
    if ! python -c "import pytest" 2>/dev/null; then
        print_info "Instalando pytest..."
        pip install pytest
    fi
    
    # Run tests
    python -m pytest tests/ -v
}

run_clean() {
    print_info "Limpando arquivos temporários..."
    
    # Remove Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Remove node modules (if any)
    rm -rf node_modules/ 2>/dev/null || true
    
    # Remove build artifacts
    rm -rf build/ dist/ *.egg-info/ 2>/dev/null || true
    
    print_success "Limpeza concluída!"
}

# Main script logic
case "${1:-help}" in
    setup)
        run_setup
        ;;
    verify)
        run_verify
        ;;
    deploy)
        run_deploy
        ;;
    k8s)
        run_k8s
        ;;
    dev)
        run_dev
        ;;
    dev-frontend)
        run_dev_frontend
        ;;
    test)
        run_test
        ;;
    clean)
        run_clean
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Comando inválido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac 