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
                        let currentTime = new Date(); // Get the current date and time
                        let currentDate = currentTime.toISOString().split('T')[0]; // Format as YYYY-MM-DD
                        let currentTimeStr = `${String(currentTime.getHours()).padStart(2, '0')}:${String(currentTime.getMinutes()).padStart(2, '0')}`;

                        let availableSlots = [];

                        data.time_grid.forEach((slots) => {
                            slots.forEach((slot) => {
                                const slotStartTime = `${slot.start_time}`;
                                const slotEndTime = `${slot.end_time}`;

                                // Only show slots that are in the future
                                if (date > currentDate || (date === currentDate && slotEndTime > currentTimeStr)) {
                                    const startTime12Hour = convertTo12HourFormat(slotStartTime);
                                    const endTime12Hour = convertTo12HourFormat(slotEndTime);

                                    availableSlots.push(`
                                        <div class="col-md-6">
                                            <label>
                                                <input type="radio" name="time" value="${slot.start_time}-${slot.end_time}" />
                                                ${startTime12Hour} - <br>${endTime12Hour}
                                            </label>
                                        </div>
                                    `);
                                }
                            });
                        });

                        if (availableSlots.length > 0) {
                            availableTimesDiv.innerHTML = availableSlots.join('');
                        } else {
                            availableTimesDiv.innerHTML = '<p>No available times left for today.</p>';
                        }
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

    // Initial fetch when the page loads
    const initialDate = document.querySelector('input[name="date"]:checked');
    if (initialDate) {
        selectedDateInput.value = initialDate.value;
        fetchAvailableTimes();
    }
});
