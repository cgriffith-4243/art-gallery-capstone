from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URI']

db = SQLAlchemy()

'''
    setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config.from_object('config')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
    Artwork
'''


class Artwork(db.Model):
    __tablename__ = 'Artwork'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    medium = Column(String)
    year = Column(Integer)
    image_link = Column(String)
    medium_id = Column(Integer, ForeignKey('Medium.id'), nullable=False)

    def __init__(self, title, medium, year, image_link, medium_id):
        self.title = title
        self.medium = medium
        self.year = year
        self.image_link = image_link
        self.medium_id = medium_id

    def thumbnail(self):
        return {
            'id': self.id,
            'title': self.title,
            'image_link': self.image_link
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


'''
    Medium
'''


class Medium(db.Model):
    __tablename__ = 'Medium'

    id = Column(Integer, primary_key=True)
    title = Column(String)

    def __init__(self, title):
        self.title = title

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title
        }
