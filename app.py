from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/about')
def about():
    return render_template('about.html')  # Make sure this file exists in templates

@app.route('/login')
def login():
    return render_template('login.html')  # Make sure this file exists in templates

if __name__ == '__main__':
    app.run(debug=True)
