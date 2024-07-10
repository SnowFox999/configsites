
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Computer, Order_Computer
from django.db.models import Q


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
        'custom_type': computer.custom_type,
        'processor': list(computer.processor.values('id', 'name')),
        'ram': list(computer.ram.values('id', 'name')),
        'hardDisk': list(computer.hardDisk.values('id', 'name')),
        'diskPlace': list(computer.diskPlace.values('id', 'name')),
        'videoCard': list(computer.videoCard.values('id', 'name')),
        'typeDB': list(computer.typeDB.values('id', 'name')),
        'lanCard': list(computer.lanCard.values('id', 'name')),
        'monitor': list(computer.monitor.values('id', 'name')),
        'admin': list(computer.admin.values('id', 'login')),
        'user': list(computer.user.values('id', 'login')),
        'addSoftware': computer.addSoftware,
        'addDevices': computer.addDevices,
        'addComment': computer.addComment,
        'addSettings': list(computer.addSettings.values('id', 'name')),
    }
    return JsonResponse(data)


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

   







