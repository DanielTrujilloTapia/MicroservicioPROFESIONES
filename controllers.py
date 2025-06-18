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
