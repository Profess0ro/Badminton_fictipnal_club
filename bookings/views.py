from django.shortcuts import render, redirect, get_object_or_404
from .models import CourtType, StartTimes, EndTimes, Booking
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta

def rules_view(request):
    return render(request, 'rules.html')

@login_required
def create_booking(request):
    if request.method == 'POST':
        court_type_id = request.POST.get('court_type')
        date_str = request.POST.get('date')
        time_slot = request.POST.get('time')  # This will be in the format 'HH:MM-HH:MM'

        # Debugging: Print received data
        print(f"court_type_id: {court_type_id}")
        print(f"date_str: {date_str}")
        print(f"time_slot: {time_slot}")

        # Convert date from string to datetime object
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError as e:
            print(f"Date parsing error: {e}")
            return HttpResponse("Invalid date format.", status=400)

        # Extract start and end times from the selected time slot
        try:
            start_time_str, end_time_str = time_slot.split('-')
        except ValueError:
            return HttpResponse("Invalid time slot format.", status=400)

        # Fetch the start and end times from the database
        try:
            start_time = StartTimes.objects.get(start_time=start_time_str)
            end_time = EndTimes.objects.get(end_time=end_time_str)
        except (StartTimes.DoesNotExist, EndTimes.DoesNotExist):
            return HttpResponse("Invalid time slot.", status=400)

        court_type = get_object_or_404(CourtType, id=court_type_id)

        # Convert start_time and end_time to datetime objects
        start_datetime = datetime.combine(date, start_time.start_time)
        end_datetime = datetime.combine(date, end_time.end_time)

        # Check if the booking duration is within the 2-hour limit
        if (end_datetime - start_datetime).total_seconds() > 2 * 60 * 60:
            return HttpResponse("Booking can only be made for a maximum of 2 hours.", status=400)

        # Check if the selected time slot is already booked
        if Booking.objects.filter(court_type=court_type, date=date, start_time=start_time, end_time=end_time).exists():
            return HttpResponse("This time slot is already booked.", status=400)

        # Create the booking
        booking = Booking.objects.create(
            court_type=court_type,
            date=date,
            start_time=start_time,
            end_time=end_time,
            booked_by=request.user
        )
        return redirect('booking_success', booking_id=booking.id)  # Redirect to the success page

    context = {
        'court_types': CourtType.objects.all(),
        'dates': [datetime.now().date() + timedelta(days=i) for i in range(15)],
    }
    return render(request, 'booking_form.html', context)



@login_required
def booking_form(request):
    if request.method == 'POST':
        court_type_id = request.POST.get('court_type')
        date_str = request.POST.get('date')
        time_slot = request.POST.get('time')  # This will be in the format 'HH:MM-HH:MM'

        # Debugging: Print the form data
        print("Form Data Received:")
        print(f"court_type_id: {court_type_id}")
        print(f"date_str: {date_str}")
        print(f"time_slot: {time_slot}")

        if not time_slot:
            return HttpResponse("Time slot not selected.", status=400)

        # Convert date from string to datetime object
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Invalid date format.", status=400)

        # Extract start and end times from the selected time slot
        try:
            start_time_str, end_time_str = time_slot.split('-')
        except ValueError:
            return HttpResponse("Invalid time slot format.", status=400)

        # Fetch the start and end times from the database
        try:
            start_time = StartTimes.objects.get(start_time=start_time_str)
            end_time = EndTimes.objects.get(end_time=end_time_str)
        except (StartTimes.DoesNotExist, EndTimes.DoesNotExist):
            return HttpResponse("Invalid time slot.", status=400)

        court_type = CourtType.objects.get(id=court_type_id)

        # Convert start_time and end_time to datetime objects
        start_datetime = datetime.combine(date, start_time.start_time)
        end_datetime = datetime.combine(date, end_time.end_time)

        # Check if the booking duration is within the 2-hour limit
        if (end_datetime - start_datetime).total_seconds() > 2 * 60 * 60:
            return HttpResponse("Booking can only be made for a maximum of 2 hours.", status=400)

        # Check if the selected time slot is already booked
        if Booking.objects.filter(court_type=court_type, date=date, start_time=start_time, end_time=end_time).exists():
            return HttpResponse("This time slot is already booked.", status=400)

        # Create the booking
        booking = Booking.objects.create(
            court_type=court_type,
            date=date,
            start_time=start_time,
            end_time=end_time,
            booked_by=request.user
        )
        return redirect('bookings:booking_success', booking_id=booking.id)  # Redirect to the success page

    context = {
        'court_types': CourtType.objects.all(),
        'dates': [datetime.now().date() + timedelta(days=i) for i in range(15)],
    }
    return render(request, 'booking_form.html', context)


def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})

def get_available_times(request):
    court_type_id = request.GET.get('court_type')
    date_str = request.GET.get('date')

    # Parse date
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Retrieve the court type
    court_type = get_object_or_404(CourtType, id=court_type_id)

    # Fetch existing bookings
    bookings = Booking.objects.filter(court_type=court_type, date=date)

    # Fetch start and end times
    start_times = StartTimes.objects.all()
    end_times = EndTimes.objects.all()

    # Create a list to store available time slots in a grid format
    time_grid = []

    for start_time in start_times:
        row = []
        for end_time in end_times:
            if start_time.start_time < end_time.end_time and (end_time.end_time.hour - start_time.start_time.hour) <= 2:
                # Check if this time slot is booked
                if not bookings.filter(start_time=start_time, end_time=end_time).exists():
                    row.append({
                        'start_time': start_time.start_time.strftime('%H:%M'),
                        'end_time': end_time.end_time.strftime('%H:%M')
                    })
        if row:
            time_grid.append(row)

    return JsonResponse({'time_grid': time_grid})
