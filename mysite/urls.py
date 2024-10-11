"""
URL configuration for schedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from members import views
from carshops import views as csviews

from carshops.views import BookingDetailAPIView, CarshopViewSet, add_carshop, car_pickup_photos, car_wash_photos, carshop_detail,carshop_id,BookingViewSet, create_booking, fetch_available_slots, get_cars_by_phone, get_carshop_and_bookings, get_driver_bookings, get_driver_notifications, respond_to_booking, update_car_details
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework.routers import DefaultRouter
router = DefaultRouter() 
router.register(r'carshops', CarshopViewSet)
router.register(r'booking', BookingViewSet)
from my_app.views import get_addresses_by_phone, login_view, update_address, update_user, verify_view, add_address
#from kensist import views as kenviews
from campaign import views as campviews


urlpatterns = [
    #path('api/', include((router.urls, 'carshops'), namespace='carshop')),
    path('api/', include('my_app.urls')),
    path("api/carshops/<int:id>/<str:phone>/", carshop_id, name ='carsingle'),
    path('api/auth2/login/', login_view, name="login_view"),
    path('api/auth2/verify-otp/', verify_view, name="verify_view"),
    path('api/carshops/<str:lat>/<str:longt>/', csviews.carshops_geo, name= "geocars"),
    # path('api/booking2/', csviews.booking2, name= "booking2"),
    path('api/get_previous_orders/<int:phone>/', csviews.get_previous_orders, name= "get_previous_orders"),
    path('api/detailbooking/<int:bookingid>/', csviews.detailbooking, name= "detailbooking"),
    path('api/add_car_details/', csviews.add_car_details, name= "detailboadd_car_detailsking"),
    path('api/get_services/', csviews.get_services, name= "get_services"),
    path('api/add_review/', csviews.add_review, name= "add_review"),
    #path('kensist', kenviews.home, name='kensist'),
    #path('kensist/get_project/<str:project>', kenviews.get_project, name='get_project'),
    path('nearones', views.nearones, name='nearones'),
    path('nearones2', views.nearones2, name='nearones2'),
    #path('xing', kenviews.xing, name='xing'),
    #path('campaign/', include('campaign.urls')),
    path('campaign/', campviews.send_bulk_email, name='send_email'),

    #path('map', views.map, name='map'),
    #path('booking', views.booking, name='booking'),
    path('nearhome', views.nearhome, name='nearones2'),
    path('hubio', views.hubio, name='hubio'),
    path('milk', views.milk, name='milk'),
    path('milk2', views.milk2, name='milk2'),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('add-address/', add_address, name='add_address'),
    path('addresses/<str:phone>/', get_addresses_by_phone, name='get_addresses_by_phone'),
    path('updateaddress/<int:address_id>/', update_address, name='update_address'),
    path('api/car/<str:phone>/', get_cars_by_phone, name='get_cars_by_phone'),  # URL pattern for phone
    path('api/car/update/<int:id>/', update_car_details, name='update_car_details'),  # URL pattern for updating car
    path('update_user/<int:user_id>/', update_user, name='update_user'),
    path('api/fetch_available_slots/', fetch_available_slots, name='fetch_available_slots'),
    path('api/create_booking/', create_booking, name='create_booking'),


    #Driver Booking
    path('api/get_driver_notifications/<str:driver_phone>/', get_driver_notifications, name='get_driver_notifications'),  # Include phone in the path

    path('respond_to_booking/<int:booking_id>/', respond_to_booking, name='respond_to_booking'),
    path('api/bookings/<int:booking_id>/', BookingDetailAPIView.as_view(), name='booking_detail'),
    path('api/driver/bookings/<str:driver_phone>/', get_driver_bookings, name='get_driver_bookings'),

    path('api/booking/<int:booking_id>/pickup_photos/<str:driver_phone>/', car_pickup_photos, name='car_pickup_photos'),
    path('car-wash-photos/<int:booking_id>/<str:user_phone>/', car_wash_photos, name='car_wash_photos'),
    
    
    path('api/carshop/add/', add_carshop, name='add_carshop'),  
    path('carshops/<int:carshop_id>/', carshop_detail, name='carshop_detail'),
    
    #to get Booking aganist to the carshop
    path('api/carshop/<str:phone>/', get_carshop_and_bookings, name='get_carshop_and_bookings'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()
