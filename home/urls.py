from django.urls import path

from . import views
from django.urls import path
from .views import computer_detail, computer_edit, order_list, index, search_orders

urlpatterns = [
    path('', index, name='index'),
    path('computer/<int:computer_id>/', views.computer_detail, name='computer_detail'),
    path('computer/<int:computer_id>/edit/', computer_edit, name='computer_edit'),
    path('orders/', order_list, name='order_list'),
    path('orders/search/', search_orders, name='search_orders'), 
]