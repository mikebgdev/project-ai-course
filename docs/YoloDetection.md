## Archivo `websocket_server.py`

Este archivo constituye el servidor WebSocket que facilita la comunicación en tiempo real con los clientes. Utiliza la biblioteca `websockets` para manejar las conexiones WebSocket y se encarga de iniciar la detección y el seguimiento de objetos.

### Funcionalidad Principal

El archivo `websocket_server.py` se encarga de:

1. **Iniciar el servidor WebSocket**: Utiliza la función `websockets.serve()` para iniciar un servidor WebSocket en el puerto `8765` de `localhost`.

2. **Ejecutar la detección de objetos**: Al recibir una conexión WebSocket, inicia la detección de objetos utilizando la función `run_detection()` definida en `detector.py`.

### Código Importante

- `async def main()`: La función principal del programa. Inicia el servidor WebSocket.

- `if __name__ == "__main__":` : Verifica si el script está siendo ejecutado directamente y llama a la función `main()` dentro de un bucle de eventos asyncio.

---

## Archivo `detector.py`

Este archivo contiene la lógica para la detección y el seguimiento de personas y caras en un flujo de video en tiempo real. Utiliza la biblioteca `cv2` para procesamiento de imágenes, `YOLO` para la detección de objetos, y `DeepSort` para el seguimiento de objetos.

### Clases Principales

1. **`FaceDetector`**: Una clase que utiliza un modelo YOLO especializado para detectar rostros en un marco de imagen.

2. **`PersonDetector`**: Una clase que utiliza un modelo YOLO para detectar personas en un marco de imagen y `DeepSort` para seguir y rastrear objetos.

### Funcionalidades Clave

- **Envío de datos a RabbitMQ**: Establece una conexión con RabbitMQ y envía datos sobre personas detectadas y su historial de seguimiento.

- **Detección de personas**: Utiliza un modelo YOLO para detectar personas en un marco de imagen y luego sigue y rastrea estas personas utilizando `DeepSort`.

### Código Importante

- `async def run_detection(websocket)`: Función asincrónica que ejecuta la detección y el seguimiento de objetos en un flujo de video en tiempo real. Utiliza modelos de detección de rostros y personas para procesar cada fotograma y envía los resultados a través de WebSocket.

- `def url_video()`: Función que determina la URL del video a procesar, ya sea una transmisión en vivo o un video en línea.



