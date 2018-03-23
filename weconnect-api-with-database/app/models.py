from . import db
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    """ User class that creates a new user and responsible for operations with the rest of the classes """
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(64),unique=True,nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    businesses = db.relationship('Business', backref='user')
    reviews = db.relationship('Review', backref='user')
    
    def __repr__(self):
        return 'User %r'% self.username

    @property
    def password(self):
        raise AttributeError('password not in readable format')
    
    @password.setter
    def password(self):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Business(db.Model):
    """ Business class that creates a business for a registered user """
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64),nullable=False, index=True)
    location = db.Column(db.String(64),nullable=False) 
    category = db.Column(db.String(64),nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return 'Business name %r'% self.name

class Review(db.Modal):
    """ Review creates a review by a particular user to a specific business """
    __tablename__='reviews'
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    business_id = db.Column(db.Integer,db.ForeignKey('businesses.id'))
    review = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return 'Review %r', % self.review
    