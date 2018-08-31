from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
bcrypt = Bcrypt(app) 
app.secret_key = "ThisIsSecret!"

mysql = connectToMySQL("userdb")

# def emailDUB ():
    


@app.route("/")
def index():
    # print("*****!!!WORKS!!!*****")
    return render_template("index.html")

@app.route('/regprocess', methods=['POST'])

def submit():
    session["first_name"] = request.form["first_name"]
    session["last_name"] = request.form["last_name"]
    session["email"] = request.form["email"]
        

    if len(session["first_name"]) < 1:
        flash("First name cannot be blank!", "first_name")
        
    
    elif len(session["first_name"]) < 3:
        flash("First name must contain at least 2 letters!", "first_name")
    
    elif not session["first_name"].isalpha():
        flash("First name must contain letters only!", "first_name") 
        

    if len(session["last_name"]) < 1:
        flash("Last name cannot be blank!", "last_name")
        

    elif len(session["last_name"]) < 3:
        flash("Last name must contain at least 2 letters!", "last_name")
    
    elif not session["last_name"].isalpha():
        flash("Last name must contain letters only!", "last_name") 
        

    if len(session["email"]) < 1:
        flash("Email cannot be blank!", "email")
        
    
    elif not EMAIL_REGEX.match(request.form["email"]):
        flash("Invalid Email Address!", "email")
    
        

    if len(request.form["password"]) < 1:
        flash("Password cannot be blank!", "password")
        

    if len(request.form["password"]) < 8:
        flash("Password must contain at least 8 characters!", "password")
        return redirect("/")

    if request.form["password"] != request.form["confirm_password"]:
        flash("Password does not match!", "confirm_password")
        # print("*****???WORKS???*****")
        return redirect("/")


    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash) 
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, NOW(), NOW());"
        data = { "first_name" : request.form['first_name'],
                 "last_name" : request.form['last_name'],
                 "email" : request.form['email'],
                 "password_hash" : pw_hash }
        mysql.query_db(query, data)
        print("*********???WORKS???*********", mysql.query_db("SELECT * FROM users;"))
        return redirect("/success")




# @app.route('/loginprocess', methods=['POST'])
# def submit():
#     if request.form["email"] != mysql.query_db("SELECT email FROM users;"):
#         flash("EMAIL OR PASSWORD IS INCORRECT")

#     elif request.form["password"] != mysql.query_db("SELECT password FROM users;"):
#         return redirect("/")

#     else:

#         return redirect ("/success")


@app.route("/success")
def success():
    # flash("The email address you entered is a valid email address. Thank you!!")
    # emails = mysql.query_db("SELECT email, created_at FROM email_list;")
    return render_template("success.html")
    # return render_template("success.html", emails=emails)

@app.route("/logout")
def logout():
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)