from rest_framework import serializers
from .models import Booking, Countries, Hotels, Rooms

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ('country', )

class HotelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotels
        fields = ('hotel_name', 'country_id', 'slug')

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ('__all__')

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('__all__')