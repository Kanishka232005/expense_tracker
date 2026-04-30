from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_FILE = 'expenses.json'

# Initialize data file
def init_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

def load_data():
    init_data()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    expenses = load_data()
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    expenses = load_data()
    
    expense = {
        'id': len(expenses) + 1,
        'amount': float(data['amount']),
        'category': data['category'],
        'description': data['description'],
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d'))
    }
    
    expenses.append(expense)
    save_data(expenses)
    return jsonify(expense), 201

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expenses = load_data()
    expenses = [e for e in expenses if e['id'] != expense_id]
    save_data(expenses)
    return jsonify({'message': 'Expense deleted'})

@app.route('/api/total')
def get_total():
    expenses = load_data()

    today = datetime.now().date()
    current_month = datetime.now().month
    current_year = datetime.now().year

    daily_total = 0
    monthly_total = 0
    yearly_total = 0

    for expense in expenses:

        expense_date = datetime.strptime(
            expense['date'],
            '%Y-%m-%d'
        ).date()

        # Daily Total
        if expense_date == today:
            daily_total += expense['amount']

        # Monthly Total
        if (
            expense_date.month == current_month and
            expense_date.year == current_year
        ):
            monthly_total += expense['amount']

        # Yearly Total
        if expense_date.year == current_year:
            yearly_total += expense['amount']

    return jsonify({
        'daily_total': round(daily_total, 2),
        'monthly_total': round(monthly_total, 2),
        'yearly_total': round(yearly_total, 2)
    })
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)