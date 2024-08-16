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


def get_previous_orders(request, userid):
    """url: api/car/pk"""
    try:
    	print("in PRE")
    	user = User.objects.get(id = userid)
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


def carshop_id(request, id, userid):
    """url: api/car/pk"""
    try:
    	print("in csid55...")
    	car = Carshop.objects.get(id=id)
    	user = User.objects.get(id = userid)
    	coords_1 = (car.latitude, car.longitude)
    	coords_2 = (user.latitude, user.longitude)
    	distance = int(geopy.distance.geodesic(coords_1, coords_2).km)
    except:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": f"car  with id {id} not found"}),
            content_type="application/json",
        )
   

    # Serialise your car or do something with it
    return JsonResponse([CarshopSerializer(car).data, distance], safe= False)


def detailbooking(request, bookingid):
    """url: api/car/pk"""
    try:
    	print("in booking...")
    	booking = Booking.objects.get(id=bookingid)
    	shop = Carshop.objects.get(id = booking.shop.id)
    	
    except:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": f"car  with id {id} not found"}),
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
    	user = User.objects.get(id=int(data['user']))
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