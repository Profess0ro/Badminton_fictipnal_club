from django.shortcuts import render
from django.views import View
from .models import AboutUs


class AboutUsView(View):
    """
    View to display the 'About Us' page content.

    This view retrieves the first instance of the AboutUs model and renders it
    on the 'About Us' page. If no content is found in the database,
    a default message is displayed that the content is not available.

    Methods:
        get: Handles GET requests to display the 'About Us' content.
    """
    def get(self, request, *args, **kwargs):
        content = AboutUs.objects.first()
        if content:
            return render(request, "aboutus.html", {"content": content})
        else:
            return render(request, "aboutus.html",
                          {"content": "Content not found."})
