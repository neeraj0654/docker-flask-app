from flask import Flask, render_template
from flask_socketio import SocketIO
import mysql.connector
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

def get_db_data():
    conn = mysql.connector.connect(
        host='mysql',
        user='root',
        password='rootpassword',
        database='flaskdb'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM updates ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else "No data"

def insert_db_data(message):
    conn = mysql.connector.connect(
        host='mysql',
        user='root',
        password='rootpassword',
        database='flaskdb'
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO updates (message) VALUES (%s)", (message,))
    conn.commit()
    cursor.close()
    conn.close()

def background_thread():
    current = ""
    while True:
        time.sleep(2)
        message = get_db_data()
        if message != current:
            socketio.emit('update', {'data': message})
            current = message

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('new_message')
def handle_new_message(json):
    message = json.get('data')
    if message:
        insert_db_data(message)
        socketio.emit('update', {'data': message})

if __name__ == '__main__':
    thread = threading.Thread(target=background_thread)
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5002)
