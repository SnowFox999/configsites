
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Computer, Order_Computer, Customer, Location, UserName, Employee, Processor, VideoCard, LANcard, RAM, HardDisk, Windows, TypeDB, Monitor, DiskPlace, AdditionalSettings
from django.db.models import Q
import json
from .forms import ComputerForm
from datetime import datetime


# Create your views here.


def index(request):
    # Page from the theme 
    return render(request, 'pages/index.html')

def computer_detail(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)
    customers = Customer.objects.all()
    employees = Employee.objects.all()
    locations = computer.locations.values('name')
    windowses = computer.windowses.values('name', 'licenseNumber', 'licenseKeys')

    
    users = list(computer.user.values('user_type', 'login', 'password', 'id'))
    print(users)
    processors = list(computer.processor.values('name'))
    videoCards = list(computer.videoCard.values('name'))
    lanCards = list(computer.lanCard.values('type', 'series'))
    rams = list(computer.ram.values('type', 'gigabytes'))
    hardDisks = list(computer.hardDisk.values('type', 'gigabytes'))
  
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
            
            'user': users,
            'windows': windowses,
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
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            form.save()

            # Обработка POST-запроса для сохранения изменений
            computer.name = request.POST.get('name')
            computer.status = request.POST.get('status')
            computer.serial_number = request.POST.get('serial_number')
            computer.type = request.POST.get('type') if not request.POST.get('custom_type') else None
            computer.custom_type = request.POST.get('custom_type')
            
            
            computer.hardDisk = request.POST.get('hardDisk')
            computer.diskPlace = request.POST.get('diskPlace')
            
            
            
            
            
            
            computer.addDevices = request.POST.get('addDevices')
            computer.addComment = request.POST.get('addComment')
            computer.date = request.POST.get('date')

        
            

            
        

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

            user = request.POST.get('user')
            if user:
                # Assuming `user` is a ManyToManyField or ForeignKey, handle it appropriately
                computer.user.clear()
                user_ids = user.split(',')  # Assuming user ids are sent as a comma-separated string
                for user_id in user_ids:
                    user_instance = get_object_or_404(UserName, pk=user_id)
                    computer.user.add(user_instance)


            processors = request.POST.getlist('processor')
            if processors:
                computer.processor.clear()
                for processor in processors:
                    processor_instance = get_object_or_404(Processor, pk=processor)
                    computer.processor.add(processor_instance)

            videoCards = request.POST.getlist('videoCard')
            if videoCards:
                computer.videoCard.clear()
                for videoCard in videoCards:
                    videoCard_instance = get_object_or_404(VideoCard, pk=videoCard)
                    computer.videoCard.add(videoCard_instance)

            lanCards = request.POST.getlist('lanCard')
            if videoCards:
                computer.lanCard.clear()
                for lanCard in lanCards:
                    lanCard_instance = get_object_or_404(LANcard, pk=lanCard)
                    computer.lanCard.add(lanCard_instance)

            rams = request.POST.get('ram')
            if rams:
                computer.ram.clear()
                for ram in rams:
                    ram_instance = get_object_or_404(RAM, pk=ram)
                    computer.ram.add(ram_instance)
        

            hardDisks = request.POST.get('hardDisk')
            if hardDisks:
                computer.hardDisk.clear()
                for hardDisk in hardDisks:
                    hardDisk_instance = get_object_or_404(HardDisk, pk=hardDisk)
                    computer.hardDisk.add(hardDisk_instance)

            user = request.POST.get('user')
            if user:
                # Assuming `user` is a ManyToManyField or ForeignKey, handle it appropriately
                computer.user.clear()
                user_ids = user.split(',')  # Assuming user ids are sent as a comma-separated string
                for user_id in user_ids:
                    user_instance = get_object_or_404(UserName, pk=user_id)
                    computer.user.add(user_instance)

            windowses = request.POST.getlist('windows')
            if windowses:
                computer.windows.clear()
                for windows in windowses:
                    windows_instance = get_object_or_404(Windows, pk=windows)
                    computer.windows.add(windows_instance)

            typeDBs = request.POST.get('typeDB')
            if typeDBs:
                computer.typeDB.clear()
                for typeDB in typeDBs:
                    typeDB_instance = get_object_or_404(TypeDB, pk=typeDB)
                    computer.typeDB.add(typeDB_instance)


            monitors = request.POST.get('monitor')
            if monitors:
                computer.monitor.clear()
                for monitor in monitors:
                    monitor_instance = get_object_or_404(Monitor, pk=monitor)
                    computer.monitor.add(monitor_instance)
            

            addSettings = request.POST.get('addSetting')
            if addSettings:
                computer.addSetting.clear()
                for addSetting in addSettings:
                    addSetting_instance = get_object_or_404(AdditionalSettings, pk=addSetting)
                    computer.addSetting.add(addSetting_instance)

            computer.save()
            return JsonResponse({'message': 'Success'})
        else:

        
            return JsonResponse({'errors': form.errors}, status=400)

    else:
        
        form = ComputerForm(instance=computer)
        context = {
            'computer': computer,
            'form': form,
            'customers': Customer.objects.filter(id=computer.customer.id),
            'employees': Employee.objects.filter(id=computer.employee.id),
            'locations': Location.objects.filter(computer=computer),
            'type_choices': Computer.TYPE_CHOICES,
          
            'users': UserName.objects.filter(computer=computer),
            'processors': Processor.objects.filter(computer=computer),
            'videoCards': VideoCard.objects.filter(computer=computer),
            'lanCards': LANcard.objects.filter(computer=computer),
            'rams': RAM.objects.filter(computer=computer),
            'hardDisks': HardDisk.objects.filter(computer=computer),
            'windowses': Windows.objects.filter(computer=computer),
            'typeDBs': TypeDB.objects.all(),
            'monitors': Monitor.objects.all(),
            'diskPlaces': DiskPlace.objects.filter(computer=computer),
            'addSettings': AdditionalSettings.objects.filter(computer=computer),
            
        }
       

        return render(request, 'home/computer_edit.html', context)
    

    return JsonResponse({'error': 'Invalid request'}, status=400)




