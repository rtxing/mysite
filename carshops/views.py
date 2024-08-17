from django.shortcuts import render
from rest_framework import viewsets
import geopy.distance
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
# Create your views here.
from .models import Carshop, Booking
from django.forms.models import model_to_dict
from carshops.serializers import CarshopSerializer,BookingSerializer
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from my_app.models import User
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

def carshops_geo(request, lat, longt, phone):
    """url: api/car/pk"""
    try:
        print("in CG")
        return_list = []
        distance = []
        print(lat, longt)
        user = User.objects.get(phone = phone)
        user.latitude = lat
        user.longitude = longt 
        user.save()
        carshops = Carshop.objects.all()
        for i in carshops:
            coords_1 = (lat, longt)
            coords_2 = (i.latitude, i.longitude)
            dist = int(geopy.distance.geodesic(coords_1, coords_2).km)
            if dist <= 20:
                distance.append(dist)
                return_list.append(i)
        print(return_list)
        keydict = dict(zip(return_list, distance))
        return_list.sort(key=keydict.get)
        distance.sort()
        print(return_list)
        print(distance)
    except:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": "No Car Wash shops found"}),
            content_type="application/json",
        )

   

    serialized_qs = serializers.serialize('json', return_list)
    serialized_qs = json.loads(serialized_qs)
    # Serialise your car or do something with it
    return JsonResponse([serialized_qs,distance], safe = False)


def get_previous_orders(request, phone):
    """url: api/car/pk"""
    try:
        print("in PRE")
        user = User.objects.get(phone = phone)
        bookings = Booking.objects.filter(customer = user).order_by('-id') 
        
    except:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": "No Car Wash shops found"}),
            content_type="application/json",
        )

   

    serialized_qs = serializers.serialize('json', bookings)
    serialized_qs = json.loads(serialized_qs)
    # Serialise your car or do something with it
    return JsonResponse([serialized_qs], safe = False)





class CarshopViewSet(viewsets.ModelViewSet):
    queryset = Carshop.objects.all()
    for i in queryset:

        serializer_class = CarshopSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def carshop_id(request, id, phone):
    """url: api/car/pk"""
    try:
        print("in csid55...")
        carshop = Carshop.objects.get(id = id)
        user = User.objects.get(phone = phone)
        coords_1 = (carshop.latitude, carshop.longitude)
        coords_2 = (user.latitude, user.longitude)
        distance = int(geopy.distance.geodesic(coords_1, coords_2).km)
    except Exception as e: 
        # Whoopsie
        print(repr(e))
        return HttpResponseNotFound(
            json.dumps({"ERR": f"carshop  with id {id} not found"}),
            content_type="application/json",
        )

    # Serialise your car or do something with it
    return JsonResponse([CarshopSerializer(carshop).data, distance], safe= False)


def detailbooking(request, bookingid):
    """url: api/car/pk"""
    try:
        print("in booking...")
        booking = Booking.objects.get(id=bookingid)
        shop = Carshop.objects.get(id = booking.shop.id)
        
    except:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": f"booking  with id {id} not found"}),
            content_type="application/json",
        )
   

    # Serialise your car or do something with it
    return JsonResponse([BookingSerializer(booking).data, CarshopSerializer(shop).data], safe= False)





@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@csrf_exempt
def booking2(request):
    """url: api/car/pk"""
    try:
        print("in booking 2 ")
        data = json.loads(request.body.decode())
        user = User.objects.get(phone=int(data['user']))
        shop = Carshop.objects.get(id = int(data['shop']) )
        b = Booking.objects.create(booking_status= "In Progress", shop= shop, customer = user, driver = data['driver'], date_time = data['date_time'])
        b.save()
    except:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": error.message}),
            content_type="application/json",
        )

    # Serialise your car or do something with it
    data = {'message': "Booking successfully created."}
    return JsonResponse(data)



@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@csrf_exempt
def add_car_details(request):
    """url: api/car/pk"""
    try:
        data = json.loads(request.body.decode())
        model =data['model']
        color = data['color']
        car_number = data['car_number']
        car_name = data['car_name']
        user = User.objects.get(phone=int(data['phone']))
        car_type = data['car_type']
        c = Car.objects.create(color = color, model = model, car_type= car_type, customer = user, car_name = car_name, car_number = car_number)
        c.save()
    except:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": error.message}),
            content_type="application/json",
        )

    # Serialise your car or do something with it
    data = {'message': "Car successfully added."}
    return JsonResponse(data)
