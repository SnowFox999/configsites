from django.db import models
from datetime import date
from django.core.exceptions import ValidationError




class Customer(models.Model):
    name = models.CharField(max_length=100) #name customer

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Computer(models.Model):
    STATUS_CHOICES = [
        ('Progress', 'In Progress'),
        ('Ready', 'Ready'),
        ('Confirm', 'Confirm'),
    ]

    TYPE_CHOICES = [
        ('Fujitsu ESPRIMO P5011', 'Fujitsu ESPRIMO P5011'),
        ('Fujitsu ESPRIMO G9013 ESTAR', 'Fujitsu ESPRIMO G9013 ESTAR'),
        ('Fujitsu ESPRIMO P558/E85+', 'Fujitsu ESPRIMO P558/E85+'),
        ('Fujitsu ESPRIMO P557', 'Fujitsu ESPRIMO P557'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='computers', blank=True) #connect to customer
    name = models.CharField(max_length=20, blank=True) # name of computer
    serial_number = models.CharField(max_length=30, unique=True, blank=True) #serial numer
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, blank=True, null=True)
    custom_type = models.CharField(max_length=30, blank=True, null=True)

    processor = models.ManyToManyField('Processor', blank=True) #many processors to many computers
    ram = models.ManyToManyField('RAM', blank=True) # many to many RAM
    hardDisk = models.ManyToManyField('HardDisk', blank=True) # many to many HardDisk
    diskPlace = models.ManyToManyField('DiskPlace', blank=True) # many to many CD/DVD
    videoCard = models.ManyToManyField('VideoCard', blank=True) # many to many graphics card
    typeDB = models.ManyToManyField('TypeDB', blank=True) #type of data base
    lanCard = models.ManyToManyField('LANcard', blank=True) # netzwerkkarte
    monitor = models.ManyToManyField('Monitor', blank=True) #Monitor
    
    user = models.ManyToManyField('UserName', blank=True)
    
    date = models.DateField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='computer', null=True, blank=True)
    addSoftware = models.TextField(null=True, blank=True)
    addDevices = models.TextField(null=True, blank=True)
    addComment = models.TextField(null=True, blank=True)
    addSettings = models.ManyToManyField('AdditionalSettings', blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Progress')
    
    


    def __str__(self):
        return f'{self.name} - {self.customer.name}'
    
class Processor(models.Model):
    name = models.CharField(max_length=20) #name of processor

    def __str__(self):
        return self.name
    
class RAM(models.Model):
    GIGABYTES_TYPES = [
        ('16', '16'),
        ('32', '32'),
        ('64', '64'),
        ('128', '128'),
        
    ]
    RAM_TYPES = [
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        
    ]
    gigabytes = models.PositiveSmallIntegerField(choices=GIGABYTES_TYPES) #gigabytes of RAM
    type = models.CharField(max_length=10, choices=RAM_TYPES) #type of RAM (DDR4, DDR3)

    def __str__(self):
        return f'{self.gigabytes} GB {self.type}'
    
class HardDisk(models.Model):
    GIGABYTES_TYPES = [
        ('128', '128'),
        ('256', '256'),
        ('512', '512'),
        ('1024', '1024'),
        
    ]
    DISK_TYPES = [
        ('SSD', 'SSD'),
        ('HDD', 'HDD'),
        
    ]
    gigabytes = models.PositiveSmallIntegerField(choices=GIGABYTES_TYPES) #gigabytes of disk
    type = models.CharField(max_length=10, choices=DISK_TYPES) #type of disk (SSD,HDD)

    def __str__(self):
        return f'{self.gigabytes} GB {self.type}'
    
class DiskPlace(models.Model):
    name = models.CharField(max_length=10, blank=True) #CD/DVD

    def __str__(self):
        return self.name

class VideoCard(models.Model):
    name = models.CharField(max_length=50) # graphics card

    def __str__(self):
        return self.name
    
class TypeDB(models.Model):
    DATABASE_TYPES = [
        ('Access', 'Access'),
        ('SQL', 'SQL'),
    ]
    type = models.CharField(max_length=10, choices=DATABASE_TYPES) #type of Data Base
    version = models.CharField(max_length=10) #version of DB

    def __str__(self):
        return f'{self.get_type_display()} {self.version}'
    
class LANcard(models.Model): 
    type = models.CharField(max_length=30) #lan card
    series = models.CharField(max_length=30)

    def __str__(self):
        return self.type

class Location(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, related_name='locations') #location Buro, Anlage..
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name} - {self.computer.name}'
    
class Monitor(models.Model):
    MONITOR_CHOICES = [
        ('Monitor1', 'Monitor1'),
        ('Monitor2', 'Monitor2'),
    ]

    name = models.CharField(max_length=30, choices=MONITOR_CHOICES, blank=True)
    custom_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        if self.custom_name:
            return self.custom_name
        return self.get_name_display()
    

class UserName(models.Model):
    USER_TYPES = [
    ('Admin', 'Admin'),
    ('User', 'User'),
]

    user_type = models.CharField(max_length=5, choices=USER_TYPES)
    login = models.CharField(max_length=20, unique=False,)
    password = models.CharField(max_length=20, unique=False)

    def __str__(self):
        return f'{self.login} - {self.password}'
    
class AdditionalSettings(models.Model):
    name = models.CharField(max_length=30)
    text = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name} - {self.text}'
    
class Windows(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, related_name='windowses')
    name = models.CharField(max_length=30)
    licenseNumber = models.CharField(max_length=60)
    licenseKeys = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name} - {self.licenseNumber} - {self.licenseKeys}'
    


class Order_Computer(models.Model):
    
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    text = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.computer.customer.name} ({self.computer.name} - {self.computer.status})"
    


