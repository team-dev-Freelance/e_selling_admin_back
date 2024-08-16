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

