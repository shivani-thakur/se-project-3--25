document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    // Simple validation to check if fields are empty (update as per your validation logic)
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    if (username && password) {
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
            // Check if the HTTP status code is 200 or a specific success code that your API sends
            if (response.status == 200) {
                window.location.href = '../html/events.html';
            } else if(response.status == 401) {
                throw new Error('Login failed: ' + response.statusText);
            } else {
                throw new Error('Login failed: ' + (data.message || 'Unknown error'));
            }
            return response.json();
        })
        .catch(error => {
            alert(error.message);
        });
    }
    else {
        alert('Please enter username and password');
    }
});
