import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodmarket.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import Order, OrderHistory
from django.utils import timezone

print("\n" + "="*60)
print("MIGRACAO DE PEDIDOS ANTIGOS PARA O HISTORICO")
print("="*60 + "\n")

# Buscar pedidos DONE que têm usuário mas não estão no histórico
done_orders = Order.objects.filter(status=Order.STATUS_DONE, user__isnull=False)

migrated_count = 0

for order in done_orders:
    # Verificar se já existe no histórico (evitar duplicatas)
    existing = OrderHistory.objects.filter(
        user=order.user,
        order_date=order.created_at,
        total=order.total
    ).exists()
    
    if not existing:
        OrderHistory.objects.create(
            user=order.user,
            order_data=order.items,
            total=order.total,
            order_date=order.created_at
        )
        migrated_count += 1
        print(f"OK Pedido #{order.id} ({order.customer_name}) migrado para o historico de {order.user.username}")

print(f"\n{migrated_count} pedido(s) migrado(s) com sucesso!")

# Mostrar resumo
print("\nResumo por usuario:")
for user in User.objects.filter(is_staff=False):
    history_count = OrderHistory.objects.filter(user=user).count()
    if history_count > 0:
        print(f"   {user.username}: {history_count} pedido(s) no historico")

print("\n" + "="*60)
print("MIGRACAO CONCLUIDA")
print("="*60 + "\n")
