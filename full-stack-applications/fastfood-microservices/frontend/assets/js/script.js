// ===== CONFIGURAÇÕES =====
const CONFIG = {
    API_BASE_URL: 'https://fastfood-vwtq.onrender.com',
    ENDPOINTS: {
        PRODUCTS: '/v1/api/public/produtos/',
        ORDERS: '/v1/api/public/pedidos/',
        CUSTOMERS: '/v1/api/public/clientes/',
        PAYMENTS: '/v1/api/public/pagamento/',
        ADMIN_LOGIN: '/v1/api/public/login',
        ADMIN_ORDERS: '/v1/api/admin/pedidos/',
        ADMIN_PRODUCTS: '/v1/api/admin/produtos/',
        ADMIN_CUSTOMERS: '/v1/api/admin/clientes/'
    },
    ADMIN_CREDENTIALS: {
        USERNAME: 'admin',
        PASSWORD: 'postech'
    }
};

// ===== ESTADO GLOBAL =====
const STATE = {
    products: [],
    cart: [],
    currentUser: null,
    isAdmin: false,
    adminToken: null,
    currentTab: 'orders',
    orders: [],
    customers: []
};

// ===== UTILITÁRIOS =====
const Utils = {
    formatPrice: (price) => {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(price);
    },

    showNotification: (message, type = 'info') => {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },

    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    getCategoryIcon: (category) => {
        const icons = {
            burgers: 'fas fa-hamburger',
            drinks: 'fas fa-glass-martini',
            sides: 'fas fa-french-fries',
            desserts: 'fas fa-ice-cream'
        };
        return icons[category] || 'fas fa-utensils';
    },

    getCategoryName: (category) => {
        const names = {
            burgers: 'Burgers',
            drinks: 'Bebidas',
            sides: 'Acompanhamentos',
            desserts: 'Sobremesas'
        };
        return names[category] || category;
    }
};

// ===== API SERVICE =====
const API = {
    async request(endpoint, options = {}) {
        const url = `${CONFIG.API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            mode: 'cors',
            credentials: 'omit',
            ...options
        };

        if (STATE.adminToken) {
            config.headers.Authorization = `Bearer ${STATE.adminToken}`;
        }

        console.log('🌐 API Request:', { url, method: options.method || 'GET', body: options.body });
        console.log('🌐 API Config:', config);

        try {
            const response = await fetch(url, config);
            console.log('🌐 API Response status:', response.status);
            console.log('🌐 API Response headers:', Object.fromEntries(response.headers.entries()));
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('🌐 API Error response:', errorText);
                
                // Se for erro 403, pode ser problema de autenticação
                if (response.status === 403) {
                    console.log('🔑 Erro 403 - Removendo token inválido');
                    localStorage.removeItem('adminToken');
                    STATE.adminToken = null;
                    STATE.isAdmin = false;
                }
                
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('🌐 API Response data:', data);
            return data;
        } catch (error) {
            console.error('❌ API Error:', error);
            console.error('❌ API Error details:', { url, config, error: error.message });
            
            // Se for erro de CORS, mostrar mensagem específica
            if (error.message.includes('Failed to fetch')) {
                throw new Error('Erro de conexão com o servidor. Verifique sua conexão com a internet.');
            }
            
            throw error;
        }
    },

    async getProducts() {
        return await this.request(CONFIG.ENDPOINTS.PRODUCTS);
    },

    async createOrder(orderData) {
        return await this.request(CONFIG.ENDPOINTS.ORDERS, {
            method: 'POST',
            body: JSON.stringify(orderData)
        });
    },

    async createCustomer(customerData) {
        return await this.request(CONFIG.ENDPOINTS.CUSTOMERS, {
            method: 'POST',
            body: JSON.stringify(customerData)
        });
    },

    async getOrders() {
        return await this.request(CONFIG.ENDPOINTS.ADMIN_ORDERS);
    },

    async getPublicOrders() {
        return await this.request(CONFIG.ENDPOINTS.ORDERS);
    },

    async getCustomerByCPF(cpf) {
        return await this.request(`/v1/api/public/clientes/cpf/${cpf}`);
    },

    async getCustomers() {
        return await this.request(CONFIG.ENDPOINTS.ADMIN_CUSTOMERS);
    },

    async adminLogin(username, password) {
        console.log('🔑 API: Login attempt for username:', username);
        console.log('🔑 API: Endpoint:', CONFIG.ENDPOINTS.ADMIN_LOGIN);
        
        // Create FormData for login (backend expects form data)
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.ADMIN_LOGIN}`, {
            method: 'POST',
            body: formData
        });
        
        console.log('🔑 API: Login response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('🔑 API: Login response data:', data);
        
        if (data.access_token) {
            STATE.adminToken = data.access_token;
            STATE.isAdmin = true;
            localStorage.setItem('adminToken', data.access_token);
            console.log('✅ API: Token saved successfully');
        }
        
        return data;
    }
};

