from flask import Flask, request
from flask import render_template
from flask import current_app as app
# from .__init__ import app

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        return "<h1>Pending Page</h1>"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        return "<h1>Pending Page</h1>"
    return render_template("register.html")