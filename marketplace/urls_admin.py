from django.urls import path
from . import views_admin

urlpatterns = [
    # Admin authentication
    path('login/', views_admin.admin_login, name='admin_login'),
    path('logout/', views_admin.admin_logout, name='admin_logout'),
    path('', views_admin.admin_dashboard, name='custom_admin_dashboard'),
    
    # Kitchen Users
    path('kitchen-users/', views_admin.kitchen_user_list, name='admin_kitchen_user_list'),
    path('kitchen-users/add/', views_admin.kitchen_user_add, name='admin_kitchen_user_add'),
    path('kitchen-users/<int:user_id>/edit/', views_admin.kitchen_user_edit, name='admin_kitchen_user_edit'),
    path('kitchen-users/<int:user_id>/delete/', views_admin.kitchen_user_delete, name='admin_kitchen_user_delete'),
    
    # Products
    path('products/', views_admin.product_list, name='admin_product_list'),
    path('products/add/', views_admin.product_add, name='admin_product_add'),
    path('products/<int:product_id>/edit/', views_admin.product_edit, name='admin_product_edit'),
    path('products/<int:product_id>/delete/', views_admin.product_delete, name='admin_product_delete'),
    
    # SubProducts
    path('subproducts/', views_admin.subproduct_list, name='admin_subproduct_list'),
    path('subproducts/add/', views_admin.subproduct_add, name='admin_subproduct_add'),
    path('subproducts/<int:subproduct_id>/edit/', views_admin.subproduct_edit, name='admin_subproduct_edit'),
    path('subproducts/<int:subproduct_id>/delete/', views_admin.subproduct_delete, name='admin_subproduct_delete'),
    
    # Combos
    path('combos/', views_admin.combo_list, name='admin_combo_list'),
    path('combos/add/', views_admin.combo_add, name='admin_combo_add'),
    path('combos/<int:combo_id>/edit/', views_admin.combo_edit, name='admin_combo_edit'),
    path('combos/<int:combo_id>/delete/', views_admin.combo_delete, name='admin_combo_delete'),
    
    # Carousel
    path('carousel/', views_admin.carousel_list, name='admin_carousel_list'),
    path('carousel/add/', views_admin.carousel_add, name='admin_carousel_add'),
    path('carousel/<int:image_id>/edit/', views_admin.carousel_edit, name='admin_carousel_edit'),
    path('carousel/<int:image_id>/delete/', views_admin.carousel_delete, name='admin_carousel_delete'),
    
    # Orders
    path('orders/', views_admin.order_list, name='admin_order_list'),
    path('orders/<int:order_id>/', views_admin.order_detail, name='admin_order_detail'),
]
