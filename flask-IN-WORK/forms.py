from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField , RadioField,IntegerField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField,DateTimeField

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    designation= RadioField('Label', choices=[('Patient','Patient'),('Doctor','Doctor')],validators=[DataRequired()],default='Patient')
    terms = BooleanField('I accept all the Terms and Conditions',validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')


class EditProfileFormPat(FlaskForm):
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                            validators=[DataRequired(), Length(min=0, max=20)])
    dob=StringField('Birth Date',validators=[DataRequired()])
    address = StringField('Address',
                           validators=[DataRequired()])
    state=StringField('State',
                           validators=[DataRequired()])
    country = StringField('Country',
                        validators=[DataRequired()])
    pincode=IntegerField('Pincode',validators=[DataRequired()])
    phoneno=IntegerField('Phone Number',validators=[DataRequired()])
    picture = FileField('edit', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

class EditProfileFormDoc(FlaskForm):
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                            validators=[DataRequired(), Length(min=0, max=20)])
    dob=StringField('Birth Date',validators=[DataRequired()])
    address = StringField('Address',
                           validators=[DataRequired()])
    state=StringField('State',
                           validators=[DataRequired()])
    country = StringField('Country',
                        validators=[DataRequired()])
    pincode=IntegerField('Pincode',validators=[DataRequired()])
    phoneno=IntegerField('Phone Number',validators=[DataRequired()])
    dropdown = [('Physician', 'Physician'), ('Oncologist', 'Oncologist'), ('Orthopedic', 'Orthopedic')]
    department = SelectField('Department', choices=dropdown)
    picture = FileField('edit', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

class MakeAppointmentForm(FlaskForm):
    dropdown=[('Physician','Physician'),('Oncologist','Oncologist'),('Orthopedic','Orthopedic')]
    department=SelectField('Department',choices=dropdown , validators=[DataRequired()])
    message=TextAreaField('Message(optional)')
    date=DateField('Date',validators=[DataRequired()])
    time=StringField('Time', validators=[DataRequired()])
    submit=SubmitField('Create Appointment')

class ChatForm(FlaskForm):
    apid = IntegerField('Appointment ID', validators=[DataRequired()])
    submit = SubmitField('Join Chat')