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

from carshops.views import CarshopViewSet,carshop_id,BookingViewSet
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework.routers import DefaultRouter
router = DefaultRouter() 
router.register(r'carshops', CarshopViewSet)
router.register(r'booking', BookingViewSet)


urlpatterns = [
    #path('api/', include((router.urls, 'carshops'), namespace='carshop')),
    path('api/auth2/', include('my_app.urls')),
    path("api/carshops/<int:id>/<str:userid>/", carshop_id, name ='carsingle'),
    path('api/carshops/<str:lat>/<str:longt>/<str:userid>/', csviews.carshops_geo, name= "geocars"),
    path('api/booking2/', csviews.booking2, name= "booking2"),
    path('api/get_previous_orders/<int:userid>/', csviews.get_previous_orders, name= "get_previous_orders"),
    path('api/detailbooking/<int:bookingid>/', csviews.detailbooking, name= "detailbooking"),

    path('nearones', views.nearones, name='nearones'),
    path('nearones2', views.nearones2, name='nearones2'),

    #path('map', views.map, name='map'),
    #path('booking', views.booking, name='booking'),
    #path('nearhome', views.nearhome, name='nearones2'),
    path('hubio', views.hubio, name='hubio'),
    path('milk', views.milk, name='milk'),
    path('milk2', views.milk2, name='milk2'),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()
