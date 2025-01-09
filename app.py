from flask import Flask , render_template , jsonify , redirect , request , url_for
import mysql.connector
import os
app = Flask("__name__")
# Set the upload folder
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# Creating mysql client


# List to store tour data
tours = []
db = mysql.connector.connect(
    host="localhost",
    username="root",
    password="root",
    database="ascendtours"
)

cursor = db.cursor()

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


    # inserting into database
    cursor.execute(
    f"INSERT INTO enquiry (name, mobile, plan_date, referenced_by, tour_type) VALUES ('{name}', '{mobile}', '{date_planning}', '{reference}', '{tour_type}');"
    )
    db.commit()

    print("Inserted Successfully")

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

@app.route('/add_tour', methods=['POST'])
def add_tour():
    tour_name = request.form['tour_name']
    tour_location = request.form['tour_location']
    tour_price = request.form['tour_price']
    tour_type = request.form['tour_type']
    tour_highlights = request.form['tour_highlights']

    # Handle file uploads
    tour_images = request.files.getlist('tour_images')
    tour_banner = request.files['tour_banner']

    # Save images
    image_filenames = []
    for image in tour_images:
        if image:
            image_filename = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(image_filename)
            image_filenames.append(image_filename)

    # Save banner
    if tour_banner:
        banner_filename = os.path.join(UPLOAD_FOLDER, tour_banner.filename)
        tour_banner.save(banner_filename)
    else:
        banner_filename = ""

    # Create a tour dictionary
    tour_data = {
        "tour_name": tour_name,
        "tour_location": tour_location,
        "tour_price": tour_price,
        "tour_type": tour_type,
        "tour_highlights": tour_highlights,
        "tour_images": image_filenames,
        "tour_banner": banner_filename
    }

    # Add the tour to the list
    tours.append(tour_data)

    return render_template('admin.html', tours=tours)


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")


