import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodmarket.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import OrderHistory
from django.utils import timezone
from datetime import timedelta

print("\n" + "="*60)
print("TESTE DE FILTROS DE HISTORICO")
print("="*60 + "\n")

# Pegar um usuário
user = User.objects.filter(is_staff=False, order_history__isnull=False).first()

if not user:
    print("Nenhum usuario com historico encontrado!")
else:
    print(f"Usuario: {user.username}")
    print(f"Data atual: {timezone.now()}\n")
    
    # Todos os pedidos
    all_orders = OrderHistory.objects.filter(user=user)
    print(f"Total de pedidos no historico: {all_orders.count()}")
    
    for order in all_orders:
        days_ago = (timezone.now() - order.order_date).days
        print(f"  - Pedido #{order.id}: {order.order_date} ({days_ago} dias atras)")
    
    # Teste dos filtros
    print("\nTestando filtros:")
    
    cutoff_7 = timezone.now() - timedelta(days=7)
    count_7 = OrderHistory.objects.filter(user=user, order_date__gte=cutoff_7).count()
    print(f"  Ultimos 7 dias (>= {cutoff_7}): {count_7} pedidos")
    
    cutoff_30 = timezone.now() - timedelta(days=30)
    count_30 = OrderHistory.objects.filter(user=user, order_date__gte=cutoff_30).count()
    print(f"  Ultimos 30 dias (>= {cutoff_30}): {count_30} pedidos")
    
    cutoff_90 = timezone.now() - timedelta(days=90)
    count_90 = OrderHistory.objects.filter(user=user, order_date__gte=cutoff_90).count()
    print(f"  Ultimos 90 dias (>= {cutoff_90}): {count_90} pedidos")

print("\n" + "="*60)
print("TESTE CONCLUIDO")
print("="*60 + "\n")
