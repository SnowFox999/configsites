from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Computer, Order_Computer
import json


# Create your views here.


def index(request):
    # Page from the theme 
    return render(request, 'pages/index.html')

def computer_detail(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)
    data = {
        'name': computer.name,
        'status': computer.status,
        'date': computer.date.strftime('%Y-%m-%d'),
        'serial_number': computer.serial_number,
        'type': computer.type,
        'custom>type': computer.custom_type,
        'processor': computer.processor,
        'ram': computer.ram,
        'hardDisk': computer.hardDisk,
        'diskPlace': computer.diskPlace,
        'videoCard': computer.videoCard,
        'typeDB': computer.typeDB,
        'lanCard': computer.lanCard,
        'monitor': computer.monitor,
        'admin': computer.admin,
        'user': computer.user,
        'addSoftware': computer.addSoftware,
        'addDevices': computer.addDevices,
        'addComment': computer.addComment,
        'addSettings': computer.addSettings,
    }
    return JsonResponse(data)

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
    orders = Order_Computer.objects.all()  # Получаем все заказы из базы данных
    return render(request, 'home/order_list.html', {'orders': orders})

   






