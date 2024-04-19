# Proyecto IA
## Cosas para fer
### IA
#### YOLO v8 o v9
- Detectar personas
- Recorrido que realizan

#### Computer Vision
- Timer de cuanto tiempo llevan en el sitio
- Detección de emociones
- Pixelar caras


### Big Data
#### Objetivo

uid | aparece | desaparece 
12  | 5131321 | 12312412
123 | 1231451 | 12314123
122 | 1231412 | 13145123

- Tiempo promedio: 50min
- Hora mas concurrida: 18:00


### Despliegue / Presentación / ETC 
- Estaría bien hacer una web con el modelo, mejor que ejecutar un .py en local
- Poder utilizar una feed de video web


## Roadmap
##### IA 
1. Implementar la parte del YOLO para que detecte personas en vídeo
2. Implementar la detección de cuanto tiempo pasan en escena (si se puede) 
3. Guardar los datos previos (Tratamiento de datos al final)
4. Simultaneamente:
    - Pixelar caras
    - Detectar emociones
    - Tracking
5. Implementar el modelo en web (Como perros y gossos)

##### Big Data 
1. Sacar y guardar más datos del vídeo
2. Seguir pensando en base al apartado "Fumar droga"

#### Fumar droga (invento)
- Datos IA -> Redis -> Hadoop -> BBDD -> API 
- Hadoop a traves de API -> Insertar filas en CSV -> Visualizacion PowerBI
- Poder detectar si una misma persona vuelve a pasar por el mismo sitio
