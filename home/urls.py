from django.urls import path

from . import views
from django.urls import path
from .views import computer_detail, computer_edit, order_list, index

urlpatterns = [
    path('', index, name='index'),
    path('computer/<uuid:computer_id>/', computer_detail, name='computer_detail'),
    path('computer/<uuid:computer_id>/edit/', computer_edit, name='computer_edit'),
    path('orders/', order_list, name='order_list'), 
]