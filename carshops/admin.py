from django.contrib import admin

# Register your models here.
from .models import Carshop,Booking, Car, Service, Rating


admin.site.register(Carshop)
admin.site.register(Booking)
admin.site.register(Car)
admin.site.register(Service)
admin.site.register(Rating)