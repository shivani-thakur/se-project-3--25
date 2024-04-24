document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    if (username && password) {
        sessionStorage.setItem('username', username);

        const apiUrl = 'http://127.0.0.1:5000/login';
        const credentials = {
            username: username,
            password: password
        };

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        })
        .then(response => {
            if (response.status == 200) {
                window.user = username;
                window.location.href = '../templates/dashboard.html';
            } else if(response.status == 401) {
                throw new Error('Login failed: ' + response.statusText);
            } else {
                throw new Error('Login failed: Unknown error');
            }
            return response.json();
        })
        .catch(error => {
            alert(error.message);
        });
    } else {
        alert('Please enter both username and password.');
    }
});
