from django.db import models

# Create your models here.


class Project(models.Model):
	Project_CHOICES =( 
    ("CIOX", "CIOX"), 
    ("Centine", "Centine"), 
	) 
	name = models.CharField(max_length=20, choices = Project_CHOICES)
	scope_from = models.IntegerField(null=True, blank=True)
	scope_to = models.IntegerField(null=True, blank=True)
	version = models.CharField(max_length=20)

	def __str__(self):
		return str(self.id) 
