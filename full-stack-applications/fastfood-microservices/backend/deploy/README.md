# Dockerfile - FastFood Backend

Este diretório contém o Dockerfile oficial para o backend FastAPI do projeto FastFood.

## Como usar

### Build local/manual

Execute o build a partir da raiz do projeto ou do diretório backend:

```bash
# A partir da raiz do projeto

docker build -f backend/deploy/Dockerfile -t fastfood-api:latest backend/

# Ou, se estiver dentro de backend/
docker build -f deploy/Dockerfile -t fastfood-api:latest .
```

### Contexto de build
- O contexto deve ser o diretório `backend/` para garantir que todos os arquivos necessários sejam copiados corretamente.
- O Dockerfile espera encontrar `src/`, `config/`, `scripts/` e `requirements.txt` dentro do contexto.

### Para Kubernetes
O script `scripts/kubernetes/deploy-k8s.sh` já usa o caminho correto do Dockerfile.

---

Dúvidas? Consulte o README principal do projeto ou abra uma issue. 