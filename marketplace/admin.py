from django.contrib import admin
from .models import Product, Combo, CarouselImage, SubProduct

admin.site.register(Product)
admin.site.register(Combo)
admin.site.register(CarouselImage)
admin.site.register(SubProduct)
