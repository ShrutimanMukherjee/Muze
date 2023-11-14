from flask import Flask, request
from flask import render_template
from flask import current_app as app
# from .__init__ import app
from application.models import *

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        
    return render_template("register.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("loginoptions.html")

@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    if request.method == 'POST':
        return "<h1>Pending Page</h1>" #
    return render_template("login.html", person_type="User")

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == 'POST':
        return "<h1>Pending Page</h1>" #
    return render_template("login.html", person_type="Administrator")