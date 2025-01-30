from api import db
from datetime import datetime

class Communication(db.Model):
    __tablename__ = 'Communications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, default='general')
    rating = db.Column(db.Integer)
    userId = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    user = db.relationship('User', backref='communications', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'question': self.question,
            'answer': self.answer,
            'category':self.category,
            'rating': self.rating,
            'userId': self.userId
        }