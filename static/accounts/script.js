$(document).ready(function() {
    // Toggle password visibility
    $('#togglePassword').click(function() {
        const passwordField = $('#password');
        const passwordFieldType = passwordField.attr('type');
        const icon = $(this).find('i');
        
        if (passwordFieldType === 'password') {
            passwordField.attr('type', 'text');
            icon.removeClass('fa-eye').addClass('fa-eye-slash');
        } else {
            passwordField.attr('type', 'password');
            icon.removeClass('fa-eye-slash').addClass('fa-eye');
        }
    });
    
    // Form submission
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();
        
        const username = $('#username').val();
        const password = $('#password').val();
        
        if (!username || !password) {
            showAlert('Please fill in all fields', 'danger');
            return;
        }
        
        // Check if remember me is checked
        const rememberMe = $('#rememberMe').is(':checked');
        
        // Simulate login process
        const loginBtn = $(this).find('button[type="submit"]');
        loginBtn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Signing in...');
        loginBtn.prop('disabled', true);
        
        setTimeout(function() {
            // This is a simulation - in a real app, you would validate credentials with your backend
            if (username && password) {
                // If remember me is checked, store credentials (in a real app, use secure methods)
                if (rememberMe) {
                    localStorage.setItem('rememberedUsername', username);
                } else {
                    localStorage.removeItem('rememberedUsername');
                }
                
                showAlert('Login successful! Redirecting...', 'success');
                
                // Simulate redirect
                setTimeout(function() {
                    window.location.href = '/dashboard'; // This would be your actual dashboard URL
                }, 1500);
            } else {
                showAlert('Invalid credentials. Please try again.', 'danger');
                loginBtn.html('Sign In');
                loginBtn.prop('disabled', false);
            }
        }, 1500);
    });
    
    // Social login buttons
    $('.social-btn').click(function() {
        const provider = $(this).text().trim();
        showAlert(`${provider} login clicked. This would redirect to ${provider} OAuth in a real application.`, 'info');
    });
    
    // Forgot password
    $('.forgot-password').click(function(e) {
        e.preventDefault();
        showAlert('Password reset functionality would be implemented here.', 'info');
    });
    
    // Sign up link
    $('.signup-link a').click(function(e) {
        e.preventDefault();
        showAlert('Registration page would be shown here.', 'info');
    });
    
    // Check for remembered username
    const rememberedUsername = localStorage.getItem('rememberedUsername');
    if (rememberedUsername) {
        $('#username').val(rememberedUsername);
        $('#rememberMe').prop('checked', true);
    }
    
    // Helper function to show alerts
    function showAlert(message, type) {
        // Remove any existing alerts
        $('.alert').remove();
        
        // Create alert element
        const alert = $(`<div class="alert alert-${type} alert-dismissible fade show" role="alert">
                            ${message}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>`);
        
        // Add alert to form
        $('#loginForm').prepend(alert);
        
        // Auto remove after 5 seconds
        setTimeout(function() {
            alert.alert('close');
        }, 5000);
    }
});

console.log("Hello")