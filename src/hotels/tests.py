
import pytest
from datetime import date

from rest_framework import status
from rest_framework.test import APIClient

from .models import Countries, Hotels, Rooms, Booking


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def country(db):
    return Countries.objects.create(
        country="Estonia",
        slug="estonia",
    )


@pytest.fixture
def hotel(country):
    return Hotels.objects.create(
        hotel_name="Test Hotel",
        slug="test-hotel",
        country_id=country,
    )


@pytest.fixture
def room(hotel):
    return Rooms.objects.create(
        hotel_id=hotel,
        room_num=101,
        room_type="soft",
    )


@pytest.fixture
def booking(room):
    return Booking.objects.create(
        room_id=room,
        check_in=date(2026, 11, 1),
        check_out=date(2026, 11, 5),
    )


@pytest.mark.django_db
def test_get_countries(api_client, country):
    response = api_client.get("/api/countries/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_hotels_by_country(api_client, country, hotel):
    response = api_client.get(
        f"/api/country/{country.slug}/hotels/"
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_rooms_by_hotel(api_client, hotel, room):
    response = api_client.get(
        f"/api/hotel/{hotel.slug}/rooms/"
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_room(api_client, room):
    response = api_client.patch(
        f"/api/room/{room.pk}/update/",
        {"room_type": "deluxe"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_room_reservations(api_client, room, booking):
    response = api_client.get(
        f"/api/room/{room.pk}/reservations/"
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_booking(api_client, room):
    response = api_client.post(
        f"/api/room/{room.pk}/reservations/",
        {
            "room_id": room.pk,
            "check_in": "2026-12-01",
            "check_out": "2026-12-05",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_get_booking(api_client, booking):
    response = api_client.get(
        f"/api/reservation/{booking.pk}/delete/"
    )

    # Этот URL может поддерживать только удаление.
    # Если GET не разрешён, ожидаем 405 Method Not Allowed.
    assert response.status_code in (
        status.HTTP_200_OK,
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@pytest.mark.django_db
def test_delete_booking(api_client, booking):
    booking_id = booking.pk

    response = api_client.delete(
        f"/api/reservation/{booking_id}/delete/"
    )

    assert response.status_code in (
        status.HTTP_200_OK,
        status.HTTP_204_NO_CONTENT,
    )

    assert not Booking.objects.filter(pk=booking_id).exists()