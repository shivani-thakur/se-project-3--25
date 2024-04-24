from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/templates/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/templates/create_event.html')
def createevent():
    return render_template('create_event.html')

@app.route('/templates/signup.html')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
