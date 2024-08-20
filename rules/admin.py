from django.contrib import admin
from .models import Rules
from django_summernote.admin import SummernoteModelAdmin

class RulesAdmin(SummernoteModelAdmin):
    list_display = ('content',)
    summernote_fields = ('content',)

admin.site.register(Rules, RulesAdmin)