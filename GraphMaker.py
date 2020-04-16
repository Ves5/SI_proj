import networkx as nx
import matplotlib.pyplot as plt
import json
from networkx.readwrite import json_graph
import WebWrapper as WW

class GraphMaker:

    graph = nx.Graph()

    def __init__(self):
        super().__init__()


    def create_graph(self, arr, pdf_names, pdf_paths):
        for i,file, path in zip(range(0, len(pdf_names)),pdf_names, pdf_paths):
            self.graph.add_node(i, name=file, path=path)
            #print(file, path)
            #print(self.graph.nodes[0]['name'])
            #print(self.graph.nodes[0]['path'])
            #print(self.graph.number_of_nodes())

        for i in range(0, len(pdf_names)):
            for j in range(i + 1, len(pdf_names)):
                self.graph.add_edge(i, j, weight = arr[i][j])
                

    def graph_to_json(self):
        d = json_graph.node_link_data(self.graph)
        graph_in_json = json.dumps(d)

        with open('SI_proj/static/graph.json', 'w') as outfile:
            json.dump(d, outfile)

        return graph_in_json

        """
        pos = nx.spring_layout(self.graph)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(self.graph, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(self.graph, pos, width=6)

        # labels
        nx.draw_networkx_labels(self.graph, pos, font_size=20, font_family='sans-serif')

        plt.axis('off')
        plt.show()
        """

# tests
arr = [[0, 0.53682293, 0.49240103, 0.49318128, 0.04009207, 0.03515585],
           [0.53682293, 0, 0.49677289, 0.54755336, 0.01423449, 0.01342816],
           [0.49240103, 0.49677289, 0, 0.4856281, 0.03298175, 0.0299892],
           [0.49318128, 0.54755336, 0.4856281, 0, 0.02699985, 0.02418876],
           [0.04009207, 0.01423449, 0.03298175, 0.02699985, 0, 0.97959166],
           [0.03515585, 0.01342816, 0.0299892, 0.02418876, 0.97959166, 0]]
filenames = ['IO Analiza biznesowa i systemowa.pdf', 'IO Obszary działań IO.pdf', 'IO Projektowanie.pdf',
                 'IO Wprowadzenie.pdf', 'Kamizelka.pdf', 'Latarnik.pdf']
GM = GraphMaker()
GM.create_graph(arr, filenames, filenames)
GM.graph_to_json()
# WW.run()