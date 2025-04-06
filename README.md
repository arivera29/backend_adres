# Prueba de conocimientos para ADRES

Este es el codigo de la prueba de conocimientos de desarrollo de la ADRES

## Instalación


### Requisitos previos

1. **Instalar Python**: Descarga e instala la última versión de Python desde [python.org](https://www.python.org/).
2. **Instalar pip**: Asegúrate de que `pip` esté instalado junto con Python.
3. **Clonar el repositorio**: Clona este repositorio en tu máquina local usando el siguiente comando:
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    ```
4. **Crear un entorno virtual**: Crea un entorno virtual para aislar las dependencias del proyecto.
    ```bash
    python -m venv venv
    ```

### Instalación de dependencias

1. Activa el entorno virtual:
    - En Windows:
      ```bash
      venv\Scripts\activate
      ```
    - En macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
2. Instala las dependencias del proyecto desde el archivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

### Ejecución de la aplicación

1. Asegúrate de que el entorno virtual esté activado.
2. Ejecuta la aplicación utilizando el siguiente comando:
    ```bash
    python app.py
    ```
3. La aplicación estará disponible en `http://localhost:5000` o en el puerto configurado.

### Pruebas

Para ejecutar las pruebas, utiliza el siguiente comando:
```bash
pytest
```


### Ejecución de la aplicación en un contenedor

1. Asegúrate de tener Docker instalado en tu máquina. Si no lo tienes, descárgalo e instálalo desde [docker.com](https://www.docker.com/).
2. Construye la imagen Docker a partir del archivo `Dockerfile` ubicado en el repositorio:
    ```bash
    docker build -t nombre-de-la-imagen .
    ```
3. Ejecuta un contenedor basado en la imagen creada:
    ```bash
    docker run -p 5000:5000 nombre-de-la-imagen
    ```
4. La aplicación estará disponible en `http://localhost:5000` o en el puerto configurado en el contenedor.

