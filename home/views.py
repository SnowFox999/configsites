
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Computer, Order_Computer, Customer, Location, UserName
from django.db.models import Q
import json


# Create your views here.


def index(request):
    # Page from the theme 
    return render(request, 'pages/index.html')

def computer_detail(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)
    customers = Customer.objects.all()
    locations = Location.objects.all()

    if request.method == 'POST':
        # Получаем данные из формы
        computer_name = request.POST.get('computer_name')
        serial_number = request.POST.get('serial_number')
        user_types = request.POST.getlist('user_type[]')
        user_names = request.POST.getlist('user_name[]')
        user_passwords = request.POST.getlist('user_password[]')

        # Обновляем информацию о компьютере
        computer.name = computer_name
        computer.serial_number = serial_number
        computer.save()

        # Удаляем старых пользователей
        #computer.user.clear()
        
        # Добавляем новых пользователей
        #for user_type, user_name, user_password in zip(user_types, user_names, user_passwords):
        #    user = UserName.objects.create(
        #        user_type=user_type,
        #        login=user_name,
        #        password=user_password
        #    )
        #    computer.user.add(user)

        # Перенаправляем обратно на страницу
        return redirect('computer_detail', computer_id=computer.id)

    else:
        data = {
            'name': computer.name,
            'status': computer.status,
            'location': list(computer.location.values('id', 'name')),
            'date': computer.date.strftime('%Y-%m-%d'),
            'serial_number': computer.serial_number,
            'type': computer.type,
            'custom_type': computer.custom_type,
            'processor': list(computer.processor.values('id', 'name')),
            'ram': list(computer.ram.values('id', 'type', 'gigabytes')),
            'hardDisk': list(computer.hardDisk.values('id', 'type', 'gigabytes')),
            'diskPlace': list(computer.diskPlace.values('id', 'name')),
            'videoCard': list(computer.videoCard.values('id', 'name')),
            'typeDB': list(computer.typeDB.values('id', 'type', 'version')),
            'lanCard': list(computer.lanCard.values('id', 'type')),
            'monitor': list(computer.monitor.values('id', 'name', 'custom_name')),
            'admin': list(computer.admin.values('id', 'login', 'password')),
            'user': list(computer.user.values('id', 'login', 'password')),
            'addSoftware': computer.addSoftware,
            'addDevices': computer.addDevices,
            'addComment': computer.addComment,
            'addSettings': list(computer.addSettings.values('id', 'name', 'text')),
            'customer': computer.customer.name if computer.customer else None,
            'employee': computer.employee.name if computer.employee else None,
        }
        context = {
            'computer': computer,
            'customers': customers,
            'locations': locations,  # Передаем locations в контекст
        }
        return render(request, 'home/computer_detail.html', context)
        




def computer_detail_view(request):
    return render(request, 'computer_detail.html')


def computer_edit(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)
    if request.method == 'POST':
        computer.name = request.POST['name']
        computer.status = request.POST['status']
        computer.serial_number = request.POST['serial_number']
        computer.type = request.POST['type']
        computer.custom_type = request.POST['custom_type']
        computer.processor = request.POST['[processor]']
        computer.ram = request.POST['ram']
        computer.hardDisk = request.POST['hardDisk']
        computer.diskPlace = request.POST['diskPlace']
        computer.videoCard = request.POST['videoCard']
        computer.typeDB = request.POST['typeDB']
        computer.lanCard = request.POST['lanCard']
        computer.monitor = request.POST['monitor']
        computer.admin = request.POST['admin']
        computer.user = request.POST['user']
        computer.addSoftware = request.POST['addSoftware']
        computer.addDevices = request.POST['addDevices']
        computer.addComment = request.POST['addComment']
        computer.addSettings = request.POST['addSettings']

        computer.date = request.POST['date']
        computer.save()
        return JsonResponse({'message': 'Success'})
    
    return JsonResponse({'error': 'Invalid request'})



def order_list(request):
    orders = Order_Computer.objects.all()
    return render(request, 'home/order_list.html', {'orders': orders})

def search_orders(request):
    query = request.GET.get('q', '')
    orders = Order_Computer.objects.all()

    if query:
        orders = orders.filter(
            Q(computer__name__icontains=query) |
            Q(computer__customer__name__icontains=query) |
            Q(computer__date__icontains=query) |  # Здесь нужно указать поле даты в модели Computer
            Q(computer__status__icontains=query) |  # Здесь нужно указать поле статуса в модели Computer
            Q(id__icontains=query)  # Поиск по айди заказа
        )
    return render(request, 'home/order_list_results.html', {'orders': orders})

   







