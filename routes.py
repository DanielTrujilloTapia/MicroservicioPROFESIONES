from flask import Blueprint
from controllers import (
    get_profesiones, 
    get_profesion_by_nombre, 
    create_profesion, 
    update_profesion,  
    delete_profesion_by_nombre
)

profesiones_bp = Blueprint('profesiones_bp', __name__)

# Obtener todas las profesiones
@profesiones_bp.route('/obtenerProfesiones', methods=['GET'])
def obtener_profesiones():
    return get_profesiones()

# Obtener profesión por nombre
@profesiones_bp.route('/obtenerProfesion/nombre/<nombre>', methods=['GET'])
def obtener_profesion_por_nombre(nombre):
    return get_profesion_by_nombre(nombre)

# Crear nueva profesión
@profesiones_bp.route('/guardarProfesion', methods=['POST'])
def agregar_profesion():
    return create_profesion()

# Actualizar profesión por ID
@profesiones_bp.route('/actualizarProfesion/<id_profesion>', methods=['PUT'])
def actualizar_profesion(id_profesion):
    return update_profesion(id_profesion)

# Eliminar profesión por nombre
@profesiones_bp.route('/eliminarProfesion/nombre/<nombre>', methods=['DELETE'])
def eliminar_profesion_por_nombre(nombre):
    return delete_profesion_by_nombre(nombre)


