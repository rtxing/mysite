from django.shortcuts import render
from rest_framework import viewsets
import geopy.distance
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
# Create your views here.
from .models import Carshop, Booking, Service, Rating
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

def carshops_geo(request, lat, longt):
    """url: api/car/pk"""
    try:
        #print("in CG")
        return_list = []
        services = []
        distance = []
        #print(lat, longt)
        #user = User.objects.get(phone = phone)
        carshops = Carshop.objects.all()
        for i in carshops:
            coords_1 = (lat, longt)
            coords_2 = (i.latitude, i.longitude)
            dist = int(geopy.distance.geodesic(coords_1, coords_2).km)
            services.append(list(i.services.values()))
            if dist <= 20:
                distance.append(dist)
                return_list.append(i)
        print(return_list)
        keydict = dict(zip(return_list, distance))
        return_list.sort(key=keydict.get)
        distance.sort()
        #print(return_list)
        #print(distance)
    except Exception as e: 
        # Whoopsie
        print(repr(e))
        return HttpResponseNotFound(
            json.dumps({"ERR": "No Car Wash shops found"}),
            content_type="application/json",
        )

   

    serialized_qs = serializers.serialize('json', return_list)
    serialized_qs = json.loads(serialized_qs)
    #serialized_ss = serializers.serialize('json', services)
    #serialized_ss = json.loads(serialized_ss)
    # Serialise your car or do something with it
    return JsonResponse([serialized_qs,distance, services], safe = False)


def get_previous_orders(request, phone):
    """url: api/car/pk"""
    try:
        print("in PRE")
        shops = []
        user = User.objects.get(phone = phone)
        bookings = Booking.objects.filter(customer = user).order_by('-id') 
        for i in bookings:
            shops.append(i.shop)
            #print(dir(i.shop))
        print(shops)
    except Exception as e: 
        # Whoopsie
        print(repr(e))
        return HttpResponseNotFound(
            json.dumps({"ERR": "No Car Wash shops found"}),
            content_type="application/json",
        )

   

    serialized_qs = serializers.serialize('json', bookings)
    serialized_qs = json.loads(serialized_qs)
    serialized_ss = serializers.serialize('json', shops)
    serialized_ss = json.loads(serialized_ss)
    # Serialise your car or do something with it
    return JsonResponse([serialized_qs,serialized_ss], safe = False)


def get_services(request):
    """url: api/car/pk"""
    try:
        print("in Service")
        services = Service.objects.all()
        
    except Exception as e: 
        # Whoopsie
        print(repr(e))
        return HttpResponseNotFound(
            json.dumps({"ERR": "No services found"}),
            content_type="application/json",
        )

   

    serialized_qs = serializers.serialize('json', services)
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
        #service = Service.objects.get(id = carshop.services.id)
        services = list(carshop.services.values())
    except Exception as e: 
        # Whoopsie
        print(repr(e))
        return HttpResponseNotFound(
            json.dumps({"ERR": f"carshop  with id {id} not found"}),
            content_type="application/json",
        )

    # Serialise your car or do something with it
    return JsonResponse([CarshopSerializer(carshop).data, distance, services], safe= False)


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
        print("in booking 2... ")
        data = json.loads(request.body.decode())
        user = User.objects.get(phone=int(data['user']))
        shop = Carshop.objects.get(id = int(data['shop']) )
        service = Service.objects.get(id = int(data['service']) )
        b = Booking.objects.create(service = service, booking_status= "In Progress", shop= shop, customer = user, driver = data['driver'], date_time = data['date_time'])
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



@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@csrf_exempt
def add_review(request):
    """url: api/car/pk"""
    try:
        data = json.loads(request.body.decode())
        stars =data['stars']
        review = data['review']
        booking = Booking.objects.get(id=data['booking'])
        r = Rating.objects.create(stars = stars, review = review, booking= booking)
        r.save()
    except:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": error.message}),
            content_type="application/json",
        )

    # Serialise your car or do something with it
    data = {'message': "Rating successfully added."}
    return JsonResponse(data)

