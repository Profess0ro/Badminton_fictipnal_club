from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_courts, name='list_courts'),
    path('make_booking/', views.make_booking, name='make_booking'),
]