# 🚀 Guia de Deploy no Netlify

## Método 1: Deploy Manual (Mais Rápido)

### Passo 1: Preparar os arquivos
Todos os arquivos já estão prontos! Você tem:
- ✅ `netlify.toml` (configuração)
- ✅ `_redirects` (redirecionamentos)
- ✅ Todos os arquivos HTML, CSS e JS

### Passo 2: Acessar Netlify
1. Acesse: https://app.netlify.com
2. Faça login (pode usar GitHub, Google, ou email)

### Passo 3: Deploy Manual
1. Na dashboard do Netlify, clique em **"Add new site"** → **"Deploy manually"**
2. Arraste a pasta do projeto OU selecione os arquivos:
   - Todos os arquivos `.html`
   - Pasta `assets/` completa
   - Arquivos `netlify.toml` e `_redirects`
3. Clique em **"Deploy site"**

### Passo 4: Configurar Domínio
1. Após o deploy, você verá uma URL tipo: `https://random-name-123.netlify.app`
2. Para mudar o nome:
   - Vá em **Site settings** → **Change site name**
   - Escolha um nome personalizado (ex: `reabilitacao-saude-maputo`)

---

## Método 2: Deploy via GitHub (Recomendado)

### Passo 1: Criar Repositório no GitHub
1. Acesse: https://github.com/new
2. Crie um novo repositório (ex: `site-jaime-reabilitacao`)
3. Faça upload dos arquivos:
   ```bash
   git init
   git add .
   git commit -m "Site Reabilitação & Saúde"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
   git push -u origin main
   ```

### Passo 2: Conectar no Netlify
1. No Netlify, clique em **"Add new site"** → **"Import an existing project"**
2. Escolha **GitHub**
3. Autorize o Netlify a acessar seus repositórios
4. Selecione o repositório criado

### Passo 3: Configurar Build
- **Build command**: Deixe vazio (site estático)
- **Publish directory**: `.` (raiz)
- Clique em **"Deploy site"**

### Passo 4: Deploy Automático
- A cada `git push`, o Netlify faz deploy automaticamente! 🎉

---

## 📋 Checklist de Arquivos

Certifique-se de que estes arquivos estão na raiz:
- ✅ `index.html`
- ✅ `reabilitacao.html`
- ✅ `idosos.html`
- ✅ `atletas.html`
- ✅ `avaliacao.html`
- ✅ `metodo.html`
- ✅ `planos.html`
- ✅ `funil.html`
- ✅ `netlify.toml`
- ✅ `_redirects`
- ✅ Pasta `assets/` com:
  - `css/jaime.css`
  - `js/main.js`
  - `js/funil.js`

---

## 🔧 Configurações Importantes

### Arquivo `netlify.toml`
Já está configurado para:
- Publicar da raiz do projeto
- Redirecionar todas as rotas para `index.html` (SPA-like)

### Arquivo `_redirects`
Garante que todas as páginas funcionem corretamente.

---

## 🌐 Domínio Personalizado (Opcional)

### Passo 1: Comprar Domínio
- Compre um domínio (ex: `reabilitacaomaputo.com`)
- Em qualquer registrador (GoDaddy, Namecheap, etc.)

### Passo 2: Configurar no Netlify
1. No Netlify: **Site settings** → **Domain management**
2. Clique em **"Add custom domain"**
3. Digite seu domínio
4. Siga as instruções de DNS:
   - Adicione os registros CNAME ou A apontando para o Netlify
   - O Netlify fornece os valores exatos

### Passo 3: SSL Automático
- O Netlify fornece SSL gratuito automaticamente! 🔒

---

## ✅ Testar Após Deploy

1. Acesse a URL fornecida pelo Netlify
2. Teste todas as páginas:
   - `/` (landing page)
   - `/reabilitacao.html`
   - `/idosos.html`
   - `/atletas.html`
   - `/funil.html` (mais importante!)
3. Teste o funil completo:
   - Preencha todas as etapas
   - Verifique se o WhatsApp abre corretamente
   - Confirme que a mensagem está formatada

---

## 🐛 Problemas Comuns

### Páginas não carregam
- Verifique se o arquivo `_redirects` está na raiz
- Confirme que os caminhos dos arquivos CSS/JS estão corretos

### CSS não aplica
- Verifique se `assets/css/jaime.css` existe
- Abra o console do navegador (F12) e veja erros

### WhatsApp não abre
- Verifique o número no `funil.js`: `258842391741`
- Teste o link manualmente

### Menu mobile não funciona
- Verifique se `assets/js/main.js` está carregando
- Abra o console do navegador para ver erros

---

## 📱 Testar no Mobile

1. Acesse a URL no celular
2. Teste o funil completo
3. Verifique se o WhatsApp abre corretamente
4. Confirme que a mensagem está formatada

---

## 🎉 Pronto!

Seu site está no ar! Compartilhe a URL com o Jaime.

**URL do site**: `https://seu-site.netlify.app`

---

## 📞 Suporte Netlify

- Documentação: https://docs.netlify.com
- Comunidade: https://community.netlify.com
- Status: https://www.netlifystatus.com

