import os
from flask import Flask, request, send_from_directory, url_for, jsonify
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
    def get(self):
        args = self.parser.parse_args()
        user = User.query.filter_by(name=args["name"]).first()
        n_songs = len(Song.query.filter_by(name=args["name"]).all())
        n_albums = len(Album.query.filter_by(name=args["name"]).all())
        
        resp = jsonify({
            "name" : user.name,
            "creator" : bool(user.creator),
            "n_songs" : n_songs,
            "n_albums" : n_albums
        })
        return resp
    
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
        # if #pwd check
        # new_pwd = args["password"]

api.add_resource(StatAPI, '/api/stat')
api.add_resource(UserAPI, '/api/user', '/api/user/<string:p_name>')
# curl -X GET http://127.0.0.1:8080/api/user/user1
# curl -X GET http://127.0.0.1:8080/api/user -H "Content-Type: application/json" -d "{\"name\": \"user1\"}"