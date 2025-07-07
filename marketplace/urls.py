from django.urls import path, include
from . import views
from .views_payment import finalizar_pedido, compra_sucesso, compra_errada, compra_pendente

urlpatterns = [
    path('', views.loading_screen, name='loading'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('combo/<int:combo_id>/', views.combo_detail, name='combo_detail'),
    path('cart/', views.cart, name='cart'),
    path('alterar-senha/', views.change_password, name='change_password'),
    path('alterar-nome/', views.change_name, name='change_name'),
    path('alterar-email/', views.change_email, name='change_email'),
    path('combo/<int:combo_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),
    path('finalizar-pedido/', finalizar_pedido, name='finalizar_pedido'),
    path('compra-sucesso', compra_sucesso, name='compra_sucesso'),
    path('compraerrada', compra_errada, name='compra_errada'),
    path('compra-pendente', compra_pendente, name='compra_pendente'),
    path('conta/', include('marketplace.urls_account')),
]
