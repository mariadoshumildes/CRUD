from flask import Flask, render_template, request, redirect, url_for
import pymysql
from config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        db=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM usuario")
            usuarios = cursor.fetchall()
    return render_template('index.html', usuarios=usuarios)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
                conn.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                nome = request.form['nome']
                email = request.form['email']
                senha = request.form['senha']
                cursor.execute("UPDATE usuario SET nome=%s, email=%s, senha=%s WHERE id=%s", (nome, email, senha, id))
                conn.commit()
                return redirect(url_for('index'))
            else:
                cursor.execute("SELECT * FROM usuario WHERE id=%s", (id,))
                usuario = cursor.fetchone()
    return render_template('update.html', usuario=usuario)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM usuario WHERE id=%s", (id,))
            conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
