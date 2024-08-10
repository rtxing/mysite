from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from my_app.models import User
# Create your models here.


class Carshop(models.Model):
  shop_name = models.CharField(max_length=255)
  latitude = models.CharField(max_length=255)
  longitude = models.CharField(max_length=255)
  owner_name = models.CharField(max_length=255)
  phone1 = models.CharField(max_length=255)
  address = models.TextField()
  upload_carshop_image = models.ImageField(upload_to ='uploads/') 
  services = models.ManyToManyField('Service')
  time_for_wash = models.IntegerField()

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
  driver = models.BooleanField()
  date_time = models.DateTimeField()
  #services = models.ManyToManyField(Service)
  Booking_status_choices = (
    ("In_Progress", "In Progress"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled")
  )
  booking_status = models.CharField(max_length=20,
                  choices=Booking_status_choices, default = "In_Progress"
                  )


  def __str__(self):
    return str(self.id)


class Car(models.Model):
  car_name = models.CharField(max_length=255)
  model = models.CharField(max_length=255)
  color = models.CharField(max_length=255)
  car_number = models.TextField()
  upload = models.ImageField(upload_to ='uploads/') 


  def __str__(self):
    return str(self.id)





class Service(models.Model):
  service_name = models.CharField(max_length=255)
  cost = models.CharField(max_length=255, blank=True, null = True)
  description = models.CharField(max_length=255, blank=True, null = True)
  

  def __str__(self):
    return str(self.service_name)

  	


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


