from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Court, Booking

@login_required
def list_courts(request):
    courts = Court.objects.all()
    return render(request, 'list_courts.html', {'courts': courts})

@login_required
def make_booking(request, court_id):
    court = Court.objects.get(id=court_id)
    if request.method == 'POST':
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        Booking.objects.create(court=court, start_time=start_time, end_time=end_time)
        return redirect('list_courts')
    else:
        return render(request, 'make_booking.html', {'court': court})
