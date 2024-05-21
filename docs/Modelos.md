# Noteboks - Modelos

## Notebook: `prepare_data.ipynb`

### Objetivo
El objetivo de este notebook es preparar los datos almacenados en archivos JSON para su uso en modelos de aprendizaje automático. Los datos provienen de dos archivos JSON: uno contiene información de las personas (`proyecto_ia_arch.persons.json`) y el otro contiene información de las pistas (`proyecto_ia_arch.tracks.json`).

### Pasos Realizados

1. **Cargar Archivos JSON**:
    - Se cargan los archivos JSON utilizando la función `read_data_from_json`.
    - Archivos cargados: `persons_file` y `tracks_file`.

2. **Procesar Datos de las Pistas**:
    - Se crea un DataFrame a partir de los datos de las pistas.
    - Se expanden las columnas `mean` y `covariance` en múltiples columnas separadas.
    - Se eliminan las columnas originales `mean` y `covariance`.

3. **Guardar Datos Combinados**:
    - Se combinan los DataFrames de personas y pistas utilizando la columna `track_id`.

## Notebook: `eda.ipynb`

### Objetivo
El objetivo de este notebook es realizar un análisis exploratorio de datos (EDA) en el archivo CSV generado en el notebook de preparación de datos (`combined_data.csv`). El EDA ayuda a entender las características de los datos y a identificar patrones y relaciones importantes.

### Pasos Realizados

1. **Cargar Datos Combinados**:
    - Se carga el archivo CSV `combined_data.csv` en un DataFrame para su análisis.

2. **Eliminar Columnas No Útiles**:
    - Se eliminan las columnas que no son relevantes para el análisis, tales como `'_id_x'`, `'_id_y'`, `start_time`, `end_time`, `conf`, `hits`, `age`, `time_since_update`, `state`, y `time`.

3. **Mostrar Información del DataFrame**:
    - Se muestran las primeras filas del DataFrame para obtener una vista general de los datos.
    - Se proporciona información detallada del DataFrame, incluyendo tipos de datos y valores nulos.
    - Se generan estadísticas descriptivas de las variables numéricas.

4. **Visualización de Distribuciones**:
    - Se crean gráficos de distribución para las coordenadas `cord_x` y `cord_y` utilizando `seaborn`.

5. **Visualización de Correlaciones**:
    - Se crea un mapa de calor para visualizar las correlaciones entre todas las variables del DataFrame.

6. **Visualización de Relaciones Entre Variables**:
    - Se crean gráficos de dispersión para explorar relaciones entre `cord_x` y `cord_y`.

7. **Visualización de Variables Expandidas**:
    - Se utilizan gráficos de pares (`pairplot`) para explorar relaciones entre las columnas expandidas `mean` y `covariance`.


[//]: # (TODO)
