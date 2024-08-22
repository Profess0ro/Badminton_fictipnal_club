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
                        const currentTime = new Date();
                        const currentDate = currentTime.toISOString().split('T')[0];
                        const currentTimeStr = `${String(currentTime.getHours()).padStart(2, '0')}:${String(currentTime.getMinutes()).padStart(2, '0')}`;

                        let availableSlots = [];

                        data.time_grid.forEach((slots) => {
                            slots.forEach((slot) => {
                                const slotStartTime24 = convertTo24HourFormat(slot.start_time);

                                if (date > currentDate || (date === currentDate && slotStartTime24 >= currentTimeStr)) {
                                    availableSlots.push(`
                                        <div class="col-md-6">
                                            <label>
                                                <input type="radio" name="time" value="${slot.start_time}-${slot.end_time}" />
                                                ${slot.start_time} - ${slot.end_time}
                                            </label>
                                        </div>
                                    `);
                                }
                            });
                        });

                        if (availableSlots.length > 0) {
                            availableTimesDiv.innerHTML = availableSlots.join('');
                            document.querySelectorAll('input[name="time"]').forEach(radio => {
                                radio.addEventListener('change', () => {
                                    selectedTimeInput.value = radio.value;
                                });
                            });
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

    function convertTo24HourFormat(timeStr) {
        const [time, modifier] = timeStr.split(' ');
        let [hours, minutes] = time.split(':');

        if (modifier === 'PM' && hours !== '12') {
            hours = parseInt(hours, 10) + 12;
        } else if (modifier === 'AM' && hours === '12') {
            hours = '00';
        }

        return `${String(hours).padStart(2, '0')}:${minutes}`;
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

    const initialDate = document.querySelector('input[name="date"]:checked');
    if (initialDate) {
        selectedDateInput.value = initialDate.value;
        fetchAvailableTimes();
    }
});
