from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management and flashing messages

# Example in-memory data structures for simplicity
accounts = {}  # Stores user data in memory
current_user = None  # Stores the currently logged-in user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    global current_user
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if email in accounts:
            flash('Account already exists!', 'danger')
            return redirect(url_for('create_account'))
        accounts[email] = {'name': name, 'password': password, 'balance': 0}
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in accounts and accounts[email]['password'] == password:
            current_user = email
            flash('Logged in successfully!', 'success')
            return redirect(url_for('account_details'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/account-details')
def account_details():
    if current_user:
        account_info = accounts[current_user]
        return render_template('account_details.html', account=account_info)
    flash('Please log in first!', 'warning')
    return redirect(url_for('login'))

@app.route('/transfer-funds', methods=['GET', 'POST'])
def transfer_funds():
    if request.method == 'POST':
        recipient = request.form['recipient']
        amount = float(request.form['amount'])
        if current_user and recipient in accounts and accounts[current_user]['balance'] >= amount:
            accounts[current_user]['balance'] -= amount
            accounts[recipient]['balance'] += amount
            flash(f'Transferred ${amount} to {recipient} successfully!', 'success')
            return redirect(url_for('account_details'))
        else:
            flash('Invalid transfer details or insufficient balance!', 'danger')
    return render_template('transfer_funds.html')

@app.route('/logout')
def logout():
    global current_user
    current_user = None
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