def edit(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)
    customer_queryset = Customer.objects.filter(name=computer.customer.name)
    employee_queryset = Employee.objects.filter(name=computer.employee.name)
    
    if request.method == 'POST':
        form = ComputerForm(request.POST, request.FILES, instance=computer, customer_queryset=customer_queryset, employee_queryset=employee_queryset)
        if form.is_valid():
            computer = form.save(commit=False)
            computer.date = form.cleaned_data.get('date') or computer.date

            status = request.POST.get('status')
            if status in ['Progress', 'Ready', 'Confirm']:
                computer.status = status

            # Обработка поля location_name
            location_name = form.cleaned_data.get('location_name')
            if location_name:
                location, created = Location.objects.get_or_create(name=location_name, computer=computer)
                computer.locations.clear()
                computer.locations.add(location)

            processor_name = form.cleaned_data.get('processor_name')
            if processor_name:
                processor, created = Processor.objects.get_or_create(name=processor_name, computer=computer)
                computer.processor.clear()
                computer.processor.add(processor)

            videoCard_name = form.cleaned_data.get('videoCard_name')
            if videoCard_name:
                videoCard, created = VideoCard.objects.get_or_create(name=videoCard_name, computer=computer)
                computer.videoCard.clear()
                computer.videoCard.add(videoCard)

            lanCard_type = form.cleaned_data.get('lanCard_type')
            lanCard_series = form.cleaned_data.get('lanCard_series')
            if lanCard_type and lanCard_series:
                lanCard, created = LANcard.objects.get_or_create(type=lanCard_type, series=lanCard_series, computer=computer)
                computer.lanCard.clear()
                computer.lanCard.add(lanCard)

            ram_type = form.cleaned_data.get('ram_type')
            ram_gigabytes = form.cleaned_data.get('ram_gigabytes')
            if ram_type and ram_gigabytes:
                ram, created = RAM.objects.get_or_create(type=ram_type, gigabytes=ram_gigabytes, computer=computer)
                computer.ram.clear()
                computer.ram.add(ram)

            hardDisk_type = request.POST.get('hardDisk_type')
            hardDisk_gigabytes = request.POST.get('hardDisk_gigabytes')
            if hardDisk_type and hardDisk_gigabytes:
                hardDisk, created = HardDisk.objects.get_or_create(type=hardDisk_type, gigabytes=hardDisk_gigabytes)
                computer.hardDisk.clear()
                computer.hardDisk.add(hardDisk)

            windows_name = request.POST.get('windows_name')
            windows_licenseNumber = request.POST.get('windows_licenseNumber')
            windows_licenseKeys = request.POST.get('windows_licenseKeys')
            if windows_name and windows_licenseNumber and windows_licenseKeys:
                windowses, created = Windows.objects.get_or_create(name=windows_name, licenseNumber=windows_licenseNumber, licenseKeys=windows_licenseKeys)
                computer.windowses.clear()
                computer.windowses.add(windowses)

            typeDB_type = request.POST.get('typeDB_type')
            typeDB_version = request.POST.get('typeDB_version')
            if typeDB_type and typeDB_version:
                typeDB, created = TypeDB.objects.get_or_create(type=typeDB_type, version=typeDB_version)
                computer.typeDB.clear()
                computer.typeDB.add(typeDB)

            computer.addComment = form.cleaned_data.get('addComment_value')
            computer.addDevices = form.cleaned_data.get('addDevices_value')
            computer.addSoftware = form.cleaned_data.get('addSoftware_value')

            monitor_name = form.cleaned_data.get('monitor_name')
            if monitor_name:
                monitor, created = Monitor.objects.get_or_create(name=monitor_name)
                computer.monitor.clear()
                computer.monitor.add(monitor)

            diskPlace_name = form.cleaned_data.get('diskPlace_name')
            if diskPlace_name:
                diskPlace, created = DiskPlace.objects.get_or_create(name=diskPlace_name)
                computer.monitor.clear()
                computer.monitor.add(diskPlace)

            addSettings_name = request.POST.get('addSettings_name')
            addSettings_text = request.POST.get('addSettings_text')
            if addSettings_name and addSettings_text:
                addSettings, created = AdditionalSettings.objects.get_or_create(name=addSettings_name, text=addSettings_text)
                computer.addSettings.clear()
                computer.addSettings.add(addSettings)

            for user in UserName.objects.filter(computer=computer):
                user_type = request.POST.get(f'user_type_{user.pk}')
                user_name = request.POST.get(f'user_name_{user.pk}')
                user_password = request.POST.get(f'password_{user.pk}')
                if user_type:
                    user.user_type = user_type
                if user_name:
                    user.login = user_name
                if user_password:
                    user.password = user_password
                user.save()

            computer.save()
            form.save_m2m()  # Сохранение ManyToMany полей
            return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = ComputerForm(instance=computer, customer_queryset=customer_queryset)
        form.fields['location_name'].initial = ', '.join(
            [location.name for location in computer.locations.all()]
        )

    context = {
        'form': form,
        'customer_queryset': customer_queryset,
        'location_queryset': computer.locations.all(),
        'type_choices': Computer.objects.values_list('type', flat=True).distinct(),
        'computer': computer,
        'user_types': [choice[0] for choice in UserName.USER_TYPES],
        'users': UserName.objects.filter(computer=computer),
        'processor': computer.processor.all(),
        'processor_queryset': computer.processor.all(),
        'videoCard': computer.videoCard.all(),
        'videoCard_queryset': computer.videoCard.all(),
        'lanCard_queryset': computer.lanCard.all(),
        'ram_queryset': computer.ram.all(),
        'hardDisk_queryset': computer.hardDisk.all(),
        'windows_queryset': computer.windowses.all(),
        'typeDB_queryset': computer.typeDB.all(),
        'monitor_queryset': computer.monitor.all(),
        'diskPlace_queryset': computer.diskPlace.all(),
        'addSettings_queryset': computer.addSettings.all(),
        'employee_queryset': employee_queryset,
    }
    return render(request, 'home/edit.html', context)




def update_computer_status(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)
    new_status = request.POST.get('status')

    valid_transitions = {
        'Progress': ['Ready'],
        'Ready': ['Confirm'],
        'Confirm': []
    }

    if new_status in valid_transitions[computer.status]:
        computer.status = new_status
        computer.save()
        return JsonResponse({'success': True, 'status': new_status})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid status transition'}, status=400)







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

   







