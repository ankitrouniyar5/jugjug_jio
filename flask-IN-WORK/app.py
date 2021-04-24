import os
import secrets
import random
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect,request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm , LoginForm ,EditProfileFormDoc,EditProfileFormPat, MakeAppointmentForm,ChatForm
from flask_bcrypt import Bcrypt
from flask_login import login_user,current_user,logout_user,LoginManager,UserMixin,login_required
from datetime import datetime

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
    appointments=db.relationship('Appointment',backref='user',lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Appointment(db.Model):
    apid = db.Column(db.Integer, primary_key=True)
    department=db.Column(db.String(20),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time=db.Column(db.DateTime,nullable=False)
    message = db.Column(db.Text)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Appointment('{self.department}', '{self.date}')"


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
            flash('That email is taken.Please enter another email', 'danger')
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
    noofdoc=User.query.filter_by(designation='Doctor').all()
    noofdoc=len(noofdoc)
    noofpat = User.query.filter_by(designation='Patient').all()
    noofpat=len(noofpat)
    apps = Appointment.query.all()
    apps = sorted(apps, key=lambda x: (x.date, x.time))
    pending=len(apps)
    appointments = []
    for appo in apps:
        if appo.user.id == current_user.id and current_user.designation == 'Patient':
            time = appo.time
            time = time.strftime("%I %p")
            date = appo.date
            date = date.strftime("%d %B, %Y")
            doctor = User.query.filter_by(id=appo.doctor_id).first()
            patient = current_user.firstname + " " + current_user.lastname
            image_file = url_for('static', filename='img/' + current_user.image_file)
            doctor = doctor.firstname + " " + doctor.lastname
            appointments.append((appo, patient, time, doctor,image_file))
        elif appo.doctor_id == current_user.id and current_user.designation == 'Doctor':
            time = appo.time
            time = time.strftime("%I %p")
            date = appo.date
            date = date.strftime("%d %B, %Y")
            patient = User.query.filter_by(id=appo.patient_id).first()
            doctor = current_user.firstname + " " + current_user.lastname
            image_file = url_for('static', filename='img/' + patient.image_file)
            patient = patient.firstname + " " + patient.lastname
            appointments.append((appo, patient, time, doctor,image_file))
    appointments=appointments[0:5]
    docs=User.query.filter_by(designation='Doctor').all()
    docs=[x for x in docs if x.firstname!=None]
    if current_user.firstname==None and current_user.designation=='Patient':
        flash('Please update your details before making an appointment','danger')
    elif current_user.firstname==None and current_user.designation=='Doctor':
        flash('Please update your details before taking up an appointment','danger')
    return render_template("dashboard.html",pending=pending,noofdoc=noofdoc,noofpat=noofpat,appointments=appointments,docs=docs)

@app.route('/add_appointment',methods=['GET', 'POST'])
@login_required
def add_appointment():
    form =MakeAppointmentForm()
    if request.method=='GET':
        return render_template("add-appointment.html", form=form)
    if form.validate_on_submit():
        time=form.time.data
        time=datetime.strptime(time,'%H:%M')
        date = form.date.data
        date = date.strftime("%d %B, %Y")
        date = datetime.strptime(date, '%d %B, %Y')
        doctors = User.query.filter_by(department=form.department.data).all()
        apps = Appointment.query.all()
        apps = sorted(apps, key=lambda x: (x.date, x.time))
        doc=random.choice(doctors)
        docid=None
        flag=0
        while(doc):
            doctors.remove(doc)
            for appo in apps:
                if appo.doctor_id == doc.id:
                    if appo.date==date and appo.time==time:
                        flag=1
                        break
            if flag==0:
                docid=doc.id
                break
            if len(doctors)==0:
                break
            doc=random.choice(doctors)
        if docid==None:
            flash('No doctors are available for this slot.Please choose a diff date and time','danger')
            return redirect(url_for('appointments'))
        appointment=Appointment(doctor_id=docid,department=form.department.data,time=time,date=date,message=form.message.data,user=current_user)
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment has been made', 'success')
        return redirect(url_for('appointments'))
    else:
        flash('Unable to make the appointment', 'danger')
        return redirect(url_for('appointments'))

@app.route('/appointments',methods=['GET', 'POST'])
@login_required
def appointments():
    apps=Appointment.query.all()
    apps=sorted(apps,key=lambda x:(x.date,x.time))
    appointments=[]
    for appo in apps:
        if appo.user.id==current_user.id and current_user.designation=='Patient' :
            time=appo.time
            time = time.strftime("%I %p")
            date=appo.date
            date=date.strftime("%d %B, %Y")
            doctor=User.query.filter_by(id=appo.doctor_id).first()
            patient=current_user.firstname+" "+current_user.lastname
            doctor=doctor.firstname+" "+doctor.lastname
            appointments.append((appo,patient,time,date,doctor))
        elif appo.doctor_id==current_user.id and current_user.designation=='Doctor' :
            time = appo.time
            time = time.strftime("%I %p")
            date = appo.date
            date = date.strftime("%d %B, %Y")
            patient=User.query.filter_by(id=appo.patient_id).first()
            doctor=current_user.firstname+" "+current_user.lastname
            patient=patient.firstname+" "+patient.lastname
            appointments.append((appo,patient,time,date,doctor))
    return render_template("appointments.html",appointments=appointments)



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
    if current_user.designation=='Doctor' :
        form = EditProfileFormDoc()
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
            current_user.department = form.department.data
            current_user.pincode = form.pincode.data
            current_user.phoneno = form.phoneno.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
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
    elif current_user.designation=='Patient':
        form=EditProfileFormPat()
        if form.validate_on_submit() :
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
@login_required
def chat():
    form=ChatForm()
    if form.validate_on_submit():
        apid=str(form.apid.data)
        name=current_user.firstname
        url="https://jugjug-jio-chat.herokuapp.com/meet/" + apid + "/"+ name
        return redirect(url)
    return render_template("chat.html",form=form)

@app.route('/appointment/<int:apid>',methods=['GET', 'POST'])
@login_required
def del_appointment(apid):
    appoint=Appointment.query.get(apid)
    db.session.delete(appoint)
    db.session.commit()
    flash('Your appointment has been deleted!', 'success')
    return redirect(url_for('appointments'))

if __name__ == "__main__":
    app.run(debug=True)