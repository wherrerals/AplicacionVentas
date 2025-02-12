FROM python:3.10-alpine

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
    build-base \
    libintl \
    libuuid \
    && pip install --upgrade pip

# Copiar el archivo de requerimientos antes de la instalación
COPY ./requirements.txt ./ 

# Instalar dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Generar la caché de fuentes
RUN fc-cache -f

# Eliminar las herramientas de compilación para reducir el tamaño de la imagen
RUN apk del build-base

# Copiar el código de la aplicación
COPY ./ ./

RUN ls -la /app

# Dar permisos de ejecución al entrypoint
RUN chmod +x entrypoint.sh

# Exponer el puerto 7000 para la aplicación
EXPOSE 7000

# Comando por defecto para ejecutar el servidor
CMD ["sh", "entrypoint.sh"]