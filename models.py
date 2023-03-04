"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://tinyurl.com/demo-cupcake"


class Cupcake (db.Model):
    """Cupcake"""
    
    __tablename__ = "cupcake"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    flavor = db.Column(
        db.Text,
        nullable=False
    )

    size = db.Column(db.Text,
        nullable=False
    )

    rating = db.Column(
        db.Float,
        nullable=False
    )

    image = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )

    
    def serialize(self):
        """returns a dictionary of a single cupcake instance"""
        return {
            'id' : self.id,
            'flavor' : self.flavor,
            'size' : self.size,
            'rating': self.rating,
            'image' : self.image,
        }

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

