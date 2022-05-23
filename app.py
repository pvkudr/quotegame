import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from FDataBase import FDataBase
from UserLogin import UserLogin



#config
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'fjhf5jJjjfjdklsjfjsksKk'



app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db'))) #change database path


# *************** login **********************
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


#********************DB********************

def connect_db():
  conn = sqlite3.connect(app.config['DATABASE'])
  conn.row_factory = sqlite3.Row  # as a dict
  return conn


#connection
def get_db():
    '''connect to db if not'''
    if not hasattr(g, 'link_db'):  #g has an attribute "link_db"
        g.link_db = connect_db()
    return g.link_db

# connect to db before EVERY request
dbase =None
@app.before_request
def before_request():
  global dbase
  db = get_db()
  dbase = FDataBase(db)


# close connection
@app.teardown_appcontext
def close_db(error):
    '''close connection db if any'''
    if hasattr(g, 'link_db'):
        g.link_db.close()




# ************  MAIN PAGE *****************


@app.route("/")
def index():
  # send template
  return render_template('index.html', menu = dbase.getMenu(), qoutes = dbase.getQoutes()) 


@app.route("/rules")
def rules():
  return render_template('rules.html', title = "rules", menu = dbase.getMenu())


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST": #information was recieved from client
        session.pop('_flashes', None)
        if len(request.form['email']) > 4 and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['email'], hash)
            if res:
                flash("Registration completed", "success")
                return redirect(url_for('login'))
            else:
                flash("Db error", "error")
        else:
            flash("Input mistake, try again", "error")
 
    return render_template("register.html", menu=dbase.getMenu(), title="Reg")



@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('index'))
 
        flash("wrong email/password", "error")
 
    return render_template("login.html", menu=dbase.getMenu(), title="Login")


# <username> goes to function as a paramenter
@app.route("/profile/<username>")  #path: username, int:usernamw
def profile(username):
  if 'userLogged' not in session or session['userLogged'] != username: #defennce form visiting profile page

    abort(401)
  return f"User: {username}"



# only ones to create db
#create_db()

# test reqest context without run the server
#with app.test_request_context():
 # print(url_for('index'))



if __name__ == "__main__":
  app.run(debug=True)    #change to False


#*************************************TEST************
# db = connect_db()
# dbase = FDataBase(db) #instance of class
# d= dbase.getMenu()
# print(d)

