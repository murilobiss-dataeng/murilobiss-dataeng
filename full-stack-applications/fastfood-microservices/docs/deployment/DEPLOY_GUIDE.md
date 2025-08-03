# 🚀 Guia de Deploy - FastFood

Guia completo para deploy do sistema FastFood no Render e Vercel.

## 📋 Pré-requisitos

- ✅ Conta no [Render.com](https://render.com)
- ✅ Conta no [Vercel.com](https://vercel.com)
- ✅ Repositório no GitHub
- ✅ PostgreSQL no Render

## 🎯 Deploy Rápido

### **1. Setup Inicial**

```bash
# Clone o repositório
git clone https://github.com/murilobiss/fastfood.git
cd fastfood

# Execute o script de setup
./scripts/setup-env.sh
```

### **2. Deploy Backend (Render)**

#### **Passo 1: Criar Web Service**
1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório GitHub
4. Selecione o repositório `fastfood`

#### **Passo 2: Configurar Build**
```yaml
Name: fastfood-api
Environment: Python 3
Build Command: cd backend && pip install -r requirements.txt
Start Command: cd backend && python scripts/init_database.py && uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

#### **Passo 3: Variáveis de Ambiente**
Adicione as seguintes variáveis no Render:

```env
# Database
DATABASE_URL=postgresql://postech:lqIYZ8F3PcPCQBxeViQUbJZh0fw6dRDN@dpg-d1p7s4juibrs73dfuceg-a.ohio-postgres.render.com:5432/fastfood_vi5x

# Security
SECRET_KEY=fastfood-secret-key-2025-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Environment
ENVIRONMENT=production
DEBUG=false

# CORS
CORS_ALLOW_ORIGINS=https://fastfood-murex.vercel.app

# API
API_PREFIX=/v1
PROJECT_NAME=FastFood API
VERSION=1.0.0
LOG_LEVEL=INFO
```

#### **Passo 4: Deploy**
1. Clique em **"Create Web Service"**
2. Aguarde o build e deploy automático
3. Verifique os logs para confirmar sucesso

### **3. Deploy Frontend (Vercel)**

#### **Passo 1: Criar Projeto**
1. Acesse [Vercel Dashboard](https://vercel.com/dashboard)
2. Clique em **"New Project"**
3. Importe o repositório `fastfood`

#### **Passo 2: Configurar Build**
```yaml
Framework Preset: Other
Root Directory: ./
Output Directory: frontend
Build Command: (deixar vazio)
Install Command: (deixar vazio)
```

#### **Passo 3: Deploy**
1. Clique em **"Deploy"**
2. Aguarde o deploy automático
3. Acesse a URL gerada

## 🔧 Configurações Avançadas

### **Render - Auto Scaling**

```yaml
# No render.yaml
services:
  - type: web
    name: fastfood-api
    env: python
    plan: free
    buildCommand: |
      cd backend
      pip install --upgrade pip
      pip install -r requirements.txt
    startCommand: |
      cd backend
      python scripts/init_database.py && uvicorn src.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 30
      - key: ADMIN_USERNAME
        value: admin
      - key: ADMIN_PASSWORD
        sync: false
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false
      - key: CORS_ALLOW_ORIGINS
        value: https://fastfood-murex.vercel.app
      - key: API_PREFIX
        value: /v1
      - key: PROJECT_NAME
        value: FastFood API
      - key: VERSION
        value: 1.0.0
      - key: LOG_LEVEL
        value: INFO
```

### **Vercel - Configuração**

```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

## 🧪 Testes de Deploy

### **Backend Health Check**
```bash
curl https://fastfood-api.onrender.com/health
```

### **API Documentation**
```bash
# Swagger UI
https://fastfood-api.onrender.com/docs

# ReDoc
https://fastfood-api.onrender.com/redoc
```

### **Frontend Test**
```bash
# Acesse a URL do Vercel
https://fastfood-murex.vercel.app
```

## 🔍 Troubleshooting

### **Problemas Comuns**

#### **1. Erro de Conexão com Database**
```bash
# Verificar logs no Render
# Confirmar DATABASE_URL está correta
# Verificar se o PostgreSQL está ativo
```

#### **2. Erro de Build**
```bash
# Verificar requirements.txt
# Confirmar Python 3.11+
# Verificar dependências
```

#### **3. CORS Errors**
```bash
# Verificar CORS_ALLOW_ORIGINS
# Confirmar URL do frontend
# Testar com Postman
```

#### **4. Produtos não aparecem**
```bash
# Verificar logs de inicialização
# Confirmar script init_database.py executou
# Verificar tabela produtos no banco
```

### **Logs Úteis**

```bash
# Render Logs
# Dashboard → Web Service → Logs

# Vercel Logs
# Dashboard → Project → Functions → Logs
```

## 📊 Monitoramento

### **Render Metrics**
- **CPU Usage**: Monitorar uso de CPU
- **Memory Usage**: Monitorar uso de memória
- **Response Time**: Tempo de resposta da API
- **Error Rate**: Taxa de erros

### **Vercel Analytics**
- **Page Views**: Visualizações de página
- **Performance**: Core Web Vitals
- **Errors**: Erros de JavaScript
- **Real User Monitoring**: Dados reais de usuários

## 🔄 CI/CD

### **GitHub Actions (Opcional)**

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v1.0.0
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 🎯 URLs de Produção

- **Frontend**: https://fastfood-murex.vercel.app
- **Backend API**: https://fastfood-api.onrender.com
- **API Docs**: https://fastfood-api.onrender.com/docs
- **Health Check**: https://fastfood-api.onrender.com/health

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/murilobiss/fastfood/issues)
- **Render Support**: [Render Docs](https://render.com/docs)
- **Vercel Support**: [Vercel Docs](https://vercel.com/docs)

---

**🚀 Deploy concluído com sucesso!** 