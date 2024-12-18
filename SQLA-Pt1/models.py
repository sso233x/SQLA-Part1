from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

#Create User model
class User(db.Model):
    """User."""
    
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                           nullable=False,)
    last_name = db.Column(db.String(30),
                          nullable=False,)
    image_url = db.Column(db.String(20000), nullable=True)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"