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
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='computers') #connect to customer
    name = models.CharField(max_length=20) # name of computer
    serial_number = models.CharField(max_length=30, unique=True) #serial numer
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, blank=True, null=True)
    custom_type = models.CharField(max_length=30, blank=True, null=True)

    def clean(self):
        super().clean()
        if not self.type and not self.custom_type:
            raise ValidationError("Either 'type' or 'custom_type' must be filled.")

   

    processor = models.ManyToManyField('Processor') #many processors to many computers
    ram = models.ManyToManyField('RAM') # many to many RAM
    hardDisk = models.ManyToManyField('HardDisk') # many to many HardDisk
    diskPlace = models.ManyToManyField('DiskPlace', blank=True) # many to many CD/DVD
    videoCard = models.ManyToManyField('VideoCard') # many to many graphics card
    typeDB = models.ManyToManyField('TypeDB') #type of data base
    lanCard = models.ManyToManyField('LANcard') # netzwerkkarte
    monitor = models.ManyToManyField('Monitor', blank=True) #Monitor
    admin = models.ManyToManyField('UserName', related_name='admin_computers', limit_choices_to={'user_type': 'Admin'})
    user = models.ManyToManyField('UserName', related_name='user_computers', limit_choices_to={'user_type': 'User'}, blank=True)
    
    date = models.DateField(default=date.today)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_name='computer', null=True)
    addSoftware = models.TextField(null=True, blank=True)
    addDevices = models.TextField(null=True, blank=True)
    addComment = models.TextField(null=True, blank=True)
    addSettings = models.ManyToManyField('AdditionalSettings', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    windows = models.ManyToManyField('Windows', blank = False)
    


    def __str__(self):
        return f'{self.name} - {self.customer.name}'
    
class Processor(models.Model):
    name = models.CharField(max_length=20) #name of processor

    def __str__(self):
        return self.name
    
class RAM(models.Model):
    gigabytes = models.PositiveSmallIntegerField() #gigabytes of RAM
    type = models.CharField(max_length=10) #type of RAM (DDR4, DDR3)

    def __str__(self):
        return f'{self.gigabytes} GB {self.type}'
    
class HardDisk(models.Model):
    gigabytes = models.PositiveSmallIntegerField() #gigabytes of disk
    type = models.CharField(max_length=10) #type of disk (SSD,HDD)

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

    user_type = models.CharField(max_length=5, choices=USER_TYPES, default='Admin')
    login = models.CharField(max_length=20, unique=False, default='Administrator')
    password = models.CharField(max_length=20, unique=False, default='icom')

    def __str__(self):
        return f'{self.get_user_type_display()} - {self.login} - {self.password}'
    
class AdditionalSettings(models.Model):
    name = models.CharField(max_length=30)
    text = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name} - {self.text}'
    
class Windows(models.Model):
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
    


# Create your models here.
