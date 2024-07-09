from django.contrib import admin
from .models import Computer, Employee, Customer, Processor, RAM, DiskPlace, HardDisk, VideoCard, TypeDB, LANcard, Location, Monitor, UserName, AdditionalSettings, Order_Computer

admin.site.register(Computer)
admin.site.register(Order_Computer)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Processor)
admin.site.register(RAM)
admin.site.register(DiskPlace)
admin.site.register(HardDisk)
admin.site.register(VideoCard)
admin.site.register(TypeDB)
admin.site.register(LANcard)
admin.site.register(Location)
admin.site.register(Monitor)
admin.site.register(UserName)
admin.site.register(AdditionalSettings)

# Register your models here.
