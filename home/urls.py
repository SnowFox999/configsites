from django.urls import path

from . import views
from django.urls import path
from .views import computer_detail, edit, order_list, index, search_orders, update_computer_status, save_computer_data

urlpatterns = [
    path('', index, name='index'),
    path('computer/<int:computer_id>/', views.computer_detail, name='computer_detail'),
    path('computer/<int:computer_id>/edit/', views.edit, name='edit'),
    path('orders/', order_list, name='order_list'),
    path('orders/search/', search_orders, name='search_orders'), 
    path('update_computer_status/<int:computer_id>/', update_computer_status, name='update_computer_status'),
    path('save_computer_data/', save_computer_data, name='save_computer_data'),
]