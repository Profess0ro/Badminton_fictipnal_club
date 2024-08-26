document.addEventListener('DOMContentLoaded', () => {
    const courtTypeSelect = document.getElementById('court-type');
    const dateRadios = document.querySelectorAll('input[name="date"]');
    const availableTimesDiv = document.getElementById('available-times');
    const selectedDateInput = document.getElementById('selected-date');
    const selectedTimeInput = document.getElementById('selected-time');

    /*
    The if statement below checks if the necessary elements exist 
    before adding event listeners.
    Otherwise there will be a error when the elements don´t exists,
    Since this file are loaded in the base.html
    */
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
                        /*
                        This if statement processes the response data to extract available time slots and updates 
                        the availableTimesDiv with these slots. 
                        It collects the current time a user are booking a time so that
                        no times that has past are visualised. 
                        */
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

                                    /* 
                                    Only times that´s not booked before and future times will be 
                                    calculated and show in the availableTimesDiv as radiobuttons.
                                    */
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

        /*
        Converts time from 12h format to 24h format. 
        This conversion is necessary for comparison with current time 
        and for displaying available slots correctly.
        Since the times in the database are in 24h format.
        */
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

        /*
        Add eventlisteners so when choosing court type and date
        it will calculate available times on the choices that has
        been made. 
        */
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
        /*
        In the booking_form.html there are a hidden div that collects the selected time
        when a radio button is selected.
        This eventlistener changes the value in that div, so the right information is
        sent to the database when the form getting posted.
        */
        availableTimesDiv.addEventListener('change', (event) => {
            const selectedRadio = event.target.closest('input[name="time"]');
            if (selectedRadio) {
                selectedTimeInput.value = selectedRadio.value;
            }
        });

        /*
        If the page is loaded with a pre-selected date it will
        run the function to collect available times for that date.
        */
        const initialDate = document.querySelector('input[name="date"]:checked');
        if (initialDate) {
            selectedDateInput.value = initialDate.value;
            fetchAvailableTimes();
        }
    }
});
