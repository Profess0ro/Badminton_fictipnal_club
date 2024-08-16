document.addEventListener('DOMContentLoaded', () => {
    const courtTypeSelect = document.getElementById('court-type');
    const dateRadios = document.getElementsByName('date');
    const availableTimesDiv = document.getElementById('available-times');
    const selectedTimeInput = document.getElementById('selected-time');

    // Event listener for court type change
    courtTypeSelect.addEventListener('change', fetchAvailableTimes);
    
    // Event listener for date selection
    dateRadios.forEach(radio => {
        radio.addEventListener('change', fetchAvailableTimes);
    });

    // Event listener for time slot change
    availableTimesDiv.addEventListener('change', (event) => {
        if (event.target.name === 'time') {
            selectedTimeInput.value = event.target.value;
        }
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
        // Convert dateString from format like "Aug. 20, 2024" to "YYYY-MM-DD"
        const [monthStr, day, year] = dateString.split(' ');
        const monthNames = {
            "Jan.": 1, "Feb.": 2, "Mar.": 3, "Apr.": 4, "May.": 5, "Jun.": 6,
            "Jul.": 7, "Aug.": 8, "Sep.": 9, "Oct.": 10, "Nov.": 11, "Dec.": 12
        };

        const month = monthNames[monthStr];
        if (!month) {
            throw new Error("Invalid month name");
        }

        const formattedDate = new Date(`${year}-${month}-${day}`);
        return formattedDate.toISOString().split('T')[0]; // Return YYYY-MM-DD
    }
});
