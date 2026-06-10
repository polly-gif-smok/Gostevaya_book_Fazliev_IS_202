from flask import Flask, render_template, request, redirect, url_for
from database import (
    init_db, get_all_messages, add_message, delete_message, 
    get_message_count, delete_all_messages, get_messages_sorted
)
from datetime import date

app = Flask(__name__)

# Инициализируем базу данных при запуске
init_db()

@app.route('/')
def index():
    """Главная страница со всеми сообщениями."""
    messages = get_all_messages()
    total_count = get_message_count()
    today = date.today().isoformat()
    return render_template('index.html', 
                         messages=messages, 
                         total_count=total_count,
                         today=today)

@app.route('/add', methods=['POST'])
def add():
    """Добавляет новое сообщение."""
    name = request.form.get('name')
    message = request.form.get('message')
    
    if name and message:
        add_message(name, message)
    
    return redirect(url_for('index'))

@app.route('/delete/<int:message_id>')
def delete(message_id):
    """Удаляет сообщение по id."""
    delete_message(message_id)
    return redirect(url_for('index'))

@app.route('/delete-all')
def delete_all_page():
    """Показывает страницу подтверждения удаления всех сообщений."""
    return render_template('delete_all.html')

@app.route('/delete-all-confirm', methods=['POST'])
def delete_all_confirm():
    """Удаляет все сообщения."""
    delete_all_messages()
    return redirect(url_for('index'))

@app.route('/sort/<order>')
def sort_messages(order):
    """Сортирует сообщения по дате."""
    if order == 'newest':
        messages = get_messages_sorted('DESC')
    elif order == 'oldest':
        messages = get_messages_sorted('ASC')
    else:
        messages = get_all_messages()
    
    total_count = get_message_count()
    today = date.today().isoformat()
    return render_template('index.html', 
                         messages=messages, 
                         total_count=total_count,
                         today=today)

if __name__ == '__main__':
    app.run(debug=True)