// ===== CART MANAGEMENT =====
const Cart = {
    addItem(product) {
        const existingItem = STATE.cart.find(item => item.id === product.id);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            STATE.cart.push({
                ...product,
                quantity: 1
            });
        }
        
        this.updateDisplay();
        this.saveToStorage();
    },

    removeItem(productId) {
        STATE.cart = STATE.cart.filter(item => item.id !== productId);
        this.updateDisplay();
        this.saveToStorage();
    },

    updateQuantity(productId, quantity) {
        const item = STATE.cart.find(item => item.id === productId);
        if (item) {
            if (quantity <= 0) {
                this.removeItem(productId);
            } else {
                item.quantity = quantity;
                this.updateDisplay();
                this.saveToStorage();
            }
        }
    },

    getTotal() {
        return STATE.cart.reduce((total, item) => {
            return total + (item.preco * item.quantity);
        }, 0);
    },

    clear() {
        STATE.cart = [];
        this.updateDisplay();
        this.saveToStorage();
    },

    updateDisplay() {
        const cartCount = document.getElementById('cartCount');
        const cartItems = document.getElementById('cartItems');
        const totalAmount = document.getElementById('totalAmount');
        
        // Update cart count
        const totalItems = STATE.cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
        
        // Update cart items
        if (cartItems) {
            cartItems.innerHTML = STATE.cart.length === 0 
                ? '<p class="empty-cart">Seu carrinho está vazio</p>'
                : STATE.cart.map(item => `
                    <div class="cart-item">
                        <div class="cart-item-info">
                            <div class="cart-item-name">${item.nome}</div>
                            <div class="cart-item-price">${Utils.formatPrice(item.preco)}</div>
                        </div>
                        <div class="cart-item-quantity">
                            <button class="quantity-btn" onclick="Cart.updateQuantity('${item.id}', ${item.quantity - 1})">-</button>
                            <span>${item.quantity}</span>
                            <button class="quantity-btn" onclick="Cart.updateQuantity('${item.id}', ${item.quantity + 1})">+</button>
                        </div>
                    </div>
                `).join('');
        }
        
        // Update total
        if (totalAmount) {
            totalAmount.textContent = Utils.formatPrice(this.getTotal());
        }
    },

    saveToStorage() {
        localStorage.setItem('cart', JSON.stringify(STATE.cart));
    },

    loadFromStorage() {
        const savedCart = localStorage.getItem('cart');
        if (savedCart) {
            STATE.cart = JSON.parse(savedCart);
            this.updateDisplay();
        }
    }
};

// ===== ADMIN PANEL =====
const AdminPanel = {
    init() {
        this.bindEvents();
        this.checkAuth();
    },

    bindEvents() {
        // Admin login buttons
        const adminLink = document.getElementById('adminLink');
        const footerAdminLink = document.getElementById('footerAdminLink');
        
        console.log('🔍 Admin buttons found:', { adminLink: !!adminLink, footerAdminLink: !!footerAdminLink });
        
        adminLink?.addEventListener('click', () => {
            console.log('🔑 Admin button clicked');
            this.showLoginModal();
        });
        
        footerAdminLink?.addEventListener('click', () => {
            console.log('🔑 Footer admin button clicked');
            this.showLoginModal();
        });
        
        // Admin modal events
        document.getElementById('closeAdmin')?.addEventListener('click', () => this.hideLoginModal());
        document.getElementById('adminLoginForm')?.addEventListener('submit', (e) => this.handleLogin(e));
        
        // Admin panel events
        document.getElementById('logoutBtn')?.addEventListener('click', () => this.logout());
        
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => this.switchTab(btn.dataset.tab));
        });
    },

    showLoginModal() {
        console.log('🔑 Showing login modal');
        const modal = document.getElementById('adminModal');
        if (modal) {
            modal.classList.add('active');
            console.log('✅ Modal shown');
        } else {
            console.error('❌ Modal not found');
        }
    },

    hideLoginModal() {
        document.getElementById('adminModal').classList.remove('active');
    },

    async handleLogin(e) {
        e.preventDefault();
        
        console.log('🔑 Login attempt started');
        
        const username = document.getElementById('adminUsername').value;
        const password = document.getElementById('adminPassword').value;
        
        console.log('🔑 Credentials:', { username, password: password ? '***' : 'empty' });
        
        try {
            console.log('🔑 Calling API login...');
            await API.adminLogin(username, password);
            console.log('✅ Login successful');
            this.hideLoginModal();
            this.showAdminPanel();
            Utils.showNotification('Login realizado com sucesso!', 'success');
        } catch (error) {
            console.error('❌ Login failed:', error);
            Utils.showNotification('Credenciais inválidas!', 'error');
        }
    },

    showAdminPanel() {
        document.getElementById('adminPanel').classList.add('active');
        this.loadAdminData();
    },

    hideAdminPanel() {
        document.getElementById('adminPanel').classList.remove('active');
    },

    logout() {
        STATE.isAdmin = false;
        STATE.adminToken = null;
        localStorage.removeItem('adminToken');
        this.hideAdminPanel();
        Utils.showNotification('Logout realizado com sucesso!', 'success');
    },

    checkAuth() {
        const token = localStorage.getItem('adminToken');
        if (token) {
            STATE.adminToken = token;
            STATE.isAdmin = true;
            console.log('🔑 Token carregado do localStorage:', token.substring(0, 20) + '...');
            return true;
        }
        console.log('🔑 Nenhum token encontrado no localStorage');
        return false;
    },

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });
        
        // Update tab content
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.toggle('active', pane.id === `${tabName}Tab`);
        });
        
        STATE.currentTab = tabName;
        this.loadTabData(tabName);
    },

    async loadAdminData() {
        await Promise.all([
            this.loadTabData('orders'),
            this.loadTabData('customers'),
            this.loadTabData('analytics')
        ]);
    },

    async loadTabData(tabName) {
        switch (tabName) {
            case 'orders':
                await this.loadOrders();
                break;
            case 'products':
                await this.loadProducts();
                break;
            case 'customers':
                await this.loadCustomers();
                break;
            case 'analytics':
                await this.loadAnalytics();
                break;
        }
    },

    async loadOrders() {
        try {
            // Verificar se está autenticado
            if (!STATE.adminToken) {
                throw new Error('Não autenticado. Faça login novamente.');
            }
            
            const orders = await API.getOrders();
            STATE.orders = orders;
            
            const ordersList = document.getElementById('ordersList');
            ordersList.innerHTML = orders.length === 0 
                ? '<p>Nenhum pedido encontrado</p>'
                : orders.map(order => `
                    <div class="order-card">
                        <div class="order-header">
                            <h4>Pedido #${order.id.slice(0, 8)}</h4>
                            <span class="order-status ${order.status}">${order.status}</span>
                        </div>
                        <div class="order-details">
                            <p><strong>Cliente:</strong> ${order.cliente?.nome || 'N/A'}</p>
                            <p><strong>Data:</strong> ${new Date(order.data_criacao).toLocaleString()}</p>
                            <p><strong>Total:</strong> ${Utils.formatPrice(order.total || 0)}</p>
                        </div>
                    </div>
                `).join('');
        } catch (error) {
            console.error('❌ Erro ao carregar pedidos:', error);
            if (error.message.includes('Não autenticado')) {
                Utils.showNotification('Sessão expirada. Faça login novamente.', 'error');
                this.hideAdminPanel();
                this.showLoginModal();
            } else {
                Utils.showNotification('Erro ao carregar pedidos: ' + error.message, 'error');
            }
        }
    },

    async loadProducts() {
        try {
            const products = await API.getProducts();
            STATE.products = products;
            
            const productsTable = document.getElementById('productsTable');
            productsTable.innerHTML = `
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Categoria</th>
                            <th>Preço</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${products.map(product => `
                            <tr>
                                <td>${product.nome}</td>
                                <td>${Utils.getCategoryName(product.categoria)}</td>
                                <td>${Utils.formatPrice(product.preco)}</td>
                                <td>
                                    <button class="btn btn-small" onclick="AdminPanel.editProduct('${product.id}')">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="btn btn-small btn-danger" onclick="AdminPanel.deleteProduct('${product.id}')">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        } catch (error) {
            Utils.showNotification('Erro ao carregar produtos', 'error');
        }
    },

    async loadCustomers() {
        try {
            // Verificar se está autenticado
            if (!STATE.adminToken) {
                throw new Error('Não autenticado. Faça login novamente.');
            }
            
            const customers = await API.getCustomers();
            STATE.customers = customers;
            
            const customersList = document.getElementById('customersList');
            customersList.innerHTML = customers.length === 0 
                ? '<p>Nenhum cliente encontrado</p>'
                : customers.map(customer => `
                    <div class="customer-card">
                        <div class="customer-info">
                            <h4>${customer.nome}</h4>
                            <p><strong>Email:</strong> ${customer.email}</p>
                            <p><strong>CPF:</strong> ${customer.cpf}</p>
                        </div>
                    </div>
                `).join('');
        } catch (error) {
            console.error('❌ Erro ao carregar clientes:', error);
            if (error.message.includes('Não autenticado')) {
                Utils.showNotification('Sessão expirada. Faça login novamente.', 'error');
                this.hideAdminPanel();
                this.showLoginModal();
            } else {
                Utils.showNotification('Erro ao carregar clientes: ' + error.message, 'error');
            }
        }
    },

    async loadAnalytics() {
        try {
            // Simulate analytics data
            const todaySales = STATE.orders.reduce((total, order) => {
                const orderDate = new Date(order.data_criacao);
                const today = new Date();
                if (orderDate.toDateString() === today.toDateString()) {
                    return total + (order.total || 0);
                }
                return total;
            }, 0);
            
            const todayOrders = STATE.orders.filter(order => {
                const orderDate = new Date(order.data_criacao);
                const today = new Date();
                return orderDate.toDateString() === today.toDateString();
            }).length;
            
            document.getElementById('todaySales').textContent = Utils.formatPrice(todaySales);
            document.getElementById('todayOrders').textContent = todayOrders;
            document.getElementById('activeCustomers').textContent = STATE.customers.length;
            
            // Most sold product
            const productCounts = {};
            STATE.orders.forEach(order => {
                order.itens?.forEach(item => {
                    const product = STATE.products.find(p => p.id === item.produto_id);
                    if (product) {
                        productCounts[product.nome] = (productCounts[product.nome] || 0) + item.quantidade;
                    }
                });
            });
            
            const topProduct = Object.entries(productCounts)
                .sort(([,a], [,b]) => b - a)[0];
            
            document.getElementById('topProduct').textContent = topProduct ? topProduct[0] : '-';
        } catch (error) {
            Utils.showNotification('Erro ao carregar analytics', 'error');
        }
    }
};

