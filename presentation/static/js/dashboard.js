/*function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

document.addEventListener('DOMContentLoaded', function() {
    openTab(new Event('click'), 'YourEvents');

    const username = 'currentUser';

    fetch('http://127.0.0.1:5000/get_events')
        .then(response => response.json())
        .then(data => displayEvents(data, 'allEvents'));

    fetch(`http://127.0.0.1:5000/get_events?creator=${username}`)
        .then(response => response.json())
        .then(data => displayEvents(data, 'userEvents'));

    fetch(`http://127.0.0.1:5000/get_events?genre=favoriteGenre`)
        .then(response => response.json())
        .then(data => displayEvents(data, 'notifications'));

    function displayEvents(events, containerId) {
        const container = document.getElementById(containerId);
        events.forEach(event => {
            const eventDiv = document.createElement('div');
            eventDiv.textContent = `Event: ${event.event_name} at ${event.location} on ${event.date}`;
            container.appendChild(eventDiv);
        });
    }
});*/


function fetchAndDisplayEvents(endpoint, containerId) {
    fetch(endpoint)
        .then(response => response.json())
        .then(events => {
            const container = document.getElementById(containerId);
            container.innerHTML = '';  // Clear existing content

            events.forEach(event => {
                const eventElement = document.createElement('div');
                eventElement.className = 'event-item';
                eventElement.innerHTML = `
                    <h4>${event.event_name}</h4>
                    <p>Venue: ${event.location}</p>
                    <p>Date: ${event.date}</p>
                    <p>Genre: ${event.genre}</p>
                    <p>Description: ${event.description}</p>
                    <button onclick="registerForEvent('${event.event_name}')" class="register-btn">Register</button>
                `;
                container.appendChild(eventElement);
            });
        })
        .catch(error => {
            console.error('Error fetching events:', error);
            document.getElementById(containerId).innerText = 'Failed to load events.';
        });
}

function openTab(evt, tabName) {
    const tabcontent = document.getElementsByClassName("tabcontent");
    for (let content of tabcontent) {
        content.style.display = "none";
    }

    const tablinks = document.getElementsByClassName("tablinks");
    for (let link of tablinks) {
        link.className = link.className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    if (tabName === 'AllEvents') {
        fetchAndDisplayEvents('http://127.0.0.1:5000/get_events', 'AllEvents');
    } else if (tabName === 'YourEvents') {
        fetchAndDisplayEvents('/get_user_events', 'YourEvents');
    } else if (tabName === 'Notifications') {
        fetchAndDisplayEvents('/get_notifications', 'Notifications');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const username = localStorage.getItem('username');
    if (username) {
        document.getElementById('welcomeMessage').textContent = `Welcome, ${username}!`;
    }

    document.getElementById("defaultOpen").click();
});


function registerForEvent(eventId) {
    console.log(`Registering for event with ID: ${eventId}`);
}


