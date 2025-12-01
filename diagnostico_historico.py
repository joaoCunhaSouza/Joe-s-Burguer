import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodmarket.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import Order, OrderHistory
from django.utils import timezone

print("\n" + "="*60)
print("DIAGNÓSTICO DO HISTÓRICO DE PEDIDOS")
print("="*60 + "\n")

# 1. Verificar Orders existentes
print("1. Verificando Orders no sistema:")
orders = Order.objects.all()
print(f"   Total de pedidos: {orders.count()}")

for order in orders[:5]:
    print(f"   - Pedido #{order.id}: {order.customer_name} | Status: {order.status} | User: {order.user}")

# 2. Verificar OrderHistory existentes
print("\n2. Verificando OrderHistory no sistema:")
history = OrderHistory.objects.all()
print(f"   Total no histórico: {history.count()}")

for h in history[:5]:
    print(f"   - Histórico #{h.id}: {h.user.username} | Total: R$ {h.total} | Data: {h.order_date}")

# 3. Verificar se há pedidos DONE
print("\n3. Verificando pedidos com status DONE:")
done_orders = Order.objects.filter(status=Order.STATUS_DONE)
print(f"   Pedidos finalizados: {done_orders.count()}")

for order in done_orders[:5]:
    print(f"   - Pedido #{order.id}: {order.customer_name} | User: {order.user}")

# 4. Verificar usuários
print("\n4. Verificando usuários:")
users = User.objects.filter(is_staff=False)
print(f"   Total de usuários (não staff): {users.count()}")

for user in users[:3]:
    user_orders = Order.objects.filter(user=user)
    user_history = OrderHistory.objects.filter(user=user)
    print(f"   - {user.username}: {user_orders.count()} pedidos | {user_history.count()} no histórico")

print("\n" + "="*60)
print("DIAGNÓSTICO CONCLUÍDO")
print("="*60 + "\n")
