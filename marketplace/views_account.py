from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import OrderHistory, CartItem, SubProduct
from django.utils import timezone
from datetime import timedelta
import re

def validate_password(password):
    """
    Valida se a senha atende aos requisitos de segurança:
    - Mínimo de 8 caracteres
    - Pelo menos 1 letra maiúscula
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 número
    - Pelo menos 1 caractere especial
    """
    if len(password) < 8:
        return False, "A senha deve ter no mínimo 8 caracteres."
    
    if not re.search(r'[A-Z]', password):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    
    if not re.search(r'[a-z]', password):
        return False, "A senha deve conter pelo menos uma letra minúscula."
    
    if not re.search(r'[0-9]', password):
        return False, "A senha deve conter pelo menos um número."
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]', password):
        return False, "A senha deve conter pelo menos um caractere especial (!@#$%^&* etc)."
    
    return True, ""

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
    
    # Data/hora atual
    now = timezone.now()
    
    # Busca TODOS os pedidos do usuário (até 90 dias)
    all_orders = OrderHistory.objects.filter(
        user=request.user,
        order_date__gte=now - timedelta(days=90)
    ).order_by('-order_date')
    
    # Filtra os pedidos baseado na diferença de tempo desde a criação
    filtered_orders = []
    for order in all_orders:
        # Calcula quantos dias se passaram desde que o pedido foi feito
        time_diff = now - order.order_date
        days_passed = time_diff.total_seconds() / 86400  # converte para dias (segundos / 86400)
        
        # Categoriza baseado no tempo decorrido
        if days == 7:
            # Mostra pedidos com MENOS de 7 dias completos
            if days_passed < 7:
                filtered_orders.append(order)
        elif days == 30:
            # Mostra pedidos entre 7 e 30 dias completos
            if 7 <= days_passed < 30:
                filtered_orders.append(order)
        elif days == 90:
            # Mostra pedidos entre 30 e 90 dias completos
            if 30 <= days_passed < 90:
                filtered_orders.append(order)
    
    # Processa os pedidos para exibição
    processed_orders = []
    for order in filtered_orders:
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
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('password')
        
        # Verifica a senha atual
        if not authenticate(username=user.username, password=current_password):
            messages.error(request, 'Senha atual incorreta.')
            return redirect('account_settings')
        
        changed = False
        
        # Atualiza nome
        if name and name != user.first_name:
            user.first_name = name
            changed = True
        
        # Atualiza email
        if email and email != user.email:
            # Verifica se o email já está em uso
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, 'Este e-mail já está em uso.')
                return redirect('account_settings')
            user.email = email
            changed = True
        
        # Atualiza telefone
        if profile and phone and phone != getattr(profile, 'phone', None):
            profile.phone = phone
            profile.save()
        
        # Atualiza senha se fornecida
        if new_password:
            is_valid, error_message = validate_password(new_password)
            if not is_valid:
                messages.error(request, error_message)
                return redirect('account_settings')
            
            user.set_password(new_password)
            changed = True
            
            # Atualiza a sessão para não deslogar o usuário
            update_session_auth_hash(request, user)
        
        if changed:
            user.save()
            messages.success(request, 'Dados atualizados com sucesso!')
        else:
            messages.info(request, 'Nenhuma alteração foi feita.')
        
        return redirect('account_settings')
    
    return render(request, 'account_settings.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
