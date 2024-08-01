
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Computer, Order_Computer, Customer, Location, UserName, Employee, Processor, VideoCard, LANcard, RAM, HardDisk, Windows, TypeDB, Monitor, DiskPlace, AdditionalSettings
from django.db.models import Q
import json
from .forms import ComputerForm
from datetime import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.dateparse import parse_date


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
            'rams': RAM.objects.all(),
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
            computer.date = timezone.now()
            status = request.POST.get('status')
            if status in ['Progress', 'Ready', 'Confirm']:
                computer.status = status

            location_name = form.cleaned_data.get('location_name')
            if location_name:
                location, created = Location.objects.get_or_create(name=location_name, computer=computer)
                computer.locations.clear()
                computer.locations.add(location)

            processor_name = request.POST.get('processor_name')
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
                ram, created = RAM.objects.get_or_create(type=ram_type, gigabytes=ram_gigabytes)
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
        form = ComputerForm(instance=computer, customer_queryset=customer_queryset, employee_queryset=employee_queryset)


    
    # if request.method == 'POST':
    #     form = ComputerForm(request.POST, request.FILES, instance=computer, customer_queryset=customer_queryset, employee_queryset=employee_queryset)
    #     if form.is_valid():
    #         computer = form.save(commit=False)
    #         computer.date =  timezone.now()
    #         status = request.POST.get('status')
    #         if status in ['Progress', 'Ready', 'Confirm']:
    #             computer.status = status

            

    #         # Обработка поля location_name
    #         location_name = form.cleaned_data.get('location_name')
    #         if location_name:
    #             location, created = Location.objects.get_or_create(name=location_name, computer=computer)
    #             computer.locations.clear()
    #             computer.locations.add(location)

            
    #         processor_name = request.POST.get('processor_name')
    #         if processor_name:
    #             processor, created = Processor.objects.get_or_create(name=processor_name, computer=computer)
    #             computer.processor.clear()
    #             computer.processor.add(processor)

    #         videoCard_name = form.cleaned_data.get('videoCard_name')
    #         if videoCard_name:
    #             videoCard, created = VideoCard.objects.get_or_create(name=videoCard_name, computer=computer)
    #             computer.videoCard.clear()
    #             computer.videoCard.add(videoCard)

    #         lanCard_type = form.cleaned_data.get('lanCard_type')
    #         lanCard_series = form.cleaned_data.get('lanCard_series')
    #         if lanCard_type and lanCard_series:
    #             lanCard, created = LANcard.objects.get_or_create(type=lanCard_type, series=lanCard_series, computer=computer)
    #             computer.lanCard.clear()
    #             computer.lanCard.add(lanCard)

    #         ram_type = form.cleaned_data.get('ram_type')
    #         ram_gigabytes = form.cleaned_data.get('ram_gigabytes')
    #         if ram_type and ram_gigabytes:
    #             ram, created = RAM.objects.get_or_create(type=ram_type, gigabytes=ram_gigabytes, computer=computer)
    #             computer.ram.clear()
    #             computer.ram.add(ram)

    #         hardDisk_type = request.POST.get('hardDisk_type')
    #         hardDisk_gigabytes = request.POST.get('hardDisk_gigabytes')
    #         if hardDisk_type and hardDisk_gigabytes:
    #             hardDisk, created = HardDisk.objects.get_or_create(type=hardDisk_type, gigabytes=hardDisk_gigabytes)
    #             computer.hardDisk.clear()
    #             computer.hardDisk.add(hardDisk)

    #         windows_name = request.POST.get('windows_name')
    #         windows_licenseNumber = request.POST.get('windows_licenseNumber')
    #         windows_licenseKeys = request.POST.get('windows_licenseKeys')
    #         if windows_name and windows_licenseNumber and windows_licenseKeys:
    #             windowses, created = Windows.objects.get_or_create(name=windows_name, licenseNumber=windows_licenseNumber, licenseKeys=windows_licenseKeys)
    #             computer.windowses.clear()
    #             computer.windowses.add(windowses)

    #         typeDB_type = request.POST.get('typeDB_type')
    #         typeDB_version = request.POST.get('typeDB_version')
    #         if typeDB_type and typeDB_version:
    #             typeDB, created = TypeDB.objects.get_or_create(type=typeDB_type, version=typeDB_version)
    #             computer.typeDB.clear()
    #             computer.typeDB.add(typeDB)

    #         computer.addComment = form.cleaned_data.get('addComment_value')
    #         computer.addDevices = form.cleaned_data.get('addDevices_value')
    #         computer.addSoftware = form.cleaned_data.get('addSoftware_value')

    #         monitor_name = form.cleaned_data.get('monitor_name')
    #         if monitor_name:
    #             monitor, created = Monitor.objects.get_or_create(name=monitor_name)
    #             computer.monitor.clear()
    #             computer.monitor.add(monitor)

    #         diskPlace_name = form.cleaned_data.get('diskPlace_name')
    #         if diskPlace_name:
    #             diskPlace, created = DiskPlace.objects.get_or_create(name=diskPlace_name)
    #             computer.monitor.clear()
    #             computer.monitor.add(diskPlace)

    #         addSettings_name = request.POST.get('addSettings_name')
    #         addSettings_text = request.POST.get('addSettings_text')
    #         if addSettings_name and addSettings_text:
    #             addSettings, created = AdditionalSettings.objects.get_or_create(name=addSettings_name, text=addSettings_text)
    #             computer.addSettings.clear()
    #             computer.addSettings.add(addSettings)

    #         for user in UserName.objects.filter(computer=computer):
    #             user_type = request.POST.get(f'user_type_{user.pk}')
    #             user_name = request.POST.get(f'user_name_{user.pk}')
    #             user_password = request.POST.get(f'password_{user.pk}')
    #             if user_type:
    #                 user.user_type = user_type
    #             if user_name:
    #                 user.login = user_name
    #             if user_password:
    #                 user.password = user_password
    #             user.save()

    #         computer.save()
    #         form.save_m2m()  # Сохранение ManyToMany полей
    #         return JsonResponse({'message': 'Success'})
    #     else:
    #         return JsonResponse({'error': form.errors}, status=400)
    # else:
    #     form = ComputerForm(instance=computer, customer_queryset=customer_queryset)
        

    context = {
        'form': form,
        'customer_queryset': customer_queryset,
        'location_queryset': computer.locations.all(),
        'type_choices': [choice[0] for choice in Computer.TYPE_CHOICES],
        'computer': computer,
        'user_types': [choice[0] for choice in UserName.USER_TYPES],
        'users': UserName.objects.filter(computer=computer),
        'processor': computer.processor.all(),
        'processor_queryset': computer.processor.all(),
        'videoCard': computer.videoCard.all(),
        'videoCard_queryset': computer.videoCard.all(),
        'lanCard_queryset': computer.lanCard.all(),
        'ram_gigabytes': [choice[0] for choice in RAM.GIGABYTES_TYPES],
        'ram_types': [choice[0] for choice in RAM.RAM_TYPES],
        'hardDisk_gigabytes': [choice[0] for choice in HardDisk.GIGABYTES_TYPES],
        'hardDisk_types': [choice[0] for choice in HardDisk.DISK_TYPES],
        'windows_queryset': computer.windowses.all(),
        'typeDB_queryset': computer.typeDB.all(),
        'monitor_queryset': computer.monitor.all(),
        'diskPlace_queryset': computer.diskPlace.all(),
        'addSettings_queryset': computer.addSettings.all(),
        'employee_queryset': employee_queryset,
    }
    return render(request, 'home/edit.html', context)





