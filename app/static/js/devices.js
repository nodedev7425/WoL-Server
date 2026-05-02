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

document.addEventListener('DOMContentLoaded', loadDeviceData);