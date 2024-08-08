from django.shortcuts import render
from rest_framework import viewsets
import geopy.distance
from django.http import JsonResponse, HttpResponse
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

def carshops_geo(request, lat, longt):
    """url: api/car/pk"""
    try:
    	return_list = []
    	distance = []
    	print(lat, longt)
    	carshops = Carshop.objects.all()
    	for i in carshops:
    		coords_1 = (lat, longt)
    		coords_2 = (i.latitude, i.longitude)
    		dist = int(geopy.distance.geodesic(coords_1, coords_2).km)
    		if dist <= 200:
    			distance.append(dist)
    			return_list.append(i)
    	print(return_list)
    	print(distance)
    except models.Car.DoesNotExist:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": f"car  with id {id} not found"}),
            content_type="application/json",
        )

   

    serialized_qs = serializers.serialize('json', return_list)
    serialized_qs = json.loads(serialized_qs)
    # Serialise your car or do something with it
    return JsonResponse([serialized_qs,distance], safe = False)



class CarshopViewSet(viewsets.ModelViewSet):
	queryset = Carshop.objects.all()
	for i in queryset:

		serializer_class = CarshopSerializer


class BookingViewSet(viewsets.ModelViewSet):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer


def carshop_id(request, pk):
    """url: api/car/pk"""
    try:
        car = Carshop.objects.get(id=pk)
    except models.Car.DoesNotExist:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": f"car  with id {id} not found"}),
            content_type="application/json",
        )

    # Serialise your car or do something with it
    return JsonResponse(CarshopSerializer(car).data)

@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@csrf_exempt
def booking2(request):
    """url: api/car/pk"""
    try:
    	print("in booking 2 ")
    	data = json.loads(request.body.decode())
    	user = User.objects.get(id=int(data['user']))
    	shop = Carshop.objects.get(id = int(data['shop']) )
    	b = Booking.objects.create(shop= shop, customer = user, driver = data['driver'], date_time = data['date_time'])
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