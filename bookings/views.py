from django.shortcuts import render, redirect, get_object_or_404
from .models import CourtType, StartTimes, EndTimes, Booking
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta


def rules_view(request):
    return render(request, 'rules.html')


@login_required
def booking_view(request):
    if request.method == 'POST':
        court_type_id = request.POST.get('court_type')
        date_str = request.POST.get('date')
        time_slot = request.POST.get('time')

        print(f"court_type_id: {court_type_id}")
        print(f"date_str: {date_str}")
        print(f"time_slot: {time_slot}")

        if not time_slot:
            return HttpResponse("Time slot is empty.", status=400)

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Invalid date format.", status=400)

        try:
            start_time_str, end_time_str = time_slot.split('-')
            print(f"Start time string: {start_time_str}")
            print(f"End time string: {end_time_str}")
            start_time_24 = datetime.strptime(
                start_time_str.strip(), '%I:%M %p').time()
            end_time_24 = datetime.strptime(
                end_time_str.strip(), '%I:%M %p').time()
            print(f"Parsed start time: {start_time_24}")
            print(f"Parsed end time: {end_time_24}")
        except ValueError:
            return HttpResponse("Invalid time slot format.", status=400)

        try:
            start_time = StartTimes.objects.get(start_time=start_time_24)
            end_time = EndTimes.objects.get(end_time=end_time_24)
        except (StartTimes.DoesNotExist, EndTimes.DoesNotExist) as e:
            print(f"Database lookup error: {e}")
            return HttpResponse("Invalid time slot.", status=400)

        court_type = get_object_or_404(CourtType, id=court_type_id)
        start_datetime = datetime.combine(date, start_time.start_time)
        end_datetime = datetime.combine(date, end_time.end_time)

        if (end_datetime - start_datetime).total_seconds() > 2 * 60 * 60:
            return HttpResponse(
                "Booking can only be made for a maximum of 2 hours.",
                status=400)

        overlapping_bookings = Booking.objects.filter(
            court_type=court_type,
            date=date,
            start_time__start_time__lt=end_time.end_time,
            end_time__end_time__gt=start_time.start_time
        )
        if overlapping_bookings.exists():
            return HttpResponse(
                "The time overlaps with an existing booking.",
                status=400)

        booking = Booking.objects.create(
            court_type=court_type,
            date=date,
            start_time=start_time,
            end_time=end_time,
            booked_by=request.user
        )
        return redirect('booking_success', booking_id=booking.id)

    else:
        context = {
            'court_types': CourtType.objects.all(),
            'dates': [
                datetime.now().date() + timedelta(days=i) for i in range(15)],
        }
        return render(request, 'booking_form.html', context)


def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})


def get_available_times(request):
    court_type_id = request.GET.get('court_type')
    date_str = request.GET.get('date')

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    court_type = get_object_or_404(CourtType, id=court_type_id)
    bookings = Booking.objects.filter(court_type=court_type, date=date)
    start_times = StartTimes.objects.all()
    end_times = EndTimes.objects.all()

    time_grid = []

    for start_time in start_times:
        row = []
        for end_time in end_times:
            if start_time.start_time < end_time.end_time and (
                                end_time.end_time.hour -
                                start_time.start_time.hour) <= 2:
                overlapping_bookings = bookings.filter(
                    start_time__start_time__lt=end_time.end_time,
                    end_time__end_time__gt=start_time.start_time
                )
                if not overlapping_bookings.exists():
                    row.append({
                        'start_time': start_time.start_time.strftime(
                                    '%I:%M %p'),
                        'end_time': end_time.end_time.strftime('%I:%M %p')
                    })
        if row:
            time_grid.append(row)

    return JsonResponse({'time_grid': time_grid})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(booked_by=request.user)
    context = {
        'bookings': bookings
    }
    return render(request, 'my_bookings.html', context)


@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, booked_by=request.user)

    if request.method == 'POST':
        court_type_id = request.POST.get('court_type')
        date_str = request.POST.get('date')
        time_slot = request.POST.get('time')

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Invalid date format.", status=400)

        try:
            start_time_str, end_time_str = time_slot.split('-')
            start_time_24 = datetime.strptime(
                start_time_str.strip(), '%I:%M %p').time()
            end_time_24 = datetime.strptime(
                end_time_str.strip(), '%I:%M %p').time()
        except ValueError as e:
            print(f"Time parsing error: {e}")
            return HttpResponse("Invalid time slot format.", status=400)

        try:
            start_time = StartTimes.objects.get(start_time=start_time_24)
            end_time = EndTimes.objects.get(end_time=end_time_24)
        except (StartTimes.DoesNotExist, EndTimes.DoesNotExist) as e:
            print(f"Database lookup error: {e}")
            return HttpResponse("Invalid time slot.", status=400)

        court_type = get_object_or_404(CourtType, id=court_type_id)

        start_datetime = datetime.combine(date, start_time.start_time)
        end_datetime = datetime.combine(date, end_time.end_time)

        if (end_datetime - start_datetime).total_seconds() > 2 * 60 * 60:
            return HttpResponse(
                "Booking can only be made for a maximum of 2 hours.",
                status=400)

        overlapping_bookings = Booking.objects.filter(
            court_type=court_type,
            date=date,
            start_time__start_time__lt=end_time.end_time,
            end_time__end_time__gt=start_time.start_time
        ).exclude(id=booking_id)

        if overlapping_bookings.exists():
            return HttpResponse(
                "This time overlaps with an existing booking.",
                status=400)

        # Update the booking
        booking.court_type = court_type
        booking.date = date
        booking.start_time = start_time
        booking.end_time = end_time
        booking.save()

        return redirect('my_bookings')

    context = {
        'booking': booking,
        'court_types': CourtType.objects.all(),
        'dates': [
            datetime.now().date() + timedelta(days=i) for i in range(15)
            ],
    }
    return render(request, 'edit_booking.html', context)


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, booked_by=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('my_bookings')

    return render(request, 'delete_booking.html', {'booking': booking})
