from . import views_account
from django.urls import path

urlpatterns = [
    path('editar-perfil/', views_account.edit_profile, name='edit_profile'),
    path('editar-email/', views_account.edit_email, name='edit_email'),
    path('editar-telefone/', views_account.edit_phone, name='edit_phone'),
    path('alterar-senha/', views_account.change_password, name='change_password'),
    path('historico/', views_account.order_history, name='order_history'),
    path('configuracoes/', views_account.account_settings, name='account_settings'),
    path('logout/', views_account.logout_view, name='logout'),
]
