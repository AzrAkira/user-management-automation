import sqlite3
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
EXTERNAL_API_URL = "https://jsonplaceholder.typicode.com/users"
DB_NAME = "database.db"

# --- FUNGSI DATABASE ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            company TEXT
        )
    ''')
    
    
    try:
        
        cursor.execute('SELECT count(*) FROM users')
        jumlah_data_lokal = cursor.fetchone()[0]
        
        if jumlah_data_lokal == 0:
            
            print("⏳ Sedang sinkronisasi ID dengan API...")
            response = requests.get(EXTERNAL_API_URL)
            jumlah_user_api = len(response.json()) 
            
            cursor.execute(f"INSERT OR IGNORE INTO sqlite_sequence (name, seq) VALUES ('users', {jumlah_user_api})")
            print(f"✅ Database siap! ID lokal akan mulai dari {jumlah_user_api + 1}")
            
    except Exception as e:
        print(f"⚠️ Gagal sinkronisasi ID: {e}")

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


init_db()

# --- ROUTES ---

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users_db = conn.execute('SELECT * FROM users ORDER BY id DESC').fetchall()
    conn.close()

    list_lokal = []
    for row in users_db:
        list_lokal.append({
            "id": row['id'],
            "name": row['name'],
            "email": row['email'],
            "company": {"name": row['company']},
            "sumber": "lokal"
        })

    try:
        response = requests.get(EXTERNAL_API_URL)
        list_api = response.json()
        for user in list_api:
            user['sumber'] = 'api'
    except:
        list_api = []

    return jsonify(list_lokal + list_api)

@app.route('/users/<int:id_user>', methods=['GET'])
def get_user_detail(id_user):
    conn = get_db_connection()
    user_db = conn.execute('SELECT * FROM users WHERE id = ?', (id_user,)).fetchone()
    conn.close()

    if user_db:
        return jsonify({
            "id": user_db['id'],
            "name": user_db['name'],
            "email": user_db['email'],
            "company": {"name": user_db['company']},
            "sumber": "lokal"
        })

    try:
        response = requests.get(f"{EXTERNAL_API_URL}/{id_user}")
        if response.status_code == 200:
            user_api = response.json()
            user_api['sumber'] = 'api'
            return jsonify(user_api)
    except:
        pass

    return jsonify({"pesan": "User tidak ditemukan"}), 404

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"pesan": "Nama wajib diisi"}), 400

    company_name = data.get('company', {}).get('name', '-')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, company) VALUES (?, ?, ?)',
                   (data['name'], data.get('email'), company_name))
    conn.commit()
    conn.close()

    return jsonify({"pesan": "Berhasil disimpan!"}), 201

@app.route('/users/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (id_user,))
    conn.commit()
    
    if cursor.rowcount > 0:
        return jsonify({"pesan": "Terhapus"}), 200
    else:
        return jsonify({"pesan": "Gagal"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)