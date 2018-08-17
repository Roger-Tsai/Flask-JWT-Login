from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class Users(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    salt = db.Column(db.String(8), nullable=False)
    login_time = db.Column(db.Integer)

    def __init__(self, username, password, email):
        methods, password_salt, password_hash = generate_password_hash(password).split('$')
        self.username = username
        self.password = password_hash
        self.salt = password_salt
        self.email = email

    def check_email_exists(self, email):
        return self.query.filter_by(email=email).first()

    def check_password(self, password_hash, password_salt, password):
        phash_str = 'pbkdf2:sha256:50000$' + password_salt + '$' + password_hash
        return check_password_hash(phash_str, password)

    def get(self, id):
        return self.query.filter_by(id=id).first()

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()

def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason