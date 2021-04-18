import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect,request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm , LoginForm ,EditProfileForm
from flask_bcrypt import Bcrypt
from flask_login import login_user,current_user,logout_user,LoginManager,UserMixin,login_required


app = Flask(__name__)
app.config['SECRET_KEY']= '065948a0846f60c5890b0e2e6d6e7695'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['TESTING']=True
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), nullable=False)
    firstname=db.Column(db.String(20))
    lastname=db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    designation=db.Column(db.String(20), nullable=False)
    dob=db.Column(db.String(20))
    department=db.Column(db.String(40))
    address=db.Column(db.String(250))
    state=db.Column(db.String(50))
    country=db.Column(db.String(50))
    pincode=db.Column(db.Integer)
    phoneno=db.Column(db.Integer)
    apid=db.Column(db.String(20))
    assignedperson=db.Column(db.String(20))


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


@app.route('/')
@app.route('/index')
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route('/register',methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user1 = User.query.filter_by(email=form.email.data).first()
        if user1:
            flash('That email is taken. Please enter another email', 'danger')
            return redirect(url_for('register'))
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,designation=form.designation.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/forgot',methods=['GET', 'POST'])
def forgot():
    if request.method == "GET":
        return render_template("forgot-password.html")

@app.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == "GET":
        return render_template("dashboard.html")

@app.route('/add_appointment',methods=['GET', 'POST'])
@login_required
def add_appointment():
    if request.method == "GET":
        return render_template("add-appointment.html")

@app.route('/appointments',methods=['GET', 'POST'])
@login_required
def appointments():
    if request.method == "GET":
        return render_template("appointments.html")        

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/edit_profile',methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.dob = form.dob.data
        current_user.address = form.address.data
        current_user.state = form.state.data
        current_user.country = form.country.data
        current_user.pincode = form.pincode.data
        current_user.phoneno = form.phoneno.data
        current_user.department = form.department.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.dob.data = current_user.dob
        form.address.data = current_user.address
        form.state.data = current_user.state
        form.country.data = current_user.country
        form.pincode.data = current_user.pincode
        form.phoneno.data = current_user.phoneno
        form.department.data = current_user.department
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('edit-profile.html',
                           image_file=image_file, form=form)


@app.route('/profile',methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == "GET":
        image_file = url_for('static', filename='img/' + current_user.image_file)
        return render_template("profile.html",image_file=image_file)

@app.route('/chat',methods=['GET', 'POST'])
# @login_required
def chat():
    if request.method == "POST":
        user_msg = request.form.get("textarea")
        print(user_msg)
        return render_template("chat.html",user_msg = user_msg)
    if request.method == "GET":
        return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)