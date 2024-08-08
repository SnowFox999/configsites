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





class ComputerStep1Form(forms.ModelForm):
    class Meta:
        model = Computer
        fields = ['type', 'serial_number']

class CustomerEmployeeForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name']

class LocationDiskPlaceForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']

    class Meta:
        model = DiskPlace
        fields = ['name']