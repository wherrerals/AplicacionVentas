FROM python:3.10.4-alpine3.15

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias necesarias, incluyendo herramientas para fonts y WeasyPrint
RUN apk update && apk add --no-cache \
    mysql-dev \
    python3-dev \
    libc-dev \
    libffi-dev \
    cairo \
    pango \
    gdk-pixbuf \
    harfbuzz \
    fribidi \
    fontconfig \
    ttf-freefont \
    && apk add --no-cache --virtual .build-deps build-base \
    && pip install --upgrade pip

# Copiar el archivo de requerimientos antes de la instalación
COPY ./requirements.txt ./ 

# Instalar dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Eliminar las herramientas de compilación para reducir el tamaño de la imagen
RUN apk del .build-deps

# Copiar el código de la aplicación
COPY ./ ./ 

# Exponer el puerto 8000 para la aplicación
EXPOSE 7000

# Comando por defecto para ejecutar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



#ejecutar el comando docker build -t myapp .
#docker build -t devrrior/proyectoledstudio_aplicacionventas .
#docker run -p 8000:8000 devrrior/proyectoledstudio_aplicacionventas

#docker build -t devrrior/proyectoledstudio_django -f dockerfile.django .
#docker run -p 8000:8000 devrrior/proyectoledstudio_django
#docker run -p 8000:8000 -v /ruta1/ruta2/ruta3/ProyectoLedStudio/AplicacionVentas:/app devrrior/proyectoledstudio_django

#Crear un volumen para que los cambios en el código se reflejen en el contenedor
#docker run -p 8000:8000 -v /ruta1/ruta2/ruta3/ProyectoLedStudio/AplicacionVentas:/app devrrior/proyectoledstudio_aplicacionventas