"""
URL configuration for racketclub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from aboutus.views import AboutUsView
from contact.views import contact, success
from booking.urls import urlpatterns as booking_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('about/', AboutUsView.as_view(), name='aboutus'),
    path('contact/', contact, name='contact'),
    path('success/', success, name='success'),
    path('accounts/', include('allauth.urls')),
    path('booking/', include(booking_urls)),
    path('', include('articles.urls'), name='articles_url'),
]
