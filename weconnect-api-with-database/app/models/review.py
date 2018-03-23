from .. import db
class Review(db.Modal):
    """ Review creates a review by a particular user to a specific business """
    __tablename__='reviews'
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, nullable=False)
    business_id = db.Column(db.Integer,nullable=False)
    review = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return 'Review %r', % self.review

    