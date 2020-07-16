from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os

# Inicjalizacja aplikacji/framework Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'assets')
app.config['ASSETS'] = os.path.join(app.root_path, 'assets')

ALLOWED_EXTENSIONS = {'zip'}

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

def allowed_file(filename):
    # sprawdzanie rozszerzenia pliku
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # metoda POST (wysłany plik)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
        else:
            flash('Wrong file extension')
            return redirect(request.url)
    return render_template('upload.html')