from flask import Flask, render_template, request, redirect, session
from database import (
    init_db, get_all_messages, add_message, delete_message, 
    get_message_count, check_user
)

app = Flask(__name__)
app.secret_key = 'секретный_ключ_для_гостевой_книги_12345'

# Инициализируем базу данных
init_db()

@app.route('/')
def index():
    messages = get_all_messages()
    total_count = get_message_count()
    
    return render_template(
        'index.html',
        messages=messages,
        total_count=total_count,
        logged_in=session.get('logged_in', False),
        username=session.get('username')
    )

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    if name and message:
        add_message(name, message)
    
    return redirect('/')

@app.route('/delete/<int:message_id>')
def delete(message_id):
    # Защита удаления - только для авторизованных
    if not session.get('logged_in'):
        return redirect('/login')
    
    delete_message(message_id)
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if check_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect('/')
        else:
            error = 'Неверный логин или пароль'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)