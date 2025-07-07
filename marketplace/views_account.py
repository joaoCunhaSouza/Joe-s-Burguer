from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

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
    # Exemplo: pedidos = Order.objects.filter(user=request.user)
    pedidos = []
    return render(request, 'order_history.html', {'pedidos': pedidos})

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
