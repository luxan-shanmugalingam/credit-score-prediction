from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from datetime import datetime

# -------------------
# User Model
# -------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# ----------------------------
# CreditCustomer Model
# ----------------------------
class CreditCustomer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(64), unique=True, nullable=False)
    age = db.Column(db.Float, nullable=False)
    occupation = db.Column(db.String(64), nullable=False)
    annual_income = db.Column(db.Float, nullable=False)
    payment_behaviour = db.Column(db.String(64), nullable=False)

    # One-to-many relationship with MonthlyCreditRecord
    monthly_records = db.relationship('MonthlyCreditRecord', backref='customer', lazy=True)

    def __repr__(self):
        return f'<CreditCustomer {self.customer_id}>'

# ----------------------------
# MonthlyCreditRecord Model
# ----------------------------
class MonthlyCreditRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(64), db.ForeignKey('credit_customer.customer_id'), nullable=False)
    month = db.Column(db.Integer)
    num_bank_accounts = db.Column(db.Float)
    num_credit_card = db.Column(db.Integer)
    interest_rate = db.Column(db.Float)
    num_of_loan = db.Column(db.Float)
    delay_from_due_date = db.Column(db.Integer)
    num_of_delayed_payment = db.Column(db.Integer)
    changed_credit_limit = db.Column(db.Float)
    num_credit_inquiries = db.Column(db.Integer)
    outstanding_debt = db.Column(db.Float)
    credit_utilization_ratio = db.Column(db.Float)
    total_emi_per_month = db.Column(db.Float)
    amount_invested_monthly = db.Column(db.Float)
    month_no = db.Column(db.Integer)
