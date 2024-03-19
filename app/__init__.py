from flask import Flask
from config import Config

from app.extensions import db, limiter
from app.models import models
from app.routes.routes import bp as routes_blueprint

app = Flask(__name__)
# to load te config file into the flask application
app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatapp.db"

db.init_app(app)  # attaching the db to flask application
limiter.init_app(app)  # attaching the limiter to flask application
app.register_blueprint(routes_blueprint)  # registering all the routes

# to initialize all the tables after defining the models
with app.app_context():
    db.create_all()
