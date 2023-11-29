from flask import Flask, request, send_from_directory, url_for
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
    
    songs_res = Song.query.all()
    user_songs_res = Song.query.filter_by(creator_id=user_obj.id).all()
    return render_template("user_home.html", user=user_obj, songs=songs_res, user_songs=user_songs_res)

@app.route("/admin_home/<p_name>", methods=["GET", "POST"])
def admin_home(p_name):    
    admin_obj = Administrator.query.filter_by(name=p_name).first()     
    if (not admin_obj) or (not current_login) or (current_login.name != p_name):
        return redirect("/login")
    songs_res = Song.query.all()
    users_res = User.query.all()
    creators_res = User.query.filter_by(creator=1).all()
    return render_template("admin_home.html", admin=admin_obj, songs=songs_res, users=users_res, creators=creators_res)

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
        return redirect("/login")
    user_obj.creator = 1    
    db.session.commit()    
    return redirect("/user_home/"+p_name)

# -------------- SONG -------------------------------
@app.route("/add_song", methods=["GET", "POST"])
def add_song():
    global current_login
    if not current_login:
        return redirect("/login")
    if (not isinstance(current_login, User)) or (current_login.creator==0):
        return "Only a <b>User account registered as creator</b> can add songs."
    
    if request.method == 'POST':
        p_name = request.form.get('name')
        p_genre = request.form.get('genre')
        p_singer = request.form.get('singer')
        p_release_date = request.form.get('release_date')
        p_lyrics = request.form.get('lyrics')
        p_file = request.files['file']
        

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

            return render_template("add_song.html")

        return redirect("/user_home/"+current_login.name)
    return render_template("add_song.html")

@app.route("/edit_song/<p_name>", methods=["GET", "POST"])
def edit_song(p_name):
    global current_login
    if not current_login:
        return redirect("/login")
    
    song_res = Song.query.filter_by(name=p_name).first()
    if (not isinstance(current_login, User)) or (current_login.creator==0) or (current_login.id != song_res.creator_id):
        return "Only the <b>Creator for this file</b> can edit this song."
    
    if (not song_res):
        return redirect("/user_home/"+current_login.name)
    
    if request.method == 'POST':

        p_genre = request.form.get('genre')
        p_singer = request.form.get('singer')
        p_release_date = request.form.get('release_date')
        p_lyrics = request.form.get('lyrics')        

        print(f"{p_name}\n{p_genre}\n{p_singer}\n{p_release_date}\n{p_lyrics}\n") #{p_file}\n")
        try:
            song_res.genre = p_genre
            song_res.singer = p_singer
            song_res.release_date = p_release_date
            song_res.lyrics = p_lyrics

            db.session.commit()
        except Exception as e:
            print(e)
            return render_template("edit_song.html", song=song_res)

        return redirect("/user_home/"+current_login.name)
    return render_template("edit_song.html", song=song_res)

@app.route("/view_song/<p_name>", methods=["GET", "POST"])
def view_song(p_name):
    global current_login
    song_res = Song.query.filter_by(name=p_name).first()
    if not current_login:
        return redirect("/login")
    if (not song_res):
        return redirect("/user_home/"+current_login.name)
    
    if request.method == "POST":
        p_rate = float(request.form.get('rate'))

        rating_now = float(song_res.rating)
        n_rating_now = int(song_res.n_rating)

        song_res.rating = (rating_now*n_rating_now + p_rate)/(n_rating_now + 1)
        song_res.n_rating = n_rating_now+1
        db.session.commit()
        return redirect("/user_home/"+current_login.name)

    return render_template("view_song.html", song=song_res, user=current_login)

@app.route("/play_song/<filename>", methods=["GET", "POST"])
def play_song(filename):
    return send_from_directory(
        "../song_tracks",
        filename,
        as_attachment=True,
        mimetype='audio/wav'
    )

@app.route("/delete_song/<p_name>", methods=["GET", "POST"])
def delete_song(p_name):
    global current_login
    song_res = Song.query.filter_by(name=p_name).first()
    if not current_login:
        return redirect("/login")
    if (not isinstance(current_login, Administrator)):
        return "Only an <b>Administrator</b> can delete songs."
    if (not song_res):
        return redirect("/user_home/"+current_login.name)
    
    try:
        db.session.delete(song_res)
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect("/admin_home/"+current_login.name)

# -------------------------- Album -----------------------------------
@app.route("/add_album", methods=["GET", "POST"]) # PendingFront end - user option and display result
def add_album():
    global current_login
    if not current_login:
        return redirect("/login")
    if (not isinstance(current_login, User)) or (current_login.creator==0):
        return "Only a <b>User account registered as creator</b> can add albums."
    
    p_valid_songs = Song.query.filter_by(creator_id=current_login.id).all()
    
    if request.method == 'POST':
        p_name = request.form.get('name')
        p_genre = request.form.get('genre')
        p_singer = request.form.get('singer')
        p_song_ids = request.form.getlist('songs')        

        album_obj = Album(name=p_name, genre=p_genre, singer=p_singer, creator_id=current_login.id)
        try:
            db.session.add(album_obj)
            db.session.commit()
        except Exception as e:
            print(e)
            return render_template("add_album.html", songs=p_valid_songs)
        
        for p_song_id in p_song_ids:
            song_res = Song.query.filter_by(id=p_song_id).first()
            # update album id
            try:
                song_res.album_id = album_obj.id
                db.session.commit()
            except Exception as e:
                print(e)
                return render_template("add_album.html", songs=p_valid_songs)
        return redirect("/user_home/"+current_login.name)
    
    return render_template("add_album.html", songs=p_valid_songs)