from django import forms
from .models import Customer, Employee, Computer, Processor, RAM, HardDisk, DiskPlace, VideoCard, TypeDB, LANcard, Location, Monitor, UserName, AdditionalSettings, Windows, Order_Computer




class ComputerForm(forms.ModelForm):
    customer_name = forms.ChoiceField(required=False)
    location_name = forms.ChoiceField(required=False)
    computer_type = forms.CharField(required=False)
    processor_name = forms.MultipleChoiceField(required=False)
    videoCard_name = forms.MultipleChoiceField(required=False)
    lanCard_type = forms.MultipleChoiceField(required=False)
    lanCard_series = forms.MultipleChoiceField(required=False)
    ram_type = forms.ChoiceField(required=False)
    ram_gigabytes = forms.ChoiceField(required=False)
    hardDisk_type = forms.MultipleChoiceField(required=False)
    hardDisk_gigabytes = forms.MultipleChoiceField(required=False)
    windows_name = forms.ChoiceField(required=False)
    windows_licenseNumber = forms.ChoiceField(required=False)
    windows_licenseKeys = forms.ChoiceField(required=False)
    typeDB_type = forms.MultipleChoiceField(required=False)
    typeDB_version = forms.MultipleChoiceField(required=False)
    addComment_value = forms.CharField(required= False)
    addDevices_value = forms.CharField(required=False)
    addSoftware_value = forms.CharField(required=False)
    monitor_name = forms.MultipleChoiceField(required=False)
    diskPlace_name = forms.MultipleChoiceField(required=False)
    addSettings_name = forms.MultipleChoiceField(required=False)
    addSettings_text = forms.MultipleChoiceField(required=False)
    date = forms.DateField(
        required=False, 
        input_formats=['%b/%d/%Y'], 
        )
    employee_name = forms.ChoiceField(required=False)
    
   
    

    class Meta:
        model = Computer
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        customer_queryset = kwargs.pop('customer_queryset', Customer.objects.all())
        employee_queryset = kwargs.pop('employee_queryset', Employee.objects.all())
        super().__init__(*args, **kwargs)


        self.fields['customer_name'].choices = [(customer.id, customer.name) for customer in customer_queryset]
        self.fields['employee_name'].choices = [(employee.id, employee.name) for employee in employee_queryset]

        # Установка начальных значений для полей
        self._set_initial_values()

       
    def _set_initial_values(self):
            if self.instance:
                if self.instance.customer:
                    self.fields['customer_name'].initial = self.instance.customer.name
            
                if self.instance.locations.exists():
                    self.fields['location_name'].initial = self.instance.locations.first().name
                
                if self.instance.processor.exists():
                    self.fields['processor_name'].initial = self.instance.processor.first().name
                    
                
                if self.instance.videoCard.exists():
                    self.fields['videoCard_name'].initial = self.instance.videoCard.first().name
                
                if self.instance.lanCard.exists():
                    self.fields['lanCard_type'].initial = self.instance.lanCard.first().type
                    self.fields['lanCard_series'].initial = self.instance.lanCard.first().series
                
                if self.instance.ram.exists():
                    ram = self.instance.ram.first()
                    self.fields['ram_type'].initial = ram.type
                    self.fields['ram_gigabytes'].initial = ram.gigabytes
                
                if self.instance.hardDisk.exists():
                    self.fields['hardDisk_type'].initial = self.instance.hardDisk.first().type
                    self.fields['hardDisk_gigabytes'].initial = self.instance.hardDisk.first().gigabytes
                
                if self.instance.custom_type:
                    self.fields['computer_type'].initial = self.instance.custom_type
                else:
                    self.fields['computer_type'].initial = self.instance.type
                
                if self.instance.windowses.exists():
                    self.fields['windows_name'].initial = self.instance.windowses.first().name
                    self.fields['windows_licenseNumber'].initial = self.instance.windowses.first().licenseNumber
                    self.fields['windows_licenseKeys'].initial = self.instance.windowses.first().licenseKeys
                
                if self.instance.typeDB.exists():
                    self.fields['typeDB_type'].initial = self.instance.typeDB.first().type
                    self.fields['typeDB_version'].initial = self.instance.typeDB.first().version
                
                if self.instance.addComment:
                    self.fields['addComment_value'].initial = self.instance.addComment
                
                if self.instance.addDevices:
                    self.fields['addDevices_value'].initial = self.instance.addDevices
                
                if self.instance.addSoftware:
                    self.fields['addSoftware_value'].initial = self.instance.addSoftware
                
                if self.instance.monitor.exists():
                    monitor = self.instance.monitor.first()
                    self.fields['monitor_name'].initial = monitor.custom_name if monitor.custom_name else monitor.name
                
                if self.instance.diskPlace.exists():
                    self.fields['diskPlace_name'].initial = self.instance.diskPlace.first().name
                
                if self.instance.addSettings.exists():
                    addSettings = self.instance.addSettings.first()
                    self.fields['addSettings_name'].initial = addSettings.name
                    self.fields['addSettings_text'].initial = addSettings.text
                
                if self.instance.date:
                    self.fields['date'].initial = self.instance.date
                
                if self.instance.employee:
                    self.fields['employee_name'].initial = self.instance.employee.name


    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date:
            return date
        return None
    
    def clean(self):
        cleaned_data = super().clean()
        computer_type = cleaned_data.get('computer_type')


        # Логика обработки полей `type` и `custom_type`
        if computer_type:
            existing_types = [choice[0] for choice in Computer.objects.values_list('type', flat=True)]
            if computer_type not in existing_types:
                cleaned_data['custom_type'] = computer_type
                cleaned_data['type'] = None
            else:
                cleaned_data['type'] = computer_type
                cleaned_data['custom_type'] = None

        ram_type = cleaned_data.get('ram_type')
        if ram_type and len(ram_type) > 100:
            self.add_error('ram_type', 'The RAM type is too long.')

        return cleaned_data





