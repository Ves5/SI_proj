from flask import Flask, render_template

# Inicjalizacja aplikacji/framework Flask
app = Flask(__name__)

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

def run():
    """Włącza serwer http Flask.
    """
    app.run(port = 80)

def close():
    """Wyłącza serwer http Flask - nie sprawdzone!
    """
    app.do_teardown_appcontext()
