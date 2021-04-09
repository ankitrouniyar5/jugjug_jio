from flask import Flask,render_template,url_for,request

app = Flask(__name__)
name_user = "Samyak"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register',methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route('/login',methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/forgot',methods=['GET', 'POST'])
def forgot():
    return render_template("forgot-password.html")


if __name__ == "__main__":
    app.run(debug=True)