$(document).ready(function() {
    $('#signupForm').on('submit', function(event) {
      event.preventDefault();
      if (!isEmailValid()) {
        return;
      }
      if (!isPasswordMatch()) {
        return;
      }
      // Form is valid, proceed with AJAX submission or form submission
      this.submit();
    });
  
    function isEmailValid() {
      const emailInput = $('#emailInput');
      const emailError = $('#emailError');
      const email = emailInput.val().trim();
      // Perform email validation logic
      if (email === '') {
        emailError.text('Email is required');
        emailInput.addClass('error');
        return false;
      } else {
        emailError.text('');
        emailInput.removeClass('error');
        return true;
      }
    }
  
    function isPasswordMatch() {
      const passwordInput = $('#passwordInput');
      const confirmPasswordInput = $('#confirmPasswordInput');
      const passwordError = $('#passwordError');
      const password = passwordInput.val();
      const confirmPassword = confirmPasswordInput.val();
      // Perform password validation logic
      if (password === '' || confirmPassword === '') {
        passwordError.text('Passwords are required');
        passwordInput.addClass('error');
        confirmPasswordInput.addClass('error');
        return false;
      } else if (password !== confirmPassword) {
        passwordError.text('Passwords do not match');
        passwordInput.addClass('error');
        confirmPasswordInput.addClass('error');
        return false;
      } else {
        passwordError.text('');
        passwordInput.removeClass('error');
        confirmPasswordInput.removeClass('error');
        return true;
      }
    }
  });
  