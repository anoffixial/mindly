from flask import Flask, render_template, request, redirect, url_for,flash
import mysql.connector
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for rendering to files
import matplotlib.pyplot as plt
import io
import base64
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for sessions

# Initialize Flask extensions
# bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# MySQL configurations
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Enter your MySQL root password if you have one
    database="mental_health_db"
)
cursor = db.cursor()

# Route for the form
@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(user[0], user[1], user[2])  # User(id, username, password)
    return None

# Define User class (required by Flask-Login)
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password using passlib
        hashed_password = pbkdf2_sha256.hash(password)

        # Insert the user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        db.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.php')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch the user from the database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and pbkdf2_sha256.verify(password, user[2]):  # Verifying hashed password
            login_user(User(user[0], user[1], user[2]))
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')

# Protect routes with login_required
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)


@app.route('/progress')
def show_progress():
    # user_id = session['user_id']  # Get the logged-in user's ID from the session

    # Fetch all form submissions for this user, ordered by timestamp
    
    cursor.execute('''SELECT timestamp, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10 
                      FROM mental_health_data WHERE user_id = %s ORDER BY timestamp ASC''', (current_user.id,))
    data = cursor.fetchall()

    # Extract the timestamps and calculate total scores for each submission
    timestamps = [row[0] for row in data]
    scores = [sum(row[1:11]) for row in data]  # Sum of q1 to q10 for each submission

    # Create a line graph
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, scores, marker='o', linestyle='-', color='b', label='Total Score')
    plt.xlabel('Date')
    plt.ylabel('Score')
    plt.title('Your Stress Levels Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    # Render the progress template and pass the graph URL
    return render_template('progress.html', graph_url=f'data:image/png;base64,{graph_url}')




# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/history')
@login_required  # Ensure the user is logged in
def history():
    # Fetch all data from the database for the logged-in user
    cursor.execute("SELECT * FROM mental_health_data WHERE user_id=%s", (current_user.id,))
    data = cursor.fetchall()  # Fetch all records

    graphs = []
    
    # Generate a graph for each set of past analyses
    for record in data:
        # Assuming the first two columns are `id` and `user_id`, you need to unpack from index 2
        # Adjust according to the actual structure of your table
        q1, q2, q3, q4, q5, q6, q7, q8, q9, q10 = record[2:12]  # Change [2:12] as necessary based on your table

        score = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
        labels = [
            "Interest", "Down/Depressed", "Sleep Problems", "Energy Levels", "Appetite Issues", 
            "Self-esteem", "Concentration", "Nervousness", "Fear", "Self-harm Thoughts"
        ]
        img = io.BytesIO()

        # Create the graph using matplotlib
        plt.figure(figsize=(10, 6))
        plt.bar(labels, score, color=['#4a90e2'] * len(score))  # Optional: Change color dynamically
        plt.title('Previous Mental Health Assessment')
        plt.ylim(0, 3)
        plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
        plt.tight_layout()  # Ensure everything fits without overlapping
        plt.savefig(img, format='png')  # Save image in memory
        img.seek(0)

        # Encode the image to base64 so it can be rendered in the HTML
        graph_url = base64.b64encode(img.getvalue()).decode()
        graphs.append(graph_url)

    return render_template('history.html', graphs=graphs)



@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    # Handle form logic here
    return render_template('form.html')


# Route to handle form submission
@app.route('/submit', methods=['POST'])
@login_required
def submit():
    # Get form data from POST request
    responses = [int(request.form[f'q{i}']) for i in range(1, 11)]  # Fetching responses from q1 to q10

    # Save to database
    cursor.execute("INSERT INTO mental_health_data (user_id, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                   (current_user.id, *responses))
    db.commit()

    # Analyze the responses
    total_score = sum(responses)

    # Interpret the results
    if 30 <= total_score < 40:
        status = "severely "
        stress_level = "Severe"
    elif 20 <= total_score < 30:
        status = "Moderately "
        stress_level = "High"
    elif 10 <= total_score < 20:
        status = "Mildly "
        stress_level = "Moderate"
    elif total_score < 10:
        status = "Minimaly "
        stress_level = "Low"
    else:
        status = "Severe Symptoms"
        stress_level = "Severe"

   

    # Generate bar chart for individual responses
    questions = [
        "Interest", "Down/Depressed", "Sleep Problems", "Energy Levels", "Appetite Issues", 
        "Self-esteem", "Concentration", "Nervousness", "Fear", "Self-harm Thoughts"
    ]

    # Bar plot for individual responses
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(questions, responses, color='skyblue')
    plt.xlabel('Mental Health Aspects')
    plt.ylabel('Response Score (0-3)')
    plt.title('Mental Health Assessment Responses')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the bar chart to a BytesIO object
    img_bar = io.BytesIO()
    plt.savefig(img_bar, format='png')
    img_bar.seek(0)
    plt.close()

    # Encode bar chart image to base64 string
    bar_chart_url = base64.b64encode(img_bar.getvalue()).decode('utf-8')
    img_bar.close()

    # Generate pie chart for overall stress level
    labels = ['Low Stress', 'Moderate Stress', 'High Stress', 'Severe Stress']
    sizes = [0, 0, 0, 0]  # Initialize sizes

    if stress_level == "Low":
        sizes[0] = 10
    elif stress_level == "Moderate":
        sizes[1] = 10
    elif stress_level == "High":
        sizes[2] = 10
    elif stress_level == "Severe":
        sizes[3] = 10

    # Pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, colors=['green', 'yellow', 'orange', 'red'], autopct='%1.1f%%', startangle=140)
    plt.title('Overall Stress Level')

    # Save pie chart to a BytesIO object
    img_pie = io.BytesIO()
    plt.savefig(img_pie, format='png')
    img_pie.seek(0)
    plt.close()

    # Encode pie chart image to base64 string
    pie_chart_url = base64.b64encode(img_pie.getvalue()).decode('utf-8')
    img_pie.close()

    # Return analysis and display graphs in a rendered template
    return render_template('results.html', total_score=total_score, status=status, stress_level=stress_level, 
                           bar_chart_url=bar_chart_url, pie_chart_url=pie_chart_url)

    #return render_template('results.html', graph_url=graph_url)


if __name__ == '__main__':
    app.run(debug=True)
 