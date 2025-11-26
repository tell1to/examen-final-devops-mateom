from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

# Configuración de API (puedes usar OpenAI, Hugging Face, o similar)
API_KEY = 'default-key'
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tello - IA Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .version {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            margin-top: 10px;
        }
        
        .content {
            padding: 30px;
        }
        
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        
        .info-box strong {
            color: #667eea;
        }
        
        .chat-section {
            margin-bottom: 30px;
        }
        
        .chat-section h2 {
            font-size: 18px;
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        .chat-section h2:before {
            content: "💬";
            margin-right: 10px;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        #messageInput {
            flex: 1;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        #messageInput:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-send {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-send:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-send:active {
            transform: translateY(0);
        }
        
        .response-box {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            min-height: 50px;
            border-left: 4px solid #667eea;
        }
        
        .response-box.loading {
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.7; }
            50% { opacity: 1; }
        }
        
        .response-label {
            font-weight: 600;
            color: #667eea;
            font-size: 12px;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        
        .response-text {
            color: #333;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .endpoints-section {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }
        
        .endpoints-section h3 {
            font-size: 14px;
            color: #667eea;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        
        .endpoint-item {
            background: #f8f9fa;
            padding: 10px 15px;
            margin-bottom: 8px;
            border-radius: 5px;
            font-size: 12px;
            color: #555;
            font-family: 'Courier New', monospace;
        }
        
        .endpoint-item code {
            color: #667eea;
            font-weight: 600;
        }
        
        .status-badge {
            display: inline-block;
            background: #4caf50;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 10px;
        }
        
        .error {
            background: #ffebee;
            border-left-color: #f44336;
        }
        
        .error .response-text {
            color: #c62828;
        }
        
        .success {
            background: #e8f5e9;
            border-left-color: #4caf50;
        }
        
        .success .response-text {
            color: #2e7d32;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Murillo IA</h1>
            <p>Asistente inteligente de chat</p>
            <div class="version">v1.0.5</div>
        </div>
        
        <div class="content">
            <div class="info-box">
                <strong>✓ Estado:</strong> Sistema en línea y funcionando correctamente
            </div>
            
            <div class="chat-section">
                <h2>Envía tu mensaje</h2>
                <div class="input-group">
                    <input 
                        type="text" 
                        id="messageInput" 
                        placeholder="Escribe tu mensaje aquí..." 
                        onkeypress="handleKeyPress(event)"
                    >
                    <button class="btn btn-send" onclick="sendMessage()">Enviar</button>
                </div>
                
                <div id="response" class="response-box" style="display:none;">
                    <div class="response-label">Respuesta</div>
                    <div class="response-text" id="responseText"></div>
                </div>
            </div>
            
            <div class="endpoints-section">
                <h3>📡 Endpoints Disponibles</h3>
                <div class="endpoint-item"><code>GET /</code> - Información de la aplicación</div>
                <div class="endpoint-item"><code>POST /api/chat</code> - Enviar mensaje a IA</div>
                <div class="endpoint-item"><code>GET /api/health</code> - Estado del servicio</div>
            </div>
        </div>
    </div>
    
    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) {
                alert('Por favor ingresa un mensaje');
                return;
            }
            
            const responseDiv = document.getElementById('response');
            responseDiv.className = 'response-box loading';
            responseDiv.style.display = 'block';
            document.getElementById('responseText').innerText = 'Procesando...';
            
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                responseDiv.classList.remove('loading');
                if (data.response) {
                    responseDiv.className = 'response-box success';
                    document.getElementById('responseText').innerText = data.response;
                } else if (data.error) {
                    responseDiv.className = 'response-box error';
                    document.getElementById('responseText').innerText = 'Error: ' + data.error;
                }
                input.value = '';
                input.focus();
            })
            .catch(error => {
                responseDiv.className = 'response-box error';
                document.getElementById('responseText').innerText = 'Error: ' + error.message;
                responseDiv.classList.remove('loading');
            });
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Focus en el input al cargar
        window.addEventListener('load', function() {
            document.getElementById('messageInput').focus();
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    """Endpoint principal que retorna la interfaz web"""
    return Response(HTML_TEMPLATE, mimetype='text/html')

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
    return jsonify({"status": "healthy", "version": "1.0.5"}), 200

def process_with_ai(message: str) -> str:
    """Procesa un mensaje con IA (simulado)"""
    # Implementación simple sin API externa para evitar dependencias de pago
    responses = {
        "hola": "¡Hola! Bienvenido a Murillo IA. ¿Cómo puedo ayudarte hoy?",
        "ayuda": "Estoy aquí para ayudarte. Puedes enviarme mensajes y te responderé lo más rápido posible.",
        "nombre": "Soy Murillo, una aplicación Flask con capacidades de IA desarrollada como examen CI/CD.",
        "gracias": "¡De nada! Siempre es un placer ayudar.",
        "versión": "Estoy ejecutando la versión 1.0.5 del sistema.",
        "estado": "Todo funciona perfectamente. El sistema está en línea y listo.",
        "default": f"Recibí tu mensaje: '{message}'. Lo he procesado correctamente. ¿Hay algo más en lo que pueda ayudarte?"
    }
    
    message_lower = message.lower().strip()
    for key, response in responses.items():
        if key in message_lower:
            return response
    
    return responses["default"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)