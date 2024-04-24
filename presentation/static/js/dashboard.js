function fetchAndDisplayEvents(endpoint, containerId) {
    fetch(endpoint)
        .then(response => response.json())
        .then(events => {
            console.log("I have got "+events)
            const container = document.getElementById(containerId);
            container.innerHTML = '';

            events.forEach(event => {
                const eventElement = document.createElement('div');
                eventElement.className = 'event-item';
                eventElement.innerHTML = `
                    <h4>${event.event_name}</h4>
                    <p>Venue: ${event.location}</p>
                    <p>Date: ${event.date}</p>
                    <p>Genre: ${event.genre}</p>
                    <p>Description: ${event.description}</p>
                    <button id="register-btn-${event.event_name}" onclick="registerForEvent('${event.event_name}', this)" class="register-btn">Register</button>
                `;
                container.appendChild(eventElement);
            });
        })
        .catch(error => {
            console.error('Error fetching events:', error);
            document.getElementById(containerId).innerText = 'Failed to load events.';
        });
}

function fetchAndDisplayYourEvents(endpoint, containerId, params) {
    const queryString = new URLSearchParams(params).toString();
    const urlWithParams = `${endpoint}?${queryString}`;
    fetch(urlWithParams)
        .then(response => response.json())
        .then(events => {
            const container = document.getElementById(containerId);
            container.innerHTML = '';

            events.forEach(event => {
                const eventElement = document.createElement('div');
                eventElement.className = 'event-item';
                eventElement.innerHTML = `
                    <h4>${event.event_name}</h4>
                    <p>Venue: ${event.location}</p>
                    <p>Date: ${event.date}</p>
                    <p>Genre: ${event.genre}</p>
                    <p>Description: ${event.description}</p>
                    <p>Maximum Capacity: ${event.max_capacity}</p>
                    <p>Available Capacity: ${event.available_capacity}</p>
                `;
                container.appendChild(eventElement);
            });
        })
        .catch(error => {
            console.error('Error fetching events:', error);
            document.getElementById(containerId).innerText = 'Failed to load events.';
        });
}

function fetchAndDisplayNotifications(endpoint, containerId, params) {
    last_notfication_time= new Date();
    const queryString = new URLSearchParams(params).toString();
    const urlWithParams = `${endpoint}?${queryString}`;
    fetch(urlWithParams)
        .then(response => response.json())
        .then(events => {
            console.log("I have got "+events)
            const container = document.getElementById(containerId);
            container.innerHTML = '';

            events.forEach(event => {
//                event = JSON.parse(eventstr)
                const eventElement = document.createElement('div');
                eventElement.className = 'event-item';
                eventElement.innerHTML = `
                    <h4>${event.event_name}</h4>
                    <p>Venue: ${event.location}</p>
                    <p>Date: ${event.date}</p>
                    <p>Genre: ${event.genre}</p>
                    <p>Description: ${event.description}</p>
                    <p>Maximum Capacity: ${event.max_capacity}</p>
                    <!--<p>Available Capacity: ${event.available_capacity}</p>-->
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
        fetchAndDisplayYourEvents('http://127.0.0.1:5000/get_events', 'YourEvents', {username: sessionStorage.getItem('username')});
    } else if (tabName === 'Notifications') {
        fetchAndDisplayNotifications('http://127.0.0.1:5000/get_notifications', 'Notifications', {username: sessionStorage.getItem('username')});
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const username = sessionStorage.getItem('username');
    if (username) {
        document.getElementById('welcomeMessage').textContent = `Welcome, ${username}!`;
    }

    document.getElementById("defaultOpen").click();
});


function registerForEvent(eventId, btnElement) {

    const apiUrl = 'http://127.0.0.1:5000/register';
    const credentials = {
        event_id: eventId,
        user_id: sessionStorage.getItem('username')
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
            alert("Registered successfully")
            btnElement.textContent = "Unregister";
            btnElement.onclick = () => unregisterForEvent(eventId, btnElement);
        } else {
            throw new Error('Registration failed');
        }
        return response.json();
    })
    .catch(error => {
        alert(error.message);
    });
}

function unregisterForEvent(eventId, btnElement) {
    const apiUrl = 'http://127.0.0.1:5000/unregister_event';
    const credentials = {
        event_id: eventId,
        user_id: sessionStorage.getItem('username')
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
            alert("Unregistered successfully")
            btnElement.textContent = "Register";
            btnElement.onclick = () => registerForEvent(eventId, btnElement);
        } else {
            throw new Error('Unregistration failed');
        }
        return response.json();
    })
    .catch(error => {
        alert(error.message);
    });
}
