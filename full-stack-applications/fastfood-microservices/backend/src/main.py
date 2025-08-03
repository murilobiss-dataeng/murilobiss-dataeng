from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings

# Imports dos routers
from src.adapters.input.api.public import (
    auth_controller,
    cliente_controller,
    pagamento_controller,
    pedido_controller,
    produto_controller,
)

from src.adapters.input.api.admin import (
    cliente_controller as admin_cliente_controller,
    pedido_controller as admin_pedido_controller,
    produto_controller as admin_produto_controller,
)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

@app.get("/")
@app.head("/")
def root():
    """Rota raiz da API"""
    return {
        "message": "🍔 BurgerHouse API",
        "version": settings.API_VERSION,
        "status": "online",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "public": "/api/public",
            "admin": "/api/admin"
        }
    }

@app.get("/health")
@app.head("/health")
def health_check():
    return {"status": "healthy", "version": settings.API_VERSION}

# Rotas públicas
app.include_router(auth_controller.router)
app.include_router(cliente_controller.router)
app.include_router(produto_controller.router)
app.include_router(pedido_controller.router)
app.include_router(pagamento_controller.router)

# Rotas administrativas
app.include_router(admin_cliente_controller.router)
app.include_router(admin_pedido_controller.router)
app.include_router(admin_produto_controller.router)

