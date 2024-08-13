from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Court
from django.utils import timezone
from datetime import datetime
from .forms import BookingForm
from .utils import calculate_available_times  

@login_required
def list_courts(request):
    courts = Court.objects.all()
    return render(request, 'list_courts.html', {'courts': courts})


@login_required
@login_required
def make_booking(request, court_id=None):
    if court_id is None:
        return redirect('list_courts')
    
    court = get_object_or_404(Court, pk=court_id)
    available_times = calculate_available_times(court)  

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_time_str = request.POST.get('booking-time')
            duration = int(form.cleaned_data['duration'])

            
            booking_time = datetime.strptime(booking_time_str, "%H:%M").time()
            start_datetime = timezone.make_aware(
                timezone.datetime.combine(timezone.now().date(), booking_time)
            )
            end_datetime = start_datetime + timezone.timedelta(hours=duration)
            
            booking = form.save(commit=False)
            booking.start_time = start_datetime
            booking.end_time = end_datetime
            booking.court = court
            booking.save()
            return redirect('list_courts')
    else:
        form = BookingForm(initial={'court': court.id, 'duration': 1})

    return render(request, 'make_booking.html', {'court': court, 'available_times': available_times, 'form': form})