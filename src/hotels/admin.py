from django.contrib import admin
from .models import Countries, Hotels, Rooms, Booking

admin.site.register(Countries)
admin.site.register(Hotels)
admin.site.register(Rooms)
admin.site.register(Booking)

