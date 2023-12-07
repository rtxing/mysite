from django.contrib import admin

# Register your models here.
from products.models import Items

# Register your models here.

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    pass
