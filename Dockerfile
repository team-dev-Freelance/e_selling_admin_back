# Utiliser une image de base officielle Python
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && \
    apt-get install -y gcc g++ pkg-config libmariadb-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copier les fichiers de l'application dans le conteneur
COPY . /app/

# Installer les dépendances Python
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Exposer le port que l'application utilisera
EXPOSE 80

# Définir la commande pour démarrer l'application
CMD ["/opt/venv/bin/gunicorn", "--bind", "0.0.0.0:80", "e_selling_admin_back.wsgi:application"]
