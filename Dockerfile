FROM geonode/geonode-base:latest-ubuntu-22.04
LABEL team="GeoNoXT development team"

COPY requirements.txt .
WORKDIR /usr/src/geonode

# Actualiza y instala dependencias necesarias en una sola capa
RUN apt-get update -y && apt-get install -y \
    curl \
    wget \
    unzip \
    gnupg2 \
    locales \
    && apt-get autoremove --purge -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*  # Elimina listas de paquetes para reducir tamaño


# Copiar solo los archivos de requisitos primero (esto aprovecha la caché si no cambia)
COPY requirements.txt .
# bajar el requirements.txt desde el repo de geonoxt
# RUN wget https://raw.githubusercontent.com/GeoNoXT/geonoxt/refs/heads/xt.gcp/requirements.txt


# Instalación de las dependencias de Python (con optimización)
RUN pip install --upgrade pip \
    && yes w | pip install -r requirements.txt


# Copiar el código fuente de la aplicación
COPY . .


# Copiar y otorgar permisos a los scripts
COPY wait-for-databases.sh /usr/bin/wait-for-databases
COPY celery.sh /usr/bin/celery-commands
COPY celery-cmd /usr/bin/celery-cmd

# Conceder permisos a los scripts y archivos del proyecto
RUN chmod +x /usr/bin/wait-for-databases \
    && chmod +x /usr/bin/celery-commands \
    && chmod +x /usr/bin/celery-cmd \
    && chmod +x /usr/src/geonode/tasks.py \
    && chmod +x /usr/src/geonode/entrypoint.sh \
    && chmod +x /usr/src/geonode/geonoxt_bash_entrypoint.sh \
    && chown -R www-data:www-data /usr/src/geonode \
    && mkdir -p /usr/lib64/sasl2


# Exponer puertos
EXPOSE 8000


# Entrypoint comentado por ahora, dependiendo del uso
# ENTRYPOINT /usr/src/geonode/entrypoint.sh
