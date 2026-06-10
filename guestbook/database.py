import sqlite3
from datetime import datetime

DB_PATH = 'guestbook.db'

def get_db_connection():
    """Устанавливает соединение с базой данных."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализирует базу данных: создаёт таблицу messages."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all_messages():
    """Возвращает все сообщения из базы данных."""
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY created_at DESC').fetchall()
    conn.close()
    return messages

def add_message(name, message):
    """Добавляет новое сообщение в базу данных."""
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
        (name, message, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def delete_message(message_id):
    """Удаляет сообщение из базы данных по его id."""
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()

def get_message_count():
    """Возвращает общее количество сообщений."""
    conn = get_db_connection()
    cursor = conn.execute('SELECT COUNT(*) FROM messages')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def delete_all_messages():
    """Удаляет все сообщения из базы данных."""
    conn = get_db_connection()
    conn.execute('DELETE FROM messages')
    conn.commit()
    conn.close()

def get_messages_sorted(order='DESC'):
    """
    Возвращает сообщения с сортировкой по дате.
    order: 'DESC' - сначала новые, 'ASC' - сначала старые
    """
    conn = get_db_connection()
    messages = conn.execute(f'SELECT * FROM messages ORDER BY created_at {order}').fetchall()
    conn.close()
    return messages