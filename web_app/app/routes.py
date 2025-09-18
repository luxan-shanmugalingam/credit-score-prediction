from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, CreditCustomer, MonthlyCreditRecord
from urllib.parse import urlparse
from datetime import datetime
import plotly.graph_objs as go
import json
import pandas as pd
import numpy as np
import joblib

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/report', methods=['GET', 'POST'])
@login_required
def customer_report():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        customer = CreditCustomer.query.filter_by(customer_id=customer_id).first()

        if customer:
            records = MonthlyCreditRecord.query.filter_by(customer_id=customer_id).order_by(MonthlyCreditRecord.month_no).all()
            months = [r.month_no for r in records]
            chart_data = {
                'months': months,
                'outstanding_debt': [r.outstanding_debt for r in records],
                'credit_utilization_ratio': [r.credit_utilization_ratio for r in records],
                'total_emi_per_month': [r.total_emi_per_month for r in records],
                'num_bank_accounts': [r.num_bank_accounts for r in records],
                'num_credit_card': [r.num_credit_card for r in records],
                'interest_rate': [r.interest_rate for r in records],
                'num_of_loan': [r.num_of_loan for r in records],
                'delay_from_due_date': [r.delay_from_due_date for r in records],
                'num_of_delayed_payment': [r.num_of_delayed_payment for r in records],
                'changed_credit_limit': [r.changed_credit_limit for r in records],
                'num_credit_inquiries': [r.num_credit_inquiries for r in records],
                'amount_invested_monthly': [r.amount_invested_monthly for r in records]
            }
            return render_template('report.html', customer=customer, records=records, chart_data=chart_data)
        else:
            flash('Customer ID not found.')
    return render_template('report_form.html')

@app.route('/report_form', methods=['GET', 'POST'])
@login_required
def report_form():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        return redirect(url_for('customer_report', customer_id=customer_id))
    return render_template('report_form.html')

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    input_dict = {}

    # Load files
    with open('scaler.pkl', 'rb') as f:
        scaler = joblib.load(f)

    with open('numerical_features.pkl', 'rb') as f:
        numerical_features = joblib.load(f)

    with open('categorical_features.pkl', 'rb') as f:
        categorical_features = joblib.load(f)

    with open('model.pkl', 'rb') as f:
        model = joblib.load(f)

    if request.method == 'POST':
        # Handle numerical input
        for feature in numerical_features:
            value = request.form.get(feature)
            try:
                input_dict[feature] = float(value)
            except (TypeError, ValueError):
                input_dict[feature] = 0.0  # Default to 0.0 if invalid input

        # Initialize all categorical features to 0
        for feature in categorical_features:
            input_dict[feature] = 0

        # Get dropdown values
        month = request.form.get('Month')
        occupation = request.form.get('Occupation')
        payment_min = request.form.get('Payment_of_Min_Amount')
        payment_behaviour = request.form.get('Payment_Behaviour')

        # Set selected categorical values
        if month and f'Month_{month}' in categorical_features:
            input_dict[f'Month_{month}'] = 1
        if occupation and f'Occupation_{occupation}' in categorical_features:
            input_dict[f'Occupation_{occupation}'] = 1
        if payment_min == "Yes" and 'Payment_of_Min_Amount_Yes' in categorical_features:
            input_dict['Payment_of_Min_Amount_Yes'] = 1
        if payment_behaviour and f'Payment_Behaviour_{payment_behaviour}' in categorical_features:
            input_dict[f'Payment_Behaviour_{payment_behaviour}'] = 1

        # Convert to DataFrame
        input_df = pd.DataFrame([input_dict])

        # Scale numeric values
        input_df[numerical_features] = scaler.transform(input_df[numerical_features])

        # Predict
        prediction_code = model.predict(input_df)[0].item() # Added .item() here
        
        prediction_mapping = {
            0: 'Poor',
            1: 'Standard',
            2: 'Good'
        }
        # Use .get() with the now scalar prediction_code
        prediction_text = f'Predicted Credit Score: {prediction_mapping.get(prediction_code, "Unknown")}'

        # Generate insights based on the score
        insights = []
        if prediction_code == 2:
            insights.append("✅ This customer has good credit score. Likely to repay loans on time.")
            insights.append("💡 Consider offering premium financial products.")
        elif prediction_code == 1:
            insights.append("⚠️ This customer has standard credit score. Monitor their payment patterns closely.")
            insights.append("💡 Offer limited credit with stricter repayment terms.")
        elif prediction_code == 0:
            insights.append("❌ Poor credit score detected. High chance of loan default.")
            insights.append("💡 Recommend requiring collateral or rejecting high-value credit.")
        insights.append("Note: This result is generated by a trained predictive model and may not always reflect the actual outcome. It is recommended to use this as a supplementary insight alongside thorough expert analysis.")
        return render_template('result.html',
                                prediction_text=f"{prediction_text}",
                                insights=insights,
                                numerical_features=numerical_features)

    return render_template('predict.html', numerical_features=numerical_features)
