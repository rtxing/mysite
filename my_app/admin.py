from django.contrib import admin
from my_app.models import Address, User
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'name', 'role', 'is_user', 'is_owner', 'is_driver')
    # Ensure 'role' is in list_display to view it in the admin panel
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'latitude', 'longitude', 'phone')}),
    )


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'street', 'city', 'state', 'postal_code', 'country')
    search_fields = ('user__username', 'street', 'city', 'state', 'postal_code', 'country')
    list_filter = ('state', 'country')

admin.site.register(Address, AddressAdmin)
# 
admin.site.register(User, UserAdmin)