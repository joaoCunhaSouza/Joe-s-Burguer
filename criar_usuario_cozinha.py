#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar usuário da cozinha
Execute: python criar_usuario_cozinha.py
"""

import os
import sys
import django

# Configurar encoding para UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodmarket.settings')
django.setup()

from django.contrib.auth.models import User

def criar_usuario_cozinha():
    """Cria um usuário staff para a cozinha se não existir"""
    username = 'cozinha'
    
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        # Garantir que o usuário tem permissão de staff
        if not user.is_staff:
            user.is_staff = True
            user.save()
            print(f'OK - Usuario "{username}" atualizado para staff!')
        else:
            print(f'INFO - Usuario "{username}" ja existe e eh staff')
        
        # Resetar senha (opcional)
        print(f'\nPara resetar a senha, descomente a linha no script')
        # user.set_password('cozinha123')
        # user.save()
        # print(f'OK - Senha resetada para: cozinha123')
    else:
        user = User.objects.create_user(
            username=username,
            password='cozinha123',
            first_name='Cozinha',
            is_staff=True,  # Importante: marcar como staff
            is_active=True
        )
        print(f'OK - Usuario da cozinha criado!')
        print(f'   Usuario: {username}')
        print(f'   Senha: cozinha123')
        print(f'   Staff: Sim')

def main():
    print('\n' + '='*50)
    print('CRIANDO USUARIO DA COZINHA - JOES BURGUER')
    print('='*50 + '\n')
    
    criar_usuario_cozinha()
    
    print('\n' + '='*50)
    print('CONFIGURACAO CONCLUIDA!')
    print('='*50)
    print('\nProximos passos:')
    print('   1. Execute: python manage.py runserver')
    print('   2. Acesse: http://127.0.0.1:8000/kitchen/login/')
    print('   3. Login: cozinha')
    print('   4. Senha: cozinha123')
    print('\n' + '='*50 + '\n')

if __name__ == '__main__':
    main()
