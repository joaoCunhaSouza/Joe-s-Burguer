from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from .models import CartItem, Order
import mercadopago
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def finalizar_pedido(request):
    try:
        user = request.user
        cart_items = CartItem.objects.filter(user=user, combo__isnull=False, product=None, subproduct=None)
        if not cart_items.exists():
            return redirect(f"{reverse('cart')}?erro=Carrinho vazio.")

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

        # E-mails de teste do Mercado Pago
        vendedor_email = "TESTUSER566695291@testuser.com"  # e-mail do vendedor de teste
        comprador_teste_email = "TESTUSER1230067445@testuser.com"  # e-mail do comprador de teste
        payer_email = user.email
        # Se o usuário tentar pagar com o mesmo e-mail do vendedor, força o e-mail de comprador de teste
        if payer_email.lower() == vendedor_email.lower():
            payer_email = comprador_teste_email

        payment_data = {
            "items": product_items,
            "back_urls": {
                "success": "https://joe-s-burguer.onrender.com/compra-sucesso",
                "failure": "https://joe-s-burguer.onrender.com/compraerrada",
                "pending": "https://joe-s-burguer.onrender.com/compra-pendente",
            },
            "auto_return": "all",
            "binary_mode": True,
            "operation_type": "regular_payment",
            "marketplace_fee": 0,
            "statement_descriptor": "Joe's Burgers",
            "payer": {
                "email": payer_email,
                "name": user.first_name or "Test",
                "surname": user.last_name or "User",
                "phone": {"area_code": "11", "number": "4444-4444"},
                "identification": {"type": "CPF", "number": "19119119100"},
                "address": {
                    "zip_code": "06233200",
                    "street_name": "Rua Teste",
                    "street_number": 123
                }
            },
            "external_reference": f"Pedido de {user.username}",
            "description": f"Pedido de combos Joe's Burgers"
        }

        # Antes de criar a preferência de pagamento, criamos um pedido na fila da cozinha
        try:
            # snapshot dos itens do carrinho
            order_items = []
            for item in cart_items:
                order_items.append({
                    'combo_id': item.combo.id if item.combo else None,
                    'name': item.combo.name if item.combo else (item.product.name if item.product else ''),
                    'quantity': int(item.quantity),
                    'customization': item.customization or {},
                    'unit_price': float(item.combo.price) if item.combo else (float(item.product.price) if item.product else 0),
                    'total_price': float(item.get_total_price),
                })
            order_total = sum(i['total_price'] for i in order_items)
            order = Order.objects.create(
                user=user,
                customer_name=user.first_name or user.username,
                items=order_items,
                total=order_total,
                status=Order.STATUS_NEW,
            )
        except Exception:
            # não queremos bloquear o pagamento se por alguma razão o pedido não puder ser salvo
            order = None

        result = sdk.preference().create(payment_data)
        payment = result["response"]
        if 'sandbox_init_point' in payment:
            return redirect(payment['sandbox_init_point'])
        else:
            erro_api = payment.get('message', 'Erro desconhecido Mercado Pago')
            return redirect(f"{reverse('cart')}?erro=Erro Mercado Pago: {erro_api}")
    except Exception as e:
        return redirect(f"{reverse('cart')}?erro=Erro ao gerar link de pagamento: {str(e)}")

def compra_sucesso(request):
    return HttpResponse("""
    <div style='max-width:420px;margin:40px auto;padding:32px 24px;background:#fff;border-radius:12px;box-shadow:0 4px 24px #0001;text-align:center;'>
      <h2 style='color:#27ae60;'>Pagamento aprovado!</h2>
      <p style='color:#333;font-size:1.1em;'>Seu pedido foi realizado com sucesso.<br>Você receberá atualizações por e-mail.<br><br>Obrigado por comprar na Joe's Burgers! 🍔</p>
      <a href='/' style='display:inline-block;margin-top:18px;color:#27ae60;'>Voltar para a Home</a>
    </div>
    """)

def compra_errada(request):
    return HttpResponse("""
    <div style='max-width:420px;margin:40px auto;padding:32px 24px;background:#fff;border-radius:12px;box-shadow:0 4px 24px #0001;text-align:center;'>
      <h2 style='color:#ff4d4d;'>Pagamento não aprovado</h2>
      <p style='color:#333;font-size:1.1em;'>Ocorreu um erro ao processar seu pagamento.<br>Tente novamente ou utilize outro método.<br><br>Se o problema persistir, entre em contato conosco.</p>
      <a href='/cart/' style='display:inline-block;margin-top:18px;color:#ff4d4d;'>Voltar ao carrinho</a>
    </div>
    """)

def compra_pendente(request):
    return HttpResponse("""
    <div style='max-width:420px;margin:40px auto;padding:32px 24px;background:#fff;border-radius:12px;box-shadow:0 4px 24px #0001;text-align:center;'>
      <h2 style='color:#f1c40f;'>Pagamento pendente</h2>
      <p style='color:#333;font-size:1.1em;'>Seu pagamento está em análise ou aguardando confirmação.<br>Assim que for aprovado, você receberá um e-mail de confirmação.<br><br>Obrigado por comprar na Joe's Burgers!</p>
      <a href='/' style='display:inline-block;margin-top:18px;color:#f1c40f;'>Voltar para a Home</a>
    </div>
    """)
