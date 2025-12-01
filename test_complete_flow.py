import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodmarket.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import Order, OrderHistory, CartItem
from django.utils import timezone

print("\n" + "="*60)
print("TESTE COMPLETO - FINALIZAR PEDIDO E VER NO HISTORICO")
print("="*60 + "\n")

# 1. Pegar um usuário
user = User.objects.filter(is_staff=False).first()
if not user:
    print("ERRO: Nenhum usuario encontrado!")
    exit()

print(f"Usuario: {user.username} ({user.email})")

# 2. Ver o carrinho atual
cart_items = CartItem.objects.filter(user=user)
print(f"\nItens no carrinho ANTES: {cart_items.count()}")

# 3. Ver pedidos do usuário
orders = Order.objects.filter(user=user)
print(f"Pedidos totais do usuario: {orders.count()}")

done_orders = Order.objects.filter(user=user, status=Order.STATUS_DONE)
print(f"Pedidos finalizados: {done_orders.count()}")

# 4. Ver histórico atual
history = OrderHistory.objects.filter(user=user)
print(f"Pedidos no historico ANTES: {history.count()}")

# 5. Pegar um pedido que NÃO está finalizado
pending_order = Order.objects.filter(
    user=user,
    status__in=[Order.STATUS_NEW, Order.STATUS_PREPARING]
).first()

if pending_order:
    print(f"\nEncontrado pedido pendente: #{pending_order.id}")
    print(f"Status atual: {pending_order.status}")
    
    # Finalizar o pedido
    print("\nFinalizando pedido...")
    pending_order.status = Order.STATUS_DONE
    pending_order.save()
    
    print("Pedido finalizado!")
    
    # Verificar novamente
    cart_items_after = CartItem.objects.filter(user=user)
    history_after = OrderHistory.objects.filter(user=user)
    
    print(f"\nItens no carrinho DEPOIS: {cart_items_after.count()}")
    print(f"Pedidos no historico DEPOIS: {history_after.count()}")
    
    if cart_items_after.count() == 0:
        print("OK - Carrinho foi limpo!")
    else:
        print("ERRO - Carrinho NAO foi limpo!")
    
    if history_after.count() > history.count():
        print("OK - Pedido foi para o historico!")
    else:
        print("ERRO - Pedido NAO foi para o historico!")
        
else:
    print("\nNenhum pedido pendente encontrado.")
    print("Crie um pedido primeiro antes de testar!")

print("\n" + "="*60)
print("TESTE CONCLUIDO")
print("="*60 + "\n")
