from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from .models import CartItem
import mercadopago
from django.contrib.auth.decorators import login_required

@login_required
def finalizar_pedido(request):
    try:
        user = request.user
        cart_items = CartItem.objects.filter(user=user, combo__isnull=False, product=None, subproduct=None)
        if not cart_items.exists():
            return HttpResponseBadRequest("Carrinho vazio.")

        sdk = mercadopago.SDK("APP_USR-4385987600520242-022520-8e219cf9b9dc2a14bb03389554231964-392012604")

        product_items = []
        total = 0
        for item in cart_items:
            product_items.append({
                "id": str(item.combo.id),
                "title": item.combo.name,
                "quantity": int(item.quantity),
                "currency_id": "BRL",
                "unit_price": float(item.combo.price),
                "description": f"Combo {item.combo.name}"
            })
            total += float(item.combo.price) * int(item.quantity)

        payment_data = {
            "items": product_items,
            "back_urls": {
                "success": "http://127.0.0.1:8000/",
                "failure": "http://127.0.0.1:8000/compraerrada",
                "pending": "http://127.0.0.1:8000/compraerrada",
            },
            "auto_return": "all",
            "payer_email": user.email or "cliente@example.com",
            "external_reference": f"Pedido de {user.username}",
            "description": f"Pedido de combos Joe's Burgers"
        }

        result = sdk.preference().create(payment_data)
        payment = result["response"]
        return redirect(payment['sandbox_init_point'])
    except Exception as e:
        return HttpResponseBadRequest(f"Erro ao gerar link de pagamento: {str(e)}")
