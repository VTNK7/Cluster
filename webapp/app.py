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
        
        # Récupération des statistiques par conteneur
        cursor.execute("""
            SELECT container_name, container_ip, COUNT(*) as request_count 
            FROM requests 
            GROUP BY container_name, container_ip 
            ORDER BY request_count DESC
        """)
        container_stats = cursor.fetchall()
        
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
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f8f9fa; color: #333; }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                h1, h2 {{ color: #2c3e50; }}
                .info-box {{ background-color: #e3f2fd; border-left: 5px solid #2196f3; padding: 15px; margin-bottom: 20px; border-radius: 4px; }}
                .stats-container {{ display: flex; justify-content: space-between; margin: 20px 0; }}
                .stat-card {{ flex: 1; margin: 0 10px; padding: 15px; background-color: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; }}
                .stat-card:first-child {{ margin-left: 0; }}
                .stat-card:last-child {{ margin-right: 0; }}
                .stat-number {{ font-size: 28px; font-weight: bold; color: #2196f3; margin: 10px 0; }}
                .stat-label {{ color: #666; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #f2f2f2; color: #333; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                tr:hover {{ background-color: #f1f1f1; }}
                .container-stats {{ margin-top: 30px; background-color: white; border-radius: 8px; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                .highlight {{ background-color: #e8f5e9; }}
                .bar-container {{ height: 20px; background-color: #eceff1; border-radius: 10px; margin-top: 5px; overflow: hidden; }}
                .bar {{ height: 100%; background-color: #4caf50; border-radius: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Information du Conteneur</h1>
                
                <div class="info-box">
                    <p><strong>Nom:</strong> {HOSTNAME}</p>
                    <p><strong>Adresse IP:</strong> {IP_ADDRESS}</p>
                    <p><strong>Requêtes reçues par ce conteneur:</strong> {request_count}</p>
                </div>
                
                <div class="container-stats">
                    <h2>Statistiques par Conteneur</h2>
        """
        
        # Calcul du maximum pour normaliser les barres
        max_requests = max([stats[2] for stats in container_stats]) if container_stats else 0
        
        for container in container_stats:
            container_name = container[0]
            container_ip = container[1]
            count = container[2]
            percentage = (count / max_requests * 100) if max_requests > 0 else 0
            is_current = container_name == HOSTNAME
            
            html_response += f"""
                <div class="stat-card {'highlight' if is_current else ''}">
                    <div class="stat-label">Conteneur</div>
                    <div><strong>{container_name}</strong></div>
                    <div class="stat-label">IP</div>
                    <div>{container_ip}</div>
                    <div class="stat-label">Requêtes</div>
                    <div class="stat-number">{count}</div>
                    <div class="bar-container">
                        <div class="bar" style="width: {percentage}%;"></div>
                    </div>
                </div>
            """
        
        html_response += """
                </div>
                
                <h2>Historique des requêtes</h2>
                <table>
                    <tr>
                        <th>Conteneur</th>
                        <th>IP</th>
                        <th>Horodatage</th>
                    </tr>
        """
        
        for req in all_requests:
            is_current = req[0] == HOSTNAME
            html_response += f"""
                <tr class="{'highlight' if is_current else ''}">
                    <td>{req[0]}</td>
                    <td>{req[1]}</td>
                    <td>{req[2]}</td>
                </tr>
            """
        
        html_response += """
                </table>
            </div>
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