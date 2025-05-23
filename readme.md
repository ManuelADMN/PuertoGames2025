
# Proyecto Streamlit con Base de Datos SQL Server y Visualización

## Descripción

Esta aplicación está desarrollada en Python usando Streamlit para crear una interfaz web sencilla que se conecta a una base de datos SQL Server mediante `pyodbc`. La app permite ejecutar consultas SQL para obtener datos, los muestra en forma tabular y genera gráficos para facilitar el análisis visual.

## Funcionalidades

- Conexión a base de datos SQL Server usando `pyodbc`
- Ejecución dinámica de consultas SQL para obtener datos
- Visualización de datos en tablas con Streamlit
- Gráficos con Matplotlib embebidos en la app para análisis visual
- Interfaz simple y amigable

## Requisitos

- Python 3.7 o superior
- Librerías Python:
  - streamlit
  - pyodbc
  - pandas
  - matplotlib

## Instalación

1. Clona este repositorio o descarga los archivos del proyecto.  
2. Crea y activa un entorno virtual (recomendado):


python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


3. Instala las dependencias:


pip install -r requirements.txt

4. Configura la conexión a tu base de datos SQL Server en el archivo Python donde está el string de conexión.

## Uso

Para ejecutar la aplicación:


streamlit run nombre_de_tu_app.py


La app abrirá en tu navegador predeterminado mostrando la interfaz donde puedes ejecutar consultas y visualizar resultados.

## Archivos principales

* `nombre_de_tu_app.py`: Archivo principal con la lógica de la app Streamlit.
* `requirements.txt`: Dependencias del proyecto.

## Consideraciones

* Asegúrate de que el servidor SQL Server permita conexiones desde la máquina donde ejecutas la app.
* Revisa que la cadena de conexión en el código contenga los datos correctos (servidor, base de datos, usuario, contraseña).
* Para agregar nuevas consultas o gráficos, modifica el archivo principal.

## Contacto

Para dudas o sugerencias, puedes contactarme a:

* Email: manuel.adzm@gmail.com
* GitHub: ManuelADMN


