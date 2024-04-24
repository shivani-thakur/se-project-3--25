document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var selectGenre = document.getElementById('genre');
    var genres = Array.from(selectGenre.selectedOptions).map(option => option.value);

    if (username && password && genres.length > 0) {
        const userData = {
            userid: username,
            password: password,
            genres: genres
        };

        fetch('http://127.0.0.1:5000/add_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert("Signup successful.")
            window.location.href = '/';
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while signing up. Please try again.');
        });
    } else {
        alert('Please fill in all fields and select at least one genre.');
    }
});
