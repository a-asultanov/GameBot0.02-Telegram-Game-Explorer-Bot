from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from dotenv import load_dotenv
import os
from src.config import Config


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(120))
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username or self.id}>"


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    genre = db.Column(db.String(80))
    rating = db.Column(db.Float)
    year = db.Column(db.String(10))
    platform = db.Column(db.String(40))

    def __repr__(self):
        return self.name

class RequestLog(db.Model):
    __tablename__ = 'request_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    username = db.Column(db.String(120))
    genre = db.Column(db.String(80))
    platform = db.Column(db.String(40))
    year = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Request {self.user_id} {self.genre} {self.year}>"

