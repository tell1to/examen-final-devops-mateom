from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Configuración de API (puedes usar OpenAI, Hugging Face, o similar)
API_KEY = os.getenv('API_KEY', 'default-key')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/', methods=['GET'])
def home():
    """Endpoint principal que retorna información de la aplicación"""
    return jsonify({
        "status": "ok",
        "message": "Saludos a todos desde Python con IA",
        "version": "1.0.5"
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para procesar mensajes con IA"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Se requiere un mensaje"}), 400
        
        message = data.get('message', '')
        
        # Usar un modelo de IA simple (simulado aquí)
        response = process_with_ai(message)
        
        return jsonify({
            "status": "ok",
            "input": message,
            "response": response
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

def process_with_ai(message: str) -> str:
    """Procesa un mensaje con IA (simulado)"""
    # Implementación simple sin API externa para evitar dependencias de pago
    responses = {
        "hola": "¡Hola! ¿Cómo estás?",
        "ayuda": "Estoy aquí para ayudarte. Puedes enviarme mensajes.",
        "nombre": "Soy una aplicación Flask con capacidades de IA",
        "gracias": "¡De nada!",
        "default": f"Recibí tu mensaje: '{message}'. Procesado correctamente."
    }
    
    message_lower = message.lower().strip()
    for key, response in responses.items():
        if key in message_lower:
            return response
    
    return responses["default"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)