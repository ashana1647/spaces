from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    hostel = db.relationship('Hostels', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Hostels(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    hs_name = db.Column(db.String(length=30), nullable=False, unique=True)
    hs_address = db.Column(db.String(length=1024), nullable=False, unique=True)
    hs_contact = db.Column(db.Integer(), nullable=False)
    hs_rent = db.Column(db.Integer(), nullable=False)
    hs_description = db.Column(db.String(length=1024), nullable=False)
    rooms = db.Column(db.Integer(), nullable=False)
    caution = db.Column(db.Integer(), nullable=False)
    curfew = db.Column(db.String(length=30), nullable=False)
    maps_link = db.Column(db.String(length=1024), nullable=True, unique=True)
    type = db.Column(db.String(length=30), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self):
        return f'Hostels {self.name}'



