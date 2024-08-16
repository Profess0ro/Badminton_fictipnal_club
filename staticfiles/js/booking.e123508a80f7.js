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

                    // Populate new times in a grid format
                    let row = document.createElement('div');
                    row.classList.add('row');

                    data.time_grid.forEach((timeSlots, index) => {
                        timeSlots.forEach(slot => {
                            const timeOption = document.createElement('div');
                            timeOption.classList.add('col-md-4'); // 3 columns per row
                            timeOption.innerHTML = `
                                <label>
                                    <input type="radio" name="time" value="${slot.start_time}-${slot.end_time}" />
                                    ${slot.start_time} - ${slot.end_time}
                                </label>
                            `;

                            row.appendChild(timeOption);
                        });

                        // Start a new row every 3 items
                        if ((index + 1) % 3 === 0) {
                            availableTimesDiv.appendChild(row);
                            row = document.createElement('div');
                            row.classList.add('row');
                        }
                    });

                    // Append the last row if it's not empty
                    if (row.childNodes.length > 0) {
                        availableTimesDiv.appendChild(row);
                    }
                })
                .catch(error => console.error('Error fetching available times:', error));
        } else {
            availableTimesDiv.innerHTML = '<p>Please select a date first.</p>';
        }
    }
});
