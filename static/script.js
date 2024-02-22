document.addEventListener('DOMContentLoaded', function () {
    // Function to check if passwords match
    function checkPasswordMatch() {
        const password = document.getElementById('password').value;
        const confirmation = document.getElementById('confirmation').value;
        const errorDiv = document.getElementById('passwordError');
        const registerBtn = document.getElementById('registerBtn');

        if (password.length < 8) {
            errorDiv.textContent = 'Password is too short';
            registerBtn.disabled = true;
        } else if (password !== confirmation) {
            errorDiv.textContent = 'Passwords do not match';
            registerBtn.disabled = true;
        } else {
            errorDiv.textContent = '';
            const username = document.getElementById('username').value.trim();
            if(username === ''){
                errorDiv.textContent = 'Username form is empty'
                registerBtn.disabled = true;
            }else{
                registerBtn.disabled = false;
            }
        }
    }

    // Attach the function to both password and confirmation input fields
    document.getElementById('password').addEventListener('input', checkPasswordMatch);
    document.getElementById('confirmation').addEventListener('input', checkPasswordMatch);
    document.getElementById('username').addEventListener('input', checkPasswordMatch);
});

