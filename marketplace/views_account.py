from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import OrderHistory, CartItem, SubProduct
from django.utils import timezone
from datetime import timedelta

@login_required
def edit_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            request.user.first_name = name
            request.user.save()
            messages.success(request, 'Nome atualizado com sucesso!')
            return redirect('edit_profile')
    return render(request, 'edit_profile.html')

@login_required
def edit_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
            messages.success(request, 'E-mail atualizado com sucesso!')
            return redirect('edit_email')
    return render(request, 'edit_email.html')

@login_required
def edit_phone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        profile = request.user.profile
        if phone:
            profile.phone = phone
            profile.save()
            messages.success(request, 'Telefone atualizado com sucesso!')
            return redirect('edit_phone')
    return render(request, 'edit_phone.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def order_history(request):
    """View para exibir o histórico de pedidos do usuário com filtros de data"""
    # Primeiro, limpa pedidos antigos
    OrderHistory.cleanup_old_orders()
    
    # Pega o filtro selecionado (padrão: 7 dias)
    filter_days = request.GET.get('filter', '7')
    
    try:
        days = int(filter_days)
    except ValueError:
        days = 7
    
    # Calcula a data de corte
    cutoff_date = timezone.now() - timedelta(days=days)
    
    # Busca os pedidos do usuário dentro do período
    orders = OrderHistory.objects.filter(
        user=request.user,
        order_date__gte=cutoff_date
    ).order_by('-order_date')
    
    # Processa os pedidos para exibição
    processed_orders = []
    for order in orders:
        processed_orders.append({
            'id': order.id,
            'date': order.order_date,
            'total': order.total,
            'summary': order.get_summary(),
            'items': order.order_data
        })
    
    context = {
        'orders': processed_orders,
        'current_filter': filter_days,
        'cart_items_count': sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    }
    
    return render(request, 'order_history.html', context)

@login_required
def order_history_detail(request, order_id):
    """View para exibir os detalhes completos de um pedido do histórico"""
    order = get_object_or_404(OrderHistory, id=order_id, user=request.user)
    
    # Processa os itens do pedido
    items_data = []
    for item in order.order_data or []:
        name = item.get('name', 'Item')
        qty = item.get('quantity', 1)
        unit_price = item.get('unit_price', 0)
        line_total = item.get('total_price', 0)
        customization = item.get('customization', {})
        
        ingredientes = []
        # Reconstrói a lista de ingredientes baseado na customização
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
                pass
        
        items_data.append({
            'name': name,
            'quantity': qty,
            'unit_price': unit_price,
            'line_total': line_total,
            'ingredientes': ingredientes,
        })
    
    context = {
        'order': order,
        'items_data': items_data,
        'cart_items_count': sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    }
    
    return render(request, 'order_history_detail.html', context)

@login_required
def account_settings(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        changed = False
        if name and name != user.first_name:
            user.first_name = name
            changed = True
        if email and email != user.email:
            user.email = email
            changed = True
        if profile and phone and phone != getattr(profile, 'phone', None):
            profile.phone = phone
            profile.save()
        if password:
            user.password = make_password(password)
            changed = True
        if changed:
            user.save()
        messages.success(request, 'Dados atualizados com sucesso!')
        return redirect('account_settings')
    return render(request, 'account_settings.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
