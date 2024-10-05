from rest_framework import serializers
from .models import Carshop, Booking

class CarshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carshop
        fields = ['id', 'shop_name','owner_name', 'phone1','time_for_wash', 'upload_carshop_image', 'address', 'services']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'shop', 'customer', 'car', 'driver', 'selected_slot', 'driver_response']  # Include valid fields

