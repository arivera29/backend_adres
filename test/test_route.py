import pytest
from flask import Flask
from flask_jwt_extended import create_access_token, JWTManager
from app.routes.route import route
from app.services.services import AdquisicionesService
from app.config import Config

@pytest.fixture
def app():
    """Crea una aplicación Flask para pruebas."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    app.register_blueprint(route, url_prefix='/api')
    jwt = JWTManager(app)
    return app

@pytest.fixture
def client(app):
    """Crea un cliente de prueba."""
    return app.test_client()

@pytest.fixture
def auth_header(app):
    """Genera un token JWT para pruebas."""
    with app.app_context():
        token = create_access_token(identity='admin')
    return {'Authorization': f'Bearer {token}'}

def test_authenticate(client, mocker):
    """Prueba el endpoint /autenticar."""
    mock_service = mocker.patch('app.services.services.AdquisicionesService.autenticar')
    mock_service.return_value = ({"token": "test-token"}, 200)

    response = client.post('/api/autenticar', json={
        'username': 'admin',
        'password': 'admin'
    })

    assert response.status_code == 200
    assert response.json['token'] == 'test-token'

def test_create_adquisicion(client, auth_header, mocker):
    """Prueba el endpoint /adquisiciones (POST)."""
    mock_service = mocker.patch('app.services.services.AdquisicionesService.create_adquisicion')
    mock_service.return_value = ({"id": 1, "presupuesto": 1000}, 201)

    response = client.post('/api/adquisiciones', json={
        'presupuesto': 1000,
        'unidad_administrativa': 'Finanzas'
    }, headers=auth_header)

    assert response.status_code == 201
    assert response.json['id'] == 1

def test_get_all_adquisiciones(client, auth_header, mocker):
    """Prueba el endpoint /adquisiciones (GET)."""
    mock_service = mocker.patch('app.services.services.AdquisicionesService.get_all_adquisiciones')
    mock_service.return_value = ([{"id": 1, "presupuesto": 1000}], 200)

    response = client.get('/api/adquisiciones', headers=auth_header)

    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_adquisicion_by_id(client, auth_header, mocker):
    """Prueba el endpoint /adquisiciones/<id> (GET)."""
    mock_service = mocker.patch('app.services.services.AdquisicionesService.get_adquisicion_by_id')
    mock_service.return_value = ({"id": 1, "presupuesto": 1000}, 200)

    response = client.get('/api/adquisiciones/1', headers=auth_header)

    assert response.status_code == 200
    assert response.json['id'] == 1

def test_update_adquisicion(client, auth_header, mocker):
    """Prueba el endpoint /adquisiciones/<id> (PUT)."""
    mock_service = mocker.patch('app.services.services.AdquisicionesService.update_adquisicion')
    mock_service.return_value = ({"id": 1, "presupuesto": 2000}, 200)

    response = client.put('/api/adquisiciones/1', json={
        'presupuesto': 2000
    }, headers=auth_header)

    assert response.status_code == 200
    assert response.json['presupuesto'] == 2000

def test_delete_adquisicion(client, auth_header, mocker):
    """Prueba el endpoint /adquisiciones/<id> (DELETE)."""
    mock_service = mocker.patch('app.services.services.AdquisicionesService.delete_adquisicion')
    mock_service.return_value = ({"message": "Deleted successfully"}, 200)

    response = client.delete('/api/adquisiciones/1', headers=auth_header)

    assert response.status_code == 200
    assert response.json['message'] == "Deleted successfully"