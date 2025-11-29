from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Order
from .models import SubProduct
from django.http import JsonResponse
from django.core import serializers
import os
import json
import logging
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

logger = logging.getLogger(__name__)


def _is_kitchen_staff(user):
    # Only allow users that are marked as staff. This prevents ordinary
    # registered users from accessing the kitchen even if they pick a
    # reserved username like 'cozinha'. The actual kitchen account should
    # be created by an administrator and have is_staff=True.
    return user.is_active and user.is_staff


@ensure_csrf_cookie
def kitchen_login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and _is_kitchen_staff(user):
            login(request, user)
            return redirect('kitchen_dashboard')
        else:
            error = 'Credenciais inválidas ou usuário sem permissão.'

    return render(request, 'kitchen_login.html', {'error': error})


@login_required
@user_passes_test(_is_kitchen_staff)
def kitchen_dashboard(request):
    # List only active orders (new or preparing), newest first
    orders = Order.objects.filter(status__in=[Order.STATUS_NEW, Order.STATUS_PREPARING]).order_by('-created_at')
    return render(request, 'kitchen_dashboard.html', {'orders': orders})


@login_required
@user_passes_test(_is_kitchen_staff)
def kitchen_orders_json(request):
    """Return active orders as JSON for polling by the kitchen UI.

    This endpoint uses GET only (no CSRF) so the kitchen can poll safely
    and avoid browser refresh / POST re-submission issues.
    """
    orders = Order.objects.filter(status__in=[Order.STATUS_NEW, Order.STATUS_PREPARING]).order_by('-created_at')
    data = []
    for o in orders:
        data.append({
            'id': o.id,
            'customer_name': o.customer_name,
            'total': str(o.total),
            'status': o.get_status_display(),
            'created_at': o.created_at.isoformat(),
        })
    return JsonResponse({'orders': data})


@login_required
@user_passes_test(_is_kitchen_staff)
def kitchen_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # order.items is stored as JSON snapshot: list of dicts with keys: name, quantity, customization, unit_price, total_price
    items_data = []
    raw_items = order.items or []
    for it in raw_items:
        name = it.get('name') or 'Item'
        qty = it.get('quantity', 1)
        unit_price = it.get('unit_price')
        line_total = it.get('total_price')
        customization = it.get('customization') or {}
        ingredientes = []
        for sub_id, sub_qty in customization.items():
            try:
                sp = SubProduct.objects.get(id=sub_id)
                removed = False
                try:
                    removed = int(sub_qty) <= 0
                except Exception:
                    removed = False
                ingredientes.append({'name': sp.name, 'removed': removed})
            except SubProduct.DoesNotExist:
                ingredientes.append({'name': str(sub_id), 'removed': False})
        items_data.append({
            'name': name,
            'quantity': qty,
            'unit_price': unit_price,
            'line_total': line_total,
            'ingredientes': ingredientes,
        })

    return render(request, 'kitchen_order_detail.html', {'order': order, 'items_data': items_data})


@login_required
@user_passes_test(_is_kitchen_staff)
def kitchen_confirm_action(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    action = request.GET.get('action')
    if request.method == 'POST':
        # perform action
        choice = request.POST.get('confirm')
        if choice == 'yes':
            if action == 'finish':
                order.status = Order.STATUS_DONE
            elif action == 'cancel':
                order.status = Order.STATUS_CANCELLED
            order.save()
        return redirect('kitchen_dashboard')

    return render(request, 'kitchen_confirm.html', {'order': order, 'action': action})


def kitchen_logout(request):
    logout(request)
    return redirect('kitchen_login')


def kitchen_debug_orders(request):
    """Protected debug endpoint to return the last N orders as JSON.

    Access control: provide the secret via ?secret=XYZ or via header X-Kitchen-Debug.
    The secret must match the env var KITCHEN_DEBUG_SECRET. If not set, endpoint is disabled.
    """
    secret_expected = os.environ.get('KITCHEN_DEBUG_SECRET')
    if not secret_expected:
        return JsonResponse({'error': 'disabled'}, status=404)

    provided = request.GET.get('secret') or request.headers.get('X-Kitchen-Debug')
    if not provided or provided != secret_expected:
        return JsonResponse({'error': 'unauthorized'}, status=401)

    try:
        limit = int(request.GET.get('n', 30))
    except Exception:
        limit = 30

    orders = Order.objects.all().order_by('-created_at')[:limit]
    data = []
    for o in orders:
        data.append({
            'id': o.id,
            'customer_name': o.customer_name,
            'total': float(o.total),
            'status': o.status,
            'created_at': o.created_at.isoformat(),
            'items': o.items,
        })
    return JsonResponse({'orders': data})


@csrf_exempt
def kitchen_webhook(request):
    """Receive kitchen webhook (POST) from Render app.

    Validates header X-Kitchen-Secret against env var KITCHEN_WEBHOOK_SECRET.
    Expected JSON payload example:
    {
      "customer_name": "João",
      "total": 45.0,
      "items": [ {"name":"Combo X","quantity":1,"unit_price":40.0,"customization":{}} ]
    }
    """
    secret_expected = os.environ.get('KITCHEN_WEBHOOK_SECRET')
    if not secret_expected:
        return JsonResponse({'error': 'webhook disabled'}, status=404)

    provided = request.headers.get('X-Kitchen-Secret') or request.POST.get('secret')
    if not provided or provided != secret_expected:
        return JsonResponse({'error': 'unauthorized'}, status=401)

    if request.method != 'POST':
        return JsonResponse({'error': 'method not allowed'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        return JsonResponse({'error': 'invalid json'}, status=400)

    customer_name = payload.get('customer_name') or 'Webhook'
    items = payload.get('items') or []
    try:
        total = float(payload.get('total') or sum((float(i.get('total_price') or 0) for i in items)))
    except Exception:
        total = 0.0

    try:
        # create Order in this local app DB so kitchen UI can show it
        o = Order.objects.create(
            user=None,
            customer_name=customer_name,
            items=items,
            total=total,
            status=Order.STATUS_NEW,
        )
        return JsonResponse({'ok': True, 'order_id': o.id}, status=201)
    except Exception:
        logger.exception('Failed creating order from webhook')
        return JsonResponse({'error': 'server error'}, status=500)