class FirstForm(forms.Form):
    customer_name = forms.CharField()

    # Поля из Location модели
    location_name = forms.CharField()

    # Поля из Computer модели
    computer_type = forms.ChoiceField(choices=Computer.TYPE_CHOICES, required=False)

    

    def __init__(self, *args, **kwargs):
        # Извлечение дополнительных аргументов из kwargs
        self.customer_queryset = kwargs.pop('customer_queryset', None)
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        print(f"Cleaned data on step 1: {cleaned_data}")

        computer_type = cleaned_data.get('computer_type')
        
        customer_name = cleaned_data.get('customer_name')
        location_name = cleaned_data.get('location_name')

        if not computer_type:
            raise forms.ValidationError("You must choose an existing type")
        if not customer_name:
            raise forms.ValidationError("Customer name cannot be empty.")
        if not location_name:
            raise forms.ValidationError("Location name cannot be empty.")

        return cleaned_data



class MainInformationForm(forms.Form):

    computer_name = forms.CharField()
    computer_series = forms.CharField()
    computer_comment = forms.CharField()

    user_type = forms.ChoiceField(choices=UserName.USER_TYPES, required=False)
    user_name = forms.CharField()
    user_password = forms.CharField()
    

    def clean(self):
        cleaned_data = super().clean()
        print(f"Cleaned data on step 2: {cleaned_data}")

        user_name = cleaned_data.get('user_name')
        user_password = cleaned_data.get('user_password')
        user_type = cleaned_data.get('user_type')

        computer_name = cleaned_data.get('computer_name')
        computer_series = cleaned_data.get('computer_series')
        computer_comment = cleaned_data.get('computer_comment')

        if not computer_name:
            raise forms.ValidationError('Computer name must be filled')
        
        if not computer_series:
            raise forms.ValidationError('Computer series must be filled')


        # Проверка, что имя пользователя и пароль заполнены
        if not user_name or not user_password or not user_type:
            raise forms.ValidationError("User name and password must be provided.")
  
        return cleaned_data
    


class ComputerHardwareForm(forms.Form):

    processor_name = forms.CharField()
    videoCard_name = forms.CharField()

    ram_gigabytes = forms.ChoiceField(choices=RAM.GIGABYTES_TYPES, required=False)
    ram_types = forms.ChoiceField(choices=RAM.RAM_TYPES, required=False)

    hardDisk_gigabytes = forms.ChoiceField(choices=HardDisk.GIGABYTES_TYPES, required=False)
    hardDisk_types = forms.ChoiceField(choices=HardDisk.DISK_TYPES, required=False)

    lanCard_type = forms.CharField()
    lanCard_series = forms.CharField()

    def __init__(self, *args, **kwargs):
        # Извлечение дополнительных аргументов из kwargs
        self.processor_queryset = kwargs.pop('processor_queryset', None)
        self.videoCard_queryset = kwargs.pop('videoCard_queryset', None)
        self.lanCard_queryset = kwargs.pop('lanCard_queryset', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        print(f"Cleaned data on step 3: {cleaned_data}")

        processor_name = cleaned_data.get('processor_name')
        videoCard_name = cleaned_data.get('videoCard_name')

        ram_gigabytes = cleaned_data.get('ram_gigabytes')
        ram_types = cleaned_data.get('ram_types')

        hardDisk_gigabytes = cleaned_data.get('hardDisk_gigabytes')
        hardDisk_types = cleaned_data.get('hardDisk_types')

        

        lanCard_type = cleaned_data.get('lanCard_type')
        lanCard_series = cleaned_data.get('lanCard_series')

        if not processor_name:
            raise forms.ValidationError('Processor must be filled')
        if not videoCard_name:
            raise forms.ValidationError('Video card must be filled')

        
        return cleaned_data