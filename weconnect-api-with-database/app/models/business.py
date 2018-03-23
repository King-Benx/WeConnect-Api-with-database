from .. import db
class Business(db.Model):
    """ Business class that creates a business for a registered user """
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(64),nullable=False, index=True)
    location = db.Column(db.String(64),nullable=False) 
    category = db.Column(db.String(64),nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return 'Business name %r'% self.name
    