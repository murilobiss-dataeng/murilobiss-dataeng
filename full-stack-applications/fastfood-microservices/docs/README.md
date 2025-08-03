# 📚 Documentação - FastFood

Documentação completa do sistema de autoatendimento FastFood.

## 📋 Índice

### **📊 Arquitetura**
- [Arquitetura Geral](architecture.puml) - Visão geral do sistema
- [Arquitetura Kubernetes](arquitetura-kubernetes-fase2.puml) - Deploy em K8s
- [Diagrama Arquitetural](arquitetura.png) - Imagem da arquitetura

### **🔄 Fluxos**
- [Event Storming](event-storming-fase2.puml) - Análise de domínio
- [Fluxo de Pedido e Pagamento](fluxo_pedido_pagamento.puml)
- [Fluxo de Preparo e Entrega](fluxo_preparo_entrega_pedido.puml)
- [Fluxos Alternativos](fluxos-alternativos.puml)

### **🧪 Testes**
- [Collection Postman](postman-collection.json) - Testes da API

## 🚀 Deploy

Para informações sobre deploy, consulte:
- [Guia de Deploy](../DEPLOY_GUIDE.md)
- [Script de Deploy](../scripts/deploy.sh)

## 📁 Estrutura do Projeto

```
fastfood/
├── backend/           # API FastAPI
├── frontend/          # Interface web
├── docs/             # Documentação
├── k8s/              # Configurações Kubernetes
├── scripts/          # Scripts de automação
└── README.md         # Documentação principal
```

## 🔧 Tecnologias

- **Backend**: FastAPI, Python 3.11, PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: Render PostgreSQL
- **Deploy**: Vercel (Frontend) + Render (Backend + Database)
- **Container**: Docker
- **Orquestração**: Kubernetes (opcional)

---

*Documentação gerada em $(date)* 