from .database import db
from flask_login import UserMixin

# add not null constaint to db
class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

# add not null constaint to db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    creator =  db.Column(db.Boolean, nullable=False)

# include ratings in database
# add not null constaint to db
# include rating bounds in db i.e. 0 to 5
# include Foreign Key constraint
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text, nullable=False)
    singer = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Text)
    # ratings = db.Column(db.Integer, nullable=False)
    lyrics = db.Column(db.Text, nullable=False)
    path = db.Column(db.Text, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('Album.id'), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

# include Foreign Key constraint
# add not null constaint to db
class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text, nullable=False)
    singer = db.Column(db.Text, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

# check if relationship can be defined in sqlite and how
# add not null constaint to db
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    playlist_songs = db.relationship('PlaylistSongs', backref='playlist', lazy=True)

# fix column name user_id to song_id
# include Foreign Key constraint
# include Primary key constraint
class Song_Playlist(db.Model):
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'),  primary_key=True)
