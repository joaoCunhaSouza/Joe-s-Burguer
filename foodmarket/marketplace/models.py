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

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    subproduct = models.ForeignKey(SubProduct, on_delete=models.CASCADE, null=True, blank=True)
    combo = models.ForeignKey(
        'Combo',  # Use string literal if Combo is defined later in the same file
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.combo:
            return f"{self.quantity} x {self.combo.name} ({self.user.username}'s cart)"
        elif self.product:
            return f"{self.quantity} x {self.product.name} ({self.user.username}'s cart)"
        elif self.subproduct:
            return f"{self.quantity} x {self.subproduct.name} ({self.user.username}'s cart)"
        return f"Cart Item ({self.user.username})" # Fallback

    @property
    def get_total_price(self):
        if self.combo:
            return self.combo.price * self.quantity
        elif self.product:
            return self.product.price * self.quantity
        elif self.subproduct:
            return self.subproduct.price * self.quantity
        return 0
    
