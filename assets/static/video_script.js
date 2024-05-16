async function receiveVideoFrames() {
    const ws = new WebSocket('ws://localhost:8765');

    ws.onopen = function() {
        console.log('WebSocket connection established');
    };

    ws.onerror = function(error) {
        console.error('WebSocket error:', error);
    };

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const imageData = data.image;
        const personsData = data.persons;

        let video = document.getElementById("video")
        video.src = 'data:image/png;base64,' + imageData;

        let divPersons = document.getElementById("persons")
        divPersons.innerHTML = personsData;
    };

    ws.onclose = function() {
        console.log('WebSocket connection closed');
    };
}

function start_detection() {
    receiveVideoFrames();
}

