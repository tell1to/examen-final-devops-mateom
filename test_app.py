import pytest
from app import app, process_with_ai

@pytest.fixture
def client():
    """Fixture para el cliente de prueba de Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestApp:
    """Tests para la aplicación Flask"""
    
    def test_home_endpoint(self, client):
        """Test para el endpoint principal"""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert 'message' in data
        assert data['version'] == '1.0.5'
    
    def test_health_endpoint(self, client):
        """Test para el health check"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_chat_endpoint_valid(self, client):
        """Test para el endpoint de chat con mensaje válido"""
        response = client.post('/api/chat', 
                              json={'message': 'hola'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert 'response' in data
    
    def test_chat_endpoint_missing_message(self, client):
        """Test para el endpoint de chat sin mensaje"""
        response = client.post('/api/chat', 
                              json={},
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_chat_endpoint_empty_message(self, client):
        """Test para el endpoint de chat con mensaje vacío"""
        response = client.post('/api/chat', 
                              json={'message': ''},
                              content_type='application/json')
        assert response.status_code == 200
    
    def test_process_with_ai_known_input(self):
        """Test para procesar mensajes conocidos con IA"""
        result = process_with_ai("hola")
        assert "¡Hola!" in result
    
    def test_process_with_ai_unknown_input(self):
        """Test para procesar mensajes desconocidos con IA"""
        result = process_with_ai("xyz123")
        assert "Recibí tu mensaje" in result
    
    def test_process_with_ai_case_insensitive(self):
        """Test para verificar que el procesamiento es case-insensitive"""
        result1 = process_with_ai("HOLA")
        result2 = process_with_ai("hola")
        assert result1 == result2

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
