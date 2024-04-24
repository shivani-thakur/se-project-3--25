document.getElementById('createEventForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var selectedDate = new Date(document.getElementById('datetime').value);
    var now = new Date();
    if (selectedDate < now) {
        alert('Please select a date and time in the future.');
        event.preventDefault();
        return;
    }

    var eventName = document.getElementById('eventname').value;
    var venue = document.getElementById('venue').value;
    var date = document.getElementById('datetime').value;
    var description = document.getElementById('description').value;
    var genre = document.getElementById('genre').value;
    var maxcap = document.getElementById('maxcap').value;

    var apiEndpoint = 'http://127.0.0.1:5000/add_event';

    var eventData = {
        event_name: eventName,
        location: venue,
        date: date,
        description: description,
        genre: genre,
        max_capacity: parseInt(maxcap),
        available_capacity: parseInt(maxcap),
        create_datetime: new Date(),
        createdBy: sessionStorage.getItem('username')
    };

    fetch(apiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Event created successfully!');
        this.reset();
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while creating the event. Please try again.');
    });
});
