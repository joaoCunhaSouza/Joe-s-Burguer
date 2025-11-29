from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Product, SubProduct, Combo, CarouselImage, Order
import json


def _is_superuser(user):
    """Check if user is superuser (admin)"""
    return user.is_active and user.is_superuser


@ensure_csrf_cookie
def admin_login(request):
    """Admin login page - accepts email and password"""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('custom_admin_dashboard')
    
    error = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to find user by email
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('custom_admin_dashboard')
            else:
                error = 'Acesso negado. Apenas superusuários podem acessar o painel admin.'
        except User.DoesNotExist:
            error = 'Email ou senha inválidos.'
    
    return render(request, 'admin_custom/admin_login.html', {'error': error})


@login_required
@user_passes_test(_is_superuser)
def admin_dashboard(request):
    """Main admin dashboard with statistics"""
    total_products = Product.objects.count()
    total_combos = Combo.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status=Order.STATUS_NEW).count()
    kitchen_users = User.objects.filter(is_staff=True, is_superuser=False).count()
    
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'total_combos': total_combos,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'kitchen_users': kitchen_users,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'admin_custom/dashboard.html', context)


@login_required
@user_passes_test(_is_superuser)
def admin_logout(request):
    """Admin logout"""
    logout(request)
    return redirect('admin_login')


# ============= KITCHEN USER VIEWS =============

@login_required
@user_passes_test(_is_superuser)
def kitchen_user_list(request):
    """List all kitchen staff users"""
    kitchen_users = User.objects.filter(is_staff=True, is_superuser=False).order_by('username')
    return render(request, 'admin_custom/kitchen_user_list.html', {'kitchen_users': kitchen_users})


@login_required
@user_passes_test(_is_superuser)
def kitchen_user_add(request):
    """Add new kitchen staff user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        
        try:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Usuário "{username}" já existe!')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    is_staff=True,
                    is_superuser=False
                )
                messages.success(request, f'Usuário da cozinha "{user.username}" criado com sucesso!')
                return redirect('admin_kitchen_user_list')
        except Exception as e:
            messages.error(request, f'Erro ao criar usuário: {str(e)}')
    
    return render(request, 'admin_custom/kitchen_user_form.html', {'action': 'Adicionar'})


@login_required
@user_passes_test(_is_superuser)
def kitchen_user_edit(request, user_id):
    """Edit existing kitchen staff user"""
    kitchen_user = get_object_or_404(User, id=user_id, is_staff=True, is_superuser=False)
    
    if request.method == 'POST':
        kitchen_user.username = request.POST.get('username')
        kitchen_user.email = request.POST.get('email', '')
        kitchen_user.first_name = request.POST.get('first_name', '')
        
        # Only update password if provided
        new_password = request.POST.get('password')
        if new_password:
            kitchen_user.set_password(new_password)
        
        try:
            kitchen_user.save()
            messages.success(request, f'Usuário "{kitchen_user.username}" atualizado com sucesso!')
            return redirect('admin_kitchen_user_list')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar usuário: {str(e)}')
    
    return render(request, 'admin_custom/kitchen_user_form.html', {
        'action': 'Editar',
        'kitchen_user': kitchen_user
    })


@login_required
@user_passes_test(_is_superuser)
@require_POST
def kitchen_user_delete(request, user_id):
    """Delete kitchen staff user"""
    kitchen_user = get_object_or_404(User, id=user_id, is_staff=True, is_superuser=False)
    username = kitchen_user.username
    
    try:
        kitchen_user.delete()
        messages.success(request, f'Usuário "{username}" excluído com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir usuário: {str(e)}')
    
    return redirect('admin_kitchen_user_list')


# ============= PRODUCT VIEWS =============

@login_required
@user_passes_test(_is_superuser)
def product_list(request):
    """List all products"""
    products = Product.objects.all().order_by('name')
    return render(request, 'admin_custom/product_list.html', {'products': products})


@login_required
@user_passes_test(_is_superuser)
def product_add(request):
    """Add new product"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        
        try:
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                image=image
            )
            messages.success(request, f'Produto "{product.name}" criado com sucesso!')
            return redirect('admin_product_list')
        except Exception as e:
            messages.error(request, f'Erro ao criar produto: {str(e)}')
    
    return render(request, 'admin_custom/product_form.html', {'action': 'Adicionar'})


