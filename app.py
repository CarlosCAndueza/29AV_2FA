from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Usuario simulado para autenticación
users = {'user@example.com': {'password': 'password', 'secret': None}}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if email in users and users[email]['password'] == password:
        # Generar un secreto único para el usuario si aún no existe
        if not users[email]['secret']:
            users[email]['secret'] = pyotp.random_base32()
        # Generar el código de autenticación
        totp = pyotp.TOTP(users[email]['secret'])
        verification_code = totp.now()
        session['email'] = email
        # Imprimir el código de autenticación en la consola
        print(f'Verification code for {email}: {verification_code}')
        return redirect(url_for('verify'))
    else:
        return 'Invalid credentials'

@app.route('/verify')
def verify():
    return render_template('verify.html')

@app.route('/verify', methods=['POST'])
def verify_code():
    code = request.form['code']
    email = session.get('email')
    if email and email in users:
        # Verificar el código de autenticación
        totp = pyotp.TOTP(users[email]['secret'])
        if totp.verify(code):
            return redirect(url_for('dashboard'))
    return 'Invalid verification code'

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
