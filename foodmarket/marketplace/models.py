from django.db import models
from django.contrib.auth.models import User

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/')
    alt_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.alt_text or f"Imagem {self.id}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class SubProduct(models.Model):
    """
    Subproduto vinculado a um produto principal.
    Exemplo: sabor de refrigerante, opção adicional etc.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='subproducts'
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Preço adicional (opcional). Pode ser 0.00."
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='subproducts/', blank=True, null=True)  # imagem opcional

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class Combo(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='combos/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    products = models.ManyToManyField(Product, related_name='combos')

    def __str__(self):
        return self.name
