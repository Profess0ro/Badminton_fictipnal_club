from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Court, Booking
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import BookingForm
from .utils import calculate_available_times, calculate_available_times_for_date
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin



def booking_info(request):
    return render(request, 'booking.html')


@login_required
def select_court(request):
    courts = Court.objects.all()
    return render(request, 'select_court.html', {'courts': courts})



@login_required
def make_booking(request, court_id=None):
    if court_id is None:
        return redirect('list_courts')
    
    court = get_object_or_404(Court, pk=court_id)
    available_times = []  # Initialize an empty list for available times

    if request.method == 'POST':
        form = BookingForm(request.POST)
        selected_date_str = request.POST.get('booking-date')
        
        if selected_date_str:
            selected_date = timezone.datetime.strptime(selected_date_str, "%Y-%m-%d").date()
            available_times = calculate_available_times_for_date(court, selected_date)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.court = court

            # Set start_time and end_time manually if needed
            booking.start_time = form.cleaned_data['start_time']
            booking.end_time = form.cleaned_data['end_time']
            
            booking.save()

            # Redirect to the booking success page
            return redirect('booking_success', booking_id=booking.id)
        else:
            print("Form errors:", form.errors)  # Debugging line to print form errors
    else:
        form = BookingForm(initial={'court': court.id, 'duration': 1})
        available_times = calculate_available_times_for_date(court, timezone.now().date())

    return render(request, 'make_booking.html', {
        'court': court, 
        'form': form, 
        'available_times': available_times, 
        'current_date': timezone.now().date(),
        'max_future_date': (timezone.now() + timedelta(days=30)).date(),
    })



@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    print("Redirecting to booking success page with booking_id:", booking.id)
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
    booking = get_object_or_404(Booking, pk=booking_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)

        if form.is_valid():
            booking_time_str = request.POST.get('booking-time')
            duration = int(form.cleaned_data['duration'])

            # Parse the time in 24-hour format using datetime.time()
            booking_time = datetime.strptime(booking_time_str, "%H:%M").time()
            start_datetime = timezone.make_aware(
                datetime.combine(timezone.now().date(), booking_time)
            )
            end_datetime = start_datetime + timezone.timedelta(hours=duration)

            # Update the booking instance with the new times
            booking.start_time = start_datetime
            booking.end_time = end_datetime

            # Save the updated booking
            booking.save()

            # Redirect to the 'my_bookings' page after saving
            return redirect('my_bookings')
    else:
        form = BookingForm(instance=booking)

    # Prepare the context with form and any other data
    context = {
        'form': form,
        'booking': booking,
        'available_times': calculate_available_times(booking.court)  # Assuming you have this function
    }

    # Render the edit_booking.html template
    return render(request, 'edit_booking.html', context)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    booking.delete()
    return redirect('my_bookings')