document.addEventListener('DOMContentLoaded', () => {
    /* 
    Function to create and display a Bootstrap modal with
    a custom message to users when they sign up or sign in.
    */
    function showModal(message) {
        // HTML structure of the modal, including dynamic content insertion.
        const modalHtml = `
            <div class="modal fade" id="profileModal" tabindex="-1" aria-labelledby="profileModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title nav-font" id="profileModalLabel">Notification</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body content-text">
                            ${message}
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Insert the modal HTML into the DOM just before the closing </body> tag
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Initialize the Bootstrap modal and show it
        const modal = new bootstrap.Modal(document.getElementById('profileModal'));
        modal.show();
    }

    // Parse the URL parameters
    const urlParams = new URLSearchParams(window.location.search);

    // Check if the 'login_success' parameter is present and true
    const loginSuccess = urlParams.get('login_success');
    if (loginSuccess === 'True') {
        /*
        If 'login_success' exists in the URL it will show a modal with
        a welcome back message to confirm a successful sign in.
        */
        showModal("Welcome back! You can now comment on articles and book court times.");
    }
    
    // Check if the 'signup_success' parameter is present and true
    const signupSuccess = urlParams.get('signup_success');
    if (signupSuccess === 'True') {
        /*
        If 'signup_success' exists in the URL it will show a modal with
        a signup success message to confirm the creation of the users account.
        */
        showModal("Congratulations! You can now log in to comment on articles and book court times.");
    }
});
