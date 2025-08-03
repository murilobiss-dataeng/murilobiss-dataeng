# FastFood - Frontend Demo

Interface web moderna para demonstrar o sistema de autoatendimento FastFood.

## 🎯 Sobre

Este é um site demonstrativo que simula o funcionamento completo do sistema FastFood, incluindo:

- **Interface de usuário** moderna e responsiva
- **Cardápio digital** com categorias
- **Carrinho de compras** funcional
- **Acompanhamento de pedidos** em tempo real
- **Demonstração da arquitetura** do sistema

## 🚀 Como Usar

### Opção 1: Abrir diretamente no navegador
```bash
# Navegue até a pasta frontend
cd frontend

# Abra o arquivo index.html no seu navegador
open index.html
```

### Opção 2: Servidor local simples
```bash
# Python 3
python -m http.server 8000

# Node.js (se tiver instalado)
npx serve .

# PHP (se tiver instalado)
php -S localhost:8000
```

Depois acesse: `http://localhost:8000`

## 📱 Funcionalidades

### **Navegação**
- Menu responsivo com navegação suave
- Seções organizadas: Início, Cardápio, Pedidos, Sobre

### **Cardápio Digital**
- Produtos organizados por categoria
- Filtros dinâmicos (Todos, Hambúrgueres, Bebidas, etc.)
- Cards interativos com animações

### **Carrinho de Compras**
- Adicionar/remover produtos
- Controle de quantidade
- Cálculo automático do total
- Modal responsivo

### **Acompanhamento de Pedidos**
- Simulação de pedido em tempo real
- Barra de progresso animada
- Status do pedido (Recebido → Confirmado → Em Preparo → Pronto → Entregue)

### **Demonstração da Arquitetura**
- Cards interativos mostrando as tecnologias
- Estatísticas em tempo real
- Informações sobre o sistema

## 🎨 Design

### **Características**
- Design moderno e profissional
- Paleta de cores consistente
- Tipografia clara (Inter)
- Animações suaves
- Totalmente responsivo

### **Tecnologias Frontend**
- HTML5 semântico
- CSS3 com Grid e Flexbox
- JavaScript ES6+
- Font Awesome para ícones
- Google Fonts (Inter)

## 🔧 Personalização

### **Cores**
As cores principais estão definidas no CSS:
- Primária: `#2563eb` (azul)
- Secundária: `#1d4ed8` (azul escuro)
- Sucesso: `#10b981` (verde)
- Erro: `#ef4444` (vermelho)

### **Produtos**
Para adicionar/editar produtos, modifique o array `products` no arquivo `script.js`.

### **Animações**
As animações podem ser ajustadas no CSS através das classes `.fade-in` e keyframes.

## 📊 Integração com Backend

Este frontend está preparado para integração com a API FastFood:

### **Endpoints Simulados**
- `GET /products` - Lista de produtos
- `POST /orders` - Criar pedido
- `GET /orders/{id}` - Status do pedido
- `POST /auth/login` - Autenticação

### **Para Integração Real**
1. Substitua as chamadas mock por `fetch()` ou `axios`
2. Configure as URLs da API
3. Implemente tratamento de erros
4. Adicione autenticação JWT

## 🚀 Deploy

### **GitHub Pages**
```bash
# Faça push para o repositório
git add .
git commit -m "Add frontend demo"
git push

# Ative GitHub Pages nas configurações do repositório
```

### **Netlify/Vercel**
- Conecte o repositório
- Configure o build (não necessário para arquivos estáticos)
- Deploy automático

## 📱 Responsividade

O site é totalmente responsivo e funciona em:
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (320px - 767px)

## 🎯 Próximos Passos

1. **Integração com API real**
2. **Sistema de autenticação**
3. **Página de administração**
4. **PWA (Progressive Web App)**
5. **Testes automatizados**
6. **Otimização de performance**

## 📄 Licença

Este projeto está sob a licença MIT. 

## Variáveis de Ambiente

- Local: copie `.env.local.example` para `.env.local` e ajuste o valor de `VITE_API_URL`.
- Produção (Vercel): configure `VITE_API_URL` no painel do Vercel. 