@login_required
@user_passes_test(_is_superuser)
def product_edit(request, product_id):
    """Edit existing product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        try:
            product.save()
            messages.success(request, f'Produto "{product.name}" atualizado com sucesso!')
            return redirect('admin_product_list')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar produto: {str(e)}')
    
    return render(request, 'admin_custom/product_form.html', {
        'action': 'Editar',
        'product': product
    })


@login_required
@user_passes_test(_is_superuser)
@require_POST
def product_delete(request, product_id):
    """Delete product"""
    product = get_object_or_404(Product, id=product_id)
    name = product.name
    
    try:
        product.delete()
        messages.success(request, f'Produto "{name}" excluído com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir produto: {str(e)}')
    
    return redirect('admin_product_list')


# ============= SUBPRODUCT VIEWS =============

@login_required
@user_passes_test(_is_superuser)
def subproduct_list(request):
    """List all subproducts"""
    subproducts = SubProduct.objects.select_related('product').order_by('product__name', 'name')
    return render(request, 'admin_custom/subproduct_list.html', {'subproducts': subproducts})


@login_required
@user_passes_test(_is_superuser)
def subproduct_add(request):
    """Add new subproduct"""
    products = Product.objects.all().order_by('name')
    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        
        try:
            product = Product.objects.get(id=product_id)
            subproduct = SubProduct.objects.create(
                product=product,
                name=name,
                description=description,
                price=price,
                image=image if image else None
            )
            messages.success(request, f'Subproduto "{subproduct.name}" criado com sucesso!')
            return redirect('admin_subproduct_list')
        except Exception as e:
            messages.error(request, f'Erro ao criar subproduto: {str(e)}')
    
    return render(request, 'admin_custom/subproduct_form.html', {
        'action': 'Adicionar',
        'products': products
    })


@login_required
@user_passes_test(_is_superuser)
def subproduct_edit(request, subproduct_id):
    """Edit existing subproduct"""
    subproduct = get_object_or_404(SubProduct, id=subproduct_id)
    products = Product.objects.all().order_by('name')
    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        subproduct.product = Product.objects.get(id=product_id)
        subproduct.name = request.POST.get('name')
        subproduct.description = request.POST.get('description', '')
        subproduct.price = request.POST.get('price')
        
        if 'image' in request.FILES:
            subproduct.image = request.FILES['image']
        
        try:
            subproduct.save()
            messages.success(request, f'Subproduto "{subproduct.name}" atualizado com sucesso!')
            return redirect('admin_subproduct_list')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar subproduto: {str(e)}')
    
    return render(request, 'admin_custom/subproduct_form.html', {
        'action': 'Editar',
        'subproduct': subproduct,
        'products': products
    })


@login_required
@user_passes_test(_is_superuser)
@require_POST
def subproduct_delete(request, subproduct_id):
    """Delete subproduct"""
    subproduct = get_object_or_404(SubProduct, id=subproduct_id)
    name = subproduct.name
    
    try:
        subproduct.delete()
        messages.success(request, f'Subproduto "{name}" excluído com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir subproduto: {str(e)}')
    
    return redirect('admin_subproduct_list')


# ============= COMBO VIEWS =============

@login_required
@user_passes_test(_is_superuser)
def combo_list(request):
    """List all combos"""
    combos = Combo.objects.prefetch_related('products').order_by('name')
    return render(request, 'admin_custom/combo_list.html', {'combos': combos})


@login_required
@user_passes_test(_is_superuser)
def combo_add(request):
    """Add new combo"""
    products = Product.objects.all().order_by('name')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        product_ids = request.POST.getlist('products')
        
        try:
            combo = Combo.objects.create(
                name=name,
                price=price,
                image=image
            )
            combo.products.set(product_ids)
            messages.success(request, f'Combo "{combo.name}" criado com sucesso!')
            return redirect('admin_combo_list')
        except Exception as e:
            messages.error(request, f'Erro ao criar combo: {str(e)}')
    
    return render(request, 'admin_custom/combo_form.html', {
        'action': 'Adicionar',
        'products': products
    })


@login_required
@user_passes_test(_is_superuser)
def combo_edit(request, combo_id):
    """Edit existing combo"""
    combo = get_object_or_404(Combo, id=combo_id)
    products = Product.objects.all().order_by('name')
    
    if request.method == 'POST':
        combo.name = request.POST.get('name')
        combo.price = request.POST.get('price')
        product_ids = request.POST.getlist('products')
        
        if 'image' in request.FILES:
            combo.image = request.FILES['image']
        
        try:
            combo.save()
            combo.products.set(product_ids)
            messages.success(request, f'Combo "{combo.name}" atualizado com sucesso!')
            return redirect('admin_combo_list')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar combo: {str(e)}')
    
    return render(request, 'admin_custom/combo_form.html', {
        'action': 'Editar',
        'combo': combo,
        'products': products
    })


@login_required
@user_passes_test(_is_superuser)
@require_POST
def combo_delete(request, combo_id):
    """Delete combo"""
    combo = get_object_or_404(Combo, id=combo_id)
    name = combo.name
    
    try:
        combo.delete()
        messages.success(request, f'Combo "{name}" excluído com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir combo: {str(e)}')
    
    return redirect('admin_combo_list')


# ============= CAROUSEL VIEWS =============

@login_required
@user_passes_test(_is_superuser)
def carousel_list(request):
    """List all carousel images"""
    images = CarouselImage.objects.all().order_by('id')
    return render(request, 'admin_custom/carousel_list.html', {'images': images})


@login_required
@user_passes_test(_is_superuser)
def carousel_add(request):
    """Add new carousel image"""
    if request.method == 'POST':
        alt_text = request.POST.get('alt_text', '')
        image = request.FILES.get('image')
        
        try:
            carousel_image = CarouselImage.objects.create(
                image=image,
                alt_text=alt_text
            )
            messages.success(request, 'Imagem do carrossel adicionada com sucesso!')
            return redirect('admin_carousel_list')
        except Exception as e:
            messages.error(request, f'Erro ao adicionar imagem: {str(e)}')
    
    return render(request, 'admin_custom/carousel_form.html', {'action': 'Adicionar'})


@login_required
@user_passes_test(_is_superuser)
def carousel_edit(request, image_id):
    """Edit carousel image"""
    carousel_image = get_object_or_404(CarouselImage, id=image_id)
    
    if request.method == 'POST':
        carousel_image.alt_text = request.POST.get('alt_text', '')
        
        if 'image' in request.FILES:
            carousel_image.image = request.FILES['image']
        
        try:
            carousel_image.save()
            messages.success(request, 'Imagem do carrossel atualizada com sucesso!')
            return redirect('admin_carousel_list')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar imagem: {str(e)}')
    
    return render(request, 'admin_custom/carousel_form.html', {
        'action': 'Editar',
        'carousel_image': carousel_image
    })


@login_required
@user_passes_test(_is_superuser)
@require_POST
def carousel_delete(request, image_id):
    """Delete carousel image"""
    carousel_image = get_object_or_404(CarouselImage, id=image_id)
    
    try:
        carousel_image.delete()
        messages.success(request, 'Imagem do carrossel excluída com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir imagem: {str(e)}')
    
    return redirect('admin_carousel_list')


# ============= ORDER VIEWS =============

@login_required
@user_passes_test(_is_superuser)
def order_list(request):
    """List all orders"""
    orders = Order.objects.select_related('user').order_by('-created_at')
    return render(request, 'admin_custom/order_list.html', {'orders': orders})


@login_required
@user_passes_test(_is_superuser)
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id)
    
    # Process items with customization details
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
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f'Status do pedido #{order.id} atualizado!')
            return redirect('admin_order_list')
    
    return render(request, 'admin_custom/order_detail.html', {
        'order': order,
        'items_data': items_data,
        'status_choices': Order.STATUS_CHOICES
    })
