from flask import Flask,request,render_template,url_for,redirect,session,Blueprint, flash
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


app.secret_key = 'Kveno'
app.permanent_session_lifetime = timedelta(seconds=40)


class group8(db.Model):
    id = db.Column('student_id',db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    uni = db.Column(db.String(100))
    password = db.Column(db.String(100))


def __ini__(self,name,lastname,age,uni, password):
    self.name = name
    self.lastname = lastname
    self.age = age
    self.uni = uni
    self.password = password

@app.route('/registration',methods = ['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        age = request.form['age']
        uni = request.form['uni']
        password = generate_password_hash(request.form["psw"])
        user_info = group8(name=name,lastname=lastname,uni=uni,age=age, password=password)
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('registration.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        global name
        name = request.form['name']
        password = request.form['psw']
        user = group8.query.filter_by(name=name).first()
        session['client'] = name

        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('login'))
        return redirect(url_for('info'))
    else:
        if 'client' in session:
            return redirect(url_for('info'))


@app.route('/info')
def info():
    if 'client' in session:
        username = session['client']
        return render_template('information.html', name = username)
    else:
        return redirect(url_for('login'))




