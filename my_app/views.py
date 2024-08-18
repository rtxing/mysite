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

@csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def login_view(request):
    data = json.loads(request.body)

    phone = data['phone']
    name = data['name']
    latitude = data['latitude']
    longitude = data['longitude']
    print("phone is ", phone)
    print("name is ", name)
    
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
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        max_otp_try = int(user.max_otp_try) - 1

        user.otp = otp
        user.otp_expiry = otp_expiry
        user.max_otp_try = max_otp_try

        if max_otp_try == 0:
            otp_max_out = timezone.now() + datetime.timedelta(hours=1)
        elif max_otp_try == -1:
            user.max_otp_try = 3
        else:
            user.otp_max_out = None
            user.max_otp_try = max_otp_try
        user.latitude = latitude
        user.longitude = longitude
        user.save()

        print(user.otp, 'OTP', user.phone)

        send_otp(user.phone, otp)
        data = {'message': "Successfully generated OTP", 'status':status.HTTP_200_OK }
        return JsonResponse(data)

#        return Response("Successfully generated OTP", status=status.HTTP_200_OK, template_name='')

    except:
        user = User.objects.create(phone=phone, name = name, username=name.replace(" ", ""))
        print(user)
        print("in 2nd")
        
        otp = random.randint(100000, 999999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        max_otp_try = int(user.max_otp_try) - 1

        user.otp = otp
        user.otp_expiry = otp_expiry
        user.max_otp_try = max_otp_try

        if max_otp_try == 0:
            otp_max_out = timezone.now() + datetime.timedelta(hours=1)
        elif max_otp_try == -1:
            user.max_otp_try = 3
        else:
            user.otp_max_out = None
            user.max_otp_try = max_otp_try

        user.latitude = latitude
        user.longitude = longitude
        user.is_passenger = True
        user.save()

        send_otp(user.phone, otp)
        data = {'message': "Successfully generated OTP", 'status':status.HTTP_200_OK }
        return JsonResponse(data)

        #return Response("Successfully generated OTP", status=status.HTTP_200_OK, template_name='')
    else:
        data = {'message': 'Phone number is incorrect', 'status':status.HTTP_401_UNAUTHORIZED }
        return JsonResponse(data)

@csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def verify_view(request):
    data = json.loads(request.body)
    print(data)
    otp = data['otp']
    print(otp)
    try:
        user = User.objects.get(otp=otp)
        if user:
            login(request, user)
            user.otp = None
            user.otp_expiry = None
            user.max_otp_try = 3
            user.otp_max_out = None
            user.save()
            refresh = RefreshToken.for_user(user)
            serialized_obj = serializers.serialize('json', [ user, ])
            data = {'access': str(refresh.access_token), 'user':serialized_obj,  'status':status.HTTP_200_OK }
            return JsonResponse(data)

           # return Response({'access': str(refresh.access_token), 'user': serialized_obj}, status=status.HTTP_200_OK, template_name='')
    except ObjectDoesNotExist:
        data = {'message': 'Please enter the correct OTP', 'status':status.HTTP_400_BAD_REQUEST }
        return JsonResponse(data)
