# 🍔 FastFood - Sistema de Autoatendimento

Sistema completo de autoatendimento para restaurantes fast food, desenvolvido com arquitetura hexagonal e tecnologias modernas.

## ✨ Funcionalidades

- ✅ Interface responsiva e moderna
- ✅ Carrinho de compras funcional
- ✅ Sistema de pedidos completo
- ✅ API REST documentada
- ✅ Autenticação JWT
- ✅ Banco de dados PostgreSQL
- ✅ Deploy automatizado
- ✅ Auto scaling
- ✅ Health checks
- ✅ Produtos populados automaticamente

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (Vercel)      │◄──►│   (Render)      │◄──►│  (Render)       │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │    │ • FastAPI       │    │ • PostgreSQL    │
│ • Responsive    │    │ • Hexagonal     │    │ • Managed       │
│ • PWA Ready     │    │ • Clean Code    │    │ • Backups       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Backend - Arquitetura Hexagonal**
- **API Layer**: Controllers e DTOs
- **Application Layer**: Services e Use Cases
- **Domain Layer**: Models e Business Logic
- **Infrastructure Layer**: Repositories e External Services

## 🛠️ Tecnologias

### **Backend**
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL (Render)
- **ORM**: SQLAlchemy + Alembic
- **Auth**: JWT
- **Validation**: Pydantic
- **Testing**: pytest

### **Frontend**
- **Language**: Vanilla JavaScript
- **Styling**: CSS3 + Flexbox/Grid
- **Icons**: Font Awesome
- **Responsive**: Mobile-first

### **Infrastructure**
- **Frontend Host**: Vercel
- **Backend Host**: Render
- **Database**: Render PostgreSQL
- **Container**: Docker
- **CI/CD**: GitHub Actions (opcional)

## 📁 Estrutura do Projeto

```
fastfood/
├── 📁 backend/                    # API FastAPI
│   ├── 📁 src/                    # Código fonte
│   │   ├── 📁 adapters/           # Controllers e DTOs
│   │   ├── 📁 application/        # Services
│   │   ├── 📁 domain/             # Models
│   │   ├── 📁 infrastructure/     # Repositories
│   │   └── 📁 ports/              # Interfaces
│   ├── 📁 config/                 # Configurações
│   │   ├── 📁 alembic/            # Migrations
│   │   └── 📄 alembic.ini         # Config Alembic
│   ├── 📁 deploy/                 # Deploy
│   │   ├── 🐳 Dockerfile          # Container
│   │   ├── 📄 .render-buildpacks  # Render config
│   │   └── 📄 runtime.txt         # Python version
│   ├── 📁 scripts/                # Scripts utilitários
│   │   ├── 📁 database/           # Scripts de banco
│   │   └── 📁 utils/              # Utilitários
│   ├── 📦 requirements.txt        # Dependências Python
│   └── 📄 main.py                 # Entry point
├── 📁 frontend/                   # Interface web
│   ├── 📁 assets/                 # Recursos estáticos
│   │   ├── 📁 css/                # Estilos
│   │   ├── 📁 js/                 # JavaScript
│   │   └── 📁 images/             # Imagens
│   ├── 📁 components/             # Componentes
│   ├── 📁 pages/                  # Páginas
│   ├── 📁 utils/                  # Utilitários
│   └── 📄 index.html              # Página principal
├── 📁 deploy/                     # Configurações de deploy
│   ├── 📋 render.yaml             # Config Render
│   └── 🌐 vercel.json             # Config Vercel
├── 📁 scripts/                    # Scripts de automação
│   ├── 📁 deploy/                 # Scripts de deploy
│   ├── 📁 setup/                  # Scripts de setup
│   ├── 📁 verify/                 # Scripts de verificação
│   ├── 📁 kubernetes/             # Scripts K8s
│   └── 🚀 main.sh                 # Script principal
├── 📁 docs/                       # Documentação
│   ├── 📁 architecture/           # Diagramas de arquitetura
│   ├── 📁 api/                    # Documentação da API
│   ├── 📁 deployment/             # Guias de deploy
│   └── 📁 development/            # Documentação de desenvolvimento
├── 📁 k8s/                        # Kubernetes (opcional)
├── 🚀 scripts/main.sh             # Script principal
└── 📖 README.md                   # Este arquivo
```

## 🚀 Deploy Rápido

### **1. Pré-requisitos**
```bash
# Clone o repositório
git clone https://github.com/murilobiss/fastfood.git
cd fastfood

# Execute o script principal
./scripts/main.sh setup
```

### **2. Deploy Automático**

#### **Backend (Render)**
1. Acesse [Render.com](https://render.com)
2. New Web Service → Connect Repository
3. Selecione o repositório `fastfood`
4. Configure as variáveis de ambiente (ver script setup)
5. Deploy automático

#### **Frontend (Vercel)**
1. Acesse [Vercel.com](https://vercel.com)
2. New Project → Import Git Repository
3. Configure Output Directory: `frontend`
4. Deploy automático

### **3. Variáveis de Ambiente (Render)**

Todas as variáveis são configuradas automaticamente no Render:

```env
DATABASE_URL=postgresql://postech:password@host:port/db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-admin-password
ENVIRONMENT=production
DEBUG=false
CORS_ALLOW_ORIGINS=https://fastfood-murex.vercel.app
API_PREFIX=/v1
PROJECT_NAME=FastFood API
VERSION=1.0.0
LOG_LEVEL=INFO
```

## 🧪 Desenvolvimento Local

### **Usando o Script Principal**
```bash
# Iniciar desenvolvimento
./scripts/main.sh dev

# Executar testes
./scripts/main.sh test

# Verificar deploy
./scripts/main.sh verify

# Limpar arquivos temporários
./scripts/main.sh clean
```

### **Manual**
```bash
# Frontend
cd frontend
python -m http.server 3000

# Backend
cd backend
pip install -r requirements.txt
python scripts/database/init_database.py
uvicorn src.main:app --reload
```

### **Build Docker manual/local**

Se for rodar o build manualmente, use:
```bash
docker build -f backend/deploy/Dockerfile -t fastfood-api:latest backend/
```

## 📊 API Endpoints

### **Públicos**
- `GET /health` - Health check
- `GET /v1/api/public/produtos` - Listar produtos
- `POST /v1/api/public/pedidos` - Criar pedido
- `GET /v1/api/public/pedidos/{id}` - Consultar pedido

### **Administrativos**
- `POST /v1/api/public/login` - Login admin
- `GET /v1/api/admin/produtos` - Gestão produtos
- `GET /v1/api/admin/pedidos` - Gestão pedidos
- `GET /v1/api/admin/clientes` - Gestão clientes

## 🔧 Comandos Úteis

```bash
# Script principal
./scripts/main.sh help

# Setup de variáveis
./scripts/main.sh setup

# Deploy Kubernetes (opcional)
./scripts/main.sh k8s

# Verificar qualidade do código
./scripts/main.sh test
```

## 📈 Monitoramento

- **Vercel**: Analytics e performance do frontend
- **Render**: Logs e métricas do backend e database
- **Render PostgreSQL**: Queries e storage do banco

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 👥 Equipe

- **Desenvolvimento**: Thais Miranda, Matheus Luchiari e Murilo Biss
- **Arquitetura**: Clean Architecture + Hexagonal
- **Deploy**: Vercel + Render

---

**🍔 FastFood - Sistema de Autoatendimento Moderno**
