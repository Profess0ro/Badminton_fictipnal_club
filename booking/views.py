from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Court, Booking
from django.utils import timezone
from datetime import datetime
from .forms import BookingForm
from .utils import calculate_available_times
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def list_courts(request):
    courts = Court.objects.all()
    return render(request, 'list_courts.html', {'courts': courts})



@login_required
def make_booking(request, court_id=None):
    if court_id is None:
        return redirect('list_courts')
    
    court = get_object_or_404(Court, pk=court_id)
    available_times = calculate_available_times(court)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        booking_time_str = request.POST.get('booking-time')
        duration = int(form.data['duration'])

        # Parse the time in 24-hour format using datetime.time()
        booking_time = datetime.strptime(booking_time_str, "%H:%M").time()
        start_datetime = timezone.make_aware(
            datetime.combine(timezone.now().date(), booking_time)
        )
        end_datetime = start_datetime + timezone.timedelta(hours=duration)
        
        # Update the form's instance with start_time and end_time
        form.instance.start_time = start_datetime
        form.instance.end_time = end_datetime
        form.instance.court = court

        # Check if the selected time slot overlaps with existing bookings
        overlapping_bookings = Booking.objects.filter(
            court=court,
            start_time__lt=end_datetime,
            end_time__gt=start_datetime,
        )
        
        if overlapping_bookings.exists():
            form.add_error(None, "This time slot is already booked. Please choose another time.")
        
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            
            # Redirect to booking success page
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm(initial={'court': court.id, 'duration': 1})

    return render(request, 'make_booking.html', {'court': court, 'available_times': available_times, 'form': form})


@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})

class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # Filter bookings to only show those of the logged-in user
        return Booking.objects.filter(user=self.request.user).order_by('-start_time')


@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('my_bookings')
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    booking.delete()
    return redirect('my_bookings')