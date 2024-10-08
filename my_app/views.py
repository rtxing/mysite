from my_app.serializers import AddressSerializer, CarshopSerializer, UserUpdateSerializer
from .utils import send_otp
import datetime
from rest_framework.permissions import BasePermission,AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from rest_framework import viewsets, status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


@csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def login_view(request):
    print("Login view called") 
    
    data = json.loads(request.body)

    phone = data['phone']
    name = data['name']
    latitude = data['latitude']
    longitude = data['longitude']
    role = data.get('role', 'user')  # Default to 'user' if not provided
    print("phone is ", phone)
    print("name is ", name)
    print("role is ", role)  # Log the role for debugging

    try:
        user = User.objects.get(phone=phone)
        print(user)

        # Check for max OTP attempts
        if int(user.max_otp_try) == 0 and user.otp_max_out and timezone.now() < user.otp_max_out:
            return Response(
                "Max OTP try reached, try after an hour",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate OTP and update user record
        otp = random.randint(100000, 999999)
        print("otp",otp)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        max_otp_try = int(user.max_otp_try) - 1

        user.otp = otp
        print("user.otp",user.otp)
        user.otp_expiry = otp_expiry
        user.max_otp_try = max_otp_try
        user.latitude = latitude
        user.longitude = longitude

        # Assign role
        user.role = role
        user.is_user = (role == 'user')
        user.is_owner = (role == 'owner')
        user.is_driver = (role == 'driver')

        if max_otp_try <= 0:
            user.otp_max_out = timezone.now() + datetime.timedelta(hours=1)
        else:
            user.otp_max_out = None
            user.max_otp_try = max_otp_try

        user.save()

        print(user.otp, 'OTP', user.phone)
        send_otp(user.phone, otp)
        data = {'message': "Successfully generated OTP", 'status': status.HTTP_200_OK}
        return JsonResponse(data)

    except User.DoesNotExist:
        # Create a new user with the specified role
        user = User.objects.create(
            phone=phone, 
            latitude=latitude, 
            longitude=longitude, 
            name=name, 
            username=name.replace(" ", ""),
            role=role  # Set role on creation
        )
        print(user)
        print("in 2nd")

        otp = random.randint(100000, 999999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        user.otp = otp
        user.otp_expiry = otp_expiry
        user.max_otp_try = 3  # Reset to maximum tries on creation

        user.latitude = latitude
        user.longitude = longitude
        user.is_user = (role == 'user')
        user.is_owner = (role == 'owner')
        user.is_driver = (role == 'driver')
        user.save()

        send_otp(user.phone, otp)
        data = {'message': "Successfully generated OTP", 'status': status.HTTP_200_OK}
        return JsonResponse(data)

    else:
        data = {'message': 'Phone number is incorrect', 'status': status.HTTP_401_UNAUTHORIZED}
        return JsonResponse(data)




otp_validator = RegexValidator(regex=r'^\d{6}$', message='OTP must be a 6-digit number.')


@csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def verify_view(request):
    try:
        data = json.loads(request.body)
        print(data)

        phone = data.get('phone', None)
        print(phone)

        otp = data.get('otp', '')
        print(otp)

    # otp = data['otp']
    # print(otp)

        if not phone or not otp:
            return JsonResponse({'message': 'Phone and OTP are required', 'status': status.HTTP_400_BAD_REQUEST})

        try:
            otp_validator(otp) 
        except ValidationError as e:
            return JsonResponse({'message': 'Invalid OTP format. OTP must be 6 digits.', 'status': status.HTTP_400_BAD_REQUEST})

        try:
            user = User.objects.get(phone=phone,otp=otp)
            print("user",user)
            
            if timezone.now() > user.otp_expiry:
                return JsonResponse({'message': 'OTP has expired', 'status': status.HTTP_400_BAD_REQUEST})

            login(request, user)
            user.otp = None
            user.otp_expiry = None
            user.max_otp_try = 3
            user.otp_max_out = None
            user.save()
            refresh = RefreshToken.for_user(user)
            serialized_obj = serializers.serialize('json', [ user, ])
            data = {
                'access': str(refresh.access_token), 
                'user':serialized_obj,  
                'status':status.HTTP_200_OK 
            }
            return JsonResponse(data)

            # return Response({'access': str(refresh.access_token), 'user': serialized_obj}, status=status.HTTP_200_OK, template_name='')
        except ObjectDoesNotExist:
            data = {'message': 'Please enter the correct OTP', 'status':status.HTTP_400_BAD_REQUEST }
            return JsonResponse(data)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON format', 'status': status.HTTP_400_BAD_REQUEST})



from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes


import logging

@api_view(['GET', 'PUT'])
@parser_classes([MultiPartParser, FormParser])
def update_user(request, phone):
    """URL: api/update_user/<phone>"""
    
    logging.info(f"Searching for user with phone: {phone}")
    
    user = User.objects.filter(phone=phone).first()
    if not user:
        logging.error(f"No user found with phone: {phone}")
        return JsonResponse({"error": "User not found."}, status=404)

    if request.method == 'GET':
        user_data = {
            "id": user.id,
            "name": user.name,
            "phone": user.phone,
            "profile_picture": user.profile_picture.url if user.profile_picture else None,
            "role": user.role,
            "driving_license_no": user.driving_license_no
        }
        print("user_data",user_data)
        return JsonResponse(user_data, status=200)

    elif request.method == 'PUT':
        phone = request.data.get('phone')
        name = request.data.get('name')
        profile_picture = request.FILES.get('profile_picture')
        driving_license = request.FILES.get('driving_license')
        driving_license_no = request.data.get('driving_license_no')

        if phone:
            user.phone = phone
        if name:
            user.name = name
        if profile_picture:
            user.profile_picture = profile_picture
        
        if user.role == 'driver':
            if driving_license:
                user.driving_license = driving_license
            if driving_license_no:
                user.driving_license_no = driving_license_no 
        
        elif user.role != 'driver' and (driving_license or driving_license_no):
            return JsonResponse({"error": "Only drivers can upload a driving license or license number."}, status=400)

        user.save()

        return JsonResponse({'message': 'User updated successfully.', 'user_id': user.id}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)




@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@csrf_exempt
@api_view(['POST'])
def add_address(request):
    """URL: api/add-address"""
    try:
        print("In add_address...")

        data = json.loads(request.body.decode())
        phone = data.get('phone')
        
        if not phone:
            return JsonResponse({
                "error": {
                    "user": ["This field is required."]
                }
            }, status=400)

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return HttpResponseNotFound(
                json.dumps({"error": "User not found."}),
                content_type="application/json",
            )

        address_data = {
            'street': data.get('street'),
            'city': data.get('city'),
            'state': data.get('state'),
            'postal_code': data.get('postal_code'),
            'country': data.get('country'),
        }

        serializer = AddressSerializer(data=address_data)
        if serializer.is_valid():
            serializer.save(user=user) 
            return JsonResponse({'message': 'Address added successfully.', 'data': serializer.data}, status=201)
        
        return JsonResponse({'error': serializer.errors}, status=400)

    except Exception as e:
        return HttpResponseNotFound(
            json.dumps({"error": str(e)}),
            content_type="application/json",
        )
    return JsonResponse({'message': "Address addition process completed."})


@api_view(['GET'])
@csrf_exempt
def get_addresses_by_phone(request, phone):
    """URL: api/get-addresses/<phone>"""
    try:
        print(f"In get_addresses_by_phone with phone: {phone}")

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return HttpResponseNotFound(
                json.dumps({"error": "User not found."}),
                content_type="application/json",
            )

        addresses = Address.objects.filter(user=user)
        print("addresses",addresses)

        serializer = AddressSerializer(addresses, many=True)
        print("serializer",serializer)

        addresses_with_id = [
            {
                "id": address.id, 
                **address_data  
            }
            for address, address_data in zip(addresses, serializer.data)
        ]
        print("addresses_with_id",addresses_with_id)

        return JsonResponse({'addresses': addresses_with_id}, status=200)

    except Exception as e:
        return HttpResponseNotFound(
            json.dumps({"error": str(e)}),
            content_type="application/json",
        )
        
        

@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@api_view(['PUT','GET'])
def update_address(request, address_id):
    """URL: api/update-address/<address_id>"""
    try:
        print(f"In update_address with address_id: {address_id}")

        # Retrieve the address by ID
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return HttpResponseNotFound(
                json.dumps({"error": "Address not found."}),
                content_type="application/json",
            )

        # Deserialize the incoming data
        data = json.loads(request.body.decode())
        serializer = AddressSerializer(address, data=data, partial=True)  # Allow partial updates

        if serializer.is_valid():
            serializer.save()  # Save the updated address
            return JsonResponse({'message': 'Address updated successfully.', 'data': serializer.data}, status=200)
        
        return JsonResponse({'error': serializer.errors}, status=400)

    except Exception as e:
        return HttpResponseNotFound(
            json.dumps({"error": str(e)}),
            content_type="application/json",
        )
        