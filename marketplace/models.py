from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render

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
    customization = models.JSONField(default=dict, blank=True, null=True)  # Campo de customização

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
    
    @staticmethod
    def calculate_custom_total(combo, customization):
        """
        Calcula o preço total do combo considerando customizações (extras, subprodutos).
        customization: dict {subproduct_id: quantidade}
        """
        from .models import SubProduct
        total = float(combo.price)
        if customization:
            for sub_id, qty in customization.items():
                try:
                    sub = SubProduct.objects.get(id=sub_id)
                    # O mínimo padrão é 1 para todos (inclusive refrigerante)
                    min_qty = 1
                    if qty > min_qty:
                        total += (qty - min_qty) * float(sub.price)
                    # Se qty < min_qty, não soma nada (ingrediente removido)
                except SubProduct.DoesNotExist:
                    continue
        return total
    
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('combo', 'product', 'subproduct')

    # Calcular total do carrinho
    cart_total = sum(item.get_total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_items_count': sum(item.quantity for item in cart_items),
    }
    return render(request, 'cart.html', context)


class APIToken(models.Model):
    """Simple token model to allow token-based login for a superuser or staff.
    The token is a random string stored here with an optional label and creator.
    """
    key = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=120, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label or self.key[:12]}"


class OfflineSubmission(models.Model):
    """Stores data submitted from the client when offline so server can persist later.
    The `payload` is stored as JSON; `processed` marks whether an admin processed it.
    """
    token = models.ForeignKey(APIToken, on_delete=models.SET_NULL, null=True, blank=True)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"OfflineSubmission {self.id} ({'processed' if self.processed else 'new'})"


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_PREPARING = 'preparing'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Novo'),
        (STATUS_PREPARING, 'Em preparação'),
        (STATUS_DONE, 'Finalizado'),
        (STATUS_CANCELLED, 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=150, blank=True)
    items = models.JSONField(help_text='Snapshot dos itens do pedido')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.customer_name or (self.user.username if self.user else 'Anon') } - {self.status}"