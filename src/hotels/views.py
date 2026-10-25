from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins

from . import models
from . import serializers

#Класс для передачи Стран в JSON формате - только GET запрос
class CountryAPIList(generics.ListAPIView):
    queryset = models.Countries.objects.all()
    serializer_class = serializers.CountrySerializer

#Класс для отображения отелей по заданной стране(с человекочитаемым url) - GET и POST запрос
class CountryHotelAPIList(generics.ListCreateAPIView):
    serializer_class = serializers.HotelsSerializer

    def get_country(self):
        return get_object_or_404(
            models.Countries,
            slug=self.kwargs['country']
        )

    def get_queryset(self):
        country = self.get_country()
        return models.Hotels.objects.filter(country_id=country.id)

    def perform_create(self, serializer):
        country = self.get_country()
        serializer.save(country_id=country)

#Класс для отображения всех комнат под указанный отель(человекочитаемый юрл) - только GET запрос
class HotelRoomsAPIView(generics.ListAPIView):
    serializer_class = serializers.RoomsSerializer

    def get_queryset(self):
        hotel = self.kwargs['hotel']

        if not models.Hotels.objects.filter(slug=hotel).exists():
            raise Http404('такого отеля нет')

        hotel_id = models.Hotels.objects.get(slug=hotel)

        return models.Rooms.objects.filter(hotel_id=hotel_id.pk)

#Класс для изменения данных комнаты - только PUT запрос
class RoomsAPIUpdate(generics.UpdateAPIView):
    serializer_class = serializers.RoomsSerializer
    
    def get_queryset(self):
            pk = self.kwargs['pk']
    
            if not models.Rooms.objects.filter(pk=pk).exists():
                raise Http404('такого отеля нет')
    
            return models.Rooms.objects.filter(pk=pk)

#Создать и посмотреть резервации для комнаты - GET и POST запрос
class BookingRoomsAPICreateView(generics.ListCreateAPIView):
    serializer_class = serializers.BookingSerializer

    def get_room(self):
        return get_object_or_404(
            models.Rooms,
            pk=self.kwargs['pk']
        )

    def get_queryset(self):
        room = self.get_room()
        return models.Booking.objects.filter(room_id=room.pk)

    def perform_create(self, serializer):
        room = self.get_room()
        serializer.save(room=room)

#Класс для удаления резервации - только запрос DELETE
class BookingAPIDelete(generics.DestroyAPIView):
    serializer_class = serializers.BookingSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']

        if not models.Booking.objects.filter(pk=pk).exists():
            raise Http404('такой резервации нет')

        return models.Booking.objects.filter(pk=pk)

        