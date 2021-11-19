'''build database'''

from flask_sqlalchemy import SQLAlchemy

# Create a DB Object
DB = SQLAlchemy()

# Make a Song table by creating a Song class


class Song(DB.Model):
    '''Creates a Song Table with SQLAlchemy'''
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username column
    name = DB.Column(DB.String, nullable=False)
    album = DB.Column(DB.String, nullable=True)
    artists = DB.Column(DB.String, nullable=True)

    def __repr__(self):
        return f'[Song: {self.name}]'
