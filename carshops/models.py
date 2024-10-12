from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from my_app.models import User
# Create your models here.


class Carshop(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carshops')

  shop_name = models.CharField(max_length=255)
  latitude = models.CharField(max_length=255)
  longitude = models.CharField(max_length=255)
  owner_name = models.CharField(max_length=255)
  phone1 = models.CharField(max_length=255)
  address = models.TextField()
  upload_carshop_image = models.ImageField(upload_to ='uploads/') 
  services = models.ManyToManyField('Service')
  # time_for_wash = models.IntegerField()
  opening_time = models.TimeField(default='09:00:00') 
  closing_time = models.TimeField(default='17:00:00')
  
  def __str__(self):
  	return str(self.id)


class Rating(models.Model):
  stars = models.IntegerField()
  review = models.CharField(max_length=255)
  booking = models.ForeignKey(
        "Booking",
        on_delete=models.CASCADE,
    )
  
  def __str__(self):
  	return str(self.id)



class Booking(models.Model):
  shop = models.ForeignKey(
        "Carshop",
        on_delete=models.CASCADE,
    )
  customer = models.ForeignKey(
        "my_app.User",
        on_delete=models.CASCADE, related_name = "cscustuser"
    )
  address = models.ForeignKey(
        "my_app.Address",
        on_delete=models.CASCADE,
        related_name="booking_address"
    )
  car = models.ForeignKey(
        "Car",
        on_delete=models.CASCADE,
        related_name="booking_car"
    )
    
  driver = models.BooleanField()
  driver = models.ForeignKey(
        "my_app.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='driver_bookings'
    )
  # date_time = models.TimeField()
  selected_slot = models.CharField(max_length=50)  # Store the selected time slot
  driver_response = models.CharField(max_length=20, null=True, blank=True ,default="Pending")  # 'Accepted' or 'Rejected'

  service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE, related_name = "bkservice"
    )
  Booking_status_choices = (
    ("In_Progress", "In Progress"),
    ("Completed", "Completed"),
    ("On_Way_To_Pickup", "On Way to Pickup"),
    ("Cancelled", "Cancelled")
  )
  booking_status = models.CharField(max_length=20,
                  choices=Booking_status_choices, default = "In_Progress"
                  )
  created_at = models.DateTimeField(auto_now_add=True)
  booking_date = models.DateField(blank=True, null=True) 


  def __str__(self):
    return str(self.id)


class Car(models.Model):
  car_name = models.CharField(max_length=255)
  model = models.CharField(max_length=255)
  color = models.CharField(max_length=255)
  car_number = models.TextField()
  customer = models.ForeignKey(
        "my_app.User",
        on_delete=models.CASCADE, related_name = "carcustuser"
    )
  upload = models.ImageField(upload_to ='uploads/') 
  rc_photo = models.ImageField(upload_to ='uploads/') 
  insurance_photo  = models.ImageField(upload_to ='uploads/')

  car_type_choices = (
    ("Sedan", "Sedan"),
    ("Hatch_Back", "Hatch Back")
  )
  car_type = models.CharField(max_length=20,
                  choices=car_type_choices
                  )

  def __str__(self):
    return str(self.id)



from datetime import timedelta


class Service(models.Model):
  service_name = models.CharField(max_length=255)
  cost = models.CharField(max_length=255, blank=True, null = True)
  description = models.CharField(max_length=255, blank=True, null = True)
  car_type_choices = (
    ("Sedan", "Sedan"),
    ("Hatch_Back", "Hatch Back")
  )
  car_type_status = models.CharField(max_length=20,
                  choices=car_type_choices
                  )
  duration_in_hours = models.CharField(max_length=255)

  @property
  def duration(self):
      return timedelta(hours=self.duration_in_hours)
      

  def __str__(self):
    return str(self.id)

  	

class CarPickupPhoto(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="pickup_photos")
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    image = models.ImageField(upload_to='uploads/car_pickup/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pickup Photo {self.id} for Booking {self.booking.id}"


class CarWashPhoto(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="wash_photos")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/car_wash/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wash Photo {self.id} for Booking {self.booking.id}"
      

class Notification(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)



# class Post(models.Model):
#   posted_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#   posted_date_time = models.DateTimeField()
#   description = models.TextField()


#   def __str__(self):
#     return str(self.id)


# class Comment(models.Model):
#   post = models.ForeignKey(Post,on_delete=models.CASCADE)
#   posted_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#   posted_date_time = models.DateTimeField()
#   description = models.TextField()


#   def __str__(self):
#     return str(self.id)


# class Job(models.Model):
#   title = models.CharField(max_length=255)
#   posted_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#   posted_date_time = models.DateTimeField()
#   location = models.CharField(max_length=255)
#   description = models.TextField()


#   def __str__(self):
#     return str(self.title)



# class Event(models.Model):
#   title = models.CharField(max_length=255)
#   posted_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#   date_time = models.DateTimeField()
#   location = models.CharField(max_length=255)
#   description = models.TextField()


#   def __str__(self):
#     return str(self.title)



# class MarketPlaceCategory(models.Model):
#   title = models.CharField(max_length=255)
  

#   def __str__(self):
#     return str(self.title)



# class MarketPlace(models.Model):
#   title = models.CharField(max_length=255)
#   posted_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#   category = models.ForeignKey(MarketPlaceCategory,on_delete=models.CASCADE)
#   location = models.CharField(max_length=255)
#   description = models.TextField()
#   price = models.IntegerField()
  
#   def __str__(self):
#     return str(self.title)


