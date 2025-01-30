from api import db
from datetime import datetime
import bcrypt
from flask_jwt_extended import create_access_token

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    DOB = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    nativeLang = db.Column(db.String(50))
    secondLang = db.Column(db.String(50))
    occupation = db.Column(db.String(100))
    createDate = db.Column(db.DateTime, default=datetime.utcnow)
    updateDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
    
    def to_dict(self):
        """Converts the User object to a dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'DOB': self.DOB.strftime('%Y-%m-%d'),  # Convert date to string
            'sex': self.sex,
            'nativeLang': self.nativeLang,
            'secondLang': self.secondLang,
            'occupation': self.occupation,
            'createDate': self.createDate.strftime('%Y-%m-%d %H:%M:%S'),
            'updateDate': self.updateDate.strftime('%Y-%m-%d %H:%M:%S'),
            'active': self.active
        }
    
    def generate_token(self):
        """Generate a JWT token for the user."""
        return create_access_token(identity={'id': self.id, 'email': self.email})