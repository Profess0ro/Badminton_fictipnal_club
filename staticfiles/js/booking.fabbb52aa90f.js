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
            const date = formatDate(selectedDate.value); // Convert to YYYY-MM-DD format
            const url = `/bookings/get-available-times/?court_type=${courtTypeId}&date=${date}`;
            
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data); // Debugging: Log the data received from the server

                    // Clear previous times
                    availableTimesDiv.innerHTML = '';

                    // Check if data.time_grid exists and is not empty
                    if (data.time_grid && Array.isArray(data.time_grid)) {
                        data.time_grid.forEach((slots) => {
                            const row = document.createElement('div');
                            row.classList.add('row');

                            slots.forEach((slot) => {
                                const timeOption = document.createElement('div');
                                timeOption.classList.add('col-md-4'); // 3 columns per row
                                timeOption.innerHTML = `
                                    <label>
                                        <input type="radio" name="time" value="${slot.start_time}-${slot.end_time}" />
                                        ${slot.start_time} - ${slot.end_time}
                                    </label>
                                `;

                                row.appendChild(timeOption);

                                // Start a new row every 3 items
                                if ((row.childNodes.length) % 3 === 0) {
                                    availableTimesDiv.appendChild(row);
                                }
                            });

                            // Append the last row if it's not empty
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

    function formatDate(dateString) {
        // Assuming dateString is in format like "Aug. 21, 2024"
        const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
        const date = new Date(dateString);
        return date.toISOString().split('T')[0]; // Return YYYY-MM-DD
    }
});
