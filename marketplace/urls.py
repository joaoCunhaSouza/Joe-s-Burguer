from django.urls import path, include
from . import views
from .views_payment import finalizar_pedido, compra_sucesso, compra_errada, compra_pendente
from . import views_token, views_kitchen

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
    path('historico/', views.order_history, name='order_history'),
    path('historico/<int:order_id>/', views.order_history_detail, name='order_history_detail'),
    path('conta/', include('marketplace.urls_account')),
    # Token / offline endpoints
    path('token/login/', views_token.token_login, name='token_login'),
    path('token/dashboard/', views_token.token_dashboard, name='token_dashboard'),
    path('token/generate/', views_token.generate_token, name='generate_token'),
    path('token/offline-submit/', views_token.offline_submit, name='offline_submit'),
    # CSRF helper for client-side token refresh
    path('csrf/refresh/', views.csrf_refresh, name='csrf_refresh'),
    # Kitchen (cozinha) views
    path('kitchen/login/', views_kitchen.kitchen_login, name='kitchen_login'),
    path('kitchen/logout/', views_kitchen.kitchen_logout, name='kitchen_logout'),
    path('kitchen/', views_kitchen.kitchen_dashboard, name='kitchen_dashboard'),
    path('kitchen/orders.json', views_kitchen.kitchen_orders_json, name='kitchen_orders_json'),
    path('kitchen/order/<int:order_id>/', views_kitchen.kitchen_order_detail, name='kitchen_order_detail'),
    path('kitchen/order/<int:order_id>/confirm/', views_kitchen.kitchen_confirm_action, name='kitchen_confirm_action'),
    path('kitchen/debug_orders/', views_kitchen.kitchen_debug_orders, name='kitchen_debug_orders'),
    path('kitchen/webhook/', views_kitchen.kitchen_webhook, name='kitchen_webhook'),
    # Custom Admin Panel
    path('myadmin/', include('marketplace.urls_admin')),
]
