from django.shortcuts import render
from django.views import View
from .models import Rules

class RulesView(View):
    """
    View to display the 'Rules' page content.
    This 'Rules' page are shown to the user before they can book a time.

    This view retrieves the first instance of the Rules model and renders it
    on the 'Rules' page. If no content is found in the database,
    a default message is displayed that the content is not available.

    Methods:
        get: Handles GET requests to display the 'Rules' content.
    """
    def get(self, request, *args, **kwargs):
        content = Rules.objects.first()
        if content:
            return render(request, "rules.html", {"content": content})
        else:
            return render(request, "rules.html", {"content": "Content not found."})