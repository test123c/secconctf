from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

import os

class User:
    def __init__(self, id, username, password, flag):
        self.id = id
        self.username = username
        self.password = password
        self.flag = flag

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
username1 = os.environ['username']  #username: admin
password1 = os.environ['password']  #password: **RR4wwOS28Uig1U7qzBLun7V%K3ct6*Ly^b101B&Q1qus%f1K
flag1 = os.environ['flag']
users.append(User(id=1, username=username1, password=password1, flag = flag1))

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('flag'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/flag')
def flag():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('flag.html')