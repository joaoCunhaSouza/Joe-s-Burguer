# Guia Completo - Git Commit e Deploy no Render

## 📋 Resumo das Alterações

Neste commit, foram realizadas as seguintes correções:

### ✅ Correções de CSRF (Erro 403 Forbidden)
- Adicionado `@ensure_csrf_cookie` nas views de login
- Configurado CSRF corretamente no settings.py
- Adicionado script JavaScript para refresh automático do token CSRF
- Corrigida ordem dos middlewares

### ✅ Layout do Login da Cozinha
- Login da cozinha agora está idêntico ao login do admin
- Removido background gradiente vibrante
- Aplicado design minimalista e profissional
- Cores neutras (cinza e vermelho)

### 📁 Arquivos Modificados
1. `foodmarket/foodmarket/settings.py`
2. `foodmarket/marketplace/views_admin.py`
3. `foodmarket/marketplace/views_kitchen.py`
4. `foodmarket/marketplace/templates/kitchen_login.html`
5. `foodmarket/marketplace/templates/kitchen_base.html`
6. `foodmarket/marketplace/templates/admin_custom/admin_login.html`
7. `foodmarket/criar_usuario_cozinha.py`
8. Documentações: `CORRECOES_COZINHA.md` e `CORRECAO_CSRF_FORBIDEN.md`

---

## 🚀 Opção 1: Usando o Script Automático

### No Windows:
```bash
cd foodmarket
git_push.bat
```

### No Linux/Mac:
```bash
cd foodmarket
chmod +x git_push.sh
./git_push.sh
```

---

## 🔧 Opção 2: Comandos Manuais

Execute os comandos abaixo no terminal:

### Passo 1: Navegue até a pasta do projeto
```bash
cd foodmarket
```

### Passo 2: Verifique o status
```bash
git status
```

### Passo 3: Adicione todos os arquivos modificados
```bash
git add .
```

### Passo 4: Crie o commit
```bash
git commit -m "Fix: Corrigido erro CSRF 403 entre login da cozinha e admin + Layout identico para ambos os logins"
```

### Passo 5: Envie para o GitHub
```bash
git push origin main
```

**Nota:** Se sua branch principal for `master` ao invés de `main`, use:
```bash
git push origin master
```

---

## 📦 Deploy Automático no Render

O Render está configurado para fazer deploy automático quando detectar mudanças no GitHub.

### O que acontece automaticamente:

1. ✅ Render detecta o push no GitHub
2. ✅ Inicia o build automaticamente
3. ✅ Instala as dependências (`requirements.txt`)
4. ✅ Executa as migrações do banco de dados
5. ✅ Coleta os arquivos estáticos
6. ✅ Reinicia o servidor com as novas alterações

### Acompanhar o Deploy:

1. Acesse: https://dashboard.render.com
2. Entre com sua conta
3. Clique no seu serviço "joe-s-burguer"
4. Veja o log do deploy em tempo real
5. Aguarde a mensagem "Deploy live" (geralmente leva 2-5 minutos)

---

## 🔍 Verificando se o Deploy Funcionou

Após o deploy ser concluído, teste:

### 1. Teste o Login da Cozinha
```
https://joe-s-burguer.onrender.com/kitchen/login/
```
- Verifique se o layout está correto
- Tente fazer login com: `cozinha` / `cozinha123`

### 2. Teste o Login do Admin
```
https://joe-s-burguer.onrender.com/myadmin/login/
```
- Verifique se o layout está igual ao da cozinha
- Tente fazer login com seu email e senha de admin

### 3. Teste o Erro CSRF Corrigido
1. Faça login na cozinha
2. Acesse o admin (sem fazer logout da cozinha)
3. Tente fazer login no admin
4. ✅ **Deve funcionar sem erro 403!**

---

## ⚠️ Possíveis Problemas

### Problema 1: "fatal: not a git repository"
**Solução:** Você está fora da pasta do projeto. Execute:
```bash
cd caminho/para/Joe-s-Burguer/foodmarket
```

### Problema 2: "Permission denied (publickey)"
**Solução:** Configure sua chave SSH do GitHub:
```bash
ssh-keygen -t ed25519 -C "seu-email@example.com"
cat ~/.ssh/id_ed25519.pub
# Copie a chave e adicione em: GitHub → Settings → SSH Keys
```

### Problema 3: "Updates were rejected"
**Solução:** Atualize seu repositório local primeiro:
```bash
git pull origin main
# Depois tente o push novamente
git push origin main
```

### Problema 4: Render não detecta as mudanças
**Solução:** Force o deploy manualmente:
1. Acesse https://dashboard.render.com
2. Clique no seu serviço
3. Clique em "Manual Deploy" → "Deploy latest commit"

---

## 📊 Checklist Final

Antes de fazer o push, verifique:

- [ ] Todos os arquivos importantes foram salvos
- [ ] O servidor local está funcionando sem erros
- [ ] Os testes foram feitos localmente
- [ ] O commit tem uma mensagem descritiva
- [ ] Você está na branch correta (main ou master)

Após o push:

- [ ] Verificar no GitHub se os arquivos foram enviados
- [ ] Acompanhar o deploy no Render
- [ ] Testar o site em produção
- [ ] Verificar os logs se houver erros

---

## 🆘 Suporte

Se encontrar algum erro durante o processo:

1. **Verifique os logs do Render:**
   - Dashboard → Seu serviço → Logs
   - Procure por mensagens de erro em vermelho

2. **Verifique o status do Git:**
   ```bash
   git status
   git log --oneline -5
   ```

3. **Reverta se necessário:**
   ```bash
   git reset --soft HEAD~1  # Desfaz o último commit (mantém as alterações)
   git reset --hard HEAD~1  # Desfaz o último commit (remove as alterações)
   ```

---

## 📝 Notas Importantes

- **Backup:** Sempre faça backup antes de fazer deploy em produção
- **Testes:** Teste tudo localmente antes de fazer push
- **Commits:** Faça commits frequentes com mensagens descritivas
- **Render:** O deploy automático pode levar alguns minutos
- **Cache:** Se o site não atualizar, limpe o cache do navegador (Ctrl+Shift+R)

---

## 🎉 Sucesso!

Se tudo correu bem, suas alterações agora estão:
- ✅ No GitHub (versionadas)
- ✅ No Render (em produção)
- ✅ Funcionando sem erro CSRF
- ✅ Com layout idêntico entre cozinha e admin

**Parabéns!** Seu projeto está atualizado e funcionando! 🚀
