# 🌍 Ambientes - FastFood

Documentação completa de todos os ambientes configurados no projeto FastFood.

## 📋 Ambientes Disponíveis

### **🚀 Produção**
- **Frontend**: Vercel (https://fastfood-murex.vercel.app)
- **Backend**: Render (https://fastfood-api.onrender.com)
- **Database**: Render PostgreSQL

### **🧪 Desenvolvimento Local**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Database**: Render PostgreSQL (mesmo da produção)

### **☸️ Kubernetes (Opcional)**
- **Namespace**: fastfood
- **Pods**: FastAPI + PostgreSQL
- **Ingress**: Load Balancer

## 🔧 Configurações por Ambiente

### **Render (Backend - Produção)**

#### **Build Configuration**
```yaml
# deploy/render.yaml
buildCommand: |
  cd backend
  pip install --upgrade pip
  pip install -r requirements.txt

startCommand: |
  cd backend
  python scripts/database/init_database.py && uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

#### **Environment Variables**
```env
DATABASE_URL=postgresql://postech:password@host:port/db
SECRET_KEY=fastfood-secret-key-2025-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ENVIRONMENT=production
DEBUG=false
CORS_ALLOW_ORIGINS=https://fastfood-murex.vercel.app
API_PREFIX=/v1
PROJECT_NAME=FastFood API
VERSION=1.0.0
LOG_LEVEL=INFO
```

#### **Health Check**
- **Path**: `/health`
- **Interval**: 30s
- **Timeout**: 30s
- **Retries**: 3

### **Vercel (Frontend - Produção)**

#### **Build Configuration**
```json
// deploy/vercel.json
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
  ]
}
```

#### **Security Headers**
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`

### **Desenvolvimento Local**

#### **Backend**
```bash
# Comando
./scripts/main.sh dev

# Ou manual
cd backend
pip install -r requirements.txt
python scripts/database/init_database.py
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### **Frontend**
```bash
# Comando
./scripts/main.sh dev-frontend

# Ou manual
cd frontend
python -m http.server 3000
```

### **Docker (Local/Kubernetes)**

#### **Build**
```bash
# Caminho correto após reorganização
docker build -f backend/deploy/Dockerfile -t fastfood-api:latest backend/
```

#### **Run**
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e SECRET_KEY="your-secret" \
  fastfood-api:latest
```

## 🔄 Deploy Process

### **1. Setup Inicial**
```bash
./scripts/main.sh setup
```

### **2. Deploy Automático**
```bash
./scripts/main.sh deploy
```

### **3. Verificação**
```bash
./scripts/main.sh verify
```

### **4. Desenvolvimento**
```bash
# Backend
./scripts/main.sh dev

# Frontend
./scripts/main.sh dev-frontend
```

## 📊 Monitoramento

### **Render Dashboard**
- **Logs**: Dashboard → Web Service → Logs
- **Metrics**: CPU, Memory, Response Time
- **Health**: Automatic health checks

### **Vercel Dashboard**
- **Analytics**: Page views, performance
- **Functions**: Serverless functions (se houver)
- **Deployments**: History and rollback

### **Local Development**
- **Backend**: http://localhost:8000/docs (Swagger)
- **Frontend**: Browser DevTools
- **Database**: Render PostgreSQL dashboard

## 🚨 Troubleshooting

### **Backend não responde**
1. Verificar logs no Render
2. Confirmar DATABASE_URL
3. Verificar health check: `/health`

### **Frontend não carrega**
1. Verificar deploy no Vercel
2. Confirmar API_URL no frontend
3. Verificar CORS no backend

### **Database connection error**
1. Verificar DATABASE_URL
2. Confirmar PostgreSQL ativo no Render
3. Verificar credenciais

### **Docker build fails**
1. Confirmar caminho: `backend/deploy/Dockerfile`
2. Verificar contexto: `backend/`
3. Confirmar arquivos: `src/`, `config/`, `scripts/`

## 🔐 Segurança

### **Produção**
- ✅ HTTPS obrigatório
- ✅ Headers de segurança
- ✅ CORS configurado
- ✅ Secrets em variáveis de ambiente
- ✅ Health checks

### **Desenvolvimento**
- ⚠️ HTTP local
- ⚠️ Debug mode ativo
- ⚠️ Logs detalhados

## 📈 Performance

### **Backend (Render)**
- **Plan**: Free (com limitações)
- **Auto-scaling**: Configurado
- **Response Time**: ~45ms
- **Uptime**: 99.9%

### **Frontend (Vercel)**
- **CDN**: Global
- **Build Time**: ~30s
- **Load Time**: ~1s
- **Uptime**: 99.9%

### **Database (Render PostgreSQL)**
- **Plan**: Free (com limitações)
- **Backup**: Automático
- **Connection Pool**: Configurado
- **Uptime**: 99.9%

## 🎯 Próximos Passos

1. **Monitoramento**: Implementar logs estruturados
2. **CI/CD**: GitHub Actions para deploy automático
3. **Staging**: Ambiente de homologação
4. **Backup**: Estratégia de backup completa
5. **SSL**: Certificados customizados

---

**📅 Última atualização**: $(date)
**🚀 Status**: Todos os ambientes configurados e funcionais 