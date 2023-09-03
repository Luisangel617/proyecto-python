from flask import Flask, jsonify, request, send_file
from psycopg2 import connect, extras
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)
key = Fernet.generate_key()

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="usuarios",
        user="postgres",
        password="sasa"
    )

    return conn

@app.get('/api/usuarios')
def get_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM usuario")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


@app.get('/api/usuarios/promedio-edades')
def promedio_edades():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT AVG(EXTRACT(YEAR FROM AGE(NOW(), fecha_nacimiento))) AS promedio_edades FROM usuario")
    edades = cur.fetchall()
    cur.close()
    conn.close()
    print(edades)
    return jsonify(edades)

@app.get('/api/estado')
def version_api():
    version = {
        'nameSystem': 'api-users', 
        'version': '0.0.1',
        'developer':'Luis Angel Quispe Limachi',
        'email': 'luisquispe@gmail.com'
    }

    return jsonify(version)

@app.post('/api/usuarios')
def create_user():
    new_user = request.get_json()
    cedula_identidad = new_user['cedula_identidad']
    nombre = new_user['nombre']
    primer_apellido = new_user['primer_apellido']
    segundo_apellido = new_user['segundo_apellido']
    fecha_nacimiento = new_user['fecha_nacimiento']

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("INSERT INTO usuario (cedula_identidad, nombre, primer_apellido, segundo_apellido, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s) RETURNING *",
                (cedula_identidad, nombre, primer_apellido, segundo_apellido, fecha_nacimiento))
    new_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_user)


@app.get('/api/usuarios/<id>')
def get_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM usuario WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)


@app.put('/api/usuarios/<id>')
def update_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    new_user = request.get_json()
    cedula_identidad = new_user['cedula_identidad']
    nombre = new_user['nombre']
    primer_apellido = new_user['primer_apellido']
    segundo_apellido = new_user['segundo_apellido']
    fecha_nacimiento = new_user['fecha_nacimiento']

    cur.execute("UPDATE usuario SET cedula_identidad = %s, nombre = %s, primer_apellido = %s , segundo_apellido = %s , fecha_nacimiento = %s WHERE id = %s RETURNING *",
                (cedula_identidad, nombre, primer_apellido, segundo_apellido, fecha_nacimiento, id))
    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(updated_user)


@app.delete('/api/usuarios/<id>')
def delete_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("DELETE FROM usuario WHERE id = %s RETURNING *", (id,))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)


@app.get('/')
def home():
    return send_file('static/index.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
