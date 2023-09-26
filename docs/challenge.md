# LATAM Challenge

## Overview
We need to operationalize the data science work for the airport team. For this, we have decided to enable an API in which they can consult the delay prediction of a flight.

## Consideraciones generales
Al clonar el repositorio es posible realizar los test utilizando el archivo Makefile proporcionado:

1. Para realizar el test del model se ejecuta el siguiente comando
```bash
make model-test
```
2. Para realizar el test de la api se ejecuta el siguiente comando
```bash
make api-test
```

Respecto a la ejecución de la API, surge un problema respecto a los importes de los distintos archivos y librerías utilizados. Es por eso que no se puede probar con los archivos entregados en el repositorio de GitHub. Para ello sería necesario modificar la estructura del proyecto, lo cual no sé si se podía hacer. O tener dos versiones distintas, una para realizar las pruebas y otro para la implementación de la API. De todas formas a continuación se muestran los pasos para la ejecución de la API de manera local.

Es por eso y a raíz de buscar soluciones para poder realizar la implementación de la mejor forma, en que pudiesen realizarse tanto las pruebas como el despliegue de la API que la parte 3 y 4 del desafío no pudieron ser realizadas. Además de eso la plataforma Cloud de Google, requiere datos de facturación que no estoy dispuesto a entregar.

## Instalación y ejecución
### Usando línea de comandos
1. Se instalan los requerimientos
```bash
pip install -r requirements.txt
```
2. Se ejecuta el servidor
```bash
uvicorn main:app --reload
```

### Usando docker
1. Se buildea la imagen 
```bash
docker build .
```
2. Se ejecuta la imagen de docker
```bash
docker run [OPTIONS] IMAGE
```

## Uso
La aplicación se ejecuta en un [servidor local](http://127.0.0.1:8000) donde se despliega la función POST para realizar los predict. Los datos se entregan como un json con los datos de los vuelos. 

A continuación se muestran tres ejemplos de posibles json para probar la app:

```json
{
    "flights": [
        {
            "OPERA": "Aerolineas Argentinas", 
            "TIPOVUELO": "N", 
            "MES": 3
        }
    ]
}
```
```json
{       
    "flights": [
        {
            "OPERA": "Aerolineas Argentinas", 
            "TIPOVUELO": "N",
            "MES": 12
        }
    ]
}
```