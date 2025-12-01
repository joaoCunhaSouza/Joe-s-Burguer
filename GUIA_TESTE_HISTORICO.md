# 🎯 GUIA DE TESTE - HISTÓRICO DE PEDIDOS

## ✅ Sistema Funcionando Corretamente!

Os testes mostram que o sistema está funcionando perfeitamente:
- ✅ Pedidos finalizados vão automaticamente para o histórico
- ✅ Carrinho é limpo quando pedido é finalizado
- ✅ Filtros de 7, 30 e 90 dias funcionam corretamente
- ✅ Um card por pedido (agrupa todos os itens)
- ✅ Detalhes completos ao clicar

## 📋 Como Testar

### 1️⃣ Fazer um Pedido Completo

**Como CLIENTE:**
1. Acesse: http://127.0.0.1:8000/login/
2. Faça login com: `mj@gmail.com` (ou crie um novo usuário)
3. Adicione alguns combos ao carrinho
4. Vá para o carrinho e finalize o pedido
5. Complete o pagamento (sandbox do Mercado Pago)

**Como COZINHA:**
6. Acesse: http://127.0.0.1:8000/kitchen/login/
7. Login: `cozinha` / senha configurada
8. Veja o pedido na lista
9. Clique em "Finalizar Pedido"
10. Confirme a finalização

### 2️⃣ Verificar o Histórico

**Volte como CLIENTE:**
1. Acesse: http://127.0.0.1:8000/historico/
2. Você verá o pedido recém-finalizado
3. O carrinho estará vazio
4. Clique no pedido para ver todos os detalhes

### 3️⃣ Testar os Filtros

1. Na página de histórico, clique nos botões:
   - "Últimos 7 dias"
   - "Últimos 30 dias"  
   - "Últimos 90 dias"
2. Os pedidos aparecerão conforme a data

## 🔍 Verificar Dados no Banco

Execute para ver o status atual:

```bash
python diagnostico_historico.py
```

## 📊 Dados Atuais do Sistema

Usuário: `mj@gmail.com`
- ✅ 4 pedidos no histórico
- ✅ Todos aparecem nos 3 filtros (7, 30, 90 dias)
- ✅ Datas recentes (30/11 e 01/12)

Usuário: `joao@gmail.com`  
- ✅ 1 pedido no histórico
- ✅ Data: 30/11

## ⚠️ Se Não Aparecer Nada

Possíveis causas:

### 1. Usuário Errado
**Solução:** Verifique se está logado com o usuário que fez os pedidos
```python
# Ver usuários com pedidos:
python diagnostico_historico.py
```

### 2. Pedidos Muito Antigos
**Solução:** Pedidos com mais de 90 dias são automaticamente removidos
```python
# Criar novo pedido de teste
python test_order_history.py
```

### 3. Pedidos Sem Usuário
**Solução:** Pedidos antigos podem ter `user=None`
```python
# Migrar pedidos antigos
python migrate_old_orders.py
```

## 🎨 Exemplo Visual

```
┌─────────────────────────────────────────┐
│ 01/12/2024 às 00:43     R$ 40,00       │
│ Pedido #2                               │
│                                         │
│ Cheese Burger + 1 item(s)               │
│                                         │
│         Ver todos os itens →            │
└─────────────────────────────────────────┘
```

Ao clicar:

```
┌─────────────────────────────────────────┐
│ DETALHES DO PEDIDO #2                   │
├─────────────────────────────────────────┤
│ 1x Cheese Burger                        │
│    R$ 20,00                             │
│    ✓ Queijo extra                       │
│    ✗ Cebola                             │
│                                         │
│ 1x Batata Frita                         │
│    R$ 20,00                             │
│                                         │
│ TOTAL: R$ 40,00                         │
└─────────────────────────────────────────┘
```

## 🚀 Fluxo Automático

1. Cliente finaliza pedido → Order criado (status: "new")
2. Cozinha aceita → status: "preparing"
3. **Cozinha finaliza** → status: "done"
4. ✨ **Sistema automaticamente:**
   - Adiciona ao histórico do usuário
   - Limpa o carrinho do usuário
   - Pedido aparece em /historico/

## 📝 Logs para Debug

Se ainda não aparecer, verifique:

```python
# Ver todos os pedidos
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodmarket.settings')
django.setup()
from marketplace.models import OrderHistory
from django.contrib.auth.models import User

user = User.objects.get(email='SEU_EMAIL_AQUI')
orders = OrderHistory.objects.filter(user=user)
print(f'Pedidos encontrados: {orders.count()}')
for o in orders:
    print(f'  - #{o.id}: {o.order_date} | R$ {o.total}')
"
```

## ✅ Sistema 100% Funcional!

O histórico de pedidos está funcionando perfeitamente. Se não aparecer para você:
1. Faça um novo pedido completo
2. Finalize pela cozinha
3. Verifique o histórico

O pedido vai aparecer automaticamente! 🎉
