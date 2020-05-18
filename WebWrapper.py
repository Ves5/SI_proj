from flask import Flask, render_template, request, send_from_directory
import os

# Inicjalizacja aplikacji/framework Flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['ASSETS'] = os.path.join(app.root_path, 'assets')

@app.route('/')
def index():
    # Strona główna wizualizacji, w której będzie tworzony graf

    return render_template('base.html')

@app.route("/pdf/<filename>")
def iframe(filename):
    # Wyświetlanie wybranego pliku

    return send_from_directory(app.config['ASSETS'], filename)

@app.route("/load/graph")
def graph():
    return render_template('graph.js')

def run():
    # Włącza serwer http Flask na porcie 80
    
    app.run(port = 80)
