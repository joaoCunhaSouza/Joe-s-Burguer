# Correção do Erro CSRF 403 Forbidden

## Problema Identificado

Quando você fazia login na cozinha e depois tentava acessar o admin (ou vice-versa), o sistema retornava erro **403 Forbidden** com a mensagem "CSRF verification failed. Request aborted."

## Causa Raiz

O problema ocorria porque:
1. O token CSRF não estava sendo renovado corretamente ao trocar entre diferentes áreas do sistema
2. Faltava o decorator `@ensure_csrf_cookie` nas views de login
3. O contexto CSRF não estava sendo incluído nos templates

## Soluções Implementadas

### 1. Configurações do Django (settings.py)

Adicionado configurações específicas de CSRF:

```python
# CSRF Configuration - Important for multiple login systems
CSRF_USE_SESSIONS = False  # Use cookies for CSRF token
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read CSRF cookie
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_NAME = 'csrftoken'

# Session Configuration
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
```

Adicionado o context processor do CSRF:

```python
'OPTIONS': {
    'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'django.template.context_processors.csrf',  # CSRF context processor
    ],
},
```

### 2. Views Atualizadas

Adicionado o decorator `@ensure_csrf_cookie` nas views de login:

**views_kitchen.py:**
```python
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def kitchen_login(request):
    # ... código do login
```

**views_admin.py:**
```python
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def admin_login(request):
    # ... código do login
```

### 3. Templates Atualizados

Adicionado script JavaScript para refresh automático do token CSRF em ambos os templates de login:

**kitchen_login.html e admin_custom/admin_login.html:**
```javascript
<script>
    async function refreshCsrfToken(){
        try{
            const resp = await fetch('/csrf/refresh/', {credentials: 'same-origin'});
            if(!resp.ok) return;
            const data = await resp.json();
            if(data && data.csrfToken){
                document.querySelectorAll('input[name="csrfmiddlewaretoken"]').forEach(i => i.value = data.csrfToken);
                document.cookie = 'csrftoken=' + data.csrfToken + '; path=/';
            }
        }catch(e){ console.warn('CSRF refresh failed', e); }
    }
    document.addEventListener('DOMContentLoaded', refreshCsrfToken);
</script>
```

### 4. Ordem do Middleware Corrigida

A ordem dos middlewares foi ajustada no settings.py para garantir o funcionamento correto:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

## Como Funciona Agora

1. **Login na Cozinha:**
   - Token CSRF é gerado e armazenado no cookie
   - JavaScript refresh o token automaticamente ao carregar a página

2. **Trocar para Admin:**
   - Ao acessar a página de login do admin, o JavaScript busca um novo token CSRF
   - O token é atualizado no formulário e no cookie
   - O login funciona sem erro 403

3. **Vice-versa:**
   - O mesmo processo funciona ao trocar do admin para a cozinha

## Arquivos Modificados

1. ✅ `foodmarket/foodmarket/settings.py` - Configurações CSRF e sessão
2. ✅ `foodmarket/marketplace/views_admin.py` - Decorator @ensure_csrf_cookie
3. ✅ `foodmarket/marketplace/views_kitchen.py` - Decorator @ensure_csrf_cookie
4. ✅ `foodmarket/marketplace/templates/kitchen_login.html` - Script refresh CSRF
5. ✅ `foodmarket/marketplace/templates/admin_custom/admin_login.html` - Script refresh CSRF

## Testando

Para testar se a correção funcionou:

1. Faça login na cozinha: `http://127.0.0.1:8000/kitchen/login/`
2. Sem fazer logout, acesse: `http://127.0.0.1:8000/myadmin/login/`
3. Tente fazer login no admin
4. ✅ Deve funcionar sem erro 403!

5. Faça logout do admin
6. Acesse a cozinha novamente
7. ✅ Deve funcionar sem erro 403!

## Solução Permanente

Esta solução resolve permanentemente o problema de CSRF entre diferentes áreas de autenticação no sistema, permitindo que você:

- Troque entre cozinha e admin sem problemas
- Use múltiplas abas do navegador
- Não precise limpar cookies ou cache
- Tenha uma experiência fluida de navegação

## Notas Técnicas

- O token CSRF é renovado automaticamente via JavaScript
- O cookie CSRF é compartilhado entre todas as páginas do domínio
- O decorator `@ensure_csrf_cookie` garante que sempre há um token disponível
- A configuração `CSRF_COOKIE_HTTPONLY = False` permite o JavaScript acessar o cookie
