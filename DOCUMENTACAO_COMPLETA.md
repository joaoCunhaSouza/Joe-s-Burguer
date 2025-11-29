# 🍔 PAINEL ADMIN PERSONALIZADO - DOCUMENTAÇÃO COMPLETA

## 📚 ÍNDICE
1. [Resumo do Projeto](#resumo)
2. [Como Iniciar](#como-iniciar)
3. [Estrutura Criada](#estrutura-criada)
4. [Funcionalidades](#funcionalidades)
5. [Acesso e Login](#acesso-e-login)
6. [Comparação com Django Admin](#comparação)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 RESUMO DO PROJETO {#resumo}

Foi criado um **painel administrativo completamente personalizado** para o Joe's Burguer que substitui o admin padrão do Django com:

✅ Interface moderna e profissional  
✅ Login usando EMAIL e SENHA do superusuário  
✅ Todas as funcionalidades do Django Admin mantidas  
✅ Design responsivo (funciona em mobile, tablet e desktop)  
✅ Gerenciamento completo de:
- Produtos
- Subprodutos
- Combos
- Carrossel de imagens
- Pedidos

---

## 🚀 COMO INICIAR {#como-iniciar}

### Opção 1: Usar o Script Automático (Windows)

```bash
# Clique duas vezes no arquivo:
foodmarket/iniciar_servidor.bat
```

### Opção 2: Manualmente

```bash
# 1. Navegar para a pasta do projeto
cd foodmarket

# 2. Aplicar migrações
python manage.py migrate

# 3. Criar superusuário (se ainda não tiver)
python manage.py createsuperuser

# 4. (Opcional) Criar dados de teste
python teste_admin.py

# 5. Iniciar servidor
python manage.py runserver
```

### Acesso

Após iniciar o servidor, acesse:
- **Painel Admin**: http://127.0.0.1:8000/myadmin/login/
- **Site Principal**: http://127.0.0.1:8000/

---

## 📁 ESTRUTURA CRIADA {#estrutura-criada}

```
foodmarket/
├── marketplace/
│   ├── views_admin.py              ← Todas as views do admin
│   ├── urls_admin.py               ← URLs do painel
│   ├── urls.py                     ← URLs atualizadas (+ /myadmin/)
│   └── templates/
│       └── admin_custom/
│           ├── base.html           ← Template base (navbar + CSS)
│           ├── admin_login.html    ← Página de login
│           ├── dashboard.html      ← Dashboard principal
│           ├── product_list.html   ← Lista produtos
│           ├── product_form.html   ← Form produtos
│           ├── subproduct_list.html
│           ├── subproduct_form.html
│           ├── combo_list.html
│           ├── combo_form.html
│           ├── carousel_list.html
│           ├── carousel_form.html
│           ├── order_list.html
│           └── order_detail.html
├── ADMIN_README.md                 ← Documentação completa
├── CHECKLIST_TESTES.md             ← Checklist de testes
├── teste_admin.py                  ← Script para criar dados
└── iniciar_servidor.bat            ← Script de inicialização
```

---

## ⚙️ FUNCIONALIDADES {#funcionalidades}

### 1. 📊 Dashboard
- **Estatísticas em tempo real**: Total de produtos, combos, pedidos
- **Pedidos recentes**: Últimos 5 pedidos com status
- **Acesso rápido**: Botões diretos para criar itens

### 2. 🍔 Gerenciamento de Produtos
| Ação | Descrição |
|------|-----------|
| Listar | Ver todos os produtos com imagem, nome, preço |
| Adicionar | Criar novo produto com upload de imagem |
| Editar | Modificar produto existente |
| Excluir | Remover produto (com confirmação) |

**Campos do Produto:**
- Nome (obrigatório)
- Preço (obrigatório)
- Descrição (obrigatório)
- Imagem (obrigatório)

### 3. 🥤 Gerenciamento de Subprodutos
| Ação | Descrição |
|------|-----------|
| Listar | Ver subprodutos com produto principal |
| Adicionar | Criar subproduto vinculado a produto |
| Editar | Modificar subproduto |
| Excluir | Remover subproduto |

**Campos do Subproduto:**
- Produto Principal (obrigatório)
- Nome (obrigatório)
- Preço Adicional (obrigatório, pode ser R$ 0,00)
- Descrição (opcional)
- Imagem (opcional)

**Exemplo de uso:**
- Produto: "Refrigerante"
  - Subproduto 1: "Coca-Cola" - R$ 0,00
  - Subproduto 2: "Guaraná" - R$ 0,00
- Produto: "Hambúrguer"
  - Subproduto 1: "Queijo Extra" - R$ 3,00
  - Subproduto 2: "Bacon" - R$ 4,00

### 4. 🍟 Gerenciamento de Combos
| Ação | Descrição |
|------|-----------|
| Listar | Ver combos com produtos inclusos |
| Adicionar | Criar combo selecionando produtos |
| Editar | Modificar combo e produtos |
| Excluir | Remover combo |

**Campos do Combo:**
- Nome (obrigatório)
- Preço (obrigatório)
- Produtos (seleção múltipla, obrigatório)
- Imagem (obrigatório)

### 5. 🎠 Gerenciamento de Carrossel
| Ação | Descrição |
|------|-----------|
| Listar | Ver imagens do carrossel |
| Adicionar | Upload de nova imagem |
| Editar | Alterar imagem ou texto |
| Excluir | Remover imagem |

**Campos:**
- Imagem (obrigatório)
- Texto Alternativo (opcional, para acessibilidade)

### 6. 📦 Gerenciamento de Pedidos
| Ação | Descrição |
|------|-----------|
| Listar | Ver todos os pedidos |
| Ver Detalhes | Informações completas do pedido |
| Alterar Status | Mudar status do pedido |

**Status disponíveis:**
- 🟡 Novo
- 🔵 Preparando
- 🟢 Finalizado
- 🔴 Cancelado

**Informações do pedido:**
- Número do pedido
- Cliente (nome e email)
- Itens com quantidades
- Customizações (ingredientes adicionados/removidos)
- Total do pedido
- Data e hora

---

## 🔐 ACESSO E LOGIN {#acesso-e-login}

### URL de Acesso
```
http://127.0.0.1:8000/myadmin/login/
```

### Credenciais
- **Email**: Email do superusuário
- **Senha**: Senha do superusuário

### Como Criar Superusuário

**Método 1: Manualmente**
```bash
python manage.py createsuperuser
```

Preencha:
- Username: `admin` (ou qualquer outro)
- Email: `seu@email.com` ← **ESTE será usado no login**
- Password: `senha123` (mínimo 8 caracteres)

**Método 2: Usando Script de Teste**
```bash
python teste_admin.py
```

Isso criará:
- Email: admin@joesburguer.com
- Senha: admin123

### ⚠️ IMPORTANTE
- O login usa **EMAIL**, não username
- Apenas **superusuários** têm acesso (is_superuser=True)
- Usuários comuns (staff) não conseguem acessar

---

## 🔄 COMPARAÇÃO COM DJANGO ADMIN {#comparação}

| Aspecto | Django Admin | Admin Personalizado |
|---------|--------------|---------------------|
| **URL** | /admin/ | /myadmin/login/ |
| **Login** | Username | Email |
| **Interface** | Genérica | Moderna e personalizada |
| **Design** | Básico | Profissional com cores |
| **Navegação** | Sidebar | Menu superior |
| **Responsivo** | Limitado | Totalmente responsivo |
| **Preview Imagens** | Não | Sim, ao fazer upload |
| **Mensagens** | Simples | Estilizadas e destacadas |
| **Confirmações** | Página separada | Modal inline |
| **Dashboard** | Lista de models | Estatísticas e gráficos |

### ✅ Funcionalidades Mantidas
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Upload de arquivos/imagens
- ✅ Relacionamentos (ManyToMany, ForeignKey)
- ✅ Validação de formulários
- ✅ Mensagens de feedback
- ✅ Proteção CSRF
- ✅ Autenticação e permissões

### 🎨 Melhorias Adicionadas
- ✨ Design moderno e profissional
- ✨ Interface intuitiva
- ✨ Preview de imagens antes de salvar
- ✨ Confirmações elegantes
- ✨ Cores semânticas (verde=sucesso, vermelho=erro)
- ✨ Dashboard com estatísticas
- ✨ Responsividade total
- ✨ Navegação simplificada

---

## 🔧 TROUBLESHOOTING {#troubleshooting}

### ❌ Problema: Não consigo fazer login

**Sintomas:**
- "Email ou senha inválidos"
- "Acesso negado"

**Soluções:**
1. Verifique se você está usando o **EMAIL**, não o username
2. Confirme que o usuário é superusuário:
   ```python
   from django.contrib.auth.models import User
   user = User.objects.get(email='seu@email.com')
   print(user.is_superuser)  # Deve ser True
   ```
3. Se necessário, torne o usuário superusuário:
   ```bash
   python manage.py shell
   >>> from django.contrib.auth.models import User
   >>> user = User.objects.get(email='seu@email.com')
   >>> user.is_superuser = True
   >>> user.is_staff = True
   >>> user.save()
   ```

### ❌ Problema: Erro 404 ao acessar /myadmin/

**Sintomas:**
- Página não encontrada
- URL não existe

**Soluções:**
1. Verifique se o servidor está rodando
2. Confirme a URL completa: `http://127.0.0.1:8000/myadmin/login/`
3. Verifique se adicionou as URLs corretamente:
   ```python
   # Em marketplace/urls.py deve ter:
   path('myadmin/', include('marketplace.urls_admin')),
   ```

### ❌ Problema: Imagens não aparecem

**Sintomas:**
- Ícone quebrado no lugar da imagem
- URL da imagem retorna 404

**Soluções:**
1. Verifique settings.py:
   ```python
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   ```

2. Em urls.py principal, adicione:
   ```python
   from django.conf import settings
   from django.conf.urls.static import static
   
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

3. Crie a pasta media se não existir

### ❌ Problema: CSS não carrega / página sem estilo

**Sintomas:**
- Página aparece sem formatação
- Apenas texto simples

**Soluções:**
1. Limpe o cache do navegador (Ctrl+Shift+Del)
2. Force refresh (Ctrl+F5)
3. Verifique se não há erros no console (F12)
4. Confirme que o template base.html está em `marketplace/templates/admin_custom/`

### ❌ Problema: Erro ao fazer upload de imagem

**Sintomas:**
- "PermissionError"
- "Unable to save file"

**Soluções:**
1. Verifique permissões da pasta media:
   ```bash
   # Linux/Mac
   chmod -R 755 media/
   
   # Windows: Propriedades > Segurança > Editar > Permitir todas
   ```

2. Confirme que a pasta existe:
   ```bash
   mkdir media
   mkdir media/products
   mkdir media/combos
   mkdir media/carousel
   mkdir media/subproducts
   ```

### ❌ Problema: Erro de CSRF

**Sintomas:**
- "CSRF verification failed"
- Formulário não envia

**Soluções:**
1. Verifique se tem `{% csrf_token %}` em todos os formulários
2. Confirme CSRF middleware em settings.py:
   ```python
   MIDDLEWARE = [
       ...
       'django.middleware.csrf.CsrfViewMiddleware',
       ...
   ]
   ```
3. Limpe cookies e tente novamente

### ❌ Problema: Migrations pendentes

**Sintomas:**
- Tabelas não existem
- "no such table"

**Solução:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📞 SUPORTE

### Documentação
- `ADMIN_README.md` - Guia completo
- `CHECKLIST_TESTES.md` - Lista de testes
- Django Docs: https://docs.djangoproject.com/

### Scripts Úteis
- `teste_admin.py` - Cria dados de teste
- `iniciar_servidor.bat` - Inicia servidor automaticamente

### Comandos Django
```bash
# Ver estrutura do banco
python manage.py dbshell

# Criar superusuário
python manage.py createsuperuser

# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos (produção)
python manage.py collectstatic
```

---

## 🎓 APRESENTAÇÃO PARA A PROFESSORA

### Pontos a Destacar

1. **Interface Moderna e Profissional**
   - Mostre o design limpo e cores agradáveis
   - Destaque a responsividade (teste em diferentes tamanhos)

2. **Funcionalidades Completas**
   - Demonstre CRUD completo
   - Mostre upload de imagens com preview
   - Exiba relacionamentos (combo com produtos)

3. **Melhorias sobre Django Admin**
   - Login simplificado com email
   - Dashboard com estatísticas
   - Design profissional vs genérico

4. **Facilidade de Uso**
   - Navegação intuitiva
   - Mensagens claras de sucesso/erro
   - Confirmações antes de excluir

5. **Código Organizado**
   - Views separadas (views_admin.py)
   - URLs organizadas (urls_admin.py)
   - Templates bem estruturados

### Roteiro Sugerido

1. **Login** (1 min)
   - Mostre a tela de login
   - Explique que usa email do superusuário

2. **Dashboard** (2 min)
   - Mostre estatísticas
   - Navegue pelo menu

3. **Criar Produto** (3 min)
   - Demonstre formulário
   - Faça upload de imagem
   - Mostre preview
   - Salve e mostre na lista

4. **Criar Combo** (2 min)
   - Selecione produtos
   - Mostre seleção múltipla funcionando

5. **Gerenciar Pedido** (2 min)
   - Mostre lista de pedidos
   - Entre em detalhes
   - Altere status

---

**🍔 Desenvolvido para Joe's Burguer**  
**Versão: 1.0.0**  
**Data: Novembro 2025**
