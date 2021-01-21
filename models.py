"""Models for Cupcake app."""
# make virtual env, put in git repo


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

DEFAULT_URL = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    """Cupcakes available"""
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True )
    flavor = db.Column(db.Text, nullable = False)
    size = db.Column(db.Text, nullable = False)
    rating = db.Column(db.Float, nullable = False)
    image = db.Column(db.Text, nullable = False, default= DEFAULT_URL)
