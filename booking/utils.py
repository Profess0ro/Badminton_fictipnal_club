from datetime import datetime, timedelta, time
from django.utils import timezone

def calculate_available_times(court, date):
    start_time = time(hour=8)  
    end_time = time(hour=18)   
    slot_duration = timedelta(hours=1)  
    
    available_times = []
    current_date = timezone.now().date()
    max_future_date = current_date + timedelta(days=30)
    
    # Fetch existing bookings for the selected court
    existing_bookings = court.booking_set.filter(start_time__date=date)
    
    for future_date in range((max_future_date - current_date).days + 1):
        current_date += timedelta(days=1)
        current_time = datetime.combine(current_date, start_time)
        
        while current_time.time() < end_time:
            overlap = False
            for booking in existing_bookings:
                if booking.start_time.date() == current_date and \
                   booking.start_time.time() <= current_time.time() < booking.end_time.time():
                    overlap = True
                    break
            
            if not overlap:
                available_times.append(f"{current_date.strftime('%Y-%m-%d')} {current_time.strftime('%H:%M')}")
            
            current_time += slot_duration
    
    return available_times

def calculate_available_times_for_date(court, date):
    start_time = time(hour=8)  # Start of the day
    end_time = time(hour=18)   # End of the day
    slot_duration = timedelta(hours=1)  # Duration of each time slot

    available_times = []
    current_time = datetime.combine(date, start_time)
    
    # Adjust the current_time to the next hour if it's not already there
    if current_time.time() > start_time:
        current_time += timedelta(minutes=current_time.minute % 60, seconds=current_time.second, microseconds=current_time.microsecond)
    
    # Fetch existing bookings for the selected court on the given date
    existing_bookings = court.booking_set.filter(
        start_time__date=date
    )
    
    while current_time.time() < end_time:
        overlap = False
        for booking in existing_bookings:
            if booking.start_time.time() <= current_time.time() < booking.end_time.time():
                overlap = True
                break
        
        if not overlap:
            # Skip over the current time if it's already booked
            if current_time.time() >= start_time and current_time.time() <= end_time:
                current_time += slot_duration
                continue
            
            available_times.append(current_time.strftime('%H:%M'))
        
        current_time += slot_duration
    
    return available_times