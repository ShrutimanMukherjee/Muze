from .database import db
from flask_login import UserMixin

class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    creator =  db.Column(db.Boolean, default=0)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text, default="Unknown")
    singer = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Text)
    rating = db.Column(db.Integer, default=0, db.CheckConstraint("rating >= 0 and rating <= 5"))
    lyrics = db.Column(db.Text, nullable=False)
    path = db.Column(db.Text, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('Album.id'), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text, default="Unknown")
    singer = db.Column(db.Text, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

# fix column name user_id to song_id
# include Foreign Key constraint
# include Primary key constraint
class Song_Playlist(db.Model):
    playlist_id = db.Column(db.Integer, db.ForeignKey('Playlist.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id'),  primary_key=True)
