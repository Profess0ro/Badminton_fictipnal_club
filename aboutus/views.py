from django.shortcuts import render
from django.views import View
from .models import AboutUs

class AboutUsView(View):
    def get(self, request, *args, **kwargs):
        content = AboutUs.objects.first()
        if content:
            return render(request, "aboutus.html", {"content": content})
        else:
            return render(request, "aboutus.html", {"content": "Content not found."})