# 🚀 Social FIT HTML Dashboard

## 📋 Overview

Este projeto inclui um dashboard HTML completo e interativo para visualização dos dados do Social FIT. O dashboard é totalmente client-side e pode ser hospedado em qualquer servidor web, incluindo GitHub Pages.

## 🎯 Características

- ✅ **100% Client-side** - Não requer servidor backend
- ✅ **Tempo Real** - Conecta diretamente ao Supabase
- ✅ **Responsivo** - Funciona em desktop, tablet e mobile
- ✅ **Interativo** - Gráficos dinâmicos com Chart.js
- ✅ **Profissional** - Design moderno com Bootstrap
- ✅ **Público** - Pode ser acessado de qualquer lugar
- ✅ **Gratuito** - Hospedagem gratuita no GitHub Pages

## 🚀 Setup Rápido

### 1. Configure as Credenciais

```bash
# Execute o script de configuração
python3 scripts/setup_dashboard.py
```

### 2. Teste Localmente

```bash
# Abra o arquivo no navegador
open dashboard.html
# ou
python3 -m http.server 8000
# Acesse: http://localhost:8000/dashboard.html
```

### 3. Deploy no GitHub Pages

```bash
# Commit e push
git add dashboard.html
git commit -m "Add HTML dashboard"
git push origin main

# Configure GitHub Pages:
# 1. Vá em Settings > Pages
# 2. Source: Deploy from a branch
# 3. Branch: main
# 4. Folder: / (root)
# 5. Save
```

## 📊 Funcionalidades do Dashboard

### KPIs Principais
- **Total de Alunos** - Contador em tempo real
- **Planos Ativos** - Alunos com planos ativos
- **Receita Mensal** - Valor total em R$
- **Engajamento Médio** - Taxa média do Instagram

### Visualizações
- **Distribuição por Plano** - Gráfico pizza
- **Distribuição por Gênero** - Gráfico rosca
- **Top 10 Bairros** - Gráfico barras
- **Evolução do Engajamento** - Gráfico linha
- **Top Hashtags** - Gráfico barras
- **Engajamento vs Alcance** - Gráfico scatter

### Tabelas
- **Top Alunos** - Por receita mensal
- **Top Posts Instagram** - Por engajamento

### Insights
- **Insights Acionáveis** - Gerados pelo pipeline de analytics

## 🔧 Configuração Manual

Se preferir configurar manualmente:

1. **Abra o arquivo `dashboard.html`**
2. **Localize as linhas 280-281:**
```javascript
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_KEY = 'YOUR_SUPABASE_ANON_KEY';
```

3. **Substitua pelos seus valores:**
```javascript
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_KEY = 'your-anon-key';
```

## 🌐 Opções de Hospedagem

### 1. GitHub Pages (Recomendado)
- **Gratuito**
- **Automático** - Deploy automático
- **HTTPS** - Seguro por padrão
- **URL**: `https://seu-usuario.github.io/social_fit/dashboard.html`

### 2. Netlify
- **Gratuito**
- **Drag & Drop** - Arraste o arquivo HTML
- **URL**: `https://seu-site.netlify.app`

### 3. Vercel
- **Gratuito**
- **Deploy automático** do GitHub
- **URL**: `https://seu-site.vercel.app`

### 4. Servidor Próprio
- **Qualquer servidor web** (Apache, Nginx, etc.)
- **Controle total** sobre configurações

## 🔐 Segurança

### Credenciais do Supabase
- Use apenas a **chave anônima** (não a service role)
- Configure **Row Level Security (RLS)** no Supabase
- Monitore o uso da API

### Acesso Público
- O dashboard é **público** por padrão
- Para acesso restrito, implemente autenticação
- Considere usar **HTTPS** em produção

## 📱 Mobile

O dashboard é totalmente responsivo:
- **Desktop** - Layout completo
- **Tablet** - Layout adaptado
- **Mobile** - Layout otimizado para touch

## 🔄 Atualização Automática

O dashboard atualiza automaticamente:
- **A cada 5 minutos** - Dados em tempo real
- **Ao recarregar** - Dados mais recentes
- **Manual** - Botão de refresh

## 🎨 Personalização

### Cores
```css
/* Modifique as cores no CSS */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #ff6b6b;
}
```

### Logo
```html
<!-- Substitua o emoji por sua logo -->
<span class="navbar-brand">🏋️ Social FIT Data Intelligence</span>
```

### Gráficos
```javascript
// Modifique as cores dos gráficos
const chartColors = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
];
```

## 🐛 Troubleshooting

### Dashboard não carrega
1. Verifique as credenciais do Supabase
2. Abra o console do navegador (F12)
3. Verifique se há erros de CORS
4. Confirme se o banco está acessível

### Gráficos não aparecem
1. Verifique se o Chart.js está carregando
2. Confirme se há dados no banco
3. Verifique o console para erros JavaScript

### Dados não atualizam
1. Verifique a conexão com o Supabase
2. Confirme se o ETL pipeline está rodando
3. Verifique as permissões do banco

## 📈 Próximos Passos

1. ✅ **Setup inicial** - Configure credenciais
2. ✅ **Teste local** - Verifique funcionamento
3. 🔄 **Deploy** - Hospede no GitHub Pages
4. 🔄 **Personalização** - Ajuste cores e logo
5. 🔄 **Monitoramento** - Configure alertas
6. 🔄 **Backup** - Configure backup dos dados

## 📞 Suporte

- **GitHub Issues** - Para bugs e melhorias
- **Supabase Docs** - Para questões de banco
- **Chart.js Docs** - Para customização de gráficos

## 🎯 Exemplo de URL Final

Após o deploy no GitHub Pages:
```
https://seu-usuario.github.io/social_fit/dashboard.html
```

**🎉 Seu dashboard profissional está pronto para uso público!** 