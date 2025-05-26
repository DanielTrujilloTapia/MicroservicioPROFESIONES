from flask import Blueprint
from controllers import asignar_profesion_persona, eliminar_profesion_persona

persona_profesion_bp = Blueprint('persona_profesion_bp', __name__)

# Asignar profesión a persona
@persona_profesion_bp.route('/persona_profesion', methods=['POST'])
def asignar_profesion():
    return asignar_profesion_persona()

# Eliminar asignación
@persona_profesion_bp.route('/persona_profesion', methods=['DELETE'])
def eliminar_asignacion():
    return eliminar_profesion_persona()
