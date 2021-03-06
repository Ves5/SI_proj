import networkx as nx
import json
from networkx.readwrite import json_graph
import WebWrapper as WW
from utils.IOUtils import IOUtils

class GraphMaker:
    # Klasa odpowiedzialna za tworzenie i zmiany na grafie podobieństw

    # Tworzenie grafu
    
    graph = nx.Graph()  

    def __init__(self):
        super().__init__()


    def create_graph(self, arr, coords, pdf_names, pdf_paths):
        """Tworzy graf na podstawie macierzy podobieństw, 
            nazw plików porównywanych i ścieżek do nich.
        
        Parameters
        ----------
        arr : [[Double]]
            Macierz podobieństwa wybranych plików pdf.
        pdf_names : [String]
            Lista nazw wybranych plików.
        """
        # Każdy plik otrzymuje numer identyfikacyjny.
            # Jako dodatkowe atrybuty dodawane są nazwa pliku "name"
            # oraz ścieżka do pliku "path"
        for i, file, coord in zip(range(0, len(pdf_names)),pdf_names, coords):
            # Dodawanie wierzchołków (plików) do grafu
            self.graph.add_node(i, name=file, path=IOUtils.shorten_file_name(file), x=coord[0], y=coord[1])

        id_it = 0
        for i in range(0, len(pdf_names)):
            for j in range(i + 1, len(pdf_names)):
                # Dodawanie na podstawie macierzy podobieństwa krawędzi pomiędzy wierzchołkami,
                # jeżeli takie istnieje
                if arr[i][j] != 0:
                    self.graph.add_edge(i, j, weight=arr[i][j], id=id_it)
                    id_it += 1
                

    def graph_to_json(self):
        """Konwertuje graf do zapisu w formacie JSON,
            który jest kompatybilny z biblioteką D3js używanej
            do wizualizacji grafu.
        """
        # Konwersja do formatu node/link rozumianego przez D3js.
        d = json_graph.node_link_data(self.graph)

        # Zapis do zmiennej - jeżeli będziemy zwracać, a nie zapisywać do pliku.
        #graph_in_json = json.dumps(d)

        # Zapis danych do pliku w folderze statycznych zasobów.
        with open('static/graph.json', 'w') as outfile:
            json.dump(d, outfile)

        # return graph_in_json