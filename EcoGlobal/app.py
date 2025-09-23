import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Path to the CSV file that stores user data
CSV_FILE = 'users.csv'

# Function to read users from CSV file
def read_users():
    users = []
    try:
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
    except FileNotFoundError:
        pass  # If file doesn't exist, just return an empty list
    return users

# Function to write new user to CSV file
def write_user(user):
    with open(CSV_FILE, mode='a', newline='') as file:
        fieldnames = ['name', 'class', 'roll_no', 'username', 'password', 'school', 'grade', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # If the file is empty, write the header
        if file.tell() == 0:
            writer.writeheader()
        
        writer.writerow(user)

# Route to serve the HTML page (login and registration form)
@app.route('/', methods=['GET'])
def get_started():
    return render_template('index.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if user exists in the CSV file
    users = read_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return render_template("dashboard.html")
    
    return "Invalid username or password. Please try again."

# Route to handle registration form submission
@app.route('/register', methods=['POST'])
def register():
    # Get form data
    name = request.form['name']
    class_name = request.form['class']
    roll_no = request.form['roll_no']
    username = request.form['username']
    password = request.form['password']
    school = request.form['school']
    grade = request.form['grade']
    email = request.form['email']
    
    # Check if username already exists in the CSV file
    users = read_users()
    for user in users:
        if user['username'] == username:
            return "Username already exists. Please choose another username."

    # Create a new user and write to the CSV file
    user_data = {
        'name': name,
        'class': class_name,
        'roll_no': roll_no,
        'username': username,
        'password': password,
        'school': school,
        'grade': grade,
        'email': email
    }
    write_user(user_data)  # Write the new user to CSV file
    
    return render_template("dashboard.html")


if __name__ == '__main__':
    app.run(debug=True)
