window.addEventListener('load', function() {
    document.getElementById('registerForm').addEventListener('input', function () {
        var password = document.getElementById('password').value;
        var confirmation = document.getElementById('confirmation').value;
        var username = document.getElementById('username').value;

        var passwordError = document.getElementById('passwordError');

        if (password.length < 8) {
            passwordError.textContent = 'Password must be at least 8 characters long.';
        } else if (password !== confirmation) {
            passwordError.textContent = 'Passwords do not match.';
        } else if (username === '' || password === '' || confirmation === '') {
            passwordError.textContent = 'All fields must be filled.';
        } else {
            passwordError.textContent = '';
        }

        var registerBtn = document.getElementById('registerBtn');
        registerBtn.disabled = (password.length < 8 || password !== confirmation || username === '' || password === '' || confirmation === '');
    });
});
