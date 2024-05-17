# Flujo de Análisis de IA para el Seguimiento de Personas

## Descripción del Proyecto

Este proyecto implementa un sistema avanzado para el monitoreo y análisis del flujo peatonal en tiempo real, utilizando tecnologías de inteligencia artificial de última generación. Con el objetivo de mejorar la gestión urbana y proteger la privacidad de los individuos, el proyecto se centra en la detección y seguimiento de personas, así como en la predicción de sus movimientos futuros.

### Detección y Seguimiento en Tiempo Real

- **YOLOv8:** Utilizado para detectar personas en imágenes capturadas por cámaras de vigilancia en tiempo real.
- **DeepSort:** Implementado para rastrear el movimiento continuo de cada individuo a través de múltiples frames.
- **YOLOv8-face:** Empleado para difuminar automáticamente los rostros de las personas, garantizando así su privacidad.

### Almacenamiento y Procesamiento de Datos

Los datos generados por el sistema de reconocimiento y seguimiento se almacenan y procesan de manera eficiente mediante una arquitectura robusta y escalable:

- **RabbitMQ:** Gestiona la transferencia de datos entre el sistema de reconocimiento y la base de datos, encolando las solicitudes de almacenamiento.
- **Apache NiFi:** Procesa las colas de RabbitMQ, guardando los datos en MongoDB y generando archivos CSV y JSON para su análisis posterior.
- **MongoDB:** Almacena los datos de seguimiento, permitiendo su acceso y análisis de manera estructurada.

### Monitoreo y Análisis

El proyecto incluye dashboards interactivos que proporcionan una visión detallada del rendimiento y las métricas tanto de RabbitMQ como de MongoDB:

- **Dashboard de RabbitMQ:** Monitorea el estado de las colas de mensajes, facilitando la gestión de la transferencia de datos.
- **Dashboard de BigData:** Proporciona una visión instantánea de los datos, como PowerBI, mejorando la eficiencia en la gestión de los recursos.

### Aplicaciones y Beneficios

Este sistema permite un análisis detallado de los patrones de movimiento y trayectorias de las personas en diversos entornos urbanos, proporcionando información valiosa para la planificación urbana y la mejora de la infraestructura pública. Al proteger la privacidad de los individuos y gestionar los datos de manera eficiente, el proyecto establece un estándar para la implementación ética y efectiva de tecnologías de seguimiento peatonal.

¡Descubre más sobre nuestro proyecto y cómo estamos transformando la gestión del flujo peatonal en las ciudades modernas!
