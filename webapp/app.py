from flask import Flask, request, jsonify
import socket
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Récupération des variables d'environnement pour la connexion à la DB
DB_HOST = os.environ.get('DB_HOST', 'postgres-svc')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'requestdb')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

# Récupération du nom et de l'IP du conteneur
HOSTNAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOSTNAME)

def get_db_connection():
    """Établit une connexion à la base de données PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route('/')
def home():
    """Page d'accueil affichant les informations du conteneur."""
    try:
        # Enregistrement de la requête dans la base de données
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Vérification que la table existe, sinon la créer
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id SERIAL PRIMARY KEY,
                container_name VARCHAR(255),
                container_ip VARCHAR(255),
                request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertion de la nouvelle requête
        cursor.execute(
            "INSERT INTO requests (container_name, container_ip) VALUES (%s, %s)",
            (HOSTNAME, IP_ADDRESS)
        )
        
        # Récupération du compte total des requêtes pour ce conteneur
        cursor.execute(
            "SELECT COUNT(*) FROM requests WHERE container_name = %s",
            (HOSTNAME,)
        )
        request_count = cursor.fetchone()[0]
        
        # Récupération de toutes les requêtes
        cursor.execute(
            "SELECT container_name, container_ip, request_time FROM requests ORDER BY request_time DESC"
        )
        all_requests = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Construction de la réponse HTML
        html_response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Informations du conteneur</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <h1>Container info</h1>
            <p><strong>Name :</strong> {HOSTNAME}</p>
            <p><strong>IP adress:</strong> {IP_ADDRESS}</p>
            <p><strong>Nombre de requêtes reçues par ce conteneur:</strong> {request_count}</p>
            
            <h2>Historique des requêtes</h2>
            <table>
                <tr>
                    <th>Conteneur</th>
                    <th>IP</th>
                    <th>Horodatage</th>
                </tr>
        """
        
        for req in all_requests:
            html_response += f"""
                <tr>
                    <td>{req[0]}</td>
                    <td>{req[1]}</td>
                    <td>{req[2]}</td>
                </tr>
            """
        
        html_response += """
            </table>
        </body>
        </html>
        """
        
        return html_response
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "container_name": HOSTNAME,
            "container_ip": IP_ADDRESS
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)