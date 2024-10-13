import datetime
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
import geopy.distance
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
# Create your views here.
from carshops.models import Carshop, Booking, Service, Rating
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

from my_app.utils import haversine
from .models import Car, CarPickupPhoto, CarWashPhoto, Notification
from my_app.models import Address

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


# def get_previous_orders(request, phone):
#     """url: api/car/pk"""
#     try:
#         print("in PRE")
#         shops = []
#         user = User.objects.get(phone = phone)
#         bookings = Booking.objects.filter(customer = user).order_by('-id') 
#         for i in bookings:
#             shops.append(i.shop)
#             #print(dir(i.shop))
#         print(shops)
#     except Exception as e: 
#         # Whoopsie
#         print(repr(e))
#         return HttpResponseNotFound(
#             json.dumps({"ERR": "No Car Wash shops found"}),
#             content_type="application/json",
#         )




#     serialized_qs = serializers.serialize('json', bookings)
#     serialized_qs = json.loads(serialized_qs)
#     serialized_ss = serializers.serialize('json', shops)
#     serialized_ss = json.loads(serialized_ss)
#     # Serialise your car or do something with it
#     return JsonResponse([serialized_qs,serialized_ss], safe = False)


@api_view(['GET'])
def get_previous_orders(request, phone):
    """Retrieve all previous orders by phone number."""
    try:
        # Retrieve the user based on the provided phone number
        user = User.objects.get(phone=phone)

        # Fetch previous bookings for the user
        bookings = Booking.objects.filter(customer=user)

        # Prepare the list of booking details
        order_details = [
            {
                "id": booking.id,
                "customer": {
                    "customer_id": booking.customer.id,
                    "name": booking.customer.name,
                    "phone": booking.customer.phone,
                },
                "shop": {
                    "shop_id": booking.shop.id,
                    "name": booking.shop.shop_name,
                    'upload_carshop_image_url': booking.shop.upload_carshop_image.url if booking.shop.upload_carshop_image else None,
                    "owner": booking.shop.owner_name,
                    "phone": booking.shop.phone1,
                },
                "address": {
                    "address_id": booking.address.id,
                    "street": booking.address.street,
                    "city": booking.address.city,
                    "state": booking.address.state,
                    "postal_code": booking.address.postal_code,
                    "country": booking.address.country,
                },
                "car": {
                    "car_id": booking.car.id,
                    "name": booking.car.car_name,
                    "model": booking.car.model,
                    "color": booking.car.color,
                    "car_number": booking.car.car_number,
                },
                "booking_date": booking.booking_date,
                "selected_slot": booking.selected_slot,
                "driver_response": booking.driver_response,
                "booking_status": booking.booking_status,
                "service": {
                    "service_id": booking.service.id,
                    "service_name": booking.service.service_name,
                    "cost": booking.service.cost,
                }
            }
            for booking in bookings
        ]

        if not order_details:
            return JsonResponse({'message': 'No orders found for this phone number.'}, status=404)

        return JsonResponse({'orders': order_details})

    except User.DoesNotExist:
        return JsonResponse({'ERR': 'User not found.'}, status=404)
    except Exception as error:
        return HttpResponseNotFound(
            json.dumps({"ERR": str(error)}),
            content_type="application/json",
        )

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
    #for i in queryset:

     #   serializer_class = CarshopSerializer


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


from datetime import datetime, timedelta


from django.http import JsonResponse, HttpResponseNotFound
import json

def detailbooking(request, bookingid):
    """url: api/car/pk"""
    try:
        # Fetch the booking and related shop
        booking = Booking.objects.get(id=bookingid)
        shop = Carshop.objects.get(id=booking.shop.id)
    except Booking.DoesNotExist:
        return HttpResponseNotFound(
            json.dumps({"ERR": f"Booking with id {bookingid} not found"}), 
            content_type="application/json"
        )
    except Carshop.DoesNotExist:
        return HttpResponseNotFound(
            json.dumps({"ERR": f"Carshop related to booking with id {bookingid} not found"}), 
            content_type="application/json"
        )
    
    # Serialize booking and carshop data
    booking_data = BookingSerializer(booking).data
    shop_data = CarshopSerializer(shop).data

    # Return as a dictionary instead of a list for better clarity
    return JsonResponse({
        "booking": booking_data,
        "carshop": shop_data
    }, safe=False)




from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from django.db.models import Q

SHOP_OPENING_TIME = "08:00"
SHOP_CLOSING_TIME = "20:00"

def is_conflicting(slot_start, slot_end, booked_periods):
    """
    Check if the given slot conflicts with any existing bookings.
    """
    for booked_start, booked_end in booked_periods:
        if not (slot_end <= booked_start or slot_start >= booked_end):
            return True  # Conflict found
    return False  # No conflict


