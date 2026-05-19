function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function loadDeviceData() {
    const csrfToken = getCookie('csrftoken');
    const endpoint = window.location.origin + '/api/users/me/devices';

    try {
        const response = await fetch(endpoint, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const result = await response.json();
        console.log(result);

    } catch (error) {
        console.error(error.message);
    }
}

function addDeviceToGrid() {
    
}

async function createDevice() {
    event.preventDefault();
    
    const form = event.target;

    const data = {
        name: form.name.value,
        mac: form.mac.value
    };

    const csrfToken = getCookie('csrftoken');

    await fetch('/api/devices/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    });
}

document.addEventListener('DOMContentLoaded', () => {
    loadDeviceData();

    const form = document.getElementById('createForm');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        createDevice()
        setTimeout(() => form.submit(), 2000)
    });
});