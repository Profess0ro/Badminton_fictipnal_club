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
                        let row = document.createElement('div');
                        row.classList.add('row');
    
                        data.time_grid.forEach((slots, rowIndex) => {
                            slots.forEach((slot, index) => {
                                const timeOption = document.createElement('div');
                                timeOption.classList.add('col-md-4'); // 3 columns per row
                                timeOption.innerHTML = `
                                    <label>
                                        <input type="radio" name="time" value="${slot.start_time}-${slot.end_time}" />
                                        ${slot.start_time} - ${slot.end_time}
                                    </label>
                                `;
    
                                timeOption.querySelector('input').addEventListener('change', function() {
                                    document.getElementById('selected-time').value = this.value;
                                });
    
                                row.appendChild(timeOption);
    
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
        // Convert dateString to YYYY-MM-DD format
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`; // Return YYYY-MM-DD
    }
});
