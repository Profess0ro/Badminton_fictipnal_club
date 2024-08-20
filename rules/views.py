from django.shortcuts import render
from django.views import View
from .models import Rules

class RulesView(View):
    def get(self, request, *args, **kwargs):
        content = Rules.objects.first()
        if content:
            return render(request, "rules.html", {"content": content})
        else:
            return render(request, "rules.html", {"content": "Content not found."})