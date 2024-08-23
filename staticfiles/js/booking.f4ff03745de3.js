document.addEventListener('DOMContentLoaded', () => {
    // Select the elements by their IDs
    const courtTypeSelect = document.getElementById('court-type');
    const dateRadios = document.querySelectorAll('input[name="date"]');
    const availableTimesDiv = document.getElementById('available-times');
    const selectedDateInput = document.getElementById('selected-date');
    const selectedTimeInput = document.getElementById('selected-time');

    // Check if the necessary elements exist before adding event listeners
    if (courtTypeSelect && dateRadios.length > 0 && availableTimesDiv && selectedDateInput && selectedTimeInput) {

        // Function to fetch available times based on selected court type and date
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
                            const currentTime = new Date();
                            const currentDate = currentTime.toISOString().split('T')[0];
                            const currentTimeStr = `${String(currentTime.getHours()).padStart(2, '0')}:${String(currentTime.getMinutes()).padStart(2, '0')}`;

                            let availableSlots = [];

                            data.time_grid.forEach((slots) => {
                                slots.forEach((slot) => {
                                    const slotStartTime = slot.start_time;
                                    const slotEndTime = slot.end_time;

                                    const slotStartTime24 = convertTo24HourFormat(slotStartTime);

                                    // Show available slots that are in the future
                                    if (date > currentDate || (date === currentDate && slotStartTime24 >= currentTimeStr)) {
                                        availableSlots.push(`
                                            <div class="col-md-6">
                                                <label>
                                                    <input type="radio" name="time" value="${slot.start_time}-${slot.end_time}" />
                                                    ${slotStartTime} - ${slotEndTime}
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

        // Helper function to convert 12-hour format to 24-hour format
        function convertTo24HourFormat(timeStr) {
            const [time, modifier] = timeStr.split(' ');
            let [hours, minutes] = time.split(':');

            if (hours === '12') {
                hours = '00';
            }

            if (modifier === 'PM') {
                hours = parseInt(hours, 10) + 12;
            }

            return `${String(hours).padStart(2, '0')}:${minutes}`;
        }

        // Add event listeners to the elements
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

        availableTimesDiv.addEventListener('change', (event) => {
            const selectedRadio = event.target.closest('input[name="time"]');
            if (selectedRadio) {
                selectedTimeInput.value = selectedRadio.value;
            }
        });

        // Initialize by fetching available times for the initially selected date
        const initialDate = document.querySelector('input[name="date"]:checked');
        if (initialDate) {
            selectedDateInput.value = initialDate.value;
            fetchAvailableTimes();
        }
    }
});
