# Painel Admin Personalizado - Joe's Burguer

## 🎯 Visão Geral

Este é um painel administrativo customizado para o Joe's Burguer, desenvolvido para substituir o admin padrão do Django com uma interface mais moderna e amigável, mantendo todas as funcionalidades necessárias.

## 🔐 Acesso ao Painel

### URL de Acesso
```
http://127.0.0.1:8000/myadmin/login/
```

### Credenciais
- **Email**: Email do superusuário criado no Django
- **Senha**: Senha do superusuário

### Como Criar um Superusuário

Se você ainda não tem um superusuário, execute:

```bash
cd foodmarket
python manage.py createsuperuser
```

Siga as instruções e informe:
- Username (pode ser qualquer nome)
- Email (será usado para login)
- Password

## ✨ Funcionalidades

### 1. Dashboard
- Estatísticas gerais do sistema
- Total de produtos, combos e pedidos
- Pedidos recentes
- Acesso rápido para criar novos itens

### 2. Gerenciamento de Produtos
- **Listar**: Ver todos os produtos cadastrados
- **Adicionar**: Criar novos produtos com imagem, nome, preço e descrição
- **Editar**: Modificar produtos existentes
- **Excluir**: Remover produtos (com confirmação)

### 3. Gerenciamento de Subprodutos
- **Listar**: Ver todos os subprodutos (ingredientes, opções, etc)
- **Adicionar**: Criar subprodutos vinculados a produtos
- **Editar**: Modificar subprodutos
- **Excluir**: Remover subprodutos
- Permite definir preço adicional (0.00 para ingredientes padrão)

### 4. Gerenciamento de Combos
- **Listar**: Ver todos os combos
- **Adicionar**: Criar combos selecionando produtos
- **Editar**: Modificar combos e seus produtos
- **Excluir**: Remover combos

### 5. Gerenciamento do Carrossel
- **Listar**: Ver todas as imagens do carrossel da home
- **Adicionar**: Upload de novas imagens
- **Editar**: Alterar imagens e textos alternativos
- **Excluir**: Remover imagens

### 6. Gerenciamento de Pedidos
- **Listar**: Ver todos os pedidos do sistema
- **Detalhes**: Ver informações completas do pedido
- **Status**: Alterar status dos pedidos (Novo, Preparando, Finalizado, Cancelado)
- **Customizações**: Ver quais ingredientes foram adicionados/removidos

## 🎨 Características da Interface

- **Design Moderno**: Interface limpa e profissional
- **Responsiva**: Funciona bem em desktop, tablet e mobile
- **Cores Intuitivas**:
  - Azul: Ações principais
  - Verde: Sucesso e criação
  - Vermelho: Exclusão e erros
  - Amarelo: Avisos
- **Navegação Fácil**: Menu superior com todas as seções
- **Mensagens de Feedback**: Confirmações de sucesso e erros
- **Preview de Imagens**: Visualização antes de salvar

## 🔧 Estrutura de Arquivos Criados

```
foodmarket/
├── marketplace/
│   ├── views_admin.py              # Todas as views do admin
│   ├── urls_admin.py               # URLs do painel admin
│   ├── templates/
│   │   └── admin_custom/
│   │       ├── base.html           # Template base com navbar
│   │       ├── admin_login.html    # Página de login
│   │       ├── dashboard.html      # Dashboard principal
│   │       ├── product_list.html   # Lista de produtos
│   │       ├── product_form.html   # Form de produto
│   │       ├── subproduct_list.html # Lista de subprodutos
│   │       ├── subproduct_form.html # Form de subproduto
│   │       ├── combo_list.html     # Lista de combos
│   │       ├── combo_form.html     # Form de combo
│   │       ├── carousel_list.html  # Lista de imagens
│   │       ├── carousel_form.html  # Form de carrossel
│   │       ├── order_list.html     # Lista de pedidos
│   │       └── order_detail.html   # Detalhes do pedido
│   └── urls.py                     # URLs atualizadas
```

## 🚀 Como Usar

### 1. Primeiro Acesso

1. Acesse `http://127.0.0.1:8000/myadmin/login/`
2. Faça login com email e senha do superusuário
3. Você será redirecionado para o Dashboard

### 2. Adicionando Produtos

1. Clique em "Produtos" no menu
2. Clique em "+ Adicionar Produto"
3. Preencha: Nome, Preço, Descrição e faça upload da imagem
4. Clique em "Salvar"

### 3. Adicionando Subprodutos

1. Clique em "Subprodutos" no menu
2. Clique em "+ Adicionar Subproduto"
3. Selecione o produto principal
4. Preencha nome e preço adicional (0.00 se for ingrediente padrão)
5. Clique em "Salvar"

### 4. Criando Combos

1. Clique em "Combos" no menu
2. Clique em "+ Adicionar Combo"
3. Preencha nome e preço
4. Selecione os produtos que fazem parte do combo
5. Faça upload da imagem
6. Clique em "Salvar"

### 5. Gerenciando Pedidos

1. Clique em "Pedidos" no menu
2. Clique em "Ver Detalhes" no pedido desejado
3. Visualize itens e customizações
4. Altere o status conforme necessário

## 🔒 Segurança

- **Autenticação Obrigatória**: Apenas superusuários têm acesso
- **Proteção CSRF**: Todos os formulários protegidos
- **Validação de Permissões**: Verificação em cada view
- **Mensagens Seguras**: Feedback sem expor dados sensíveis

## 📝 Diferenças do Admin Padrão do Django

| Aspecto | Admin Padrão | Admin Personalizado |
|---------|--------------|---------------------|
| Interface | Simples e genérica | Moderna e personalizada |
| Login | Username | Email |
| Navegação | Sidebar | Menu superior |
| Design | Básico | Profissional com cores |
| Responsividade | Limitada | Totalmente responsivo |
| Preview de Imagens | Não | Sim, com preview ao upload |
| Mensagens | Simples | Estilizadas e destacadas |

## 🎯 Funcionalidades Mantidas do Django Admin

✅ Todas as operações CRUD (Create, Read, Update, Delete)
✅ Upload de imagens
✅ Relacionamentos (ManyToMany, ForeignKey)
✅ Validação de formulários
✅ Mensagens de sucesso/erro
✅ Proteção contra exclusão acidental
✅ Filtros e ordenação (em tabelas)

## 🐛 Solução de Problemas

### Não consigo fazer login
- Verifique se você criou um superusuário
- Certifique-se de usar o EMAIL, não o username
- Confirme que o usuário tem is_superuser=True

### Erro 404 ao acessar /myadmin/
- Verifique se o servidor está rodando
- Confirme que adicionou as URLs corretamente
- Teste com: `http://127.0.0.1:8000/myadmin/login/`

### Imagens não aparecem
- Verifique se MEDIA_URL e MEDIA_ROOT estão configurados
- Confirme que está servindo arquivos estáticos em desenvolvimento
- Veja se as pastas de upload têm permissão de escrita

## 🎨 Personalização

Para personalizar cores e estilos, edite o arquivo `templates/admin_custom/base.html` na seção `<style>`.

## 📧 Suporte

Para dúvidas ou problemas, consulte a documentação do Django ou entre em contato com o desenvolvedor.

---

**Desenvolvido para Joe's Burguer** 🍔
