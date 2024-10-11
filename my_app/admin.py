from django.contrib import admin
from .models import User, Address

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone','otp', 'role', 'is_user', 'is_owner', 'is_driver')
    list_filter = ('role', 'is_user', 'is_owner', 'is_driver')
    search_fields = ('username', 'email', 'phone')
    readonly_fields = ('is_user', 'is_owner', 'is_driver')

admin.site.register(User, UserAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'street', 'city', 'state', 'postal_code', 'country')
    search_fields = ('user__username', 'street', 'city', 'state', 'postal_code', 'country')

admin.site.register(Address, AddressAdmin)
