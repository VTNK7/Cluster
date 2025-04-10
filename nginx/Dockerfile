FROM nginx:latest

# Copier le script
COPY generate_index.sh /usr/share/nginx/html/generate_index.sh

# Donner les permissions d'exécution au script
RUN chmod +x /usr/share/nginx/html/generate_index.sh

# Exposer le port 80
EXPOSE 80

# Utiliser ENTRYPOINT pour exécuter le script et démarrer Nginx
ENTRYPOINT ["/bin/bash", "-c", "/usr/share/nginx/html/generate_index.sh && nginx -g 'daemon off;'"]