from datetime import datetime, timedelta, time

def calculate_available_times(court):
    start_time = time(hour=8)  
    end_time = time(hour=18)   
    slot_duration = timedelta(hours=1)  
    
    available_times = []
    current_time = datetime.combine(datetime.today(), start_time)

    while current_time.time() < end_time:
        available_times.append(current_time.strftime('%H:%M'))
        current_time += slot_duration
    
    return available_times