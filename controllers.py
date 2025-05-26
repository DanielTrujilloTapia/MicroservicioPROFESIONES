from flask import jsonify, request
from db_config import get_db_connection
import uuid

#TABLA PROFESIONES

# Obtener todas las profesiones
def get_profesiones():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_profesion, nombre, descripcion, fecha FROM profesion")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    profesiones = [{"id_profesion": r[0], "nombre": r[1], "descripcion": r[2], "fecha": str(r[3])} for r in rows]
    return jsonify(profesiones)

# Obtener una profesión por nombre
def get_profesion_by_nombre(nombre):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_profesion, nombre, descripcion, fecha FROM profesion WHERE nombre = %s", (nombre,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        profesion = {"id_profesion": row[0], "nombre": row[1], "descripcion": row[2], "fecha": str(row[3])}
        return jsonify(profesion)
    else:
        return jsonify({"message": "Profesión no encontrada"}), 404

# Crear una nueva profesión
def create_profesion():
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    fecha = data['fecha']

    id_profesion = str(uuid.uuid4())  # Generar UUID

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO profesion (id_profesion, nombre, descripcion, fecha) VALUES (%s, %s, %s, %s)",
        (id_profesion, nombre, descripcion, fecha)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Profesión agregada correctamente",
        "id_profesion": id_profesion
    }), 201

# Actualizar una profesión por ID
def update_profesion(id_profesion):
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    fecha = data['fecha']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE profesion SET nombre=%s, descripcion=%s, fecha=%s WHERE id_profesion=%s", (nombre, descripcion, fecha, id_profesion))
    conn.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conn.close()

    if filas_afectadas == 0:
        return jsonify({"message": "Profesión no encontrada"}), 404
    else:
        return jsonify({"message": "Profesión actualizada correctamente"})

# Eliminar una profesión por ID
def delete_profesion_by_nombre(nombre):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profesion WHERE nombre=%s", (nombre,))
    conn.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conn.close()

    if filas_afectadas == 0:
        return jsonify({"message": "Profesión no encontrada"}), 404
    else:
        return jsonify({"message": "Profesión eliminada correctamente"})





#TABLA PERSONA PROFESIONES
# Asignar profesión a persona
def asignar_profesion_persona():
    data = request.get_json()
    persona_id = data.get('persona_id')
    profesion_id = data.get('profesion_id')
    fecha_asignacion = data.get('fecha_asignacion')

    if not persona_id or not profesion_id or not fecha_asignacion:
        return jsonify({"message": "Faltan datos: persona_id, profesion_id y fecha_asignacion son requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO persona_profesion (persona_id, profesion_id, fecha_asignacion) VALUES (%s, %s, %s)"
        cursor.execute(query, (persona_id, profesion_id, fecha_asignacion))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Asignación registrada correctamente"}), 201

# Eliminar asignación profesión-persona
def eliminar_profesion_persona():
    persona_id = request.args.get('persona_id')
    profesion_id = request.args.get('profesion_id')

    if not persona_id or not profesion_id:
        return jsonify({"message": "Faltan parámetros: persona_id y profesion_id son requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM persona_profesion WHERE persona_id=%s AND profesion_id=%s", (persona_id, profesion_id))
    conn.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conn.close()

    if filas_afectadas == 0:
        return jsonify({"message": "Asignación no encontrada"}), 404
    else:
        return jsonify({"message": "Asignación eliminada correctamente"}), 200


def obtener_personas_profesiones():
    # Consumir las APIs externas
    try:
        personas_response = requests.get("https://microservicioine.onrender.com/api/ine/personasAll")
        profesiones_response = requests.get("http://127.0.0.1:5000/api/profesiones")

        personas_response.raise_for_status()
        profesiones_response.raise_for_status()

        personas = personas_response.json()
        profesiones = profesiones_response.json()

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al consumir las APIs externas: {str(e)}"}), 500

    # Crear diccionarios para fácil búsqueda
    personas_dict = {p["id"]: p for p in personas}
    profesiones_dict = {p["id"]: p for p in profesiones}

    # Obtener relaciones desde la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT persona_id, profesion_id, fecha_asignacion FROM persona_profesion")
    relaciones = cursor.fetchall()
    cursor.close()
    conn.close()

    # Armar respuesta combinada
    resultado = []
    for r in relaciones:
        persona = personas_dict.get(r[0])
        profesion = profesiones_dict.get(r[1])

        if persona and profesion:
            resultado.append({
                "persona_id": r[0],
                "persona_nombre": persona["nombre"],  # Ajusta según cómo venga desde la API
                "profesion_id": r[1],
                "profesion_nombre": profesion["nombre"],
                "fecha_asignacion": str(r[2])
            })

    return jsonify(resultado)