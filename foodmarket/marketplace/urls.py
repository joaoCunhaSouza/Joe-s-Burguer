from django.urls import path
from . import views

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
]
