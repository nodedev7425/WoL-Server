function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

window.createDevice = async function(event) {
    event.preventDefault();
    
    const form = event.target;

    const data = {
        name: form.name.value,
        mac: form.mac.value
    };

    await fetch('/api/devices/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    });
};

window.wakeDevice = async function(event) {
    const parent = event.target.closest(".card-body");
    const url = window.origin + '/api/devices/' + parent.dataset.deviceId + '/wake/'

    fetch(url, {
        method: "POST",
        credentials: "include",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        }
    });
};

window.addEventListener("load", (event) => {
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/devices/updates/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);

        if (data.type == "status_init") {

            // TODO: ignore init whenever there is a set status so far

            console.log(data.device + " has changed status to " + data.status)

        } else if (data.type == "status_changed") {


        } else if (data.type == "ip_changed") {

        } else {
            console.error("Unexpected socket message: " + data)
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
});