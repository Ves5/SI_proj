import networkx as nx
import json
from networkx.readwrite import json_graph
import WebWrapper as WW

class GraphMaker:
    """Klasa odpowiedzialna za tworzenie i zmiany na grafie podobieństw."""

    graph = nx.Graph() # Tworzony graf

    def __init__(self):
        super().__init__()


    def create_graph(self, arr, pdf_names, pdf_paths):
        """Tworzy graf na podstawie macierzy podobieństw, 
            nazw plików porównywanych i ścieżek do nich.
        
        Parameters
        ----------
        arr : [[Double]]
            Macierz podobieństwa wybranych plików pdf.
        pdf_names : [String]
            Lista nazw wybranych plików.
        pdf_paths : [String]
            Lista ścieżek do wybranych plików.
        """
        # Każdy plik otrzymuje numer identyfikacyjny.
            # Jako dodatkowe atrybuty dodawane są nazwa pliku "name"
            # oraz ścieżka do pliku "path"
        for i, file, path in zip(range(0, len(pdf_names)),pdf_names, pdf_paths):
            # Dodawanie wierzchołków (plików) do grafu
            self.graph.add_node(i, name=file, path=path)

        for i in range(0, len(pdf_names)):
            for j in range(i + 1, len(pdf_names)):
                # Dodawanie na podstawie macierzy podobieństwa krawędzi pomiędzy wierzchołkami,
                # jeżeli takie istnieje
                if arr[i][j] != 0:
                    self.graph.add_edge(i, j, weight = arr[i][j])
                

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