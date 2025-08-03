# Ambientes e Variáveis de Ambiente

## Backend (FastAPI)

### Local
- Use o arquivo `.env` na pasta `backend`.
- Exemplo: veja `backend/.env.example`.
- O Dockerfile copia o `.env` se existir para facilitar testes locais.
- Para rodar localmente:
  ```sh
  cd backend
  cp .env.example .env
  docker build -f deploy/Dockerfile -t fastfood-backend .
  docker run --env-file .env -p 8000:8000 fastfood-backend
  ```

### Render
- Configure as variáveis de ambiente pelo painel do Render.
- Não use `.env` no Render.
- O Dockerfile ignora `.env` se não existir.

## Frontend (Vercel ou Local)

### Local
- Use o arquivo `.env.local` na pasta `frontend`.
- Exemplo: veja `frontend/.env.local.example`.
- Para rodar localmente:
  ```sh
  cd frontend
  cp .env.local.example .env.local
  npm install
  npm run dev
  ```

### Vercel
- Configure a variável `VITE_API_URL` no painel do Vercel.
- Não use `.env.local` no Vercel.

---

## Dicas
- Nunca suba arquivos `.env` reais para o repositório.
- Sempre use os exemplos para facilitar o setup de novos desenvolvedores. 