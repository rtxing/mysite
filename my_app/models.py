from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid


USER_ROLES = (
        ('user', 'User'),
        ('owner', 'Owner'),
        ('driver', 'Driver'),
    )

class User(AbstractUser):
    phone = models.CharField(max_length=10,unique=True,blank=True,null=True, validators=[RegexValidator(
        regex=r"^\d{10}", message="Phone number must be 10 digits only.")])
    # address = models.TextField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')

    is_user = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    driving_license = models.ImageField(upload_to ='uploads/')
    driving_license_no = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to ='uploads/')
    
    def save(self, *args, **kwargs):
        # Make sure the role isn't getting overridden
        self.is_user = (self.role == 'user')
        self.is_owner = (self.role == 'owner')
        self.is_driver = (self.role == 'driver')
        super().save(*args, **kwargs)

        
    def __str__(self):
        return str(self.id) 

    @classmethod
    def create_superuser(cls, username, email=None, password=None, **kwargs):
        if password is None:
            raise TypeError('Password should not be None')

        # Create the superuser
        user = cls(username=username, email=email, **kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"