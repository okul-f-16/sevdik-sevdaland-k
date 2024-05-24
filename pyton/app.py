from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'supersecretkey'  # Oturum verilerinin güvenliğini sağlamak için gizli anahtar

# Kullanıcıları depolamak için basit bir sözlük kullanıyoruz.
users = {
    'admin': {'password': 'admin123', 'role': 'Admin'},
    'user': {'password': 'user123', 'role': 'User'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            # Kullanıcıyı oturum açtır ve rolüne göre yönlendir.
            session['username'] = username
            return redirect(url_for(users[username]['role'].lower()))
        else:
            return render_template('login.html', error='Kullanıcı adı veya şifre yanlış!')
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'username' in session and users[session['username']]['role'] == 'Admin':
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

@app.route('/user')
def user():
    if 'username' in session and users[session['username']]['role'] == 'User':
        return render_template('user.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
