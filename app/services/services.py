from ..database import db
from ..models.model import Adquisiciones
from ..config import Config
from datetime import datetime
from sqlalchemy.exc import IntegrityError, DataError
import jwt
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

class AdquisicionesService:
    """
    Clase de servicio para manejar las operaciones CRUD de adquisiciones.
    """
    def __init__(self, db_session):
        self.db_session = db_session

    def _validar_data(self, data, fields_required):
        """
        Valida que los campos requeridos estén presentes en los datos de entrada.
        """
        for field in fields_required:
            if field not in data:
                return {"error": True, "message": f"Campo '{field}' es requerido"}, 400
        return None
    
    def _validar_tipo(self, data):
        """
        Valida que los tipos de datos sean correctos.
        """
        if not isinstance(data['unidad_administrativa'], str) or not isinstance(data['tipo_bien'], str) or not isinstance(data['proveedor'], str) or not isinstance(data['documentacion'], str):
            return {"error": True, "message": "Unidad administrativa, tipo de bien, proveedor y documentacion deben ser cadenas"}, 400
        if not isinstance(data['presupuesto'], (int, float)) or not isinstance(data['cantidad'], int) or not isinstance(data['valor_total'], (int, float)):
            return {"error": True, "message": "Presupuesto y valor total deben ser numeros, cantidad debe ser un entero"}, 400
        if 'fecha_adquisicion' in data and not isinstance(data['fecha_adquisicion'], str):
            return {"error": True, "message": "Fecha adquisicion debe ser una cadena en formato YYYY-MM-DD"}, 400
        if 'activo' in data and not isinstance(data['activo'], bool):
            return {"error": True, "message": "Activo debe ser un booleano"}, 400
        return None

    def create_adquisicion(self, data):
        """
        Crea una nueva adquisicion en la base de datos.
        """
        try:
            # Validar datos de entrada
            fields_required = ['presupuesto', 'unidad_administrativa', 'tipo_bien', 'cantidad', 'valor_total', 'proveedor', 'documentacion']
            validation_error = self._validar_data(data, fields_required)
            if validation_error:
                return validation_error
            
            # Validar tipos de datos
            type_error = self._validar_tipo(data)
            if type_error:
                return type_error
            

            try:
                presupuesto = float(data['presupuesto'])
                cantidad = int(data['cantidad'])
                valor_total = float(data['valor_total'])
            except (ValueError, KeyError) as e:
                raise ValueError("Formato de numero invalido") from e
            if presupuesto <= 0 or cantidad <= 0 or valor_total <= 0:
                raise ValueError("Presupuesto, cantidad y valor total deben ser mayores a cero")
            if 'fecha_adquisicion' in data:
                try:
                    data['fecha_adquisicion'] = datetime.strptime(data['fecha_adquisicion'], '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError("Formato de fecha invalido, debe ser YYYY-MM-DD")
            
            new_adquisicion = Adquisiciones(
                presupuesto=presupuesto,
                unidad_administrativa=data['unidad_administrativa'],
                tipo_bien=data['tipo_bien'],
                cantidad=cantidad,
                valor_total=valor_total,
                fecha_adquisicion=data['fecha_adquisicion'],
                proveedor=data['proveedor'],
                documentacion=data['documentacion'],
                activo=data['activo']
            )
            self.db_session.add(new_adquisicion)
            self.db_session.commit()
            return new_adquisicion.to_dict(), 201
        except IntegrityError as e:
            self.db_session.rollback()
            return {"error": True, "message": f"IntegrityError: {str(e)}"}, 409
        except DataError as e:
            self.db_session.rollback()
            return {"error": True, "message": f"DataError: Invalid data type {str(e)}"}, 400
        except ValueError as e:
            self.db_session.rollback()
            return {"error": True, "message": f"ValueError: {str(e)}"}, 400
        except Exception as e:
            self.db_session.rollback()
            return {"error": True, "message": f"Exception: {str(e)}"}, 400
        

    def get_all_adquisiciones(self):
        """
        Obtiene todas las adquisiciones de la base de datos.
        """
        try:
            adquisiciones = Adquisiciones.query.order_by(Adquisiciones.id.desc()).all()
            return [adquisicion.to_dict() for adquisicion in adquisiciones],200
        except IntegrityError as e:
            return {"error": True, "message": f"IntegrityError: {str(e)}"}, 409
        except Exception as e:
            return {"error": True, "message": f"Exception: {str(e)}"}, 400

    def get_adquisicion_by_id(self, id):
        """
        Obtiene una adquisicion por su ID.
        """
        try:
            adquisicion = Adquisiciones.query.get(id)
            if not adquisicion:
                return {"error": True, "message": f"Adqicisión no encontrado con el ID {id}"}, 404
            return adquisicion.to_dict(), 200
        except IntegrityError as e:
            return {"error": True, "message": f"IntegrityError: {str(e)}"}, 409
        except Exception as e:
            return {"error": True, "message": f"Exception: {str(e)}"}, 400

    def update_adquisicion(self, id, data):
        """
        Actualiza una adquisicion existente en la base de datos.
        """
        
        # Validar datos de entrada
        fields_required = ['presupuesto', 'unidad_administrativa', 'tipo_bien', 'cantidad', 'valor_total', 'proveedor', 'documentacion']
        validation_error = self._validar_data(data, fields_required)
        if validation_error:
            return validation_error
        
        # Validar tipos de datos
        type_error = self._validar_tipo(data)
        if type_error:
            return type_error
        
        try:
            adquisicion = Adquisiciones.query.get(id)
            if not adquisicion:
                return {"error": True, "message": f"Adqicisión no encontrado con el ID {id}"}, 404
            for key, value in data.items():
                setattr(adquisicion, key, value)
            self.db_session.commit()
            return adquisicion.to_dict(), 200
        except IntegrityError as e:
            self.db_session.rollback()
            return {"error": True, "message": f"IntegrityError: {str(e)}"}, 409
        except DataError as e:
            self.db_session.rollback()
            return {"error": True, "message": f"DataError: Invalid data type {str(e)}"}, 400
        except ValueError as e:
            self.db_session.rollback()
            return {"error": True, "message": f"ValueError: {str(e)}"}, 400
        except Exception as e:
            self.db_session.rollback()
            return {"error": True, "message": f"Exception: {str(e)}"}, 400

    def delete_adquisicion(self, id):
        """
        Elimina una adquisicion por su ID.
        """
        try:
            adquisicion = Adquisiciones.query.get(id)
            if not adquisicion:
                return {"error": True, "message": f"Adqicisión no encontrado con el ID {id}"}, 404
            self.db_session.delete(adquisicion)
            self.db_session.commit()
            return {"error": False, "message": "Adquisición eliminada correctamente"}, 200
        except IntegrityError as e:
            self.db_session.rollback()
            return {"error": True, "message": f"IntegrityError: {str(e)}"}, 409
        except Exception as e:
            self.db_session.rollback()
            return {"error": True, "message": f"Exception: {str(e)}"}, 400
        
    def autenticar(self, username, password):
        """
        Autentica un usuario y genera un token JWT.
        """
        try:
            # Aquí deberías implementar la lógica de autenticación
            # Por ejemplo, verificar el nombre de usuario y la contraseña en la base de datos
            if username == "admin" and password == "admin":

                # Generar el token
                additional_claims = {"username": username}
                
                access_token = create_access_token(
                    identity=username, additional_claims=additional_claims
                )

                return {"error": False, "message": "Autenticación exitosa", "token": access_token}, 200
            else:
                return {"error": True, "message": "Credenciales inválidas"}, 401
        except Exception as e:
            return {"error": True, "message": f"Exception: {str(e)}"}, 400
        