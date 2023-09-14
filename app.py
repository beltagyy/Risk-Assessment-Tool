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
    if request.method == 'POST':
        description = request.form['description']
        impact = int(request.form['impact'])
        likelihood = int(request.form['likelihood'])
        category_id = int(request.form['category'])
        add_risk(description, impact, likelihood, category_id)
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
    return render_template('index.html', risks=risks_with_comments, categories=categories)


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



if __name__ == '__main__':
    app.run(debug=True)
