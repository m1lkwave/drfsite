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
        read_only_fields = ('country_id',)

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ('__all__')

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, attrs):
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')

        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError({
                'check_out': 'Дата выезда должна быть позже даты заезда'
            })

        return attrs