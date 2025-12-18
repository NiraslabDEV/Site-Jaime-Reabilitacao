# 📋 Passo a Passo - Subir no GitHub

## ✅ O que já foi feito:
- ✅ Todos os arquivos foram commitados
- ✅ Remote foi adicionado: `https://github.com/NiraslabDEV/site-jaime-reabilitacao.git`

## 🚀 Próximos Passos:

### Passo 1: Criar Repositório no GitHub

1. **Acesse**: https://github.com/new
2. **Nome do repositório**: `site-jaime-reabilitacao` (ou outro nome de sua escolha)
3. **Descrição** (opcional): "Site para reabilitação física e saúde funcional em Maputo"
4. **Visibilidade**: 
   - ☑️ Público (qualquer um pode ver)
   - ☐ Privado (só você vê)
5. **IMPORTANTE**: 
   - ❌ **NÃO** marque "Add a README file"
   - ❌ **NÃO** marque "Add .gitignore"
   - ❌ **NÃO** marque "Choose a license"
   - (Já temos esses arquivos!)
6. Clique em **"Create repository"**

### Passo 2: Fazer Push

Depois de criar o repositório, execute:

```bash
git push -u origin main
```

Se pedir credenciais:
- **Usuário**: NiraslabDEV
- **Senha**: Use um **Personal Access Token** (não sua senha do GitHub)

### Passo 3: Criar Token (se necessário)

Se pedir autenticação:

1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. **Nome**: `git-push-token`
4. **Expiração**: 90 dias (ou sem expiração)
5. **Permissões**: Marque `repo` (todas as permissões de repositório)
6. Clique em **"Generate token"**
7. **COPIE O TOKEN** (você só verá uma vez!)
8. Use esse token como senha quando o Git pedir

---

## 🎯 Comandos Rápidos

Depois de criar o repositório no GitHub:

```bash
# Verificar remote
git remote -v

# Fazer push
git push -u origin main
```

---

## ✅ Depois do Push

Seu repositório estará em:
**https://github.com/NiraslabDEV/site-jaime-reabilitacao**

E você poderá:
- ✅ Conectar no Netlify para deploy automático
- ✅ Compartilhar o código
- ✅ Fazer atualizações futuras com `git push`

---

## 🔄 Para Atualizações Futuras

Sempre que fizer mudanças:

```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

