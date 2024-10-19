from django.contrib import admin

# Register your models here.
from .models import CarPickupPhoto, CarWashPhoto, Carshop,Booking, Car, Notification, Service, Rating


# admin.site.register(Carshop)
# admin.site.register(Booking)
# admin.site.register(Car)
# admin.site.register(Service)
# admin.site.register(Rating)


@admin.register(Carshop)
class CarshopAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop_name','user', 'owner_name', 'phone1', 'opening_time', 'closing_time', 'latitude', 'longitude')
    search_fields = ('shop_name', 'owner_name', 'phone1', 'address')
    list_filter = ('opening_time', 'closing_time')
    filter_horizontal = ('services',)  # To allow better UI for selecting many-to-many field


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'stars', 'review', 'booking')
    search_fields = ('review', 'booking__id')
    list_filter = ('stars',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'customer', 'car', 'service', 'selected_slot','booking_status','driver_response', "driver",'created_at', 'booking_date')
    search_fields = ('shop__shop_name', 'customer__username', 'car__car_name', 'service__service_name')
    list_filter = ('booking_status', 'created_at', 'booking_date')
    autocomplete_fields = ['shop', 'customer', 'car', 'service', 'address']
    

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'car_name', 'model', 'color', 'car_number', 'customer', 'car_type')
    search_fields = ('car_name', 'car_number', 'customer__username')
    list_filter = ('car_type',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_name', 'cost', 'car_type_status', 'duration_in_hours')
    search_fields = ('service_name',)
    list_filter = ('car_type_status',)


@admin.register(CarPickupPhoto)
class CarPickupPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'driver', 'timestamp')
    search_fields = ('booking__id', 'driver__username')
    list_filter = ('timestamp',)


@admin.register(CarWashPhoto)
class CarWashPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'user', 'timestamp')
    search_fields = ('booking__id', 'user__username')
    list_filter = ('timestamp',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'booking', 'message', 'created_at')
    search_fields = ('driver__username', 'booking__id', 'message')
    list_filter = ('created_at',)