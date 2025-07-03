from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CartItem, Combo, CarouselImage, Product, SubProduct  # Importa seu novo model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

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

    # Buscar todos os itens do carrinho deste usuário
    cart_items = CartItem.objects.filter(user=request.user)

    # Somar quantos itens no total (ex: 3 batatas + 2 refrigerantes = 5)
    cart_items_count = sum(item.quantity for item in cart_items)

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
def cart(request):
    cart_session = request.session.get('cart', {'products': {}, 'subproducts': {}})
    cart_items = []
    cart_total = 0

    # Produtos principais
    for prod_id, qty in cart_session.get('products', {}).items():
        product = get_object_or_404(Product, pk=prod_id)
        total_price = product.price * qty
        cart_items.append({
            'product': product,
            'quantity': qty,
            'total_price': total_price
        })
        cart_total += total_price

    # Subprodutos
    for sub_id, qty in cart_session.get('subproducts', {}).items():
        sub = get_object_or_404(SubProduct, pk=sub_id)
        total_price = sub.price * qty
        cart_items.append({
            'product': sub,  # Para simplificar template
            'quantity': qty,
            'total_price': total_price
        })
        cart_total += total_price

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

  

@login_required
@require_POST
def add_to_cart(request, combo_id):
    from .models import CartItem, Product, SubProduct  # Importe seus models

    print("POST recebido:", request.POST)

    try:
        data = json.loads(request.POST.get('selected_items', '{}'))
        combo = get_object_or_404(Combo, pk=combo_id)

        # Limpar itens existentes do carrinho para este combo
        CartItem.objects.filter(user=request.user, combo=combo).delete()

        created_items = []

        # Adicionar produtos principais
        for product_id, quantity in data.get('products', {}).items():
            product = get_object_or_404(Product, pk=product_id)
            item = CartItem.objects.create(
                user=request.user,
                combo=combo,
                product=product,
                quantity=quantity
            )
            created_items.append({
                'type': 'product',
                'id': product.id,
                'name': product.name,
                'quantity': quantity
            })

        # Adicionar subprodutos
        for subproduct_id, quantity in data.get('subproducts', {}).items():
            subproduct = get_object_or_404(SubProduct, pk=subproduct_id)
            item = CartItem.objects.create(
                user=request.user,
                combo=combo,
                subproduct=subproduct,
                quantity=quantity
            )
            created_items.append({
                'type': 'subproduct',
                'id': subproduct.id,
                'name': subproduct.name,
                'quantity': quantity
            })

        print("Itens adicionados ao carrinho:", created_items)

        return JsonResponse({
            'status': 'success',
            'message': 'Itens adicionados ao carrinho.',
            'items': created_items
        })

    except Exception as e:
        print("Erro ao adicionar ao carrinho:", str(e))
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



