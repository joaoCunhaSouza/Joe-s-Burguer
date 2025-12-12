"""
Script para gerar uma SECRET_KEY segura para Django
"""
from django.core.management.utils import get_random_secret_key

# Gera uma chave aleatoria e segura
secret_key = get_random_secret_key()

print("=" * 70)
print("SUA NOVA SECRET_KEY SEGURA:")
print("=" * 70)
print(secret_key)
print("=" * 70)
print("\nCOPIE a chave acima e cole no Render em:")
print("   Dashboard -> Environment Variables -> SECRET_KEY")
print("\nNUNCA compartilhe esta chave publicamente!")
print("=" * 70)
