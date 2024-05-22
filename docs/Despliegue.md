# Despliegue del Proyecto

## Requisitos Previos
- Python 3.12 o superior instalado en el sistema.
- Docker y Docker Compose instalados y configurados correctamente. (Opcional)

## Pasos para Desplegar el Proyecto

Inciar reflex
```console
reflex run
```

Iniciar websocket
```console
python yolov8/websocket_server.py
```

## Docker Reflex

docker-compose.yml:

```docker-compose
version: '3'
services:
  reflex-app:
    build: .
    ports:
      - "3000:3000"
      - "8000:8000"
    volumes:
      - .:/app
```

Dockerfile:

```dockerfile
FROM python:3.11.5

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 3000 8000

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

```

## Stack RabbitMQ - MongoDB - Nifi

```docker-compose
version: "3"

services:

  nifi:
    image: apache/nifi:latest
    container_name: nifi
    networks:
      - rabbitnet
    ports:
      - "8443:8443"
    environment:
      - SINGLE_USER_CREDENTIALS_USERNAME=USER
      - SINGLE_USER_CREDENTIALS_PASSWORD=PASSWORD

  rabbit:
    image: rabbitmq:3-management
    container_name: rabbit
    networks:
      - rabbitnet
    ports:
      - "15672:15672"
      - "5672:5672"
    environment:
      - RABBITMQ_DEFAULT_USER=USER
      - RABBITMQ_DEFAULT_PASS=PASSWORD

  mongodb:
    image: mongo
    container_name: mongodb
    networks:
      - rabbitnet
    ports:
      - "27017:27017"

networks:
  rabbitnet:
    driver: bridge

```
