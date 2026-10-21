from django.db import models


#Модель содержит страны, которые доступны для бронирования отелей
class Countries(models.Model):
    country = models.CharField(max_length=50, null=False)
    slug = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table='Countries'

    def __str__(self):
        return f'Модель стран - {self.country}'


#Модель отелей всех стран
class Hotels(models.Model):
    hotel_name = models.CharField(max_length=50)
    country_id = models.ForeignKey('Countries', on_delete=models.CASCADE, null=False)
    slug = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table='Hotels'

    def __str__(self):
        return f'Модель отелей - {self.hotel_name}'

#Модель комнат всех стран
class Rooms(models.Model):
    hotel_id = models.ForeignKey('Hotels', on_delete=models.CASCADE, null=False)
    room_num = models.IntegerField(null=False)
    room_type = models.CharField(max_length=50, default='soft', null=False)

    class Meta:
        db_table='Rooms'

    def __str__(self):
        return f'Модель комнат - {self.hotel_id}, {self.room_num}'

#Модель резерваций комнат(связь только по айди комнаты, потому что комната уже имеет айди отеля)
class Booking(models.Model):
    room_id = models.ForeignKey('Rooms', on_delete=models.PROTECT, null=False)
    check_in = models.DateField(null=False)
    check_out = models.DateField(null=False)

    class Meta:
        db_table='Booking'

    def __str__(self):
        return f'Модель бронирований - {self.pk}'

