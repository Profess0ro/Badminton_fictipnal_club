document.addEventListener('DOMContentLoaded', () => {
    const courtTypeSelect = document.getElementById('court-type');
    const dateRadios = document.getElementsByName('date');
    const availableTimesDiv = document.getElementById('available-times');

    // Event listener for court type change
    courtTypeSelect.addEventListener('change', fetchAvailableTimes);
    
    // Event listener for date selection
    dateRadios.forEach(radio => {
        radio.addEventListener('change', fetchAvailableTimes);
    });

    function fetchAvailableTimes() {
        const courtTypeId = courtTypeSelect.value;
        const selectedDate = document.querySelector('input[name="date"]:checked');
        
        if (selectedDate) {
            const date = selectedDate.value;
            const url = `/bookings/get-available-times/?court_type=${courtTypeId}&date=${date}`;
            
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    // Clear previous times
                    availableTimesDiv.innerHTML = '';

                    // Populate new times
                    data.time_slots.forEach(slot => {
                        const option = document.createElement('div');
                        option.innerHTML = `<label><input type="radio" name="time" value="${slot.start_time}-${slot.end_time}" /> ${slot.start_time} - ${slot.end_time}</label><br/>`;
                        availableTimesDiv.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching available times:', error));
        } else {
            availableTimesDiv.innerHTML = '<p>Please select a date first.</p>';
        }
    }
});
