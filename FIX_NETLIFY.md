# 🔧 Corrigir "Page Not Found" no Netlify

## Problema: Página não encontrada (404)

### Solução 1: Verificar Configuração no Netlify

1. **Acesse o Netlify Dashboard**: https://app.netlify.com
2. Vá em **Site settings** → **Build & deploy**
3. Verifique:
   - **Base directory**: Deixe vazio ou `.`
   - **Publish directory**: `.` (ponto)
   - **Build command**: Deixe **VAZIO** (não precisa de build)
4. Salve as alterações

### Solução 2: Re-fazer Deploy

1. No Netlify, vá em **Deploys**
2. Clique nos **3 pontinhos** → **Clear cache and retry deploy**
3. Ou faça um novo deploy manual arrastando os arquivos

### Solução 3: Verificar Arquivos na Raiz

Certifique-se de que estes arquivos estão na **raiz** do repositório:

```
✅ index.html
✅ netlify.toml
✅ _redirects
✅ assets/
   ✅ css/jaime.css
   ✅ js/main.js
   ✅ js/funil.js
```

### Solução 4: Verificar Caminhos dos Assets

Os caminhos no HTML devem ser **relativos**:

```html
<!-- ✅ CORRETO -->
<link rel="stylesheet" href="assets/css/jaime.css">
<script src="assets/js/main.js"></script>

<!-- ❌ ERRADO -->
<link rel="stylesheet" href="/assets/css/jaime.css">
```

### Solução 5: Configuração Manual no Netlify

Se ainda não funcionar:

1. **Site settings** → **Build & deploy** → **Build settings**
2. Clique em **"Edit settings"**
3. Configure:
   - **Build command**: (deixe vazio)
   - **Publish directory**: `.`
4. Salve

### Solução 6: Deploy via GitHub (Recomendado)

1. Certifique-se de que o código está no GitHub
2. No Netlify: **Add new site** → **Import an existing project**
3. Conecte com GitHub
4. Selecione o repositório: `Site-Jaime-Reabilitacao`
5. Configure:
   - **Build command**: (vazio)
   - **Publish directory**: `.`
6. Deploy!

### Solução 7: Verificar Logs de Deploy

1. No Netlify, vá em **Deploys**
2. Clique no deploy mais recente
3. Veja os **logs** para identificar erros
4. Procure por mensagens de erro

## ✅ Checklist Final

- [ ] `index.html` está na raiz
- [ ] `netlify.toml` está na raiz
- [ ] `_redirects` está na raiz
- [ ] Pasta `assets/` está na raiz
- [ ] Caminhos dos assets são relativos (sem `/` no início)
- [ ] Build command está vazio no Netlify
- [ ] Publish directory é `.` no Netlify

## 🚀 Teste Local Antes

Teste localmente antes de fazer deploy:

```bash
# Instalar servidor simples
npm install -g serve

# Ou usar Python
python -m http.server 8000

# Acesse: http://localhost:8000
```

Se funcionar localmente, deve funcionar no Netlify!

## 📞 Se Nada Funcionar

1. Delete o site no Netlify
2. Crie um novo site
3. Faça deploy manual arrastando os arquivos
4. Configure conforme Solução 1

---

**Arquivos atualizados:**
- ✅ `netlify.toml` - Configuração corrigida
- ✅ `_redirects` - Redirecionamentos configurados

