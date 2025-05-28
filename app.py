from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import datetime
import logging

# Initialisation de Flask et CORS
app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)

# Connexion MongoDB Atlas (corrigée avec tlsAllowInvalidCertificates)
MONGO_URI = "mongodb+srv://vzev88882:Slj3pzeMjxYwwJ8v@eurusdtrading1.cxzphj5.mongodb.net/?retryWrites=true&w=majority&appName=eurusdtrading1&tlsAllowInvalidCertificates=true"
client = MongoClient(MONGO_URI)
db = client['eurusdtrading1']
collection = db['market_data']

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data:
        data['received_at'] = datetime.datetime.now(datetime.UTC)  # Utilisation correcte de l'UTC
        collection.insert_one(data)
        logging.info(f"✅ Donnée stockée : {data}")
        return jsonify({'status': 'Webhook reçu et stocké'}), 200
    else:
        logging.warning("⚠️ Aucun JSON reçu")
        return jsonify({'status': 'Aucune donnée reçue'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