// ===== PRODUCTS MANAGEMENT =====
const Products = {
    async loadProducts() {
        try {
            // Check cache first
            const cachedProducts = localStorage.getItem('cachedProducts');
            const cacheTimestamp = localStorage.getItem('productsCacheTimestamp');
            const now = Date.now();
            
            // Use cache if it's less than 5 minutes old
            if (cachedProducts && cacheTimestamp && (now - parseInt(cacheTimestamp)) < 300000) {
                const products = JSON.parse(cachedProducts);
                STATE.products = products;
                this.renderProducts(products);
                return;
            }
            
            const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.PRODUCTS}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const products = await response.json();
            
            if (!products || products.length === 0) {
                throw new Error('Nenhum produto encontrado no backend');
            }
            
            // Cache the products
            localStorage.setItem('cachedProducts', JSON.stringify(products));
            localStorage.setItem('productsCacheTimestamp', now.toString());
            
            STATE.products = products;
            this.renderProducts(products);
            Utils.showNotification(`${products.length} produtos carregados!`, 'success');
            
        } catch (error) {
            console.error('❌ Erro detalhado ao carregar produtos:', error);
            console.error('❌ Tipo do erro:', error.name);
            console.error('❌ Mensagem do erro:', error.message);
            
            // Try to use cached data if available, even if expired
            const cachedProducts = localStorage.getItem('cachedProducts');
            if (cachedProducts) {
                console.log('📦 Usando produtos do cache (expirado):', cachedProducts);
                const products = JSON.parse(cachedProducts);
                STATE.products = products;
                this.renderProducts(products);
                Utils.showNotification('Produtos carregados do cache (offline)', 'info');
                return;
            }
            
            if (error.name === 'AbortError') {
                Utils.showNotification('Timeout ao carregar produtos (3s)', 'error');
            } else {
                Utils.showNotification(`Erro ao carregar produtos: ${error.message}`, 'error');
            }
            
            // Show loading error state
            const productsGrid = document.getElementById('productsGrid');
            if (productsGrid) {
                productsGrid.innerHTML = `
                    <div class="error-state">
                        <i class="fas fa-exclamation-triangle"></i>
                        <h3>Erro ao carregar produtos</h3>
                        <p>Não foi possível conectar com o backend.</p>
                        <p><strong>Erro:</strong> ${error.message}</p>
                        <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 1rem;">
                            <button class="btn btn-primary" onclick="Products.loadProducts()">
                                <i class="fas fa-refresh"></i> Tentar Novamente
                            </button>
                            <button class="btn btn-secondary" onclick="Products.forceRefresh()">
                                <i class="fas fa-sync"></i> Forçar Atualização
                            </button>
                        </div>
                    </div>
                `;
            }
        }
    },

    renderProducts(products) {
        const productsGrid = document.getElementById('productsGrid');
        
        if (!productsGrid) return;
        
        if (products.length === 0) {
            productsGrid.innerHTML = '<p class="no-products">Nenhum produto encontrado no backend</p>';
            return;
        }
        
        const productsHTML = products.map(product => `
            <div class="product-card">
                <div class="product-image">
                    <i class="${Utils.getCategoryIcon(product.categoria)}"></i>
                </div>
                <div class="product-info">
                    <h3 class="product-name">${product.nome}</h3>
                    <p class="product-category">${Utils.getCategoryName(product.categoria)}</p>
                    <p class="product-price">${Utils.formatPrice(product.preco)}</p>
                    <button class="add-to-cart" onclick="Products.addToCart('${product.id}')">
                        <i class="fas fa-plus"></i> Adicionar
                    </button>
                </div>
            </div>
        `).join('');
        
        productsGrid.innerHTML = productsHTML;
    },

    addToCart(productId) {
        const product = STATE.products.find(p => p.id === productId);
        if (product) {
            Cart.addItem(product);
            Utils.showNotification(`${product.nome} adicionado ao carrinho!`, 'success');
        }
    },

    filterByCategory(category) {
        const products = category === 'all' 
            ? STATE.products 
            : STATE.products.filter(product => product.categoria === category);
        
        this.renderProducts(products);
    },

    clearCache() {
        localStorage.removeItem('cachedProducts');
        localStorage.removeItem('productsCacheTimestamp');
        console.log('🗑️ Cache de produtos limpo');
    },

    forceRefresh() {
        this.clearCache();
        return this.loadProducts();
    }
};

