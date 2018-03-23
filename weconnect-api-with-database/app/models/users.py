from .. import db

class User(db.Model):
    """ User class that creates a new user and responsible for operations with the rest of the classes """
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(64),unique=True,nullable=False)
    password = db.Column(db.Text,nullable=False)
    
    def __repr__(self):
        return 'User %r'% self.username
    