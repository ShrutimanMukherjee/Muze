import os
from flask import Flask, request, send_from_directory, url_for, jsonify, make_response
from flask import render_template, redirect
from flask import current_app as app
from flask_restful import Api, Resource, reqparse

from application.models import *

api = Api(app)
app.app_context().push()

class StatAPI(Resource):
    def get(self):
        n_songs = len(Song.query.all())
        n_albums = len(Album.query.all())
        n_users = len(User.query.all())
        n_creators = len(User.query.filter_by(creator=1).all())

        resp = jsonify({
            "n_songs" : n_songs,
            "n_albums" : n_albums,
            "n_users" : n_users,
            "n_creators" : n_creators
        })

        return resp

class UserAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("new_password", type=str)
    
    def get(self, p_name):
        user = User.query.filter_by(name=p_name).first()
        n_songs = len(Song.query.filter_by(name=p_name).all())
        n_albums = len(Album.query.filter_by(name=p_name).all())
        
        resp = jsonify({
            "name" : user.name,
            "creator" : bool(user.creator),
            "n_songs" : n_songs,
            "n_albums" : n_albums
        })
        return resp
    
    def put(self):
        args = self.parser.parse_args()
        user = User.query.filter_by(name=args["name"]).first()
        curr_pwd = args["password"]
        new_pwd = args["new_password"]

        try:
            if user.password != curr_pwd:
                raise Exception("ValidationError: Incorrect Password")
        except Exception as e:
            print(e)
            resp = make_response(jsonify({
                    "Error" : "Incorrect Password or Invalid User"
                }))
            resp.status_code = 400
            return resp
        
        try:
            user.password = new_pwd
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            resp = make_response(jsonify({
                    "Error" : "Internal Server Error"
                }))
            resp.status_code = 500
            return resp

        print("Password Changed Successfully")
        resp = jsonify({"Message" : "Password Changed Successfully"})
        return resp

class SongAPI(Resource):
    def get(self, p_name):
        song = Song.query.filter_by(name=p_name).first()
        
        resp = jsonify({
            "name" : song.name,
            "singer": song.singer,
            "genre": song.genre,
            "lyrics": song.lyrics,
            "release_date": song.release_date,
            "rating": song.rating,
            "n_rating": song.n_rating
        })
        return resp

class AllSongsAPI(Resource):
    def get(self):
        songs = Song.query.all()
        resp_list = []
        for song in songs:
            resp_list.append({
                "name" : song.name,
                "singer": song.singer,
                "genre": song.genre,
                "lyrics": song.lyrics,
                "release_date": song.release_date,
                "rating": song.rating,
                "n_rating": song.n_rating
            })
        resp = jsonify({
            "all_songs" : resp_list
        })
        return resp

api.add_resource(StatAPI, '/api/stat')
api.add_resource(UserAPI, '/api/user', '/api/user/<string:p_name>')
api.add_resource(SongAPI, '/api/song', '/api/song/<string:p_name>')
api.add_resource(AllSongsAPI, '/api/all_songs')
# curl -X GET http://127.0.0.1:8080/api/user/user1
# curl -X GET http://127.0.0.1:8080/api/user -H "Content-Type: application/json" -d "{\"name\": \"user1\"}"
# curl -X PUT http://127.0.0.1:8080/api/user -H "Content-Type: application/json" -d "{\"name\": \"<uname>\", \"password\":\"<oldpwd>\", \"new_password\":\"<newpwd>\"}"
# curl -X GET http://127.0.0.1:8080/api/all_songs
# curl -X GET http://127.0.0.1:8080/api/song/Socha%20Hai!