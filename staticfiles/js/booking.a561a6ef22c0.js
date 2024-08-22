document.addEventListener('DOMContentLoaded', () => {
    const courtTypeSelect = document.getElementById('court-type');
    const dateRadios = document.querySelectorAll('input[name="date"]');
    const availableTimesDiv = document.getElementById('available-times');
    const selectedDateInput = document.getElementById('selected-date');
    const selectedTimeInput = document.getElementById('selected-time');

    function fetchAvailableTimes() {
        const courtTypeId = courtTypeSelect.value;
        const date = selectedDateInput.value;

        if (date && courtTypeId) {
            const url = `/bookings/get-available-times/?court_type=${courtTypeId}&date=${date}`;
            
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    availableTimesDiv.innerHTML = '';

                    if (data.time_grid && Array.isArray(data.time_grid)) {
                        const availableSlots = data.time_grid.flatMap(slots =>
                            slots.map(slot => `
                                <div class="col-md-6">
                                    <label>
                                        <input type="radio" name="time" value="${slot.start_time}-${slot.end_time}" />
                                        ${slot.start_time} - ${slot.end_time}
                                    </label>
                                </div>
                            `)
                        ).join('');

                        availableTimesDiv.innerHTML = availableSlots || '<p>No available times left for today.</p>';
                    } else {
                        availableTimesDiv.innerHTML = '<p>No available times found.</p>';
                    }
                })
                .catch(error => console.error('Error fetching available times:', error));
        } else {
            availableTimesDiv.innerHTML = '<p>Please select a date and court type first.</p>';
        }
    }

    courtTypeSelect.addEventListener('change', fetchAvailableTimes);

    dateRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            const selectedDate = document.querySelector('input[name="date"]:checked');
            if (selectedDate) {
                selectedDateInput.value = selectedDate.value;
                fetchAvailableTimes();
            }
        });
    });

    availableTimesDiv.addEventListener('change', () => {
        const selectedTime = document.querySelector('input[name="time"]:checked');
        if (selectedTime) {
            selectedTimeInput.value = selectedTime.value;
            console.log('Selected Time:', selectedTime.value);  // Debugging line
        }
    });

    // Initialize with selected date
    const initialDate = document.querySelector('input[name="date"]:checked');
    if (initialDate) {
        selectedDateInput.value = initialDate.value;
        fetchAvailableTimes();
    }
});
