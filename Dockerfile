## Utiliser une image de base officielle Python
#FROM python:3.10-slim
#
## Définir le répertoire de travail dans le conteneur
#WORKDIR /app
#
## Installer les dépendances système nécessaires
#RUN apt-get update && \
#    apt-get install -y gcc g++ pkg-config libmariadb-dev && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*
#
## Copier les fichiers de l'application dans le conteneur
#COPY . /app/
#
## Installer les dépendances Python
#RUN python -m venv /opt/venv && \
#    . /opt/venv/bin/activate && \
#    pip install --upgrade pip && \
#    pip install -r requirements.txt
#
## Exposer le port que l'application utilisera
#EXPOSE 8000
#
## Définir la commande pour démarrer l'application
#CMD ["/opt/venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "e_selling_admin_back.wsgi:application"]

# Utiliser une image Python officielle comme image de base
FROM python:3.10-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installer les dépendances système nécessaires pour mysqlclient
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de configuration
COPY requirements.txt /app/
COPY . /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Définir la commande d'exécution
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "e_selling_admin_back.wsgi:application"]
CMD ["sh", "-c", "python3.10 manage.py migrate && python3.10 manage.py runserver 0.0.0.0:8000"]
