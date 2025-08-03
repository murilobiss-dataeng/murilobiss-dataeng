# 📁 Organização do Projeto Social FIT

## 🎯 Estrutura Otimizada

O projeto foi reorganizado para melhor manutenibilidade e clareza:

```
social_fit/
├── 📊 dashboard/                 # 🎯 PRINCIPAL - Dashboard HTML
│   ├── dashboard.html           # Dashboard interativo
│   ├── config.py               # Configuração centralizada
│   ├── setup_dashboard.py      # Script de setup
│   └── README_DASHBOARD.md     # Documentação
├── 🗄️ metabase/                  # 🔧 ALTERNATIVA - Metabase
│   ├── metabase.jar            # Executável (495MB)
│   ├── docker-compose.yml      # Configuração Docker
│   ├── setup_metabase*.sh      # Scripts de setup
│   ├── METABASE_QUERIES.sql    # Queries prontas
│   └── README_METABASE.md      # Documentação
├── 🔧 src/                      # 💻 CÓDIGO FONTE
│   ├── etl/                    # Pipeline ETL
│   ├── analytics/              # Engine de analytics
│   ├── database/               # Gerenciamento de banco
│   ├── models/                 # Modelos de dados
│   └── config/                 # Configurações
├── 🧪 tests/                   # 🧪 TESTES
├── 📚 docs/                    # 📖 DOCUMENTAÇÃO
├── 🛠️ scripts/                 # 🔧 UTILITÁRIOS
└── 📋 data/                    # 📊 DADOS
```

## 🗑️ Arquivos Removidos

### **Temporários/Debug**
- `scripts/check_tables.py` - Script de debug
- `scripts/debug_tables.py` - Script de debug
- `scripts/create_tables*.sql` - SQLs temporários
- `docs/DEPLOYMENT.md` - Documentação antiga
- `.DS_Store` - Arquivo do macOS
- `plugins/` - Diretório não utilizado

### **Organizados**
- **Metabase** → `metabase/` (495MB isolados)
- **Dashboard** → `dashboard/` (principal)
- **Scripts** → Organizados por função

## 🎯 Foco Principal

### **Dashboard HTML (Recomendado)**
- ✅ **Acesso público** via GitHub Pages
- ✅ **Sem dependências** de servidor
- ✅ **Tempo real** via Supabase
- ✅ **Responsivo** e interativo
- ✅ **Fácil deploy** e manutenção

### **Metabase (Alternativa)**
- 🔧 **Para uso interno** ou servidor próprio
- 🔧 **Mais recursos** de BI
- 🔧 **Requer servidor** Java/Docker
- 🔧 **495MB** de arquivos

## 🚀 Como Usar

### **Dashboard Principal**
```bash
# Configure credenciais
python dashboard/setup_dashboard.py

# Abra o dashboard
open dashboard/dashboard.html

# Deploy no GitHub Pages
git add dashboard/dashboard.html
git commit -m "Update dashboard"
git push origin main
```

### **Metabase (Se necessário)**
```bash
cd metabase
./setup_metabase_jar.sh
# Acesse: http://localhost:3000
```

## 📊 Benefícios da Organização

### **✅ Limpeza**
- Estrutura clara e intuitiva
- Separação de responsabilidades
- Arquivos desnecessários removidos

### **✅ Manutenibilidade**
- Configuração centralizada
- Documentação organizada
- Scripts específicos por função

### **✅ Performance**
- Metabase isolado (495MB)
- Dashboard otimizado
- Carregamento mais rápido

### **✅ Deploy**
- Dashboard pronto para GitHub Pages
- Metabase isolado para uso interno
- Configuração simplificada

## 🔧 Configuração

### **Dashboard**
- Credenciais em `dashboard/config.py`
- Setup automático via `setup_dashboard.py`
- HTML otimizado e responsivo

### **Metabase**
- Configuração Docker em `metabase/`
- Scripts de setup automatizados
- Queries SQL prontas

## 📈 Próximos Passos

1. ✅ **Organização** - Estrutura limpa
2. 🔄 **Deploy** - Dashboard no GitHub Pages
3. 🔄 **Documentação** - Guias atualizados
4. 🔄 **Monitoramento** - Métricas de uso
5. 🔄 **Melhorias** - Novas funcionalidades

---

**🎉 Projeto organizado e otimizado para produção!** 