@csrf_exempt  # 
def save_computer_data(request):
     
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')
        computer_id = request.POST.get('computer_id')

        # Отладочный вывод
        print("Received data:", field_name, field_value, computer_id)

        if not field_name or not field_value or not computer_id:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

        try:
            computer = Computer.objects.get(id=computer_id)
        except Computer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Computer not found'}, status=404)

        try:
            if field_name == 'ComputerType':
                if field_value in dict(Computer.TYPE_CHOICES):
                    computer.type = field_value
                    computer.custom_type = ''
                else:
                    computer.type = ''
                    computer.custom_type = field_value


            elif field_name == 'locations_name':
                existing_location = computer.locations.first()

                if existing_location:
                    existing_location.name = field_value
                    existing_location.save()
                else:
                    location = Location(name=field_value)
                    
                    location.save()
                    computer.locations.add(location)
                


            elif field_name == 'diskPlace':
                existing_diskPlace = computer.diskPlace.first()

                if existing_diskPlace:
                    existing_diskPlace.name = field_value
                    existing_diskPlace.save()
                else:
                    diskPlace = DiskPlace(name=field_value)
                    
                    diskPlace.save()
                    computer.diskPlace.add(location)

                


            elif field_name == 'addSettings_name' or field_name == 'addSettings_text':
                existing_add_settings = computer.addSettings.first()

                if existing_add_settings:
                    # Если запись существует, обновляем её
                    if field_name == 'addSettings_name':
                        existing_add_settings.name = field_value
                    elif field_name == 'addSettings_text':
                        existing_add_settings.text = field_value

                    existing_add_settings.save()
                else:
                    # Если записи нет, создаем новую
                    if field_name == 'addSettings_name':
                        addSettings = AdditionalSettings(name=field_value)
                    elif field_name == 'addSettings_text':
                        addSettings = AdditionalSettings(text=field_value)

                    addSettings.save()
                    computer.addSettings.add(addSettings)

            elif field_name == 'MonitorName':
                existing_monitor = computer.monitor.first()

                if existing_monitor:
                    existing_monitor.name = field_value
                    existing_monitor.save()
                else:
                    monitor = Monitor(name=field_value)
                    
                    monitor.save()
                    computer.monitor.add(monitor)

               


            elif field_name == 'windows_name' or field_name == 'windows_licenseNumber' or field_name == 'windows_licenseKeys':
                
                existing_windows = computer.windowses.first()
                if existing_windows:
                    # Если запись существует, обновляем её
                    if field_name == 'windows_name':
                        existing_windows.name = field_value
                    elif field_name == 'windows_licenseNumber':
                        existing_windows.licenseNumber = field_value
                    elif field_name == 'windows_licenseKeys':
                        existing_windows.licenseKeys = field_value

                    existing_windows.save()
                else:
                    # Если записи нет, создаем новую
                    if field_name == 'windows_name':
                        windows = Windows(name=field_value)
                    elif field_name == 'windows_licenseNumber':
                        windows = Windows(licenseNumber=field_value)
                    elif field_name == 'windows_licenseKeys':
                        windows = Windows(licenseKeys =field_value)

                    windows.save()
                    computer.windowses.add(windows)




            elif field_name == 'Processor':

                existing_processor = computer.processor.first()

                if existing_processor:
                    existing_processor.name = field_value
                    existing_processor.save()
                else:
                    processor = Processor(name=field_value)
                    
                    processor.save()
                    computer.processor.add(processor)
 

            elif field_name == 'ram_type' or field_name =='ram_gigabytes':

                existing_ram = computer.ram.first()

                if existing_ram:
                    # Если запись существует, обновляем её
                    if field_name == 'ram_type':
                        existing_ram.type = field_value
                    elif field_name == 'ram_gigabytes':
                        existing_ram.gigabytes = field_value

                    existing_ram.save()
                else:
                    # Если записи нет, создаем новую
                    if field_name == 'ram_type':
                        ram = RAM(type=field_value)
                    elif field_name == 'ram_gigabytes':
                        ram = RAM(gigabytes=field_value)

                    ram.save()
                    computer.ram.add(ram)



            elif field_name == 'disk_type' or field_name =='disk_gigabytes':

                existing_disk = computer.hardDisk.first()

                if existing_disk:
                    # Если запись существует, обновляем её
                    if field_name == 'disk_type':
                        existing_disk.type = field_value
                    elif field_name == 'disk_gigabytes':
                        existing_disk.gigabytes = field_value

                    existing_disk.save()
                else:
                    # Если записи нет, создаем новую
                    if field_name == 'disk_type':
                        hardDisk = HardDisk(type=field_value)
                    elif field_name == 'disk_gigabytes':
                        hardDisk = HardDisk(gigabytes=field_value)

                    hardDisk.save()
                    computer.hardDisk.add(hardDisk)

            elif field_name == 'videoCard':
                existing_videoCard = computer.videoCard.first()

                if existing_videoCard:
                    existing_videoCard.name = field_value
                    existing_videoCard.save()
                else:
                    videoCard = VideoCard(name=field_value)
                    
                    videoCard.save()
                    computer.videoCard.add(videoCard)
                                           

            elif field_name =='typeDB_Version' or field_name == 'typeDB_Type':

                existing_typeDB = computer.typeDB.first()
                print(field_name)
                if existing_typeDB:
                    # Если запись существует, обновляем её
                    if field_name == 'typeDB_Type':
                        existing_typeDB.type = field_value
                        print(existing_typeDB)
                    elif field_name == 'typeDB_Version':
                        existing_typeDB.version = field_value

                    existing_typeDB.save()
                else:
                    # Если записи нет, создаем новую
                    if field_name == 'typeDB_Type':
                        typeDB = TypeDB(type=field_value)
                    elif field_name == 'typeDB_Version':
                        typeDB = TypeDB(version=field_value)

                    typeDB.save()
                    computer.typeDB.add(typeDB)


                
            elif field_name == 'LANcard':
                
                lanCard, created = LANcard.objects.get_or_create(type=lanCard_parts[0], series=lanCard_parts[1])
                computer.lanCard.set([lanCard])
            elif field_name == 'date':
                try:
                    date_obj = parse_date(field_value)
                    if date_obj is None:
                        raise ValueError("Invalid date format")
                    computer.date = date_obj
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid date format. Use "YYYY-MM-DD".'}, status=400)




            else:
                if hasattr(computer, field_name):
                    setattr(computer, field_name, field_value)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid field name'}, status=400)

            computer.save()
            return JsonResponse({'status': 'success'})
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': f'Validation error: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



    # if request.method == 'POST':
    #     field_name = request.POST.get('field_name')
    #     field_value = request.POST.get('field_value')
    #     computer_id = request.POST.get('computer_id')

    #     print("Received data:", field_name, field_value, computer_id)

    #     if field_name and field_value and computer_id:
    #         try:
    #             computer = Computer.objects.get(id=computer_id)
    #             if field_name in [field.name for field in Computer._meta.get_fields()]:
    #                 # Обработка полей ManyToMany
    #                 if field_name in ['diskPlace', 'addSettings']:  # Замените на ваши поля ManyToMany
    #                     if field_name == 'diskPlace':
    #                         diskPlace, created = DiskPlace.objects.get_or_create(name=field_value)
    #                         computer.diskPlace.set([diskPlace])
    #                     elif field_name == 'addSettings':
    #                         addSettings, created = AdditionalSettings.objects.get_or_create(name=field_value)
    #                         computer.addSettings.set([addSettings])
    #                 else:
    #                     # Обработка обычных полей
    #                     setattr(computer, field_name, field_value)
    #                 computer.save()
    #                 return JsonResponse({'status': 'success'})
    #             else:
    #                 return JsonResponse({'status': 'error', 'message': 'Invalid field name'}, status=400)
    #         except Computer.DoesNotExist:
    #             return JsonResponse({'status': 'error', 'message': 'Computer not found'}, status=400)
        
    #     return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    # else:
    #     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)













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

   







