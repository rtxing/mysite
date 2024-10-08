# from django.contrib import admin

# # Register your models here.
# from .models import Carshop,Booking, Car, Service, Rating


# admin.site.register(Carshop)
# admin.site.register(Booking)
# admin.site.register(Car)
# admin.site.register(Service)
# admin.site.register(Rating)


from django.contrib import admin

from carshops.models import Booking, Car, CarPickupPhoto, CarWashPhoto, Carshop, Notification, Rating, Service

class CarshopAdmin(admin.ModelAdmin):
    list_display = ('id','shop_name', 'owner_name', 'phone1', 'opening_time', 'closing_time')
    search_fields = ('shop_name', 'owner_name', 'phone1')
    list_filter = ('opening_time', 'closing_time')
    filter_horizontal = ('services',)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('id','stars', 'review', 'booking')
    search_fields = ('review', 'booking__id')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','shop__shop_name', 'customer__name', 'selected_slot', 'booking_status', 'created_at', 'booking_date')
    search_fields = ('shop__shop_name', 'customer__username', 'selected_slot')
    list_filter = ('booking_status', 'created_at', 'booking_date')

class CarAdmin(admin.ModelAdmin):
    list_display = ('id','car_name', 'model', 'color', 'car_number', 'customer')
    search_fields = ('car_name', 'model', 'car_number', 'customer__username')
    list_filter = ('car_type',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id','service_name', 'cost', 'car_type_status', 'duration_in_hours')
    search_fields = ('service_name',)
    list_filter = ('car_type_status',)

class CarPickupPhotoAdmin(admin.ModelAdmin):
    list_display = ('id','booking', 'driver', 'timestamp')
    search_fields = ('booking__id', 'driver__username')
    list_filter = ('timestamp',)

class CarWashPhotoAdmin(admin.ModelAdmin):
    list_display = ('id','booking', 'user', 'timestamp')
    search_fields = ('booking__id', 'user__username')
    list_filter = ('timestamp',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id','driver', 'booking', 'message', 'created_at')
    search_fields = ('message', 'driver__username', 'booking__id')
    list_filter = ('created_at',)

admin.site.register(Carshop, CarshopAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(CarPickupPhoto, CarPickupPhotoAdmin)
admin.site.register(CarWashPhoto, CarWashPhotoAdmin)
admin.site.register(Notification, NotificationAdmin)
