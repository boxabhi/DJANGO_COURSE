from django.contrib import admin

# Register your models here.
from accounts.models import CustomUser

admin.site.register(CustomUser)