from flask import Flask, request
from flask import render_template
from flask import current_app as app
# from .__init__ import app

@app.route("/", methods=["GET", "POST"])
def dummy():
    return render_template("dummy.html")