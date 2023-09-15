from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from risk_assessment_db import add_risk, get_all_risks, setup_users_table, add_user, get_user_by_username
from risk_assessment_db import add_category, get_all_categories
from models import User
from forms import RegistrationForm, LoginForm
from risk_assessment_db import add_comment
from risk_assessment_db import setup_comments_table
from risk_assessment_db import add_comment, get_comments_for_risk  
from risk_assessment_db import get_all_statuses
from risk_assessment_db import get_risk_by_id, get_all_categories, get_all_statuses, update_risk # and other required functions
from flask import Flask, render_template, request, redirect, url_for, abort
import risk_assessment_db as db
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from risk_assessment_db import get_risk_count_by_status  # Add this to your existing imports
from risk_assessment_db import get_total_risks  # Add this to your existing imports
from risk_assessment_db import get_risks_by_status # Other imports
from risk_assessment_db import get_total_risks, get_risks_by_status



setup_comments_table()


app = Flask(__name__)
app.secret_key = 'some_secret_key_here'  # Change this to a secure key in production

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    categories = get_all_categories()
    statuses = get_all_statuses()  # Fetch all statuses

    if request.method == 'POST':
        description = request.form['description']
        impact = int(request.form['impact'])
        likelihood = int(request.form['likelihood'])
        category_id = int(request.form['category'])
        print(request.form)  # Print the entire form data
        status_id = int(request.form['status'])  # Get the status from the form
        add_risk(description, impact, likelihood, category_id, status_id)
        return redirect(url_for('index'))
    
    risks = get_all_risks()
     # Fetch and append comments for each risk
    risks_with_comments = []
    for risk in risks:
        comments = get_comments_for_risk(risk[0])
        risk_data = {
            'risk': risk,
            'comments': comments
        }
    
        risks_with_comments.append(risk_data)
    print(risks_with_comments)
    return render_template('index.html', risks=risks_with_comments, categories=categories, statuses=statuses)


@app.route('/add_comment/<int:risk_id>', methods=['POST'])
@login_required
def post_comment(risk_id):
    comment_text = request.form['comment_text']
    add_comment(risk_id, comment_text)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user_exists = get_user_by_username(form.username.data)
        
        if user_exists:
            flash('Username already taken', 'danger')
        else:
            add_user(form.username.data, hashed_password)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/edit_risk/<int:risk_id>', methods=['GET','POST'])
@login_required
def edit_risk(risk_id):
    risk = get_risk_by_id(risk_id)
    if risk is None:
        abort(404)
    categories = get_all_categories()
    statuses = get_all_statuses()

    if request.method == 'POST':
        # handle form submission here
        description = request.form['description']
        impact = int(request.form['impact'])
        likelihood = int(request.form['likelihood'])
        category_id = int(request.form['category'])
        status_id = int(request.form['status'])
        
        update_risk(risk_id, description, impact, likelihood, category_id, status_id)
        return redirect(url_for('index'))
    else:
        return render_template('edit_risk.html', risk=risk, categories=categories, statuses=statuses)

@app.route('/edit/<int:risk_id>', methods=['GET'])
@login_required

def edit_page(risk_id):
    risk = get_risk_by_id(risk_id)
    categories = get_all_categories()
    statuses = get_all_statuses()
    return render_template('edit_risk.html', risk=risk, categories=categories, statuses=statuses)

@app.route('/delete_risk/<int:risk_id>', methods=['POST'])
def delete_risk(risk_id):
    if request.method == 'POST':
        db.delete_risk(risk_id)
        return redirect(url_for('index'))

@app.route('/api/dashboard_data', methods=['GET'])
@login_required
def dashboard_data():
    statuses = get_all_statuses()
    status_count = {}
    for status in statuses:
        status_id = status[0]
        status_name = status[1]
        status_count[status_name] = sum(1 for risk in get_all_risks() if risk[7] == status_name)

    return jsonify({
        'total_risks': len(get_all_risks()),
        'status_count': status_count
    })


@app.route('/dashboard')
@login_required
def dashboard():
    total_risks = get_total_risks()
    risk_count_by_status = get_risks_by_status()  # Make sure this is defined
    return render_template('dashboard.html', total_risks=total_risks, risk_count_by_status=risk_count_by_status)


if __name__ == '__main__':
    app.run(debug=True)
