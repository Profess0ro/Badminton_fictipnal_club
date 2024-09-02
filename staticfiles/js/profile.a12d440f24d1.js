document.addEventListener('DOMContentLoaded', () => {
    // Function to show a modal with a specific message
    function showModal(message) {
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
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById('profileModal'));
        modal.show();
    }

    // Check for signup success
    if (document.getElementById('signupSuccess')) {
        sessionStorage.setItem('accountCreated', 'true');
    }

    // Check for login success
    if (document.getElementById('loginSuccess')) {
        sessionStorage.setItem('userLoggedIn', 'true');
    }

    // Show modal if account created
    if (sessionStorage.getItem('accountCreated') === 'true') {
        showModal("Your account has been created successfully! You can now log in to comment on articles and book court times.");
        sessionStorage.removeItem('accountCreated');
    }

    // Show modal if user logged in
    if (sessionStorage.getItem('userLoggedIn') === 'true') {
        showModal("Welcome back! You can now comment on articles and book court times.");
        sessionStorage.removeItem('userLoggedIn');
    }
});