// ===== CHECKOUT PROCESS =====
const Checkout = {
    async processOrder() {
        if (STATE.cart.length === 0) {
            Utils.showNotification('Carrinho vazio!', 'error');
            return;
        }

        try {
            console.log('🛒 Iniciando processamento do pedido...');
            console.log('🛒 Carrinho:', STATE.cart);
            
            // Mostrar modal de identificação do cliente
            const cliente = await this.showCustomerIdentificationModal();
            if (!cliente) {
                console.log('❌ Cliente cancelou identificação');
                return;
            }
            
            console.log('👤 Cliente identificado:', cliente);

            // Verificar regras de negócio para bebidas e sobremesas
            const suggestions = this.checkOrderSuggestions();
            if (suggestions.length > 0) {
                const shouldContinue = await this.showSuggestions(suggestions);
                if (!shouldContinue) {
                    return; // Usuário cancelou para adicionar sugestões
                }
            }

            // Gerar número sequencial do pedido
            const orderNumber = this.generateOrderNumber();

            // Depois, criar o pedido
            const orderData = {
                cliente_id: cliente.id,
                itens: STATE.cart.map(item => ({
                    produto_id: item.id,
                    quantidade: item.quantity
                })),
                observacoes: 'Pedido realizado via sistema web',
                orderNumber: orderNumber
            };

            console.log('📦 Criando pedido:', orderData);
            const order = await API.createOrder(orderData);
            console.log('✅ Pedido criado:', order);
            
            // Adicionar número do pedido à resposta
            order.orderNumber = orderNumber;
            order.orderNumberDisplay = orderNumber; // Garantir que o número seja exibido corretamente
            
            // Mostrar modal de pagamento com QR Code
            await this.showPaymentModal(order);
        } catch (error) {
            console.error('❌ Erro ao processar pedido:', error);
            console.error('❌ Stack trace:', error.stack);
            Utils.showNotification('Erro ao processar pedido: ' + error.message, 'error');
        }
    },

    checkExistingCustomer() {
        // Verificar se há cliente salvo no localStorage
        const savedCustomer = localStorage.getItem('currentCustomer');
        if (savedCustomer) {
            try {
                return JSON.parse(savedCustomer);
            } catch (e) {
                console.error('Erro ao parsear cliente salvo:', e);
            }
        }
        return null;
    },

    checkOrderSuggestions() {
        const suggestions = [];
        const cartCategories = STATE.cart.map(item => item.categoria);
        
        // Verificar se não tem bebida
        if (!cartCategories.includes('drinks')) {
            suggestions.push({
                type: 'drink',
                message: 'Deseja adicionar uma bebida ao seu pedido?',
                products: STATE.products.filter(p => p.categoria === 'drinks').slice(0, 3)
            });
        }
        
        // Verificar se não tem sobremesa
        if (!cartCategories.includes('desserts')) {
            suggestions.push({
                type: 'dessert',
                message: 'Que tal uma sobremesa para completar seu pedido?',
                products: STATE.products.filter(p => p.categoria === 'desserts').slice(0, 3)
            });
        }
        
        return suggestions;
    },

    async showSuggestions(suggestions) {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'suggestions-modal';
            
            let suggestionsHtml = '';
            suggestions.forEach(suggestion => {
                suggestionsHtml += `
                <div class="suggestion-section">
                    <h3>${suggestion.message}</h3>
                    <div class="suggestion-products">
                        ${suggestion.products.map(product => `
                            <div class="suggestion-product" onclick="Checkout.addSuggestionToCart('${product.id}')">
                                <div class="product-info">
                                    <h4>${product.nome}</h4>
                                    <p>${Utils.formatPrice(product.preco)}</p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            });
            
            modal.innerHTML = `
                <div class="suggestions-content">
                    <div class="suggestions-header">
                        <h2>💡 Sugestões para seu pedido</h2>
                        <button class="close-btn" onclick="this.parentElement.parentElement.parentElement.remove(); Checkout.resolveSuggestion(true);">×</button>
                    </div>
                    <div class="suggestions-body">
                        ${suggestionsHtml}
                    </div>
                    <div class="suggestions-footer">
                        <button class="btn btn-secondary" onclick="this.parentElement.parentElement.parentElement.remove(); Checkout.resolveSuggestion(false);">
                            Continuar sem adicionar
                        </button>
                        <button class="btn btn-primary" onclick="this.parentElement.parentElement.parentElement.remove(); Checkout.resolveSuggestion(true);">
                            Finalizar pedido
                        </button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Armazenar a promise para ser resolvida
            Checkout.suggestionPromise = resolve;
        });
    },

    addSuggestionToCart(productId) {
        const product = STATE.products.find(p => p.id === productId);
        if (product) {
            Cart.addItem(product);
            Utils.showNotification(`${product.nome} adicionado ao carrinho!`, 'success');
        }
    },

    resolveSuggestion(shouldContinue) {
        if (Checkout.suggestionPromise) {
            Checkout.suggestionPromise(shouldContinue);
            Checkout.suggestionPromise = null;
        }
    },

    generateOrderNumber() {
        // Gerar número sequencial simples (100, 101, 102...)
        const lastOrderNumber = localStorage.getItem('lastOrderNumber') || 99;
        const newOrderNumber = parseInt(lastOrderNumber) + 1;
        localStorage.setItem('lastOrderNumber', newOrderNumber.toString());
        return newOrderNumber;
    },

    async showCustomerIdentificationModal() {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'customer-identification-modal';
            
            modal.innerHTML = `
                <div class="customer-identification-content">
                    <div class="customer-identification-header">
                        <h2>Identificação do Cliente</h2>
                    </div>
                    <div class="customer-identification-body">
                        <p>Como você gostaria de se identificar?</p>
                        
                        <div class="identification-tabs">
                            <button class="tab-btn active" data-tab="cpf">
                                Buscar por CPF
                            </button>
                            <button class="tab-btn" data-tab="register">
                                Cadastrar
                            </button>
                            <button class="tab-btn" data-tab="anonymous">
                                Anônimo
                            </button>
                        </div>
                        
                        <div class="tab-content">
                            <!-- Tab CPF -->
                            <div class="tab-pane active" id="cpfTab">
                                <div class="form-group">
                                    <label for="cpfInput">CPF:</label>
                                    <input type="text" id="cpfInput" placeholder="000.000.000-00" maxlength="14">
                                </div>
                                <button class="btn btn-primary" onclick="Checkout.searchCustomerByCPF()">
                                    Buscar Cliente
                                </button>
                            </div>
                            
                            <!-- Tab Cadastro -->
                            <div class="tab-pane" id="registerTab">
                                <div class="form-group">
                                    <label for="nameInput">Nome:</label>
                                    <input type="text" id="nameInput" placeholder="Seu nome completo">
                                </div>
                                <div class="form-group">
                                    <label for="emailInput">E-mail:</label>
                                    <input type="email" id="emailInput" placeholder="seu@email.com">
                                </div>
                                <div class="form-group">
                                    <label for="cpfRegisterInput">CPF (opcional):</label>
                                    <input type="text" id="cpfRegisterInput" placeholder="000.000.000-00" maxlength="14">
                                </div>
                            </div>
                            
                            <!-- Tab Anônimo -->
                            <div class="tab-pane" id="anonymousTab">
                                <p>Você fará o pedido como cliente anônimo.</p>
                                <p>Não será possível rastrear seus pedidos anteriores.</p>
                            </div>
                        </div>
                    </div>
                    <div class="customer-identification-footer">
                        <button class="btn btn-secondary" onclick="Checkout.cancelCustomerIdentification()">
                            Cancelar
                        </button>
                        <button class="btn btn-primary" onclick="Checkout.confirmCustomerIdentification()">
                            Continuar
                        </button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Bind events
            this.bindCustomerIdentificationEvents(modal, resolve);
        });
    },

    bindCustomerIdentificationEvents(modal, resolve) {
        // Tab switching
        modal.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                modal.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                modal.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
                
                btn.classList.add('active');
                const tabId = btn.dataset.tab + 'Tab';
                modal.querySelector('#' + tabId).classList.add('active');
            });
        });

        // CPF mask
        const cpfInput = modal.querySelector('#cpfInput');
        const cpfRegisterInput = modal.querySelector('#cpfRegisterInput');
        
        [cpfInput, cpfRegisterInput].forEach(input => {
            if (input) {
                input.addEventListener('input', (e) => {
                    let value = e.target.value.replace(/\D/g, '');
                    value = value.replace(/(\d{3})(\d)/, '$1.$2');
                    value = value.replace(/(\d{3})(\d)/, '$1.$2');
                    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
                    e.target.value = value;
                });
            }
        });

        // Store resolve function
        Checkout.customerIdentificationResolve = resolve;
    },

    async searchCustomerByCPF() {
        const cpf = document.getElementById('cpfInput').value.replace(/\D/g, '');
        if (!cpf || cpf.length !== 11) {
            Utils.showNotification('CPF inválido', 'error');
            return;
        }

        try {
            // Buscar cliente por CPF (implementar endpoint)
            const customer = await API.getCustomerByCPF(cpf);
            if (customer) {
                Utils.showNotification('Cliente encontrado!', 'success');
                Checkout.selectedCustomer = customer;
            } else {
                Utils.showNotification('Cliente não encontrado. Tente cadastrar-se.', 'info');
            }
        } catch (error) {
            Utils.showNotification('Erro ao buscar cliente: ' + error.message, 'error');
        }
    },

    cancelCustomerIdentification() {
        const modal = document.querySelector('.customer-identification-modal');
        if (modal) {
            modal.remove();
        }
        
        if (Checkout.customerIdentificationResolve) {
            Checkout.customerIdentificationResolve(null);
            Checkout.customerIdentificationResolve = null;
        }
    },

    async confirmCustomerIdentification() {
        const activeTab = document.querySelector('.customer-identification-modal .tab-btn.active').dataset.tab;
        
        try {
            let customer = null;
            
            switch (activeTab) {
                case 'cpf':
                    if (Checkout.selectedCustomer) {
                        customer = Checkout.selectedCustomer;
                    } else {
                        Utils.showNotification('Por favor, busque um cliente por CPF primeiro', 'error');
                        return;
                    }
                    break;
                    
                case 'register':
                    const name = document.getElementById('nameInput').value.trim();
                    const email = document.getElementById('emailInput').value.trim();
                    const cpf = document.getElementById('cpfRegisterInput').value.replace(/\D/g, '');
                    
                    if (!name) {
                        Utils.showNotification('Nome é obrigatório', 'error');
                        return;
                    }
                    
                    if (!email) {
                        Utils.showNotification('E-mail é obrigatório', 'error');
                        return;
                    }
                    
                    // Criar novo cliente
                    const customerData = {
                        nome: name,
                        email: email,
                        cpf: cpf || null
                    };
                    
                    customer = await API.createCustomer(customerData);
                    Utils.showNotification('Cliente cadastrado com sucesso!', 'success');
                    break;
                    
                case 'anonymous':
                    // Criar cliente anônimo
                    customer = await API.createCustomer({
                        nome: 'Cliente Anônimo'
                    });
                    break;
            }
            
            // Fechar modal
            const modal = document.querySelector('.customer-identification-modal');
            if (modal) {
                modal.remove();
            }
            
            // Resolver promise
            if (Checkout.customerIdentificationResolve) {
                Checkout.customerIdentificationResolve(customer);
                Checkout.customerIdentificationResolve = null;
            }
            
        } catch (error) {
            console.error('❌ Erro na identificação do cliente:', error);
            Utils.showNotification('Erro na identificação: ' + error.message, 'error');
        }
    },

    async showPaymentModal(order) {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'payment-modal';
            
            // Gerar QR Code simples (simulação)
            const qrCodeData = this.generateQRCodeData(order);
            
            modal.innerHTML = `
                <div class="payment-content">
                    <div class="payment-header">
                        <i class="fas fa-qrcode"></i>
                        <h2>Pagamento via Mercado Pago</h2>
                    </div>
                    <div class="payment-body">
                        <div class="payment-info">
                            <p><strong>Pedido:</strong> #${order.orderNumber}</p>
                            <p><strong>Total:</strong> ${Utils.formatPrice(Cart.getTotal())}</p>
                            <p><strong>Status:</strong> Aguardando Pagamento</p>
                        </div>
                        
                        <div class="qr-code-container">
                            <div class="qr-code">
                                <i class="fas fa-qrcode"></i>
                            </div>
                            <div class="payment-instructions">
                                <p>Escaneie o QR Code com o app do Mercado Pago</p>
                                <p>ou use o PIX para pagamento</p>
                            </div>
                        </div>
                        
                        <div class="payment-timer">
                            <i class="fas fa-clock"></i>
                            <span id="paymentTimer">15:00</span>
                        </div>
                    </div>
                    <div class="payment-footer">
                        <button class="btn btn-secondary" onclick="Checkout.cancelPayment()">
                            Cancelar
                        </button>
                        <button class="btn btn-primary" onclick="Checkout.confirmPayment()">
                            Já Paguei
                        </button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Iniciar timer de pagamento (15 minutos)
            this.startPaymentTimer();
            
            // Armazenar a promise para ser resolvida
            Checkout.paymentPromise = resolve;
        });
    },

    generateQRCodeData(order) {
        // Simulação de dados do QR Code do Mercado Pago
        return {
            amount: Cart.getTotal(),
            orderId: order.orderNumber,
            description: `Pedido #${order.orderNumber} - BurgerHouse`,
            pixKey: 'burgerhouse@mercadopago.com'
        };
    },

    startPaymentTimer() {
        let timeLeft = 15 * 60; // 15 minutos em segundos
        
        const timer = setInterval(() => {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            
            const timerElement = document.getElementById('paymentTimer');
            if (timerElement) {
                timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }
            
            if (timeLeft <= 0) {
                clearInterval(timer);
                this.cancelPayment();
            }
            
            timeLeft--;
        }, 1000);
        
        // Armazenar o timer para poder cancelar
        Checkout.paymentTimer = timer;
    },

    cancelPayment() {
        if (Checkout.paymentTimer) {
            clearInterval(Checkout.paymentTimer);
        }
        
        const modal = document.querySelector('.payment-modal');
        if (modal) {
            modal.remove();
        }
        
        Utils.showNotification('Pagamento cancelado', 'error');
        
        if (Checkout.paymentPromise) {
            Checkout.paymentPromise(false);
            Checkout.paymentPromise = null;
        }
    },

    confirmPayment() {
        if (Checkout.paymentTimer) {
            clearInterval(Checkout.paymentTimer);
        }
        
        const modal = document.querySelector('.payment-modal');
        if (modal) {
            modal.remove();
        }
        
        Utils.showNotification('Pagamento confirmado! Pedido em preparação.', 'success');
        
        // Limpar carrinho e fechar sidebar
        Cart.clear();
        CartSidebar.hide();
        
        // Mostrar confirmação do pedido com tracking
        const orderWithNumber = {
            ...Checkout.currentOrder,
            status: 'Pago',
            orderNumber: Checkout.currentOrder?.orderNumber,
            orderNumberDisplay: Checkout.currentOrder?.orderNumberDisplay
        };
        this.showOrderConfirmation(orderWithNumber);
        
        if (Checkout.paymentPromise) {
            Checkout.paymentPromise(true);
            Checkout.paymentPromise = null;
        }
    },

    showOrderConfirmation(order) {
        // Armazenar pedido atual para referência
        Checkout.currentOrder = order;
        
        console.log('🔍 Order object in confirmation:', order);
        console.log('🔍 Order ID:', order.id);
        console.log('🔍 Order Number:', order.orderNumber);
        console.log('🔍 Order Number Display:', order.orderNumberDisplay);
        
        const orderNumber = order.orderNumberDisplay || order.orderNumber || order.id || 'N/A';
        console.log('🔍 Final order number:', orderNumber);
        
        const modal = document.createElement('div');
        modal.className = 'order-confirmation-modal';
        modal.innerHTML = `
            <div class="order-confirmation-content">
                <div class="order-confirmation-header">
                    <h2>Pedido Confirmado!</h2>
                </div>
                <div class="order-confirmation-body">
                    <p><strong>Número do Pedido:</strong> #${orderNumber}</p>
                    <p><strong>Status:</strong> ${order.status || 'Pago'}</p>
                    <p><strong>Total:</strong> ${Utils.formatPrice(Cart.getTotal())}</p>
                    <p>Seu pedido está sendo preparado!</p>
                </div>
                <div class="order-tracking">
                    <div class="tracking-step active" data-step="received">
                        <span>Recebido</span>
                    </div>
                    <div class="tracking-step" data-step="preparing">
                        <span>Em Preparação</span>
                    </div>
                    <div class="tracking-step" data-step="ready">
                        <span>Pronto</span>
                    </div>
                    <div class="tracking-step" data-step="finished">
                        <span>Finalizado</span>
                    </div>
                </div>
                <button class="btn btn-primary" onclick="this.parentElement.parentElement.remove()">
                    Fechar
                </button>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Iniciar simulação de progresso do pedido
        this.simulateOrderProgress(order.id);
    },

    simulateOrderProgress(orderId) {
        const steps = ['received', 'preparing', 'ready', 'finished'];
        let currentStep = 0;
        
        const interval = setInterval(() => {
            if (currentStep < steps.length) {
                // Atualizar visual do progresso
                document.querySelectorAll('.tracking-step').forEach((step, index) => {
                    if (index <= currentStep) {
                        step.classList.add('active');
                    } else {
                        step.classList.remove('active');
                    }
                });
                
                // Atualizar status no texto
                const statusText = document.querySelector('.order-confirmation-body p:nth-child(2)');
                if (statusText) {
                    const statusMap = {
                        'received': 'Recebido',
                        'preparing': 'Em Preparação',
                        'ready': 'Pronto',
                        'finished': 'Finalizado'
                    };
                    statusText.innerHTML = `<strong>Status:</strong> ${statusMap[steps[currentStep]]}`;
                }
                
                currentStep++;
            } else {
                clearInterval(interval);
            }
        }, 30000); // 30 segundos entre cada status
    }
};

// ===== CART SIDEBAR =====
const CartSidebar = {
    init() {
        this.bindEvents();
    },

    bindEvents() {
        document.getElementById('cartIcon')?.addEventListener('click', () => this.show());
        document.getElementById('closeCart')?.addEventListener('click', () => this.hide());
        document.getElementById('cartOverlay')?.addEventListener('click', () => this.hide());
        document.getElementById('checkoutBtn')?.addEventListener('click', () => Checkout.processOrder());
    },

    show() {
        document.getElementById('cartSidebar').classList.add('active');
        document.getElementById('cartOverlay').classList.add('active');
        document.body.style.overflow = 'hidden';
    },

    hide() {
        document.getElementById('cartSidebar').classList.remove('active');
        document.getElementById('cartOverlay').classList.remove('active');
        document.body.style.overflow = '';
    }
};

// ===== NAVIGATION =====
const Navigation = {
    init() {
        this.bindEvents();
        this.handleScroll();
    },

    bindEvents() {
        // Mobile menu toggle
        document.getElementById('navToggle')?.addEventListener('click', () => this.toggleMobileMenu());
        
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
        
        // Category filter
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                Products.filterByCategory(btn.dataset.category);
            });
        });
    },

    toggleMobileMenu() {
        const navMenu = document.getElementById('navMenu');
        navMenu?.classList.toggle('active');
    },

    handleScroll() {
        window.addEventListener('scroll', Utils.debounce(() => {
            const header = document.querySelector('.header');
            if (window.scrollY > 100) {
                header?.classList.add('scrolled');
            } else {
                header?.classList.remove('scrolled');
            }
        }, 100));
    }
};

// ===== FORM HANDLING =====
const Forms = {
    init() {
        this.bindEvents();
    },

    bindEvents() {
        document.getElementById('contactForm')?.addEventListener('submit', (e) => this.handleContactForm(e));
    },

    async handleContactForm(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            message: formData.get('message')
        };
        
        // Simulate form submission
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        Utils.showNotification('Mensagem enviada com sucesso!', 'success');
        e.target.reset();
    }
};

// ===== LOADING SCREEN =====
const LoadingScreen = {
    init() {
        // Force hide loading screen after 1 second regardless of what happens
        setTimeout(() => {
            this.hide();
        }, 1000);
    },

    show() {
        const loadingScreen = document.getElementById('loadingScreen');
        if (loadingScreen) {
            loadingScreen.classList.remove('hidden');
            loadingScreen.style.display = 'flex';
        }
    },

    hide() {
        const loadingScreen = document.getElementById('loadingScreen');
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
            // Force hide with inline styles as backup
            loadingScreen.style.display = 'none';
        }
    }
};

// ===== ORDERS PANEL =====
const OrdersPanel = {
    init() {
        this.bindEvents();
        this.loadOrdersPanel();
        this.startAutoRefresh();
    },

    bindEvents() {
        // Listen for hash changes to load orders panel
        window.addEventListener('hashchange', () => {
            if (window.location.hash === '#orders-panel') {
                this.loadOrdersPanel();
            }
        });
    },

    startAutoRefresh() {
        // Atualizar painel a cada 20 segundos
        setInterval(() => {
            if (window.location.hash === '#orders-panel') {
                this.loadOrdersPanel();
            }
        }, 20000); // 20 segundos
    },

    async loadOrdersPanel() {
        try {
            console.log('📊 Carregando painel de pedidos...');
            console.log('📊 Hash atual:', window.location.hash);
            const orders = await API.getPublicOrders();
            console.log('📊 Pedidos recebidos:', orders);
            this.updateStats(orders);
            this.renderOrders(orders);
        } catch (error) {
            console.error('Erro ao carregar pedidos:', error);
            Utils.showNotification('Erro ao carregar pedidos', 'error');
        }
    },

    updateStats(orders) {
        const totalOrders = orders.length;
        const preparingOrders = orders.filter(order => order.status === 'preparando').length;
        const readyOrders = orders.filter(order => order.status === 'pronto').length;
        const finishedOrders = orders.filter(order => order.status === 'entregue').length;

        document.getElementById('totalOrders').textContent = totalOrders;
        document.getElementById('preparingOrders').textContent = preparingOrders;
        document.getElementById('readyOrders').textContent = readyOrders;
        document.getElementById('finishedOrders').textContent = finishedOrders;
    },

    renderOrders(orders) {
        const ordersList = document.getElementById('ordersList');
        if (!ordersList) {
            console.log('❌ Elemento ordersList não encontrado');
            return;
        }

        console.log('📊 Renderizando pedidos:', orders);
        console.log('📊 Quantidade de pedidos:', orders.length);

        if (orders.length === 0) {
            console.log('📊 Nenhum pedido para renderizar');
            ordersList.innerHTML = '';
            return;
        }

        // Ordenar pedidos por data (mais recentes primeiro)
        const sortedOrders = orders.sort((a, b) => {
            const dateA = new Date(a.data_criacao || a.created_at || 0);
            const dateB = new Date(b.data_criacao || b.created_at || 0);
            return dateB - dateA;
        });
        console.log('📊 Pedidos ordenados:', sortedOrders);

        ordersList.innerHTML = sortedOrders.map(order => {
            const statusClass = this.getStatusClass(order.status);
            const statusText = this.getStatusText(order.status);
            const orderTime = new Date(order.data_criacao || order.created_at).toLocaleString('pt-BR');
            
            const itemsText = order.itens.map(item => {
                // Verificar se temos informações do produto
                if (item.produto && item.produto.nome) {
                    return `${item.quantidade}x ${item.produto.nome}`;
                } else if (item.produto_id) {
                    // Se não temos o nome do produto, usar o ID
                    return `${item.quantidade}x Produto #${item.produto_id.slice(0, 8)}`;
                } else {
                    return `${item.quantidade}x Item`;
                }
            }).join(', ');

            console.log('📊 Renderizando pedido:', order.id, 'com status:', order.status);

            return `
                <div class="order-item">
                    <div class="order-header">
                        <span class="order-number">Pedido #${order.id}</span>
                        <span class="order-status ${statusClass}">${statusText}</span>
                    </div>
                    <div class="order-details">
                        <div class="order-items">${itemsText}</div>
                        <div class="order-total">R$ ${(order.total || 0).toFixed(2).replace('.', ',')}</div>
                    </div>
                    <div class="order-time">
                        <i class="fas fa-clock"></i> ${orderTime}
                    </div>
                </div>
            `;
        }).join('');
        
        console.log('📊 HTML gerado para ordersList');
    },

    getStatusClass(status) {
        const statusMap = {
            'pendente': 'pending',
            'preparando': 'preparing',
            'pronto': 'ready',
            'entregue': 'finished'
        };
        return statusMap[status] || 'pending';
    },

    getStatusText(status) {
        const statusMap = {
            'pendente': 'Pendente',
            'preparando': 'Em Preparação',
            'pronto': 'Pronto',
            'entregue': 'Finalizado'
        };
        return statusMap[status] || 'Pendente';
    }
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    // Show loading screen and force hide after 2 seconds
    LoadingScreen.show();
    LoadingScreen.init();
    
    // Initialize all modules
    try {
        Navigation.init();
        CartSidebar.init();
        AdminPanel.init();
        Forms.init();
        OrdersPanel.init();
        Cart.loadFromStorage();
    } catch (error) {
        console.error('Erro ao inicializar módulos:', error);
    }
    
    // Load products immediately (will use cache if available)
    Products.loadProducts().catch(error => {
        console.error('Erro ao carregar produtos:', error);
        Utils.showNotification('Erro ao carregar produtos do backend', 'error');
    });
});

// Fallback: Hide loading screen after 3 seconds maximum
setTimeout(() => {
    LoadingScreen.hide();
}, 3000);

// ===== GLOBAL FUNCTIONS =====
window.Cart = Cart;
window.Products = Products;
window.AdminPanel = AdminPanel;
window.Checkout = Checkout;
window.Utils = Utils;
window.OrdersPanel = OrdersPanel;