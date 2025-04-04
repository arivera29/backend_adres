from ..services.services import AdquisicionesService
from ..database import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

route = Blueprint('route', __name__)

adquisiciones_service = AdquisicionesService(db.session)

@route.route('/autenticar', methods=['POST'])
def authenticate():
    """
    Endpoint para autenticar un usuario.
    Recibe un JSON con 'username' y 'password'.
    Devuelve un token JWT si la autenticación es exitosa.
    """
    data = request.get_json()
    result, status = adquisiciones_service.autenticar(username=data['username'], password=data['password'])
    return jsonify(result), status

@route.route('/adquisiciones', methods=['POST'])
@jwt_required()
def create_adquisicion():
    """
    Endpoint para crear una nueva adquisicion.
    Requiere autenticación JWT.
    Recibe un JSON con los datos de la adquisicion.
    Devuelve el objeto creado y un código de estado.
    """
    data = request.get_json()
    result, status = adquisiciones_service.create_adquisicion(data)
    return jsonify(result), status

@route.route('/adquisiciones', methods=['GET'])
@jwt_required()
def get_all_adquisiciones():
    """
    Endpoint para obtener todas las adquisiciones.
    Requiere autenticación JWT.
    Devuelve una lista de adquisiciones y un código de estado.
    """
    result, status = adquisiciones_service.get_all_adquisiciones()
    return jsonify(result), status

@route.route('/adquisiciones/<int:id>', methods=['GET'])
@jwt_required()
def get_adquisicion_by_id(id):
    """
    Endpoint para obtener una adquisicion por ID.
    Requiere autenticación JWT.
    Devuelve el objeto adquisicion y un código de estado.
    """
    result, status = adquisiciones_service.get_adquisicion_by_id(id)
    return jsonify(result), status

@route.route('/adquisiciones/<int:id>', methods=['PUT'])
@jwt_required()
def update_adquisicion(id):
    """
    Endpoint para actualizar una adquisicion por ID.
    Requiere autenticación JWT.
    Recibe un JSON con los nuevos datos de la adquisicion.
    Devuelve el objeto actualizado y un código de estado.
    """
    data = request.get_json()
    result, status = adquisiciones_service.update_adquisicion(id, data)
    return jsonify(result), status

@route.route('/adquisiciones/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_adquisicion(id):
    """
    Endpoint para eliminar una adquisicion por ID.
    Requiere autenticación JWT.
    Devuelve un mensaje de éxito y un código de estado.
    """
    result, status = adquisiciones_service.delete_adquisicion(id)
    return jsonify(result), status
