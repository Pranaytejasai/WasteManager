from django.contrib import admin
from .models import UserProfile, Address

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Address)