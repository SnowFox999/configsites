from django import forms
from .models import Customer, Employee, Computer, Processor, RAM, HardDisk, DiskPlace, VideoCard, TypeDB, LANcard, Location, Monitor, UserName, AdditionalSettings, Windows, Order_Computer

class ComputerForm(forms.ModelForm):
    customer_name = forms.CharField(max_length=255, required=True)
    location_name = forms.CharField(max_length=30, required=True)
    computer_type = forms.CharField(max_length=100, required=True)
    processor_name = forms.CharField(max_length=100, required=True)
    videoCard_name = forms.CharField(max_length=100, required=True)
    lanCard_name = forms.CharField(max_length=100, required=True)
    lanCard_series = forms.CharField(max_length=100, required=True)
    ram_type = forms.CharField(max_length=100, required=True)
    ram_gigabytes = forms.CharField(max_length=4, required=True)
    hardDisk_type = forms.CharField(max_length=100, required=True)
    hardDisk_gigabytes = forms.CharField(max_length=4, required=True)
    windows_name = forms.CharField(max_length=20, required=True)
    windows_licenseNumber = forms.CharField(max_length=50, required=True)
    windows_licenseKeys = forms.CharField(max_length=50, required=True)
    typeDB_type = forms.CharField(max_length=20, required=True)
    typeDB_version = forms.CharField(max_length=20, required=True)
    addComment_value = forms.CharField(max_length=255, required= False)
    addDevices_value = forms.CharField(max_length=255, required=False)
    addSoftware_value = forms.CharField(max_length=255, required=False)
    monitor_name = forms.CharField(max_length=100, required=True)
    diskPlace_name = forms.CharField(max_length=100, required=True)
   
    

    class Meta:
        model = Computer
        fields = [
            'customer', 'name', 'serial_number', 'type', 'custom_type', 'status',
            'processor', 'ram', 'hardDisk', 'diskPlace', 'videoCard', 'typeDB', 
            'lanCard', 'monitor', 'user', 'date', 'employee', 'addSoftware', 
            'addDevices', 'addComment', 'addSettings'
        ]
        widgets = {
            'processor': forms.CheckboxSelectMultiple(),
            'ram': forms.CheckboxSelectMultiple(),
            'hardDisk': forms.CheckboxSelectMultiple(),
            'diskPlace': forms.CheckboxSelectMultiple(),
            'videoCard': forms.CheckboxSelectMultiple(),
            'typeDB': forms.CheckboxSelectMultiple(),
            'lanCard': forms.CheckboxSelectMultiple(),
            'monitor': forms.CheckboxSelectMultiple(),
            'user': forms.CheckboxSelectMultiple(),
            'addSettings': forms.CheckboxSelectMultiple(),
            
        }

    def __init__(self, *args, **kwargs):
        customer_queryset = kwargs.pop('customer_queryset', Customer.objects.all())
        super().__init__(*args, **kwargs)
        
        # Устанавливаем начальное значение для поля customer_name
        if self.instance and self.instance.customer:
            self.fields['customer_name'].initial = self.instance.customer.name
        if self.instance and self.instance.locations.exists():
            self.fields['location_name'].initial = self.instance.locations.first().name
        if self.instance and self.instance.processor.exists():
            self.fields['processor_name'].initial = self.instance.processor.first().name
        if self.instance and self.instance.videoCard.exists():
            self.fields['videoCard_name'].initial = self.instance.videoCard.first().name
        if self.instance and self.instance.lanCard.exists():
            self.fields['lanCard_name'].initial = self.instance.lanCard.first().type
            self.fields['lanCard_series'].initial = self.instance.lanCard.first().series
        if self.instance and self.instance.ram.exists():
            self.fields['ram_type'].initial = self.instance.ram.first().type
            self.fields['ram_gigabytes'].initial = self.instance.ram.first().gigabytes
        if self.instance and self.instance.hardDisk.exists():
            self.fields['hardDisk_type'].initial = self.instance.hardDisk.first().type
            self.fields['hardDisk_gigabytes'].initial = self.instance.hardDisk.first().gigabytes
        if self.instance:
            self.fields['computer_type'].initial = self.instance.custom_type if self.instance.custom_type else self.instance.type
        if self.instance and self.instance.windowses.exists():
            self.fields['windows_name'].initial = self.instance.windowses.first().name
            self.fields['windows_licenseNumber'].initial = self.instance.windowses.first().licenseNumber
            self.fields['windows_licenseKeys'].initial = self.instance.windowses.first().licenseKeys
        if self.instance and self.instance.typeDB.exists():
            self.fields['typeDB_type'].initial = self.instance.typeDB.first().type
            self.fields['typeDB_version'].initial = self.instance.typeDB.first().version
        if self.instance and self.instance.addComment:
            self.fields['addComment_value'].initial = self.instance.addComment
        if self.instance and self.instance.addDevices:
            self.fields['addDevices_value'].initial = self.instance.addDevices
        if self.instance and self.instance.addSoftware:
            self.fields['addSoftware_value'].initial = self.instance.addSoftware
        if self.instance and self.instance.monitor.exists():
            monitor = self.instance.monitor.first()
            self.fields['monitor_name'].initial = monitor.custom_name if monitor.custom_name else monitor.name
        if self.instance and self.instance.diskPlace.exists():
            self.fields['diskPlace_name'].initial = self.instance.diskPlace.first().name



    


    def clean(self):
        cleaned_data = super().clean()
        computer_type = cleaned_data.get('computer_type')
        if computer_type:
            existing_types = [choice[0] for choice in Computer.objects.values_list('type', flat=True)]
            if computer_type not in existing_types:
                cleaned_data['custom_type'] = computer_type
                cleaned_data['type'] = None
            else:
                cleaned_data['type'] = computer_type
                cleaned_data['custom_type'] = None
        return cleaned_data