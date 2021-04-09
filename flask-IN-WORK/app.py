from flask import Flask,render_template,url_for,request

app = Flask(__name__)

@app.route('/')
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")

@app.route('/forgot',methods=['GET', 'POST'])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot-password.html")

@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    if request.method == "GET":
        return render_template("dashboard.html")

@app.route('/add-appointment',methods=['GET', 'POST'])
def add_appointment():
    if request.method == "GET":
        return render_template("add-appointment.html")

@app.route('/appointments',methods=['GET', 'POST'])
def appointments():
    if request.method == "GET":
        return render_template("appointments.html")        
        
@app.route('/edit-profile',methods=['GET', 'POST'])
def edit_profile():
    if request.method == "GET":
        return render_template("edit-profile.html")     

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    if request.method == "GET":
        return render_template("profile.html")    

if __name__ == "__main__":
    app.run(debug=True)