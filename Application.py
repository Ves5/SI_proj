from functools import partial
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
from tkinter.ttk import *

from SimilarityTable import SimilarityTable
from GraphMaker import GraphMaker
from DocumentComparator import DocumentComparator
from utils.IOUtils import IOUtils
import nltk
import WebWrapper
import webbrowser
import threading
from multiprocessing import Process

DEMO_MODE = False

def start_server():
    webbrowser.open("http://127.0.0.1:80/", 2)
    WebWrapper.run()

def hide_components():
    bar['value'] = 0
    bar.grid_remove()
    bar.update()

    button_show_similarity_table.grid_remove()

    label_info_progressbar['text'] = ''


def show_similarity_table(arr, pdf_names):
    SimilarityTable().createAndShow(arr, pdf_names, window)


def compare_documents(paths_to_pdf_files, pdf_names):
    # progressbar na 0 
    bar['value'] = 0
    bar.update()

    label_info_progressbar['text'] = 'Comparing...'
    label_info_progressbar.update()
    bar.grid(row=4, column=0)

    # klasa od porownywania dokumentow
    dc = DocumentComparator()
    arr, pos = dc.compare_documents(paths_to_pdf_files, bar) #używane do krawędzi

    label_info_progressbar['text'] = 'Comparing completed.'
    label_info_progressbar.update()

    button_show_similarity_table.configure(text='Show similarity table',
                                           command=partial(show_similarity_table, arr, pdf_names))
    button_show_similarity_table.grid(row=5, column=0)

    # utworzenie wątku i upewnienie się, że poprzednie zakończyły pracę
    drawer = GraphMaker()
    drawer.create_graph(arr, pos, pdf_names, paths_to_pdf_files)
    drawer.graph_to_json()
    t = threading.Thread(target=start_server)
    t.setDaemon(True)
    t.start()
    


def browse_files():
    folder_path = filedialog.askopenfilenames(filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
    if folder_path != '':
        [paths_to_pdf_files, pdf_names] = IOUtils.list_pdf_files_in_dir(folder_path)

        # ukrycie elementów GUI
        hide_components()

        if len(pdf_names) < 2:
            messagebox.showerror('File selection', 'Select two or more PDF files.')
        else:
            # gdy 2 lub wiecej plikow wybranych, porownaj je
            # usuniecie wszystkiego z listy wybranych plikow
            listbox.delete(0, END)
            # wylistowanie plikow w prawej czesci okna
            for (index, elem) in enumerate(pdf_names):
                listbox.insert(index, elem)
            # zmiana naglowka oraz stworzenie przycisku do porownania plikow
            label_header_info['text'] = 'PDF selection:'
            button_compare_documents = Button(text="Compare documents",
                                              command=partial(compare_documents, paths_to_pdf_files, pdf_names))
            button_compare_documents.grid(column=0, row=2, sticky="S", padx=(5, 5))


def configure_styles():
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    window.option_add("*Font", default_font)


if not DEMO_MODE:
    # pobranie stopwords oraz zestawu słów
    nltk.download('stopwords')
    nltk.download('wordnet')

    # tworzenie widoku / GUI przy uzyciu Tkinter
    window = Tk()
    window.title("Document comparator")
    window.geometry('660x400')

    # konfiguracja stylow GUI
    configure_styles()

    # konfiguracja wygladu GUI do wyboru plikow
    label_program_name = Label(window, text='Document comparator')
    label_program_name.configure(font=('calibri', 20, "bold"), foreground="#efefef")
    label_program_name.grid(row=0, column=0, padx=(5, 5))

    label_header_info = Label(window, text='First select PDF files...')
    label_header_info.configure(font=('calibri', 15))
    label_header_info.grid(row=0, column=1, padx=(5, 5), sticky=W, columnspan=3)

    # okno listy plików
    listbox = Listbox(window)
    listbox.yview()
    listbox.grid(row=1, column=1, sticky=N + W, rowspan=14, columnspan=3)
    listbox.configure(width=40, height=15)

    #scrollbar do listy
    scroll_vertical = Scrollbar(window, orient=VERTICAL)
    scroll_vertical.config(command=listbox.yview)
    scroll_vertical.grid(row=1, column=4, sticky=N + S, rowspan=14)

    scroll_horizontal = Scrollbar(window, orient=HORIZONTAL)
    scroll_horizontal.config(command=listbox.xview)
    scroll_horizontal.grid(row=15, column=1, sticky=E + W, columnspan=3)

    listbox.config(yscrollcommand=scroll_vertical.set, xscrollcommand=scroll_horizontal.set)

    label_info_progressbar = Label(window, text='')
    label_info_progressbar.grid(row=3, column=0, sticky="S")

    bar = Progressbar(window, length=200)

    button_show_similarity_table = Button()

    # wybor plikow + otworzenie widoku -> funkcja z tego pliku
    button_browse = Button(text="Select files", command=browse_files)
    button_browse.grid(row=1, column=0, sticky="S", padx=(5, 5))

    window.protocol("WM_DELETE_WINDOW", IOUtils.delete_files_from_assets())
    
    # glowna petla widoku
    window.mainloop()
else:
    arr = [[0, 0.53682293, 0.49240103, 0.49318128, 0.04009207, 0.03515585],
           [0.53682293, 0, 0.49677289, 0.54755336, 0.01423449, 0.01342816],
           [0.49240103, 0.49677289, 0, 0.4856281, 0.03298175, 0.0299892],
           [0.49318128, 0.54755336, 0.4856281, 0, 0.02699985, 0.02418876],
           [0.04009207, 0.01423449, 0.03298175, 0.02699985, 0, 0.97959166],
           [0.03515585, 0.01342816, 0.0299892, 0.02418876, 0.97959166, 0]]
    filenames = ['IO Analiza biznesowa i systemowa.pdf', 'IO Obszary działań IO.pdf', 'IO Projektowanie.pdf',
                 'IO Wprowadzenie.pdf', 'Kamizelka.pdf', 'Latarnik.pdf']

    #gm = GraphMaker()
    # gm.create_graph(arr, filenames, filenames)
    # gm.graph_to_json()
    # t = threading.Thread(target=start_server)
    # t.start()
