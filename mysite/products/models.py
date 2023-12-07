from django.db import models

# Create your models here.





class Items(models.Model):
    item_name = models.CharField(max_length=200)
    price = models.IntegerField()


    def __unicode__(self):
       return self.item_name
