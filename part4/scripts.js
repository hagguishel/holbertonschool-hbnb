/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorElement = document.getElementById('login-error');

        if (errorElement) {
          errorElement.textContent = '';
        }

        try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
            },
          body: JSON.stringify({ email, password })
          });

            if (!response.ok) {
              if (errorElement) {
                errorElement.textContent = 'Login failed: Incorrect email or password.';
              }
              return;
            }

            const data = await response.json();

            console.log('Login success', data);

            document.cookie = `token=${data.access_token}; path=/`;

            window.location.href = 'index.html';

          } catch (error) {
            console.error('Error during login:', error);
            if (errorElement) {
              errorElement.textContent = 'Login failed: An unexpected error occurred.';
            }
          }
        });
        };
      }
    );
