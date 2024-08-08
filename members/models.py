from django.db import models

# Create your models here.
'''
class Member(models.Model):
  name = models.CharField(max_length=255)
  phone = models.CharField(max_length=255)
  address = models.TextField()
  notes = models.TextField()
  paid = models.TextField()



class Member_Payment(models.Model):
  member = models.ForeignKey(Member, on_delete=models.CASCADE)
  payment_date = models.DateField()
  mode_of_payment = models.CharField(max_length=255)
  amount = models.IntegerField()
  paid = models.TextField()

class Service_provider(models.Model):
  name = models.CharField(max_length=255)
  phone_1 = models.CharField(max_length=255)
  phone_2 = models.CharField(max_length=255)
  phone_3 = models.CharField(max_length=255)
  address = models.TextField()
  notes = models.TextField()


class Vehicle(models.Model):
  service_provider = models.ForeignKey(Service_provider, on_delete=models.CASCADE)
  driver_phone_1 = models.CharField(max_length=255)
  driver_phone_2 = models.CharField(max_length=255)
  driver_phone_3 = models.CharField(max_length=255)
  live_address = models.TextField()
  notes = models.TextField()

class Call_log(models.Model):
  member = models.ForeignKey(Member, on_delete=models.CASCADE)
  called_datetime = models.DateTimeField()
  vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
  tele_caller = models.ForeignKey(Member, on_delete=models.CASCADE)
  notes = models.TextField()





class SP_Payment(models.Model):
  service_provider = models.ForeignKey(Service_provider, on_delete=models.CASCADE)
  payment_date = models.DateField()
  mode_of_payment = models.CharField(max_length=255)
  amount = models.IntegerField()
  notes = models.TextField()

'''