# Utiliser une image de base avec Python et OpenCV préinstallé
FROM python:3.9-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Créer et définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY ./app/requirements.txt .
COPY ./app .

# Créer les répertoires nécessaires
RUN mkdir -p /app/utils/models \
    && mkdir -p /app/utils/uploads \
    && mkdir -p /app/utils/outputs

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port Streamlit
EXPOSE 8501

# Commande par défaut au lancement
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]