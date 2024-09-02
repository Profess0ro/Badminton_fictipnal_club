document.addEventListener('DOMContentLoaded', () => {
    // Function to show a modal when sign up or logged in
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

    // Handle form submission for login
    const loginForm = document.querySelector('form.login');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(loginForm);
            fetch(loginForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showModal("Welcome back! You can now comment on articles and book court times.");
                    // Redirect after a short delay to ensure the modal is shown
                    setTimeout(() => window.location.href = data.redirect_url, 2000);
                } else {
                    // Handle form errors (e.g., display them to the user)
                    console.log('Login failed');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Handle form submission for signup
    const signupForm = document.querySelector('form.signup');
    if (signupForm) {
        signupForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(signupForm);
            fetch(signupForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showModal("Your account has been created successfully! You can now log in to comment on articles and book court times.");
                    // Redirect after a short delay to ensure the modal is shown
                    setTimeout(() => window.location.href = data.redirect_url, 2000);
                } else {
                    // Handle form errors (e.g., display them to the user)
                    console.log('Signup failed');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
