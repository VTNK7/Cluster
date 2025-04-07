FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances
RUN pip install --no-cache-dir flask psycopg2-binary requests

# Copie du code de l'application
COPY app.py .

# Variable d'environnement pour la connexion à la base de données
ENV DB_HOST=postgres-svc
ENV DB_PORT=5432
ENV DB_NAME=requestdb
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres

# Exposition du port
EXPOSE 5000

# Démarrage de l'application
CMD ["python", "app.py"]