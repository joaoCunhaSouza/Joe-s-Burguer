from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Order
from .models import SubProduct
from django.http import JsonResponse
from django.core import serializers


def _is_kitchen_staff(user):
    return user.is_active and (user.is_staff or user.username == 'cozinha')


def kitchen_login(request):
    # Ensure test user exists
    if not User.objects.filter(username='cozinha').exists():
        User.objects.create_user(username='cozinha', email='cozinha@example.com', password='cozinha', first_name='Cozinha', is_staff=True)

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
