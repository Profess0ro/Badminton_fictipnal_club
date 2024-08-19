document.addEventListener('DOMContentLoaded', () => {
    const courtTypeSelect = document.getElementById('court-type');
    const dateRadios = document.getElementsByName('date');
    const availableTimesDiv = document.getElementById('available-times');
    const selectedDateInput = document.getElementById('selected-date');
    const selectedTimeInput = document.getElementById('selected-time');
    const bookingForm = document.getElementById('booking-form');

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

    availableTimesDiv.addEventListener('change', (event) => {
        if (event.target.name === 'time') {
            selectedTimeInput.value = event.target.value;
        }
    });

    function fetchAvailableTimes() {
        const courtTypeId = courtTypeSelect.value;
        const date = selectedDateInput.value;

        if (date) {
            const url = `/bookings/get-available-times/?court_type=${courtTypeId}&date=${date}`;
            
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data); 

                    availableTimesDiv.innerHTML = '';

                    if (data.time_grid && Array.isArray(data.time_grid)) {
                        let row = document.createElement('div');
                        row.classList.add('row');

                        data.time_grid.forEach((slots, rowIndex) => {
                            slots.forEach((slot, index) => {
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

                                if ((index + 1) % 2 === 0) {
                                    availableTimesDiv.appendChild(row);
                                    row = document.createElement('div');
                                    row.classList.add('row');
                                }
                            });

                            if (row.childNodes.length > 0) {
                                availableTimesDiv.appendChild(row);
                            }
                        });
                    } else {
                        availableTimesDiv.innerHTML = '<p>No available times found.</p>';
                    }
                })
                .catch(error => console.error('Error fetching available times:', error));
        } else {
            availableTimesDiv.innerHTML = '<p>Please select a date first.</p>';
        }
    }

    function convertTo12HourFormat(timeStr) {
        const [hour, minute] = timeStr.split(':');
        let hourInt = parseInt(hour);
        const ampm = hourInt >= 12 ? 'PM' : 'AM';
        hourInt = hourInt % 12 || 12;
        return `${hourInt}:${minute} ${ampm}`;
    }
});
