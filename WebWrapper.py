from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

def run():
    app.run()

def close():
    app.do_teardown_appcontext()

app.run()