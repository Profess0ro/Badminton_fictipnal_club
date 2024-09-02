document.addEventListener('DOMContentLoaded', () => {
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

    if (window.sessionStorage.getItem('userLoggedIn')) {
        showModal("Welcome back! You can now comment on articles and book court times.");
        window.sessionStorage.removeItem('userLoggedIn');
    }
    
    const urlParams = new URLSearchParams(window.location.search);
    
    /* 
    When you signing up an account and the form is valid it will add
    "signup_success" into the URL and if this is added the modal
    with the information under will be shown
    */
    const signupSuccess = urlParams.get('signup_success');

    if (signupSuccess === 'True') {
        showModal(
            "Congratulations! You can now log in to comment on articles and book court times.");
    }

});
