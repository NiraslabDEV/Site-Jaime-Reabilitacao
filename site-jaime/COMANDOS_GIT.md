# 🚀 Comandos para Subir no GitHub

## Opção 1: Se você JÁ CRIOU o repositório no GitHub

```bash
# Adicionar o remote (substitua NOME-DO-REPO pelo nome do seu repositório)
git remote add origin https://github.com/NiraslabDEV/NOME-DO-REPO.git

# Verificar se foi adicionado
git remote -v

# Fazer push
git push -u origin main
```

## Opção 2: Criar repositório NOVO no GitHub

### Passo 1: Criar no GitHub
1. Acesse: https://github.com/new
2. Nome do repositório: `site-jaime-reabilitacao` (ou outro nome)
3. Deixe **público** ou **privado** (sua escolha)
4. **NÃO** marque "Add a README file" (já temos)
5. Clique em **"Create repository"**

### Passo 2: Conectar e fazer push
```bash
# Adicionar remote (substitua NOME-DO-REPO pelo nome que você escolheu)
git remote add origin https://github.com/NiraslabDEV/NOME-DO-REPO.git

# Verificar
git remote -v

# Fazer push
git push -u origin main
```

## Se der erro de autenticação

Use token pessoal do GitHub:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Marque: `repo` (todas as permissões)
4. Copie o token
5. Use no lugar da senha quando pedir

Ou use SSH:
```bash
git remote set-url origin git@github.com:NiraslabDEV/NOME-DO-REPO.git
```

