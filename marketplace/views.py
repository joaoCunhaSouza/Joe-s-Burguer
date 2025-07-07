from django.http import JsonResponse
from .models import CarouselImage, CartItem, Combo, Product, SubProduct # Make sure all models are imported
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
import json
from django.db.models import F, Sum

# ... (suas outras views como login, register, etc. permanecem as mesmas)

def change_password(request):
    return render(request, 'change_password.html')

def change_name(request):
    return render(request, 'change_name.html')

def change_email(request):
    return render(request, 'change_email.html')

def loading_screen(request):
    return render(request, 'loading.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Email ou senha inválidos.'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()
        return redirect('login')
    return render(request, 'register.html')

@login_required
def home(request):
    combos = Combo.objects.all()
    carousel_images = CarouselImage.objects.all()
    cart_items_count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    return render(request, 'home.html', {
        'combos': combos,
        'carousel_images': carousel_images,
        'cart_items_count': cart_items_count
    })

@login_required
def combo_detail(request, combo_id):
    combo = get_object_or_404(Combo, pk=combo_id)
    products = combo.products.all()
    return render(request, 'combo_detail.html', {
        'combo': combo,
        'products': products
    })


@login_required
@require_POST
def add_to_cart(request, combo_id):
    try:
        data = json.loads(request.body)
        combo = get_object_or_404(Combo, pk=combo_id)

        # Serializa a customização para comparação
        customization = data.get('subproducts', {})

        # Procura por um CartItem com a mesma customização
        cart_item = CartItem.objects.filter(
            user=request.user,
            combo=combo,
            product=None,
            subproduct=None,
            customization=customization
        ).first()

        if cart_item:
            cart_item.quantity = F('quantity') + 1
            cart_item.save()
            cart_item.refresh_from_db()
        else:
            cart_item = CartItem.objects.create(
                user=request.user,
                combo=combo,
                product=None,
                subproduct=None,
                quantity=1,
                customization=customization
            )

        return JsonResponse({
            'status': 'success',
            'message': 'Combo adicionado ao carrinho.',
            'quantity': cart_item.quantity
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def cart(request):
    cart_items_queryset = (
        CartItem.objects.filter(user=request.user, combo__isnull=False, product=None, subproduct=None)
        .select_related('combo')
    )

    processed_items = []
    cart_total = 0

    from .models import SubProduct, Product

    for item in cart_items_queryset:
        unit_price = CartItem.calculate_custom_total(item.combo, item.customization)
        line_total = unit_price * item.quantity
        cart_total += line_total

        ingredientes = []
        for product in item.combo.products.all():
            for sub in product.subproducts.all():
                # Só mostra se o usuário explicitamente selecionou (qty >= 1) ou removeu (qty == 0)
                qty = None
                if item.customization and str(sub.id) in item.customization:
                    qty = item.customization[str(sub.id)]
                if qty is not None:
                    if qty == 0:
                        ingredientes.append({
                            'name': sub.name,
                            'removed': True
                        })
                    elif qty >= 1:
                        ingredientes.append({
                            'name': sub.name,
                            'removed': False
                        })
        processed_items.append({
            'combo_id': item.combo.id,
            'combo_image_url': item.combo.image.url if item.combo.image else '',
            'name': item.combo.name,
            'quantity': item.quantity,
            'unit_price': unit_price,
            'line_total': line_total,
            'cartitem_id': item.id,
            'ingredientes': ingredientes,
        })

    return render(request, 'cart.html', {
        'cart_items': processed_items,
        'cart_total': cart_total
    })


@login_required
@require_POST
def update_cart_item(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action') # 'increase', 'decrease', or 'remove'

        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user, product=None, subproduct=None)

        if action == 'increase':
            cart_item.quantity = F('quantity') + 1
            cart_item.save()
            cart_item.refresh_from_db()
            status = 'success'
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity = F('quantity') - 1
                cart_item.save()
                cart_item.refresh_from_db()
                status = 'success'
            else:
                cart_item.delete()
                status = 'removed'
        elif action == 'remove':
            cart_item.delete()
            status = 'removed'
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

        # Recalcular total do carrinho
        cart_total = sum(item.combo.price * item.quantity for item in CartItem.objects.filter(user=request.user, combo__isnull=False, product=None, subproduct=None))

        return JsonResponse({
            'status': status,
            'new_quantity': cart_item.quantity if status == 'success' else 0,
            'cart_total': f'R$ {cart_total:,.2f}'.replace('.', ','),
        })

    except CartItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item do carrinho não encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def _get_cart_totals_and_count(user):
    """Helper function to calculate total cart value and item count for a user."""
    cart_items = CartItem.objects.filter(user=user).select_related('product', 'subproduct')
    total = 0
    count = 0
    for item in cart_items:
        price = 0
        if item.product:
            price = item.product.price
        elif item.subproduct:
            price = item.subproduct.price
        
        total += item.quantity * price
        count += item.quantity
    return total, count

def cart_view(request):
    # Buscar só os CartItems que têm combo definido para este usuário
    cart_items = CartItem.objects.filter(user=request.user, combo__isnull=False).select_related('combo')
    cart_total = sum(item.get_total_price for item in cart_items)
    cart_items_count = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_items_count': cart_items_count,
    }
    return render(request, 'cart.html', context)