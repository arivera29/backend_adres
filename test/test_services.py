import pytest
from app.services.services import AdquisicionesService
from app.database import db
from app.models.model import Adquisiciones
from flask import Flask

@pytest.fixture
def app():
    """Crea una aplicación Flask para pruebas con una base de datos en memoria."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos en memoria
    yield app
    with app.app_context():
        db.drop_all()  # Limpia la base de datos después de las pruebas

@pytest.fixture
def service(app):
    """Crea una instancia del servicio con la sesión de la base de datos."""
    with app.app_context():
        yield AdquisicionesService(db.session)

@pytest.fixture
def sample_adquisicion():
    """Datos de ejemplo para una adquisición."""
    return {
        "presupuesto": 1000,
        "unidad_administrativa": "Finanzas",
        "tipo_bien": "Equipo",
        "cantidad": 10,
        "valor_total": 10000,
        "proveedor": "Proveedor A",
        "documentacion": "Doc A",
        "activo": True
    }

def test_create_adquisicion(service, sample_adquisicion):
    """Prueba la creación de una adquisición."""
    result, status = service.create_adquisicion(sample_adquisicion)
    assert status == 201
    assert result["presupuesto"] == sample_adquisicion["presupuesto"]
    assert result["unidad_administrativa"] == sample_adquisicion["unidad_administrativa"]

def test_get_all_adquisiciones(service, sample_adquisicion):
    """Prueba la obtención de todas las adquisiciones."""
    service.create_adquisicion(sample_adquisicion)
    result, status = service.get_all_adquisiciones()
    assert status == 200
    assert len(result) == 1
    assert result[0]["presupuesto"] == sample_adquisicion["presupuesto"]

def test_get_adquisicion_by_id(service, sample_adquisicion):
    """Prueba la obtención de una adquisición por ID."""
    created, _ = service.create_adquisicion(sample_adquisicion)
    result, status = service.get_adquisicion_by_id(created["id"])
    assert status == 200
    assert result["id"] == created["id"]

def test_update_adquisicion(service, sample_adquisicion):
    """Prueba la actualización de una adquisición."""
    created, _ = service.create_adquisicion(sample_adquisicion)
    updated_data = sample_adquisicion
    updated_data["presupuesto"] = 2000
    result, status = service.update_adquisicion(created["id"], updated_data)
    assert status == 200
    assert result["presupuesto"] == 2000

def test_delete_adquisicion(service, sample_adquisicion):
    """Prueba la eliminación de una adquisición."""
    created, _ = service.create_adquisicion(sample_adquisicion)
    result, status = service.delete_adquisicion(created["id"])
    assert status == 200
    assert result["message"] == "Adquisición eliminada correctamente"

def test_get_adquisicion_by_id_not_found(service):
    """Prueba la obtención de una adquisición por ID inexistente."""
    result, status = service.get_adquisicion_by_id(999)
    assert status == 404
    assert result["error"] is True

def test_update_adquisicion_not_found(service):
    """Prueba la actualización de una adquisición inexistente."""
    updated_data = {
        "presupuesto": 1000,
        "unidad_administrativa": "Finanzas",
        "tipo_bien": "Equipo",
        "cantidad": 10,
        "valor_total": 10000,
        "proveedor": "Proveedor A",
        "documentacion": "Doc A",
        "activo": True
    }
    result, status = service.update_adquisicion(999, updated_data)
    assert status == 404
    assert result["error"] is True

def test_delete_adquisicion_not_found(service):
    """Prueba la eliminación de una adquisición inexistente."""
    result, status = service.delete_adquisicion(999)
    assert status == 404
    assert result["error"] is True