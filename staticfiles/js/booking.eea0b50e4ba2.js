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

                        data.time_grid.forEach((slots, rowIndex) => {
                            let row = document.createElement('div');
                            row.classList.add('row');

                            slots.forEach((slot, index) => {
                                const startTime = new Date(`${date}T${slot.start_time}`);
                                const endTime = new Date(`${date}T${slot.end_time}`);

                                // Check if the time slot is still in the future
                                if (endTime > currentTime) {
                                    const startTime12Hour = convertTo12HourFormat(slot.start_time);
                                    const endTime12Hour = convertTo12HourFormat(slot.end_time);

                                    const timeOption = document.createElement('div');
                                    timeOption.classList.add('col-md-6'); 
                                    timeOption.innerHTML = `
                                        <label>
                                            <input type="radio" name="time" value="${slot.start_time}-${slot.end_time}" />
                                            ${startTime12Hour} - <br>${endTime12Hour}
                                        </label>
                                    `;

                                    row.appendChild(timeOption);
                                    
                                    // Add the row to the DOM after two columns
                                    if ((index + 1) % 2 === 0) {
                                        availableTimesDiv.appendChild(row);
                                        row = document.createElement('div');
                                        row.classList.add('row');
                                    }
                                }
                            });

                            // Append any remaining row elements
                            if (row.childNodes.length > 0) {
                                availableTimesDiv.appendChild(row);
                            }
                        });

                        if (availableTimesDiv.innerHTML === '') {
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

    function convertTo12HourFormat(timeStr) {
        const [hour, minute] = timeStr.split(':');
        let hourInt = parseInt(hour);
        const ampm = hourInt >= 12 ? 'PM' : 'AM';
        hourInt = hourInt % 12 || 12;
        return `${hourInt}:${minute} ${ampm}`;
    }

    courtTypeSelect.addEventListener('change', fetchAvailableTimes);
    dateRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            const selectedDate = document.querySelector('input[name="date"]:checked');
            if (selectedDate) {
                const formattedDate = selectedDate.value;
                selectedDateInput.value = formattedDate;
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
