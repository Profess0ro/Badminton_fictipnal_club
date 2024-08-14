from datetime import datetime, timedelta, time
from django.utils import timezone

def calculate_available_times(court):
    start_time = time(hour=8)  
    end_time = time(hour=18)   
    slot_duration = timedelta(hours=1)  
    
    available_times = []
    current_time = datetime.combine(datetime.today(), start_time)
    
    # Fetch existing bookings for the selected court
    existing_bookings = court.booking_set.filter(
        start_time__date=timezone.now().date()
    )
    
    while current_time.time() < end_time:
        overlap = False
        for booking in existing_bookings:
            if booking.start_time.time() <= current_time.time() < booking.end_time.time():
                overlap = True
                break
        
        if not overlap:
            available_times.append(current_time.strftime('%H:%M'))
        
        current_time += slot_duration
    
    return available_times
