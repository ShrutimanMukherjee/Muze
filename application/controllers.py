from flask import Flask, request
from flask import render_template, redirect
# , flash
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
        return redirect("/user_home/"+current_login.name)
    if current_login and isinstance(current_login, Administrator):
        return redirect("/admin_home/"+current_login.name)
    return render_template("loginoptions.html")

@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    global current_login
    if current_login and isinstance(current_login, User):
        return redirect("/user_home/"+current_login.name)
    if current_login and isinstance(current_login, Administrator):
        return redirect("/admin_home/"+current_login.name)
        
    if request.method == 'POST':
        p_name = request.form.get('name')
        p_password = request.form.get('password')
        user_obj = User.query.filter_by(name=p_name).first() 
        if (not user_obj) or (user_obj.password != p_password):
            return render_template("login.html", person_type="User", redo=True)
        
        current_login = user_obj
        return redirect("/user_home/"+p_name)
    return render_template("login.html", person_type="User", redo=False)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    global current_login
    if current_login and isinstance(current_login, User):
        return redirect("/user_home/"+current_login.name)
    if current_login and isinstance(current_login, Administrator):
        return redirect("/admin_home/"+current_login.name)

    if request.method == 'POST':
        p_name = request.form.get('name')
        p_password = request.form.get('password')
        admin_obj = Administrator.query.filter_by(name=p_name).first() 
        
        if (not admin_obj) or (admin_obj.password != p_password):
            return render_template("login.html", person_type="Administrator", redo=True)
        
        current_login = admin_obj
        return redirect("/admin_home/"+p_name)
    return render_template("login.html", person_type="Administrator")

@app.route("/user_home/<p_name>", methods=["GET", "POST"])
def user_home(p_name):    
    user_obj = User.query.filter_by(name=p_name).first()     
    if (not user_obj) or (not current_login) or (current_login.name != p_name):
        return redirect("/login")
    return render_template("user_home.html", user=user_obj)

@app.route("/admin_home/<p_name>", methods=["GET", "POST"])
def admin_home(p_name):    
    admin_obj = Administrator.query.filter_by(name=p_name).first()     
    if (not admin_obj) or (not current_login) or (current_login.name != p_name):
        return redirect("/login")
    return render_template("admin_home.html", admin=admin_obj)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    global current_login
    current_login = None
    return redirect("/")

@app.route("/make_creator/<p_name>", methods=["GET", "POST"])
def make_creator(p_name):
    global current_login
    user_obj = User.query.filter_by(name=p_name).first() 
    if (not current_login):
        return redirect("/")
    user_obj.creator = 1    
    db.session.commit()    
    return redirect("/user_home/"+p_name)

@app.route("/add_song", methods=["GET", "POST"])
def add_song():
    global current_login
    if not current_login:
        return redirect("/")
    if (not isinstance(current_login, User)) or (current_login.creator==0):
        return "Only a <b>User accont registered as creator</b> can add songs"
    
    if request.method == 'POST':
        p_name = request.form.get('name')
        p_genre = request.form.get('genre')
        p_singer = request.form.get('singer')
        p_release_date = request.form.get('release_date')
        p_lyrics = request.form.get('lyrics')
        p_file = request.files['file']
        
        # current directory is always the app root directory
        p_path = "./song_tracks/"+p_file.filename

        print(f"{p_name}\n{p_genre}\n{p_singer}\n{p_release_date}\n{p_lyrics}\n{p_file}\n")

        song_obj = Song(name=p_name, genre=p_genre, singer=p_singer, 
                        release_date=p_release_date, lyrics=p_lyrics,
                        path=p_path, creator_id=current_login.id)
        try:
            p_file.save(p_path)
            db.session.add(song_obj)
            db.session.commit()
        except Exception as e:
            print(e)
            # flash("Error in adding song. Try again.")
            return render_template("add_song.html")
        # flash(f"Song {p_file.filename} added successfully")
        return redirect("/user_home/"+current_login.name)
    return render_template("add_song.html")