def generate_available_slots(service_duration, shop_id, booking_date):
    """
    Generate available time slots based on shop hours, service duration, booked slots, and a specific date.
    """
    try:
        shop = Carshop.objects.get(id=shop_id)
    except Carshop.DoesNotExist:
        return []

    shop_opening_time = shop.opening_time
    shop_closing_time = shop.closing_time

    available_slots = []
    current_start_time = datetime.combine(booking_date, shop_opening_time)

    bookings = Booking.objects.filter(shop_id=shop_id, booking_date=booking_date)

    booked_periods = []
    for booking in bookings:
        start_time_str, end_time_str = booking.selected_slot.split(' - ')
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time() 
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
        booked_periods.append((start_time, end_time))

    while current_start_time.time() < shop_closing_time:
        next_time = (current_start_time + service_duration).time()

        if next_time > shop_closing_time:
            break

        if next_time <= current_start_time.time():
            break

        if not is_conflicting(current_start_time.time(), next_time, booked_periods):
            available_slots.append((current_start_time.time(), next_time))

        current_start_time += timedelta(minutes=service_duration.seconds // 60)

    return available_slots




from datetime import timedelta

@csrf_exempt
def fetch_available_slots(request):
    """
    Fetch available slots based on shop, service, and booking date.
    """
    if request.method == 'POST':
        data = json.loads(request.body.decode())

        if 'shop' not in data or 'service' not in data or 'booking_date' not in data:
            return JsonResponse({"error": "shop, service, or booking_date key is missing in the request data"}, status=400)

        try:
            shop = Carshop.objects.get(id=data['shop'])
            service = Service.objects.get(id=data['service'])
            booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
        except (Carshop.DoesNotExist, Service.DoesNotExist, ValueError):
            return JsonResponse({"error": "Invalid shop, service ID, or booking_date format"}, status=404)

        service_duration_hours = float(service.duration_in_hours)
        service_duration = timedelta(hours=service_duration_hours)

        available_slots = generate_available_slots(service_duration, shop.id, booking_date)

        response_data = {
            "available_slots": [f"{slot[0]} - {slot[1]}" for slot in available_slots]
        }

        return JsonResponse(response_data)

    return JsonResponse({"error": "Invalid request method"}, status=405)



from geopy.distance import geodesic

@csrf_exempt
def create_booking(request):
    """Creates a booking based on user input."""
    if request.method == 'POST':
        data = json.loads(request.body.decode())

        if 'user_phone' not in data or 'selected_slot' not in data or 'booking_date' not in data:
            return JsonResponse({"error": "user_phone, selected_slot, or booking_date key is missing in the request data"}, status=400)

        try:
            user = User.objects.get(phone=data['user_phone'])
            shop = Carshop.objects.get(id=int(data['shop']))
            service = Service.objects.get(id=int(data['service']))
            address = Address.objects.get(id=int(data['address']))
            car = Car.objects.get(id=int(data['car']))

            selected_slot = data['selected_slot']
            booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()  # Parse the booking date

            booking = Booking.objects.create(
                service=service,
                booking_status="In_Progress",
                shop=shop,
                customer=user,
                address=address,
                car=car,
                selected_slot=selected_slot,
                booking_date=booking_date  # Save the booking date
            )
            print("booking", booking)

            user_location = (float(user.latitude), float(user.longitude))
            default_radius = 20.0

            nearby_drivers = User.objects.filter(is_driver=True)

            available_drivers = []
            for driver in nearby_drivers:
                driver_location = (float(driver.latitude), float(driver.longitude))
                distance = geodesic(user_location, driver_location).kilometers  # Use geodesic to calculate distance

                if distance <= default_radius:
                    available_drivers.append(driver)

                    # Notify the driver about the new booking
                    notify_driver(driver, booking)

            response_data = {
                "message": "Booking created. Waiting for driver acceptance.",
                "booking": {
                    "id": booking.id,
                    "user_phone": user.phone,
                    "shop_id": shop.id,
                    "service_id": service.id,
                    "address_id": address.id,
                    "car_id": car.id,
                    "selected_slot": booking.selected_slot,
                    "booking_date": booking.booking_date.strftime('%Y-%m-%d'),  # Format date for response
                    "booking_status": booking.booking_status,
                    "driver": booking.driver.id if booking.driver else None,
                    "available_drivers": [available_driver.id for available_driver in available_drivers],
                },
            }

            return JsonResponse(response_data)

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except Carshop.DoesNotExist:
            return JsonResponse({"error": "Car shop not found."}, status=404)
        except Service.DoesNotExist:
            return JsonResponse({"error": "Service not found."}, status=404)
        except Address.DoesNotExist:
            return JsonResponse({"error": "Address not found."}, status=404)
        except Car.DoesNotExist:
            return JsonResponse({"error": "Car not found."}, status=404)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def notify_driver(driver, booking):
    Notification.objects.create(
        driver=driver,
        booking=booking,
        message=f"You have a new booking from {booking.customer.phone} for {booking.service.service_name} at {booking.selected_slot}."
    )

    print(f"Driver {driver.id} notified about booking ID {booking.id}")

@csrf_exempt
def get_driver_notifications(request, driver_phone):
    """Fetch notifications for the driver."""
    if request.method == 'GET':
        if not driver_phone:
            return JsonResponse({"error": "driver_phone is required."}, status=400)

        try:
            driver = User.objects.get(phone=driver_phone)
            notifications = Notification.objects.filter(driver=driver)

            notification_data = [
                {
                    "id": notification.id,
                    "booking_id": notification.booking.id,
                    "message": notification.message,
                    "created_at": notification.created_at.isoformat(),
                }
                for notification in notifications
            ]

            return JsonResponse({"notifications": notification_data})

        except User.DoesNotExist:
            return JsonResponse({"error": "Driver not found."}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def respond_to_booking(request, booking_id):
    """Driver responds to a booking."""
    if request.method == 'POST':
        data = json.loads(request.body.decode())

        if 'phone' not in data or 'response' not in data:
            return JsonResponse({"error": "phone or response key is missing in the request data"}, status=400)

        try:
            driver = User.objects.get(phone=data['phone'])
            booking = Booking.objects.get(id=booking_id)

            if booking.booking_status == "Accepted":
                return JsonResponse({"error": "This booking has already been accepted by another driver."}, status=400)

            response = data['response'].lower()
            if response not in ['accepted', 'rejected']:
                return JsonResponse({"error": "Invalid response. Must be 'accepted' or 'rejected'."}, status=400)

            if response == 'accepted':
                booking.driver = driver
                # booking.booking_status = "Accepted"
                booking.driver_response = "Accepted"
            else:
                booking.driver_response = "Rejected"

            booking.save()

            return JsonResponse({
                "message": f"Booking {response} by driver {driver.id}.",
                "booking": {
                    "id": booking.id,
                    "booking_status": booking.booking_status,
                    "driver": driver.id if response == 'accepted' else None,
                },
            })

        except User.DoesNotExist:
            return JsonResponse({"error": "Driver not found."}, status=404)
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking not found."}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)

import time
from django.http import StreamingHttpResponse


@csrf_exempt
def get_driver_bookings(request, driver_phone):
    """Fetch all relevant bookings for a specific driver based on their availability and preferences."""
    if request.method == 'GET':
        if not driver_phone:
            return JsonResponse({"error": "driver_phone is required."}, status=400)

        try:
            driver = User.objects.get(phone=driver_phone)

            def event_stream():
                while True:
                    driver_location = (float(driver.latitude), float(driver.longitude))
                    default_radius = 20.0

                    bookings = Booking.objects.filter(driver_response="Pending")
                    available_bookings = []
                    
                    for booking in bookings:
                        booking_location = (float(booking.customer.latitude), float(booking.customer.longitude))
                        distance = haversine(driver_location[0], driver_location[1], booking_location[0], booking_location[1])

                        if distance <= default_radius:
                            available_bookings.append({
                                "booking_id": booking.id,
                                "user_phone": booking.customer.phone,
                                "shop_id": booking.shop.id,
                                "shop_name": booking.shop.shop_name,
                                "service_id": booking.service.id,
                                "service_name": booking.service.service_name,
                                "address_id": booking.address.id,
                                "address": {
                                    "street": booking.address.street,
                                    "city": booking.address.city,
                                    "state": booking.address.state,
                                    "postal_code": booking.address.postal_code,
                                    "country": booking.address.country,
                                },
                                "car_id": booking.car.id,
                                "car_name": booking.car.car_name,
                                "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
                                "selected_slot": booking.selected_slot,
                                "booking_status": booking.booking_status,
                                "driver_id": booking.driver.id if booking.driver else None,
                                "driver_name": f"{booking.driver.first_name} {booking.driver.last_name}" if booking.driver else None,
                                "created_at": booking.created_at.isoformat(),
                            })

                    data = json.dumps({"bookings": available_bookings})
                    yield f"data: {data}\n\n"

                    time.sleep(1)

            return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

        except User.DoesNotExist:
            return JsonResponse({"error": "Driver not found."}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)




    
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@csrf_exempt
def add_car_details(request):
    """url: api/car/pk"""
    try:
        if request.method == 'POST':
            data = request.POST
            model = data['model']
            color = data['color']
            car_number = data['car_number']
            car_name = data['car_name']
            car_type = data['car_type']
            user = User.objects.get(phone=int(data['phone']))

            upload = request.FILES.get('upload')
            rc_photo = request.FILES.get('rc_photo')
            insurance_photo = request.FILES.get('insurance_photo')

            c = Car.objects.create(
                color=color,
                model=model,
                car_type=car_type,
                customer=user,
                car_name=car_name,
                car_number=car_number,
                upload=upload,
                rc_photo=rc_photo,
                insurance_photo=insurance_photo
            )
            c.save()
    except Exception as error:
        return HttpResponseNotFound(
            json.dumps({"ERR": str(error)}),
            content_type="application/json",
        )

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


@api_view(['GET'])
def get_cars_by_phone(request, phone):
    """url: api/car/<phone>"""
    try:
        user = User.objects.get(phone=phone)
        
        cars = Car.objects.filter(customer=user)

        car_details = [
            {
                'id': car.id,
                'car_name': car.car_name,
                'model': car.model,
                'color': car.color,
                'car_number': car.car_number,
                'car_type': car.car_type,
                'rc_photo_url': car.rc_photo.url if car.rc_photo else None,
                'insurance_photo_url': car.insurance_photo.url if car.insurance_photo else None,
            }
            for car in cars
        ]

        return JsonResponse({'cars': car_details})

    except Exception as error:
        return HttpResponseNotFound(
            json.dumps({"ERR": str(error)}),
            content_type="application/json",
        )
        
        
@api_view(['GET', 'PUT'])
def update_car_details(request, id):
    """url: api/car/update/<id>"""
    try:
        car = Car.objects.get(id=id)

        data = request.data
        print("data",data)
        car.model = data.get('model', car.model)
        car.color = data.get('color', car.color)
        car.car_number = data.get('car_number', car.car_number)
        car.car_name = data.get('car_name', car.car_name)
        car.car_type = data.get('car_type', car.car_type)

        if 'upload' in request.FILES:
            car.upload = request.FILES['upload']
        if 'rc_photo' in request.FILES:
            car.rc_photo = request.FILES['rc_photo']
        if 'insurance_photo' in request.FILES:
            car.insurance_photo = request.FILES['insurance_photo']

        car.save()

        response_data = {
            'message': "Car details successfully updated.",
            'car_details': {
                'id': car.id,
                'car_name': car.car_name,
                'model': car.model,
                'color': car.color,
                'car_number': car.car_number,
                'car_type': car.car_type,
                'rc_photo_url': car.rc_photo.url if car.rc_photo else None,
                'insurance_photo_url': car.insurance_photo.url if car.insurance_photo else None,
            }
        }

        return JsonResponse(response_data)

    except Car.DoesNotExist:
        return JsonResponse({'ERR': 'Car not found.'}, status=404)
    except Exception as error:
        return HttpResponseNotFound(
            json.dumps({"ERR": str(error)}),
            content_type="application/json",
        )
        
        
@csrf_exempt
def get_available_bookings(request):
    """Get available bookings for a driver based on their location."""
    if request.method == 'GET':
        driver_phone = request.GET.get('driver_phone') 
        radius = float(request.GET.get('radius', 5))

        try:
            driver = User.objects.get(phone=driver_phone)
            driver_location = (float(driver.latitude), float(driver.longitude))

            bookings = Booking.objects.filter(booking_status='In_Progress', driver=None)

            available_bookings = []
            for booking in bookings:
                user_location = (float(booking.address.latitude), float(booking.address.longitude))
                distance = geodesic(driver_location, user_location).kilometers

                if distance <= radius:
                    available_bookings.append({
                        "booking_id": booking.id,
                        "user_phone": booking.customer.phone,
                        "shop_id": booking.shop.id,
                        "service_id": booking.service.id,
                        "address_id": booking.address.id,
                        "car_id": booking.car.id,
                        "selected_slot": booking.selected_slot,
                        "booking_status": booking.booking_status,
                    })

            return JsonResponse({"available_bookings": available_bookings})

        except User.DoesNotExist:
            return JsonResponse({"error": "Driver not found."}, status=404)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)

from rest_framework.views import APIView


@api_view(['GET'])
def get_booking_details(request, booking_id):
    """url: api/booking/details/<booking_id>"""
    try:
        booking = Booking.objects.get(id=booking_id)

        # Get car pickup photos related to the booking
        pickup_photos = CarPickupPhoto.objects.filter(booking=booking)
        pickup_photos_data = [{"id": photo.id, "image_url": photo.image.url} for photo in pickup_photos]

        # Get car wash photos related to the booking
        car_wash_photos = CarWashPhoto.objects.filter(booking=booking)
        car_wash_photos_data = [{"id": photo.id, "image_url": photo.image.url} for photo in car_wash_photos]

        # Prepare booking data
        booking_data = {
            "id": booking.id,
            "shop": {
                "name": booking.shop.shop_name if booking.shop else None,
                "owner": booking.shop.owner_name if booking.shop else None,
                "phone": booking.shop.phone1 if booking.shop else None,
            },
            "customer": {
                "name": booking.customer.name if booking.customer else None,
                "phone": booking.customer.phone if booking.customer else None,
            },
            "address": {
                "street": booking.address.street,
                "city": booking.address.city,
                "state": booking.address.state,
                "postal_code": booking.address.postal_code,
                "country": booking.address.country,
            },
            "car": {
                "name": booking.car.car_name,
                "model": booking.car.model,
                "color": booking.car.color,
                "car_number": booking.car.car_number,
            },
            "selected_slot": booking.selected_slot,
            "driver_response": booking.driver_response,
            "booking_status": booking.booking_status,
            "service": {
                "service_id": booking.service.id if booking.service else None,
                "service_name": booking.service.service_name if booking.service else None,
                "service_wash_time": booking.service.duration_in_hours if booking.service else None,
                "cost": booking.service.cost if booking.service else None,
            },
            "driver": {
                "driver_id": booking.driver.id if booking.driver else None,
                "driver_name": booking.driver.name if booking.driver else None,
            },
            "pickup_photos": pickup_photos_data,
            "car_wash_photos": car_wash_photos_data,
        }

        print("booking_data",booking_data)

        return JsonResponse({"message": "Booking details fetched successfully.", "booking_details": booking_data})

    except Booking.DoesNotExist:
        return JsonResponse({"ERR": "Booking not found."}, status=404)
    except Exception as error:
        return HttpResponseNotFound(
            json.dumps({"ERR": str(error)}),
            content_type="application/json",
        )

        
        
        
@csrf_exempt
def car_pickup_photos(request, booking_id, driver_phone):
    """Handle POST requests for car pickup photos."""
    booking = get_object_or_404(Booking, id=booking_id)
    print("booking",booking)

    driver = get_object_or_404(User, phone=driver_phone, role='driver')
    print("driver",driver)

    if booking.driver != driver:
        print("booking.driver",booking.driver)
        
        return JsonResponse({"error": "This driver is not assigned to the booking."}, status=403)

    if booking.booking_status != "On_Way_To_Pickup":
        return JsonResponse({"error": "Photos can only be uploaded when the booking status is 'On Way to Pickup'."}, status=403)

    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({"error": "No images provided."}, status=400)

        images = request.FILES.getlist('image')
        uploaded_photos = []
        
        for image in images:
            photo = CarPickupPhoto.objects.create(booking=booking, driver=driver, image=image)
            uploaded_photos.append({
                "id": photo.id,
                "image_url": photo.image.url
            })

        booking_data = {
            "id": booking.id,
            "shop": booking.shop.shop_name,
            "customer": {
                "name": booking.customer.name,
                "phone": booking.customer.phone,
            },
            "address": {
                "street": booking.address.street,
                "city": booking.address.city,
                "state": booking.address.state,
                "postal_code": booking.address.postal_code,
                "country": booking.address.country,
            },
            "car": {
                "name": booking.car.car_name,
                "model": booking.car.model,
                "color": booking.car.color,
                "car_number": booking.car.car_number,
            },
            "selected_slot": booking.selected_slot,
            "booking_status": booking.booking_status,
            "service": booking.service.service_name,
            "pickup_photos": uploaded_photos
        }

        return JsonResponse({
            "booking_id": booking.id,
            "message": f"{len(images)} pickup photos successfully uploaded.",
            "booking_data": booking_data
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)




@csrf_exempt
def car_wash_photos(request, booking_id, user_phone):
    """Handle POST requests for car wash photos."""
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return JsonResponse({"error": "Booking not found."}, status=404)

    try:
        user = User.objects.get(phone=user_phone)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if booking.booking_status != "Completed":
        return JsonResponse({"error": "Photos can only be uploaded when the service is Completed."}, status=403)

    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({"error": "No images provided."}, status=400)

        images = request.FILES.getlist('image')
        uploaded_photos = []
        
        for image in images:
            photo = CarWashPhoto.objects.create(booking=booking, user=user, image=image)
            uploaded_photos.append({
                "id": photo.id,
                "image_url": photo.image.url
            })

        booking_data = {
            "id": booking.id,
            "shop": booking.shop.shop_name,
            "customer": {
                "name": booking.customer.name,
                "phone": booking.customer.phone,
            },
            "address": {
                "street": booking.address.street,
                "city": booking.address.city,
                "state": booking.address.state,
                "postal_code": booking.address.postal_code,
                "country": booking.address.country,
            },
            "car": {
                "name": booking.car.car_name,
                "model": booking.car.model,
                "color": booking.car.color,
                "car_number": booking.car.car_number,
            },
            "selected_slot": booking.selected_slot,
            "booking_status": booking.booking_status,
            "service": booking.service.service_name,
            "wash_photos": uploaded_photos
        }

        return JsonResponse({
            "booking_id": booking.id,
            "message": f"{len(images)} car wash photos successfully uploaded.",
            "booking_data": booking_data
        })


    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
@api_view(['POST'])
def add_carshop(request):
    """Add a new car shop associated with the owner and multiple services."""
    try:
        phone = request.data.get('phone')
        shop_name = request.data.get('shop_name')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        owner_name = request.data.get('owner_name')
        phone1 = request.data.get('phone1')
        address = request.data.get('address')
        upload_carshop_image = request.FILES.get('upload_carshop_image')

        services_data = request.data.get('services', [])

        opening_time_str = request.data.get('opening_time', '09:00:00')
        closing_time_str = request.data.get('closing_time', '17:00:00')

        opening_time = datetime.strptime(opening_time_str, '%H:%M:%S').time()
        closing_time = datetime.strptime(closing_time_str, '%H:%M:%S').time()

        user = User.objects.get(phone=phone)
        print("user",user)

        carshop = Carshop.objects.create(
            shop_name=shop_name,
            latitude=latitude,
            longitude=longitude,
            owner_name=owner_name,
            phone1=phone1,
            address=address,
            upload_carshop_image=upload_carshop_image,
            opening_time=opening_time,
            closing_time=closing_time,
            user=user
        )

        for service_data in services_data:
            service_id = service_data.get('id')
            if service_id:
                service = get_object_or_404(Service, id=service_id)
            else:
                service = Service.objects.create(
                    service_name=service_data.get('service_name'),
                    cost=service_data.get('cost'),
                    description=service_data.get('description'),
                    car_type_status=service_data.get('car_type_status'),
                    duration_in_hours=service_data.get('duration_in_hours'),
                )
            carshop.services.add(service)

        carshop.save()

        response_data = {
            'message': 'Car shop successfully added.',
            'carshop_id': carshop.id,
            'user_id': user.id,
            'carshop_data': {
                'shop_name': carshop.shop_name,
                'latitude': carshop.latitude,
                'longitude': carshop.longitude,
                'owner_name': carshop.owner_name,
                'phone1': carshop.phone1,
                'address': carshop.address,
                'upload_carshop_image': carshop.upload_carshop_image.url if carshop.upload_carshop_image else None,
                'services': [
                    {
                        'id': service.id,
                        'service_name': service.service_name,
                        'cost': service.cost,
                        'description': service.description,
                        'car_type_status': service.car_type_status,
                        'duration_in_hours': service.duration_in_hours,
                    }
                    for service in carshop.services.all()
                ],
                'opening_time': carshop.opening_time.strftime('%H:%M:%S'),
                'closing_time': carshop.closing_time.strftime('%H:%M:%S'),
            }
        }

        return JsonResponse(response_data, status=201)

    except User.DoesNotExist:
        return JsonResponse({'ERR': 'User not found.'}, status=404)
    except Exception as error:
        return JsonResponse({'ERR': str(error)}, status=400)

from django.utils.dateparse import parse_time

@csrf_exempt
@api_view(['GET', 'PUT'])
def carshop_detail(request, carshop_id):
    """Retrieve or update a car shop by ID."""
    carshop = get_object_or_404(Carshop, id=carshop_id)

    if request.method == 'GET':
        response_data = {
            'carshop_id': carshop.id,
            'user_id': carshop.user.id,
            'shop_name': carshop.shop_name,
            'latitude': carshop.latitude,
            'longitude': carshop.longitude,
            'owner_name': carshop.owner_name,
            'phone1': carshop.phone1,
            'address': carshop.address,
            'upload_carshop_image': carshop.upload_carshop_image.url if carshop.upload_carshop_image else None,
            'opening_time': carshop.opening_time.strftime('%H:%M:%S'),
            'closing_time': carshop.closing_time.strftime('%H:%M:%S'),
            'services': [
                {
                    'id': service.id,
                    'service_name': service.service_name,
                    'cost': service.cost,
                    'description': service.description,
                    'car_type_status': service.car_type_status,
                    'duration_in_hours': service.duration_in_hours,
                }
                for service in carshop.services.all()
            ]
        }
        return JsonResponse(response_data, status=200)

    elif request.method == 'PUT':
        try:
            carshop.shop_name = request.data.get('shop_name', carshop.shop_name)
            carshop.latitude = request.data.get('latitude', carshop.latitude)
            carshop.longitude = request.data.get('longitude', carshop.longitude)
            carshop.owner_name = request.data.get('owner_name', carshop.owner_name)
            carshop.phone1 = request.data.get('phone1', carshop.phone1)
            carshop.address = request.data.get('address', carshop.address)

            opening_time_str = request.data.get('opening_time', None)
            closing_time_str = request.data.get('closing_time', None)

            if opening_time_str:
                carshop.opening_time = parse_time(opening_time_str)
            
            if closing_time_str:
                carshop.closing_time = parse_time(closing_time_str)

            if 'upload_carshop_image' in request.FILES:
                carshop.upload_carshop_image = request.FILES['upload_carshop_image']

            services = request.data.get('services', [])
            if services:
                for service_data in services:
                    service_id = service_data.get('id')
                    if service_id:
                        service_instance = get_object_or_404(Service, id=service_id)
                        service_instance.service_name = service_data.get('service_name', service_instance.service_name)
                        service_instance.cost = service_data.get('cost', service_instance.cost)
                        service_instance.description = service_data.get('description', service_instance.description)
                        service_instance.car_type_status = service_data.get('car_type_status', service_instance.car_type_status)
                        service_instance.duration_in_hours = service_data.get('duration_in_hours', service_instance.duration_in_hours)
                        service_instance.save()

                carshop.services.clear()
                for service_data in services:
                    service_id = service_data.get('id')
                    service_instance = get_object_or_404(Service, id=service_id)
                    carshop.services.add(service_instance)  # Add the service to the car shop

            carshop.save()

            return JsonResponse({
                'message': 'Car shop successfully updated.',
                'carshop_id': carshop.id,
                'user_id': carshop.user.id,
                'carshop_data': {
                    'shop_name': carshop.shop_name,
                    'latitude': carshop.latitude,
                    'longitude': carshop.longitude,
                    'owner_name': carshop.owner_name,
                    'phone1': carshop.phone1,
                    'address': carshop.address,
                    'opening_time': carshop.opening_time.strftime('%H:%M:%S'),
                    'closing_time': carshop.closing_time.strftime('%H:%M:%S'),
                    'upload_carshop_image': carshop.upload_carshop_image.url if carshop.upload_carshop_image else None,
                    'services': [
                        {
                            'id': service.id,
                            'service_name': service.service_name,
                            'cost': service.cost,
                            'description': service.description,
                            'car_type_status': service.car_type_status,
                            'duration_in_hours': service.duration_in_hours,
                        }
                        for service in carshop.services.all()
                    ]
                }
            }, status=200)

        except Exception as error:
            return JsonResponse({'ERR': str(error)}, status=400)



@api_view(['GET'])
def get_carshop_and_bookings(request, phone):
    
    try:
        carshop = Carshop.objects.get(user__phone=phone)
        print("carshop",carshop)

        bookings = Booking.objects.filter(shop=carshop)
        print("bookings",bookings)

        booking_details = [
            {
                "id": booking.id,
                "customer": {
                    "customer_id": booking.customer.id,
                    "name": booking.customer.name,
                    "phone": booking.customer.phone,
                },
                "address": {
                    "address_id": booking.address.id,
                    "street": booking.address.street,
                    "city": booking.address.city,
                    "state": booking.address.state,
                    "postal_code": booking.address.postal_code,
                    "country": booking.address.country,
                },
                "car": {
                    "car_id": booking.car.id,
                    "name": booking.car.car_name,
                    "model": booking.car.model,
                    "color": booking.car.color,
                    "car_number": booking.car.car_number,
                },
                "selected_slot": booking.selected_slot,
                "driver_response": booking.driver_response,
                "booking_status": booking.booking_status,
                "booking_date": booking.booking_date,
                "service": {
                    "service_id": booking.service.id,
                    "service_name": booking.service.service_name,
                    "cost": booking.service.cost,
                }
            }
            for booking in bookings
        ]

        print("booking_details",booking_details)

        carshop_details = {
            "shop_id": carshop.id,
            "shop_name": carshop.shop_name,
            "owner": carshop.owner_name,
            "phone": carshop.user.phone,
            "latitude": carshop.latitude,
            "longitude": carshop.longitude,
            "address": carshop.address,
            "upload_carshop_image_url": carshop.upload_carshop_image.url if carshop.upload_carshop_image else None,
            "services": [service.service_name for service in carshop.services.all()],
            "bookings": booking_details
        }

        print("carshop_details",carshop_details)

        return JsonResponse({'carshop': carshop_details})

    except Carshop.DoesNotExist:
        return JsonResponse({'ERR': 'Carshop not found for this phone number.'}, status=404)
    except Exception as error:
        return HttpResponseNotFound(
            json.dumps({"ERR": str(error)}),
            content_type="application/json",
        )
        
@api_view(['GET'])
def get_accepted_bookings_by_driver(request, phone):
    try:
        # Fetch the driver by phone number
        driver = User.objects.get(phone=phone, role='driver')
        
        # Get all bookings accepted by the driver
        accepted_bookings = Booking.objects.filter(driver=driver, driver_response='Accepted')

        # Prepare booking details for response
        booking_details = [
            {
                "id": booking.id,
                "shop": {
                    "shop_id": booking.shop.id,
                    "shop_name": booking.shop.shop_name,
                    "latitude": booking.shop.latitude,
                    "longitude": booking.shop.longitude,
                    "owner_name": booking.shop.owner_name,
                },
                "customer": {
                    "customer_id": booking.customer.id,
                    "name": booking.customer.name,
                    "phone": booking.customer.phone,
                },
                "address": {
                    "address_id": booking.address.id,
                    "street": booking.address.street,
                    "city": booking.address.city,
                    "state": booking.address.state,
                    "postal_code": booking.address.postal_code,
                    "country": booking.address.country,
                },
                "car": {
                    "car_id": booking.car.id,
                    "name": booking.car.car_name,
                    "model": booking.car.model,
                    "color": booking.car.color,
                    "car_number": booking.car.car_number,
                },
                "selected_slot": booking.selected_slot,
                "driver_response": booking.driver_response,
                "booking_status": booking.booking_status,
                "booking_date": booking.booking_date,
                "service": {
                    "service_id": booking.service.id,
                    "service_name": booking.service.service_name,
                    "cost": booking.service.cost,
                }
            }
            for booking in accepted_bookings
        ]

        return JsonResponse({'accepted_bookings': booking_details}, status=200)

    except User.DoesNotExist:
        return JsonResponse({'ERR': 'Driver not found for this phone number.'}, status=404)
    except Exception as error:
        return HttpResponseNotFound(
            json.dumps({"ERR": str(error)}),
            content_type="application/json",
        )
        
        
@api_view(['PUT'])
def update_booking_status(request, booking_id):
    """url: api/booking/update-status/<booking_id>"""
    try:
        # Fetch the booking by ID
        booking = Booking.objects.get(id=booking_id)

        # Get the new booking status from the request body
        new_status = request.data.get('booking_status')

        # Check if the new status is valid based on the available choices
        valid_statuses = [choice[0] for choice in Booking.Booking_status_choices]
        if new_status not in valid_statuses:
            return JsonResponse({"ERR": "Invalid booking status."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the booking status
        booking.booking_status = new_status
        booking.save()

        return JsonResponse({
            "message": "Booking status updated successfully.",
            "booking_id": booking.id,
            "new_status": booking.booking_status
        })

    except Booking.DoesNotExist:
        return JsonResponse({"ERR": "Booking not found."}, status=404)
    except Exception as error:
        return JsonResponse({"ERR": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def add_service(request):
    """Add a new service."""
    try:
        service_name = request.data.get('service_name')
        cost = request.data.get('cost')
        description = request.data.get('description')
        car_type_status = request.data.get('car_type_status')
        duration_in_hours = request.data.get('duration_in_hours')

        # Create a new Service instance
        service = Service.objects.create(
            service_name=service_name,
            cost=cost,
            description=description,
            car_type_status=car_type_status,
            duration_in_hours=duration_in_hours,
        )

        service.save()

        return JsonResponse({
            'message': 'Service successfully added.',
            'service_id': service.id,
            'service_data': {
                'service_name': service.service_name,
                'cost': service.cost,
                'description': service.description,
                'car_type_status': service.car_type_status,
                'duration_in_hours': service.duration_in_hours,
            }
        }, status=status.HTTP_201_CREATED)
    except Exception as error:
        return JsonResponse({'ERR': str(error)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def service_detail(request, service_id):
    """Retrieve or update a service by ID."""
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'GET':
        # Prepare response data with service details
        response_data = {
            'service_id': service.id,
            'service_name': service.service_name,
            'cost': service.cost,
            'description': service.description,
            'car_type_status': service.car_type_status,
            'duration_in_hours': service.duration_in_hours,
        }
        return JsonResponse(response_data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        try:
            service.service_name = request.data.get('service_name', service.service_name)
            service.cost = request.data.get('cost', service.cost)
            service.description = request.data.get('description', service.description)
            service.car_type_status = request.data.get('car_type_status', service.car_type_status)
            service.duration_in_hours = request.data.get('duration_in_hours', service.duration_in_hours)

            service.save()

            return JsonResponse({
                'message': 'Service successfully updated.',
                'service_id': service.id,
                'service_data': {
                    'service_name': service.service_name,
                    'cost': service.cost,
                    'description': service.description,
                    'car_type_status': service.car_type_status,
                    'duration_in_hours': service.duration_in_hours,
                }
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return JsonResponse({'ERR': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'ERR': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)