from django.urls import path
from . import views


urlpatterns = [
    path('api/countries/', views.CountryAPIList.as_view()),
    path('api/country/<slug:country>/hotels/', views.CountryHotelAPIList.as_view()),
    path('api/hotel/<slug:hotel>/rooms/', views.HotelRoomsAPIView.as_view()),
    path('api/room/<int:pk>/', views.RoomsAPIUpdate.as_view()),
    path('api/room/<int:pk>/reservations/', views.BookingRoomsAPICreateView.as_view()),
    path('api/reservation/<int:pk>/', views.BookingAPIDelete.as_view())
]