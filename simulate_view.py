import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodmarket.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import OrderHistory
from django.utils import timezone
from datetime import timedelta

print("\n" + "="*60)
print("SIMULACAO DE ACESSO AO HISTORICO")
print("="*60 + "\n")

# Pegar o usuário mj
user = User.objects.get(username='mj@gmail.com')

print(f"Usuario: {user.username}")
print(f"Data/hora atual: {timezone.now()}\n")

# Simular o que a view faz
for filter_days in ['7', '30', '90']:
    days = int(filter_days)
    cutoff_date = timezone.now() - timedelta(days=days)
    
    orders = OrderHistory.objects.filter(
        user=user,
        order_date__gte=cutoff_date
    ).order_by('-order_date')
    
    print(f"\nFiltro: Ultimos {days} dias")
    print(f"Data de corte: {cutoff_date}")
    print(f"Pedidos encontrados: {orders.count()}")
    
    for order in orders:
        print(f"  - Pedido #{order.id}: {order.order_date} | Total: R$ {order.total}")
        print(f"    Resumo: {order.get_summary()}")

print("\n" + "="*60)
print("SIMULACAO CONCLUIDA")
print("="*60 + "\n")
