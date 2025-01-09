from flask import Flask , render_template , jsonify , redirect , request , url_for
import mysql.connector
import os
app = Flask("__name__")
# Set the upload folder
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# Creating mysql client



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tour")
def tour():
    return render_template('tour.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    mobile = request.form['mobile']
    date_planning = request.form['date_planning']
    reference = request.form['reference']
    tour_type = request.form['tour_type']

    # Here you can process the data, e.g., save it to the database or send an email
    print(f"Received contact from {name}, Mobile: {mobile}, Date: {date_planning}, Reference: {reference}, Tour Type: {tour_type}")


    # Redirect or render a success page
    return redirect('/')  # You can create a thank you page or return a message


@app.route('/admin/view')
def check_admin():
    return render_template('admin_form.html')

@app.route('/admin',methods=["POST"])
def admin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "root":
            return render_template('admin.html')
        else:
            return redirect('/admin/view')

    return render_template("admin_form.html")



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")


