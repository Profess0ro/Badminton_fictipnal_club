from django.contrib import admin
from django.urls import path, include
from aboutus.views import AboutUsView
from contact.views import contact, success
from rules.views import RulesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('about/', AboutUsView.as_view(), name='aboutus'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('contact/', contact, name='contact'),
    path('success/', success, name='success'),
    path('accounts/', include('allauth.urls')),
    path('', include('articles.urls'), name='articles_url'),
    path('bookings/', include('bookings.urls')), 
]