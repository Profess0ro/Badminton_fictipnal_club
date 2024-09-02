document.addEventListener('DOMContentLoaded', () => {
    // Function to show a modal when logged in or signed up
    function showModal(message) {
        const modalHtml = `
            <div class="modal fade" id="profileModal" tabindex="-1" aria-labelledby="profileModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title nav-font" id="profileModalLabel">Notification</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
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

    // Check for custom flags set by the server to load the message
    if (window.sessionStorage.getItem('userLoggedIn')) {
        showModal("Welcome back! You can now comment on articles and book court times.");
        window.sessionStorage.removeItem('userLoggedIn');
    }

    if (window.sessionStorage.getItem('accountCreated')) {
        showModal("Your account has been created successfully! You can now log in to comment on articles and book court times.");
        window.sessionStorage.removeItem('accountCreated');
    }
});
