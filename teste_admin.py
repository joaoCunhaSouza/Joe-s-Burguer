#!/usr/bin/env python
"""
Script para criar dados de teste no painel admin
Execute: python teste_admin.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodmarket.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import Product, SubProduct, Combo, CarouselImage

def criar_superusuario():
    """Cria um superusuário de teste se não existir"""
    email = 'admin@joesburguer.com'
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_superuser(
            username='admin',
            email=email,
            password='admin123',
            first_name='Administrador'
        )
        print(f'✅ Superusuário criado!')
        print(f'   Email: {email}')
        print(f'   Senha: admin123')
    else:
        print(f'ℹ️  Superusuário já existe: {email}')

def criar_produtos_teste():
    """Cria produtos de teste"""
    produtos = [
        {
            'name': 'Hambúrguer Clássico',
            'price': 15.90,
            'description': 'Hambúrguer suculento com queijo, alface e tomate'
        },
        {
            'name': 'Batata Frita',
            'price': 8.90,
            'description': 'Porção de batatas fritas crocantes'
        },
        {
            'name': 'Refrigerante',
            'price': 5.00,
            'description': 'Refrigerante gelado 350ml'
        }
    ]
    
    criados = 0
    for p in produtos:
        if not Product.objects.filter(name=p['name']).exists():
            Product.objects.create(**p)
            criados += 1
    
    if criados > 0:
        print(f'✅ {criados} produtos criados')
    else:
        print('ℹ️  Produtos já existem')

def criar_subprodutos_teste():
    """Cria subprodutos de teste"""
    try:
        hamburguer = Product.objects.get(name='Hambúrguer Clássico')
        refrigerante = Product.objects.get(name='Refrigerante')
        
        subprodutos = [
            {
                'product': hamburguer,
                'name': 'Queijo Extra',
                'price': 3.00,
                'description': 'Fatia adicional de queijo cheddar'
            },
            {
                'product': hamburguer,
                'name': 'Bacon',
                'price': 4.00,
                'description': 'Bacon crocante'
            },
            {
                'product': refrigerante,
                'name': 'Coca-Cola',
                'price': 0.00,
                'description': 'Coca-Cola 350ml'
            },
            {
                'product': refrigerante,
                'name': 'Guaraná',
                'price': 0.00,
                'description': 'Guaraná Antarctica 350ml'
            }
        ]
        
        criados = 0
        for sp in subprodutos:
            if not SubProduct.objects.filter(name=sp['name'], product=sp['product']).exists():
                SubProduct.objects.create(**sp)
                criados += 1
        
        if criados > 0:
            print(f'✅ {criados} subprodutos criados')
        else:
            print('ℹ️  Subprodutos já existem')
    except Product.DoesNotExist:
        print('⚠️  Crie os produtos primeiro')

def criar_combo_teste():
    """Cria um combo de teste"""
    try:
        hamburguer = Product.objects.get(name='Hambúrguer Clássico')
        batata = Product.objects.get(name='Batata Frita')
        refri = Product.objects.get(name='Refrigerante')
        
        if not Combo.objects.filter(name='Combo Clássico').exists():
            combo = Combo.objects.create(
                name='Combo Clássico',
                price=25.90
            )
            combo.products.set([hamburguer, batata, refri])
            print('✅ Combo criado')
        else:
            print('ℹ️  Combo já existe')
    except Product.DoesNotExist:
        print('⚠️  Crie os produtos primeiro')

def main():
    print('\n' + '='*50)
    print('🍔 CRIANDO DADOS DE TESTE - JOE\'S BURGUER')
    print('='*50 + '\n')
    
    criar_superusuario()
    criar_produtos_teste()
    criar_subprodutos_teste()
    criar_combo_teste()
    
    print('\n' + '='*50)
    print('✅ DADOS DE TESTE CRIADOS COM SUCESSO!')
    print('='*50)
    print('\n📝 Próximos passos:')
    print('   1. Execute: python manage.py runserver')
    print('   2. Acesse: http://127.0.0.1:8000/myadmin/login/')
    print('   3. Login: admin@joesburguer.com')
    print('   4. Senha: admin123')
    print('\n' + '='*50 + '\n')

if __name__ == '__main__':
    main()
