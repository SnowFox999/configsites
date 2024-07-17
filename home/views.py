
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Computer, Order_Computer, Customer, Location, UserName, Employee
from django.db.models import Q
import json


# Create your views here.


def index(request):
    # Page from the theme 
    return render(request, 'pages/index.html')

def computer_detail(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)
    customers = Customer.objects.all()
    employees = Employee.objects.all()
    locations = computer.locations.values('name')

    admins = list(computer.admin.values('user_type', 'login', 'password'))
    users = list(computer.user.values('user_type', 'login', 'password'))
    processors = list(computer.processor.values('name'))
    videoCards = list(computer.videoCard.values('name'))
    lanCards = list(computer.lanCard.values('type', 'series'))
    rams = list(computer.ram.values('type', 'gigabytes'))
    hardDisks = list(computer.hardDisk.values('type', 'gigabytes'))
    windows = list(computer.windows.values('name', 'licenseNumber', 'licenseKeys'))
    typeDBs = list(computer.typeDB.values('type', 'version'))
    monitors = list(computer.monitor.values('name', 'custom_name'))
    diskPlaces = list(computer.diskPlace.values('name'))
    addSettings = list(computer.addSettings.values('name', 'text'))
    computer_type = computer.custom_type if computer.custom_type else computer.type
    

   

 
    data = {
            'name': computer.name,
            'status': computer.status,
            'locations': list(locations),
            'date': computer.date.strftime('%Y-%m-%d'),
            'serial_number': computer.serial_number,
            'type': computer_type,
            'custom_type': computer.custom_type,
            'processor': processors,
            'ram': rams,
            'hardDisk': hardDisks,
            'diskPlace': diskPlaces,
            'videoCard': videoCards,
            'typeDB': typeDBs,
            'lanCard': lanCards,
            'monitor': monitors,
            'admin': admins,
            'user': users,
            'windows': windows,
            'addSoftware': computer.addSoftware,
            'addDevices': computer.addDevices,
            'addComment': computer.addComment,
            'addSetting': addSettings,
            'customer': computer.customer.name if computer.customer else None,
            'employee': computer.employee.name if computer.employee else None,
    }
    
    context = {
            'computer': computer,
            'customers': customers,
            'employees': employees,
            'data': data,
        } 
        
    return render(request, 'home/computer_detail.html', context)
        



def computer_edit(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)

    if request.method == 'POST':
        # Обработка POST-запроса для сохранения изменений
        computer.name = request.POST.get('name')
        computer.status = request.POST.get('status')
        computer.serial_number = request.POST.get('serial_number')
        computer.type = request.POST.get('type') if not request.POST.get('custom_type') else None
        computer.custom_type = request.POST.get('custom_type')
        computer.processor = request.POST.get('processor')
        computer.ram = request.POST.get('ram')
        computer.hardDisk = request.POST.get('hardDisk')
        computer.diskPlace = request.POST.get('diskPlace')
        computer.videoCard = request.POST.get('videoCard')
        computer.typeDB = request.POST.get('typeDB')
        computer.lanCard = request.POST.get('lanCard')
        computer.monitor = request.POST.get('monitor')
        
        computer.windows = request.POST.get('windows')
        computer.addDevices = request.POST.get('addDevices')
        computer.addComment = request.POST.get('addComment')
        computer.date = request.POST.get('date')

        admin_ids = request.POST.getlist('admin')
        user_ids = request.POST.getlist('user')

        # Очищаем текущие связи
        computer.admin.clear()
        computer.user.clear()

        # Добавляем новые связи
        for admin_id in admin_ids:
            admin = UserName.objects.get(pk=admin_id)
            computer.admin.add(admin)

        for user_id in user_ids:
            user = UserName.objects.get(pk=user_id)
            computer.user.add(user)
       

        # Для связанных объектов обработка может быть сложнее, в зависимости от того, как у вас настроены модели.
        # Вы должны убедиться, что связанные объекты существуют или создать их.
        
        # Пример:
        # Если ваши связанные поля являются ForeignKey или ManyToManyField, нужно обрабатывать их отдельно.
        customer = request.POST.get('customer')
        if customer:
           computer.customer = get_object_or_404(Customer, pk=customer)

        employee = request.POST.get('employee')
        if employee:
           computer.employee = get_object_or_404(Employee, pk=employee)

        location_name = request.POST.get('Location')
        if location_name:
            location, created = Location.objects.get_or_create(name=location_name, computer=computer)
            computer.locations.clear()
            computer.locations.add(location)
        
        # Сохранение изменений
        computer.save()
        return JsonResponse({'message': 'Success'})

    else:
        admins = UserName.objects.filter(user_type='Admin')
        users = UserName.objects.filter(user_type='User')
        # Обработка GET-запроса для отображения формы редактирования
        context = {
            'computer': computer,
            'customers': Customer.objects.all(),
            'employees': Employee.objects.all(),
            'locations': Location.objects.all(),
            'type_choices': [choice[0] for choice in Computer.TYPE_CHOICES],
            'admin_list': UserName.objects.filter(user_type='Admin'),  # Исправлено на admin_list
            'user_list': UserName.objects.filter(user_type='User'),     # Исправлено на user_list
            'user_types': [user_type.user_type for user_type in UserName.objects.all()],
            
            
            # Добавьте в контекст все необходимые данные для формы
        }
        return render(request, 'home/computer_edit.html', context)

    return JsonResponse({'error': 'Invalid request'}, status=400)



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

   







