# 🚀 Guia de Deploy Kubernetes - FastFood

Guia completo para fazer deploy do sistema FastFood usando Kubernetes.

## 📋 Pré-requisitos

- ✅ [kubectl](https://kubernetes.io/docs/tasks/tools/) instalado
- ✅ [Docker](https://docs.docker.com/get-docker/) instalado
- ✅ Cluster Kubernetes configurado (minikube, kind, ou cloud)
- ✅ [kustomize](https://kustomize.io/) (opcional, mas recomendado)

## 🏗️ Arquitetura Kubernetes

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ingress       │    │   FastAPI       │    │   PostgreSQL    │
│   Controller    │◄──►│   Deployment    │◄──►│   Deployment    │
│                 │    │   (2 replicas)  │    │   (1 replica)   │
│ • Load Balancer │    │ • Auto Scaling  │    │ • Persistent    │
│ • SSL/TLS       │    │ • Health Checks │    │ • Backup        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Deploy Rápido

### **1. Deploy Automático**
```bash
# Execute o script de deploy
chmod +x scripts/deploy-k8s.sh
./scripts/deploy-k8s.sh
```

### **2. Deploy Manual**

#### **Passo 1: Construir Imagem**
```bash
# Construir imagem Docker
# Caminho correto do Dockerfile após reorganização:
docker build -f backend/deploy/Dockerfile -t fastfood-api:latest backend/
```

#### **Passo 2: Aplicar Recursos**
```bash
# Criar namespace
kubectl apply -f k8s/namespace.yaml

# Aplicar todos os recursos
kubectl apply -k k8s/
```

#### **Passo 3: Verificar Status**
```bash
# Verificar pods
kubectl get pods -n fastfood

# Verificar serviços
kubectl get services -n fastfood

# Verificar ingress
kubectl get ingress -n fastfood
```

## 📁 Estrutura dos Recursos

### **Namespace**
- `fastfood` - Namespace isolado para o projeto

### **Persistent Storage**
- `fastfood-postgres-pv` - Volume persistente
- `fastfood-postgres-pvc` - Claim do volume

### **Database**
- `fastfood-postgres` - Deployment PostgreSQL
- `fastfood-postgres-service` - Service PostgreSQL

### **Application**
- `fastfood-api` - Deployment FastAPI
- `fastfood-api-service` - Service FastAPI
- `fastfood-ingress` - Ingress para acesso externo

### **Configuration**
- `fastfood-config` - ConfigMap com variáveis
- `fastfood-secrets` - Secrets com credenciais
- `fastfood-init-scripts` - Scripts de inicialização

### **Scaling**
- `fastfood-api-hpa` - Horizontal Pod Autoscaler

## 🔧 Configuração

### **Secrets (Obrigatório)**
```bash
# Gerar secrets base64
echo -n "postech-password" | base64
echo -n "fastfood-secret-key-2025" | base64
echo -n "admin" | base64
echo -n "admin123" | base64

# Atualizar k8s/secret.yaml com os valores gerados
```

### **ConfigMap**
- Todas as variáveis de ambiente estão no `k8s/configmap.yaml`
- Inclui configurações de CORS, API, etc.

## 🔄 Inicialização do Banco

### **Init Container**
O deploy usa um **init container** que:
1. ✅ Aguarda o PostgreSQL ficar disponível
2. ✅ Executa migrações Alembic
3. ✅ Popula dados iniciais
4. ✅ Verifica a configuração

### **Script de Inicialização**
```python
# backend/scripts/init_database.py
- wait_for_database()     # Aguarda banco
- run_migrations()        # Executa Alembic
- populate_products()     # Insere produtos
- verify_database()       # Verifica setup
```

## 📊 Monitoramento

### **Health Checks**
- **Liveness Probe**: `/health` a cada 10s
- **Readiness Probe**: `/health` a cada 5s
- **Startup Probe**: Aguarda 30s inicial

### **Logs**
```bash
# Logs da aplicação
kubectl logs -n fastfood -l app=fastfood-api

# Logs do init container
kubectl logs -n fastfood -l app=fastfood-api -c init-database

# Logs do PostgreSQL
kubectl logs -n fastfood -l app=fastfood-postgres
```

### **Métricas**
```bash
# Status dos pods
kubectl top pods -n fastfood

# Status dos nodes
kubectl top nodes
```

## 🔄 Auto Scaling

### **HPA Configuration**
- **Min Replicas**: 2
- **Max Replicas**: 10
- **CPU Target**: 70%
- **Memory Target**: 80%

### **Scaling Manual**
```bash
# Escalar manualmente
kubectl scale deployment fastfood-api -n fastfood --replicas=5

# Verificar HPA
kubectl get hpa -n fastfood
```

## 🛠️ Troubleshooting

### **Problemas Comuns**

#### **1. Pod não inicia**
```bash
# Verificar eventos
kubectl describe pod -n fastfood -l app=fastfood-api

# Verificar logs
kubectl logs -n fastfood -l app=fastfood-api
```

#### **2. Banco não conecta**
```bash
# Verificar PostgreSQL
kubectl get pods -n fastfood -l app=fastfood-postgres

# Verificar logs do init container
kubectl logs -n fastfood -l app=fastfood-api -c init-database
```

#### **3. Ingress não funciona**
```bash
# Verificar ingress controller
kubectl get ingress -n fastfood

# Verificar endpoints
kubectl get endpoints -n fastfood
```

## 🧹 Limpeza

### **Remover Deploy**
```bash
# Remover todos os recursos
kubectl delete -k k8s/

# Remover namespace
kubectl delete namespace fastfood
```

### **Limpar Volumes**
```bash
# Remover PVC
kubectl delete pvc fastfood-postgres-pvc -n fastfood

# Remover PV
kubectl delete pv fastfood-postgres-pv
```

## 📈 Próximos Passos

1. **Configurar SSL/TLS** com cert-manager
2. **Implementar backup automático** do PostgreSQL
3. **Adicionar monitoring** com Prometheus/Grafana
4. **Configurar CI/CD** com GitHub Actions
5. **Implementar blue-green deployment**

---

**🎯 Sistema pronto para produção com Kubernetes!** 