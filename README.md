# Proyecto IA
## Cosas para fer
### IA
#### YOLO v8 o v9
- :white_check_mark: Detectar personas
- :white_check_mark: Recorrido que realizan

#### Computer Vision
- :white_check_mark: Timer de cuanto tiempo llevan en el sitio
- Detección de emociones
- :white_check_mark: Pixelar caras
- Genero (Hombre o Mujer)


### Big Data
#### Objetivo

uid | aparece | desaparece
12  | 5131321 | 12312412
123 | 1231451 | 12314123
122 | 1231412 | 13145123

- Tiempo promedio: 50min
- Hora mas concurrida: 18:00


### Despliegue / Presentación / ETC
- :white_check_mark: Estaría bien hacer una web con el modelo, mejor que ejecutar un .py en local
- :interrobang: Poder utilizar una feed de video web


## Roadmap
##### IA
1. :white_check_mark: Implementar la parte del YOLO para que detecte personas en vídeo
2. :white_check_mark: Implementar la detección de cuanto tiempo pasan en escena (si se puede)
3. :interrobang: Guardar los datos previos (Tratamiento de datos al final)
4. Simultaneamente:
    - :white_check_mark: Pixelar caras
    - Detectar emociones
    - :white_check_mark: Tracking
5. :white_check_mark: Implementar el modelo en web (Como perros y gossos)

##### Big Data
1. Sacar y guardar más datos del vídeo
2. Seguir pensando en base al apartado "Fumar droga"

#### Fumar droga (invento)
- Datos IA -> Redis -> Hadoop -> BBDD -> API
- Hadoop a traves de API -> Insertar filas en CSV -> Visualizacion PowerBI
- Poder detectar si una misma persona vuelve a pasar por el mismo sitio
