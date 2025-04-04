#!/bin/bash

# Récupérer l'adresse IP du conteneur
CONTAINER_IP=$(hostname -I | awk '{print $1}')

# Récupérer le nom du conteneur
CONTAINER_NAME=$(hostname)

# Créer un fichier HTML avec les informations
cat <<EOF > /usr/share/nginx/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Container Info</title>
</head>
<body>
    <h1>NGINX</h1>
    <p>IP Container : $CONTAINER_IP</p>
    <p>ID Container : $CONTAINER_NAME</p>
</body>
</html>
EOF