from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Carshop

# @receiver(post_save, sender=Carshop, dispatch_uid="update_image_path")
# def update_image_path(sender, instance, **kwargs):
# 	print(instance.upload4.url)
# 	i = Carshop.objects.get(id = instance.id)
# 	i.image_path = i.upload4.url
# 	i.save()
# 	#print(dir(instance))