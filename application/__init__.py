import os
from flask import Flask

from .config import LocalDevelopmentConfig
from .database import db

app = None

def create_app():
    app = Flask(__name__, template_folder="../templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from .controllers import *
from .api import api