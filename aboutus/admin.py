from django.contrib import admin
from .models import AboutUs
from django_summernote.admin import SummernoteModelAdmin


class AboutUsAdmin(SummernoteModelAdmin):
    list_display = ('content',)
    summernote_fields = ('content',)

admin.site.register(AboutUs, AboutUsAdmin)