from flask import Flask, request
from flask import render_template, redirect
from flask import current_app as app
# from .__init__ import app
from application.models import *
# imports db=SQLAlchemy() too

current_login = None

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        p_name = request.form.get('name')
        p_password = request.form.get('password')
        user_obj = User(name=p_name, password=p_password)
        try:
            db.session.add(user_obj)
            db.session.commit()
        except Exception as e:
            print(e)
            return render_template("register.html", redo=True)
        finally:
            del user_obj
        return redirect('/')
        
    return render_template("register.html", redo=False)

@app.route("/login", methods=["GET"])
def login():
    global current_login
    if current_login and isinstance(current_login, User):
        return redirect("/user_home")
    if current_login and isinstance(current_login, Administrator):
        return redirect("/admin_home")
    return render_template("loginoptions.html")

@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    global current_login
    if current_login and isinstance(current_login, User):
        return redirect("/user_home")
    if current_login and isinstance(current_login, Administrator):
        return redirect("/admin_home")
        
    if request.method == 'POST':
        p_name = request.form.get('name')
        p_password = request.form.get('password')
        user_obj = User.query.filter_by(name=p_name).first() 
        if (not user_obj) or (user_obj.password != p_password):
            return render_template("login.html", person_type="User", redo=True)
        
        current_login = user_obj
        return redirect("/user_home")
    return render_template("login.html", person_type="User", redo=False)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    global current_login
    if current_login and isinstance(current_login, User):
        return redirect("/user_home")
    if current_login and isinstance(current_login, Administrator):
        return redirect("/admin_home")

    if request.method == 'POST':
        p_name = request.form.get('name')
        p_password = request.form.get('password')
        admin_obj = Administrator.query.filter_by(name=p_name).first() 
        print("* Admin select result =",admin_obj)
        if (not admin_obj) or (admin_obj.password != p_password):
            return render_template("login.html", person_type="Administrator", redo=True)
        
        current_login = admin_obj
        return redirect("/admin_home")
    return render_template("login.html", person_type="Administrator")

@app.route("/user_home", methods=["GET", "POST"])
def user_home():
    global current_login
    if (not current_login) or (not isinstance(current_login, User)):
        return redirect("/login")
    return render_template("user_home.html", name=current_login.name)

@app.route("/admin_home", methods=["GET", "POST"])
def admin_home():
    global current_login
    if (not current_login) or (not isinstance(current_login, Administrator)):
        return redirect("/login")
    return render_template("admin_home.html", name=current_login.name)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    global current_login
    current_login = None
    return redirect("/")