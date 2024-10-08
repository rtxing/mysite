from rest_framework import serializers

from carshops.models import Carshop, Service
from .models import Address, User

class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Set read_only=True

    class Meta:
        model = Address
        fields = ['user', 'street', 'city', 'state', 'postal_code', 'country']
        extra_kwargs = {
            'user': {'required': True}  # Ensure the user field is required
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone', 
            'dob', 
            'otp', 
            'otp_expiry', 
            'max_otp_try', 
            'name', 
            'latitude', 
            'longitude', 
            'role', 
            'is_user', 
            'is_owner', 
            'is_driver', 
            'profile_picture',
            'driving_license',  # Optional for drivers only
        ]
    
    def validate(self, attrs):
        role = attrs.get('role')
        if role == 'driver' and 'driving_license' not in attrs:
            raise serializers.ValidationError({"driving_license": "This field is required for drivers."})
        return attrs


class CarshopSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(many=True, queryset=Service.objects.all())

    class Meta:
        model = Carshop
        fields = '__all__'
