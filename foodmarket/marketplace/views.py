from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Combo, CarouselImage  # Importa seu novo model

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
    carousel_images = CarouselImage.objects.all()  # Busca imagens do carrossel
    return render(request, 'home.html', {
        'combos': combos,
        'carousel_images': carousel_images  # Passa para o template
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
    return render(request, 'cart.html')
