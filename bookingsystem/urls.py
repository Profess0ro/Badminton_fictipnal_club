from django.urls import path
from .views import BookingListView, BookingCreateView, BookingUpdateView, BookingDeleteView

urlpatterns = [
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking-delete'),
]
