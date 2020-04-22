from flask import Flask, render_template, request, send_from_directory
import os

# Inicjalizacja aplikacji/framework Flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['ASSETS'] = os.path.join(app.root_path, 'assets')

@app.route('/')
def index():
    """Strona główna wizualizacji/index.
    Tu będzie tworzony graf.
    
    Returns
    -------
    [HTML Template (Flask)]
        Zwraca zawartość strony html na podstawie template.
    """
    return render_template('base.html')

@app.route("/<filename>")
def iframe(filename):
    """Wyświetla wybrany plik.
    
    Parameters
    ----------
    filename : [String]
        Nazwa pliku do wyświetlenia.
    
    Returns
    -------
    [File]
        Plik wybrany o podanej nazwie.
    """
    return send_from_directory(app.config['ASSETS'], filename)

def run():
    """Włącza serwer http Flaskna porcie 80.
    """
    app.run(port = 80)
