from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os, shutil
from zipfile import ZipFile 

# Inicjalizacja aplikacji/framework Flask
app = Flask(__name__)
app.config['ASSETS'] = os.path.join(app.root_path, 'assets')
app.config['SECRET_KEY'] = b')*9 Y+:?BsImANM|'
app.config['PASSWORD'] = generate_password_hash('yoolek123')

ALLOWED_EXTENSIONS = {'zip'}

@app.route('/')
def index():
    # Strona główna wizualizacji, w której będzie tworzony graf
    if not os.path.isdir(app.config['ASSETS']):
        os.mkdir(app.config['ASSETS'])
    return render_template('base.html')

@app.route("/pdf/<filename>")
def iframe(filename):
    # Wyświetlanie wybranego pliku

    return send_from_directory(app.config['ASSETS'], filename)

@app.route("/load/graph")
def graph():
    return render_template('graph.js')

@app.route('/load/json')
def json():
    return send_from_directory(app.config['ASSETS'], 'graph.json')


def allowed_file(filename):
    # sprawdzanie rozszerzenia pliku
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # metoda POST (wysłana forma)
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
            # czyszczenie zawartości /assets przed zapisaniem nowych plików

            if not check_password_hash(app.config['PASSWORD'], request.form['password']):
                flash('Wrong password')
                return redirect(request.url)
            
            if os.path.isdir(app.config['ASSETS']):
                shutil.rmtree(app.config['ASSETS'])
            
            os.mkdir(app.config['ASSETS'])
            filename = secure_filename(file.filename)
            # zapisanie archiwum do assets
            file.save(os.path.join(app.config['ASSETS'], filename))

            with ZipFile(os.path.join(app.config['ASSETS'], filename)) as zip:
                # rozpakowywanie archiwum
                zip.extractall(path=app.config['ASSETS'])

            return redirect(url_for('index'))
        else:
            flash('Wrong file extension')
            return redirect(request.url)
    return render_template('upload.html')

@app.after_request
def add_header(response):
    response.cache_control.max_age = 30
    return response