# SI_proj

Projekt na przedmiot Sztuczna Inteligencja.

Kod pisany w Python (>=3.7).

## Wymagane moduły Python

Instalacja przez `pip install ...` zalecana:

* [Flask][1]
* [NetworkX][2]
* [NLTK][3]
* [NumPy][4]
* [PDFMiner][5]
* [scikit-learn][6]

[1]: https://pypi.org/project/Flask/ "Flask PyPI page"
[2]: https://pypi.org/project/networkx/ "NetworkX PyPI page"
[3]: https://pypi.org/project/nltk/ "Natural Language Toolkit (NLTK) PyPI page"
[4]: https://pypi.org/project/numpy/ "NumPy PyPI page"
[5]: https://pypi.org/project/pdfminer/ "PDFMiner PyPI page"
[6]: https://pypi.org/project/scikit-learn/ "scikit-learn PyPI page"

## Etap 1 - Wizualizacja

Wizualizacja podobieństw pomiędzy plikami pdf na grafie ważonym.
Wyświetalnie jest wykonane za pomocą biblioteki [D3js](https://d3js.org/) w przeglądarce na lokalnym serwerze uruchamianym przez aplikację.

Podobieństwo pomiędzy plikami jest przedstawione jako odległość pomiędzy nimi, jak i przez kolor połączenia - im ciemniejsze tym większe podobieństwo. Po kliknieciu na wierzchołek grafu (lub w pewnych sytuacjach także po przeciągnięciu), obok otwiera się podgląd zawartości pliku .pdf przedstawianego przez ten wierzchołek.

Podwójne kilknięcie na wierzchołek dołącza do widocznego grafu wszystkie inne wierzchołki które są podobne do wybranego.

## Etap 2 - MDS (Multidimensional Scaling)

Użycie algorytmu MDS z modułu scikit-learn do określenia położenia plików względem siebie na płaszczyźnie.

Jako wejście do algorytmu podawana jest macierz dokumentów względem słów (cechy). Wiersze to wektory dokumentów w wysoko-wymiarowej przestrzeni. Kolumny to słowa (cechy). Wartość na skrzyżowaniu to ilość występowań danego słowa w dokumencie. Na wyjściu algorytmu dostajemy macierz pozycji dokumentów na płaszyźnie.

Koordynaty są zapisywane dalej do grafu, a potem przeskalowywane tak, żeby można było je wyświtlić na stronie internetowej skonstruowanej w etapie 1.

Przy tej zmianie, cały graf jest wyświetlany na samym początku, według położenia zwracanego przez MDS. Podwójne kliknięcie na którykolwiek wierzchołek chowa inne wierzchołki niepodobne do niego (podobna funkcjonalność do przycisku Select na górze strony). Następne podwójne kliknięcia działąją tak samo jak w etapie 1.
