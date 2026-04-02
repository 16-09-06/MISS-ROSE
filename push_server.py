from flask import Flask, request, jsonify
from flask_cors import CORS
from pywebpush import webpush, WebPushException
import json

app = Flask(__name__)
CORS(app) # Isso impede que o navegador bloqueie o robô

# Suas chaves VAPID geradas
VAPID_PRIVATE_KEY = "7sgXHbkDLECmWtIOw8HB34sYz0UBndUlK5ot1DTVpO4"
VAPID_CLAIMS = {
    "sub": "mailto:faturamento@missrosebra.com"
}

@app.route('/enviar-push', methods=['POST'])
def enviar_push():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado fornecido"}), 400
        
    subscription_info = dados.get('subscription')
    
    mensagem = json.dumps({
        "title": dados.get('title', 'Miss Rôse'),
        "body": dados.get('body', 'Nova notificação!'),
        "url": "/"
    })
    
    try:
        # Disparo nativo criptografado
        webpush(
            subscription_info=subscription_info,
            data=mensagem,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS,
            ttl=86400 # Tempo de Vida (TTL) de 24 horas
        )
        return jsonify({"status": "sucesso"}), 200
        
    except WebPushException as ex:
        return jsonify({"status": "erro", "detalhe": repr(ex)}), 500

@app.route('/', methods=['GET'])
def hello_world():
    return 'Robô de Mensagens da Miss Rôse 🚀 (Online)'

if __name__ == '__main__':
    app.run(port=5000, debug=True)