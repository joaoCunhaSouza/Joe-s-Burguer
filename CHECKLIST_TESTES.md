# ✅ CHECKLIST DE TESTES - PAINEL ADMIN

## 📋 Antes de Começar

- [ ] Servidor Django está rodando (`python manage.py runserver`)
- [ ] Superusuário foi criado
- [ ] Navegador está aberto

## 🔐 Teste 1: Login

1. [ ] Acessar http://127.0.0.1:8000/myadmin/login/
2. [ ] Página de login carrega corretamente
3. [ ] Design está bonito e profissional
4. [ ] Inserir email do superusuário
5. [ ] Inserir senha
6. [ ] Clicar em "Entrar no Painel"
7. [ ] Redireciona para o Dashboard

### ❌ Se falhar:
- Verifique se o superusuário existe
- Confirme que está usando EMAIL, não username
- Veja se há erros no console do navegador

## 📊 Teste 2: Dashboard

1. [ ] Dashboard carrega corretamente
2. [ ] Estatísticas aparecem (Total de Produtos, Combos, Pedidos)
3. [ ] Menu superior está visível
4. [ ] Todas as opções do menu estão presentes
5. [ ] Botões de "Acesso Rápido" funcionam

## 🍔 Teste 3: Produtos

### Listar Produtos
1. [ ] Clicar em "Produtos" no menu
2. [ ] Lista de produtos carrega
3. [ ] Botão "+ Adicionar Produto" está visível

### Adicionar Produto
1. [ ] Clicar em "+ Adicionar Produto"
2. [ ] Formulário carrega corretamente
3. [ ] Preencher todos os campos:
   - Nome: "Hambúrguer Teste"
   - Preço: 19.90
   - Descrição: "Um hambúrguer delicioso de teste"
   - Imagem: (fazer upload de uma imagem)
4. [ ] Preview da imagem aparece
5. [ ] Clicar em "Salvar"
6. [ ] Mensagem de sucesso aparece
7. [ ] Redireciona para lista de produtos
8. [ ] Produto aparece na lista

### Editar Produto
1. [ ] Clicar em "Editar" no produto criado
2. [ ] Formulário carrega com dados preenchidos
3. [ ] Alterar o preço para 21.90
4. [ ] Clicar em "Salvar"
5. [ ] Mensagem de sucesso aparece
6. [ ] Preço atualizado na lista

### Excluir Produto (NÃO EXECUTE AINDA)
1. [ ] Botão "Excluir" está presente
2. [ ] Ao clicar, confirmação aparece
3. [ ] (Cancelar a exclusão para não perder dados)

## 🥤 Teste 4: Subprodutos

### Adicionar Subproduto
1. [ ] Clicar em "Subprodutos" no menu
2. [ ] Clicar em "+ Adicionar Subproduto"
3. [ ] Formulário carrega
4. [ ] Selecionar produto principal
5. [ ] Preencher:
   - Nome: "Queijo Extra"
   - Preço: 3.00
   - Descrição: "Fatia adicional de queijo"
6. [ ] Upload de imagem (opcional)
7. [ ] Salvar
8. [ ] Subproduto aparece na lista

### Verificar na Lista
1. [ ] Nome do subproduto está correto
2. [ ] Produto principal está associado
3. [ ] Preço adicional está correto
4. [ ] Botões de editar/excluir funcionam

## 🍟 Teste 5: Combos

### Adicionar Combo
1. [ ] Clicar em "Combos" no menu
2. [ ] Clicar em "+ Adicionar Combo"
3. [ ] Preencher:
   - Nome: "Combo Teste"
   - Preço: 29.90
4. [ ] Selecionar produtos (marcar checkboxes)
5. [ ] Upload da imagem
6. [ ] Preview aparece
7. [ ] Salvar
8. [ ] Combo aparece na lista

### Verificar Combo
1. [ ] Nome está correto
2. [ ] Preço está correto
3. [ ] Produtos inclusos estão listados
4. [ ] Imagem aparece

### Editar Combo
1. [ ] Clicar em "Editar"
2. [ ] Produtos selecionados aparecem marcados
3. [ ] Marcar/desmarcar produtos
4. [ ] Salvar
5. [ ] Alterações foram aplicadas

## 🎠 Teste 6: Carrossel

### Adicionar Imagem
1. [ ] Clicar em "Carrossel" no menu
2. [ ] Clicar em "+ Adicionar Imagem"
3. [ ] Preencher texto alternativo
4. [ ] Upload da imagem
5. [ ] Preview aparece
6. [ ] Salvar
7. [ ] Imagem aparece na lista

### Verificar Lista
1. [ ] Miniatura da imagem está visível
2. [ ] Texto alternativo está correto
3. [ ] Botões funcionam

## 📦 Teste 7: Pedidos

### Verificar Lista de Pedidos
1. [ ] Clicar em "Pedidos" no menu
2. [ ] Lista carrega (pode estar vazia)
3. [ ] Se houver pedidos, todos os dados aparecem:
   - Número do pedido
   - Cliente
   - Total
   - Status com cores
   - Data

### Ver Detalhes (se houver pedidos)
1. [ ] Clicar em "Ver Detalhes"
2. [ ] Informações do cliente aparecem
3. [ ] Itens do pedido estão listados
4. [ ] Customizações são exibidas
5. [ ] Dropdown de status funciona
6. [ ] Alterar status e salvar
7. [ ] Mensagem de sucesso aparece

## 📱 Teste 8: Responsividade

### Desktop
1. [ ] Layout em tela cheia está correto
2. [ ] Menu não quebra
3. [ ] Tabelas são legíveis

### Tablet (redimensione o navegador)
1. [ ] Layout se adapta
2. [ ] Botões permanecem clicáveis
3. [ ] Texto permanece legível

### Mobile (redimensione para ~400px)
1. [ ] Menu pode virar vertical
2. [ ] Cards ficam empilhados
3. [ ] Tabelas são scrolláveis
4. [ ] Formulários permanecem usáveis

## 🎨 Teste 9: Design e UX

1. [ ] Cores são agradáveis e profissionais
2. [ ] Mensagens de sucesso aparecem em verde
3. [ ] Mensagens de erro aparecem em vermelho
4. [ ] Botões têm hover effects
5. [ ] Links mudam de cor ao passar o mouse
6. [ ] Preview de imagens funciona
7. [ ] Confirmações de exclusão aparecem

## 🔒 Teste 10: Segurança

### Logout
1. [ ] Clicar em "Sair" no canto superior direito
2. [ ] Redireciona para página de login
3. [ ] Não consegue acessar dashboard sem login

### Proteção de Rotas
1. [ ] Tentar acessar http://127.0.0.1:8000/myadmin/ sem login
2. [ ] Deve redirecionar para login

## ✅ RESULTADO FINAL

- [ ] Todos os testes passaram
- [ ] Nenhum erro no console
- [ ] Interface está funcionando perfeitamente
- [ ] Professora vai aprovar! 🎉

## 📝 Problemas Encontrados

_(Anote aqui qualquer problema)_

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

## 🎯 Próximos Passos

Se todos os testes passaram:
1. [ ] Criar produtos reais do seu negócio
2. [ ] Adicionar subprodutos reais
3. [ ] Criar combos atrativos
4. [ ] Adicionar imagens bonitas ao carrossel
5. [ ] Testar fluxo completo de pedido
6. [ ] Apresentar para a professora

---

**Boa sorte com os testes! 🍔**
