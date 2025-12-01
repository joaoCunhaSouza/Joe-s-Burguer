"""
Script para testar o sistema de histórico de pedidos.
Execute com: python manage.py shell < test_order_history.py
"""

from django.contrib.auth.models import User
from marketplace.models import Order, OrderHistory, Combo
from django.utils import timezone
from datetime import timedelta
import json

print("\n" + "="*60)
print("TESTE DO SISTEMA DE HISTÓRICO DE PEDIDOS")
print("="*60 + "\n")

# 1. Verificar se existe um usuário de teste
print("1. Verificando usuário de teste...")
try:
    user = User.objects.filter(is_staff=False).first()
    if not user:
        print("   ⚠️  Nenhum usuário encontrado. Crie um usuário primeiro.")
        exit()
    print(f"   ✓ Usuário encontrado: {user.username} ({user.email})")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    exit()

# 2. Criar um pedido de teste
print("\n2. Criando pedido de teste...")
try:
    combo = Combo.objects.first()
    if not combo:
        print("   ⚠️  Nenhum combo encontrado. Adicione combos primeiro.")
        exit()
    
    order = Order.objects.create(
        user=user,
        customer_name=user.first_name or user.username,
        items=[
            {
                "name": combo.name,
                "quantity": 2,
                "unit_price": float(combo.price),
                "total_price": float(combo.price) * 2,
                "customization": {}
            }
        ],
        total=float(combo.price) * 2,
        status=Order.STATUS_NEW
    )
    print(f"   ✓ Pedido #{order.id} criado com status '{order.status}'")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    exit()

# 3. Simular finalização do pedido
print("\n3. Finalizando pedido (mudando status para DONE)...")
try:
    order.status = Order.STATUS_DONE
    order.save()
    print(f"   ✓ Status alterado para '{order.status}'")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    exit()

# 4. Verificar se foi adicionado ao histórico
print("\n4. Verificando histórico...")
try:
    history = OrderHistory.objects.filter(user=user).order_by('-created_at').first()
    if history:
        print(f"   ✓ Pedido adicionado ao histórico!")
        print(f"   - ID do histórico: {history.id}")
        print(f"   - Total: R$ {history.total}")
        print(f"   - Data do pedido: {history.order_date.strftime('%d/%m/%Y %H:%M')}")
        print(f"   - Resumo: {history.get_summary()}")
    else:
        print(f"   ✗ Pedido NÃO foi adicionado ao histórico")
except Exception as e:
    print(f"   ✗ Erro: {e}")

# 5. Testar filtros de período
print("\n5. Testando filtros de período...")
try:
    cutoff_7 = timezone.now() - timedelta(days=7)
    cutoff_30 = timezone.now() - timedelta(days=30)
    cutoff_90 = timezone.now() - timedelta(days=90)
    
    count_7 = OrderHistory.objects.filter(user=user, order_date__gte=cutoff_7).count()
    count_30 = OrderHistory.objects.filter(user=user, order_date__gte=cutoff_30).count()
    count_90 = OrderHistory.objects.filter(user=user, order_date__gte=cutoff_90).count()
    
    print(f"   - Últimos 7 dias: {count_7} pedido(s)")
    print(f"   - Últimos 30 dias: {count_30} pedido(s)")
    print(f"   - Últimos 90 dias: {count_90} pedido(s)")
except Exception as e:
    print(f"   ✗ Erro: {e}")

# 6. Testar limpeza de pedidos antigos
print("\n6. Testando limpeza de pedidos antigos...")
try:
    # Criar um pedido antigo (95 dias atrás)
    old_date = timezone.now() - timedelta(days=95)
    old_order = Order.objects.create(
        user=user,
        customer_name=user.first_name or user.username,
        items=[{"name": "Teste Antigo", "quantity": 1, "unit_price": 10.0, "total_price": 10.0}],
        total=10.0,
        status=Order.STATUS_NEW,
        created_at=old_date
    )
    old_order.status = Order.STATUS_DONE
    old_order.save()
    
    # Forçar a data do histórico para ser antiga
    old_history = OrderHistory.objects.filter(user=user).order_by('-created_at').first()
    old_history.order_date = old_date
    old_history.save()
    
    print(f"   ✓ Pedido antigo criado ({old_date.strftime('%d/%m/%Y')})")
    
    # Executar limpeza
    deleted_count = OrderHistory.cleanup_old_orders()
    print(f"   ✓ Limpeza executada: {deleted_count} pedido(s) removido(s)")
    
except Exception as e:
    print(f"   ✗ Erro: {e}")

print("\n" + "="*60)
print("TESTE CONCLUÍDO!")
print("="*60 + "\n")

print("Próximos passos:")
print("1. Acesse http://127.0.0.1:8000/historico/ para ver o histórico")
print("2. Teste os filtros de período (7, 30, 90 dias)")
print("3. Clique em um pedido para ver os detalhes")
print("\n")
