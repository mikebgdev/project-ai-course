// async function runDetection() {
//     // Crea un elemento iframe para cargar el reproductor de YouTube
//     const iframe = document.createElement('iframe');
//     iframe.src = 'https://www.youtube.com/watch?v=AoaLgrVn2vw'; // Reemplaza esto con la URL del video de YouTube
//     iframe.setAttribute('allow', 'autoplay; encrypted-media');
//     iframe.style.display = 'none'; // Oculta el iframe
//     document.body.appendChild(iframe);
//
//     // Espera a que el iframe se cargue completamente
//     await new Promise((resolve) => {
//         iframe.onload = resolve;
//     });
//
//     // Crea un elemento canvas para dibujar los frames
//     const canvas = document.createElement('canvas');
//     document.body.appendChild(canvas);
//     const ctx = canvas.getContext('2d');
//
//     // Función para procesar cada frame del video
//     const processFrame = () => {
//         // Extrae el frame actual del video del reproductor de YouTube
//         const video = iframe.contentWindow.document.querySelector('video');
//         const currentTime = video.currentTime;
//         const base64Data = video.toDataURL('image/jpeg');
//
//         // Carga la imagen base64 en un objeto de imagen
//         const img = new Image();
//         img.onload = () => {
//             // Dibuja la imagen en el canvas
//             canvas.width = img.width;
//             canvas.height = img.height;
//             ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
//
//             // Realiza la detección de objetos en el frame
//             // (Aquí debes agregar el código de detección de objetos)
//
//             // Repite el proceso para el siguiente frame
//             requestAnimationFrame(processFrame);
//         };
//         img.src = base64Data;
//
//         // Avanza al siguiente frame
//         video.currentTime = currentTime + (1 / video.playbackRate);
//     };
//
//     // Inicia el procesamiento de frames
//     processFrame();
// }
//
// function start_detection(){
// // Ejecuta la detección de objetos
// runDetection();
//
// }
async function receiveVideoFrames() {
    const ws = new WebSocket('ws://localhost:8765');

    ws.onopen = function() {
        console.log('WebSocket connection established');
    };

    ws.onerror = function(error) {
        console.error('WebSocket error:', error);
    };

    ws.onmessage = function(event) {
        const imageData = event.data;
        let video = document.getElementById("video")
        video.src = 'data:image/png;base64,' + imageData;

        // Aquí puedes procesar el frame utilizando YOLOv8 en JavaScript
        // (Reemplaza este ejemplo con tu lógica de detección de objetos)
        // console.log('Received frame:', imageData);
    };

    ws.onclose = function() {
        console.log('WebSocket connection closed');
    };
}

// let btnStart = document.getElementById("start");
// btnStart.addEventListener("click", receiveVideoFrames());

function start_detection() {
    receiveVideoFrames();
}

