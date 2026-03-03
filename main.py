import networkx as nx
import matplotlib.pyplot as plt
import graphviz as gv
import json

# Fonctions -----------------------------------
    # Choisir le batiment
def choixBatiment():
    print("\n Quel bâtiment voulez-vous tester ? :" \
    "\n [1] - Bâtiment Principal" \
    "\n [2] - Petit Bâtiment" \
    "\n [3] - Bâtiment Linéaire" \
    "\n [4] - Bâtiment avec Étages" \
    "\n [5] - Bâtiment Étoile" \
    "\n [6] - Bâtiment Grille" \
    "\n [7] - Bâtiment Complexe" \
    "\n [8] - Bâtiment Carré" \
    "\n [9] - Bâtiment Disconnecté" \
    "\n [10] - Bâtiment Arbre" \
    "\n [11] - Retour")

    response = input()

    match int(response):
        case 1:
            return 0
        case 2:
            return 1
        case 3:
            return 2
        case 4:
            return 3
        case 5:
            return 4
        case 6:
            return 5
        case 7:
            return 6
        case 8:
            return 7
        case 9:
            return 8
        case 10:
            return 9
        case 11:
            return None
        case _:
            print("Mauvaise valeur entrée")
            return choixBatiment()


    # Intersections "Critiques"

def is_articulation_point(G, node):
    G_copy = G.copy()
    G_copy.remove_node(node)
    return nx.number_connected_components(G_copy) > nx.number_connected_components(G)

    # Couloirs "Vitales"

def is_isthme(G, edge):
    G_copy = G.copy()
    G_copy.remove_edge(edge[0], edge[1])
    return nx.number_connected_components(G_copy) > nx.number_connected_components(G)

    # Emplacement des caméras
    
def initVF(nodes, edges):
    VoisinFerme = {}

    for node in nodes:
        VoisinFerme[node] = {node}

        for u, v in edges:
            if u == node:
                VoisinFerme[node].add(v)
            if v == node:
                VoisinFerme[node].add(u)

    return VoisinFerme

def minimum_dominating_set(nodes, edges):
    VoisinFerme = initVF(nodes, edges)
    nodes_set = set(nodes)

    meilleure_solution = [set(nodes)]

    def backtrack(D, Dom):
        if Dom == nodes_set:
            if len(D) < len(meilleure_solution[0]):
                meilleure_solution[0] = D.copy()
            return

        if len(D) >= len(meilleure_solution[0]):
            return

        non_domines = nodes_set - Dom
        u = next(iter(non_domines))

        for v in VoisinFerme[u]:
            if v not in D:
                new_D = D | {v}
                new_Dom = Dom | VoisinFerme[v]

                backtrack(new_D, new_Dom)

    backtrack(set(), set())
    return meilleure_solution[0]

def creer_pos_pour_edges(edges):
    """
    Crée un dictionnaire de positions à partir d'une liste d'arêtes.
    
    Args:
        edges: liste de tuples (nœud1, nœud2)
    
    Returns:
        dict: dictionnaire {nœud: (x, y)}
    """
    import networkx as nx
    
    G = nx.Graph()
    
    G.add_edges_from(edges)
    
    pos = nx.spring_layout(G, seed=3113794652)
    
    return pos

def suppDeList(l1, l2):
    return [elem for elem in l1 if elem not in l2]

def affiche():
    plt.axis("off")
    plt.show()

def continuer():
    print("\n Entrée une touche :" \
    "\n [1] - Revenir au menu" \
    "\n [2] - Quitter")
    response = input()

    match int(response):
        case 1:
            return True
        case 2:
            return False


# Import du json des batiments ----------------------------------------------------

building_index = choixBatiment()
with open('batiments.json', 'r') as f:
    data = json.load(f)

    # Charger le bâtiment principal
edges = data['buildings'][building_index]['edges']

nodes = set([n for edge in edges for n in edge])

nom_bat = data['buildings'][building_index]['name']
desc_bat = data['buildings'][building_index]['description']

G =gv.Graph('G', engine='neato')

for node in nodes:
    G.node(str(node), shape='square', color='gray')

for u, v in edges:
    G.edge(str(u), str(v))

Gnx = nx.Graph()
Gnx.add_edges_from(edges)

# Initialisation ------------------------------

intersectionsCritiques = []
couloirsVitales = []
connexe = nx.is_connected(Gnx)
diametre = nx.diameter(Gnx)
ensemblesDomi = []
ZUC = []
Densite = 0

    # Intersections "Critiques"

for node in nodes:
    if is_articulation_point(Gnx, node):
        intersectionsCritiques.append(node)

    # Couloirs "Vitales"

for edge in edges:
    if is_isthme(Gnx, edge):
        couloirsVitales.append(edge)

    # Emplacement des caméras

ensemblesDomi = minimum_dominating_set(nodes, edges)

    # Zone Ultra Connecté

cliques = list(nx.find_cliques(Gnx))

cliqueM = max(cliques, key=len)
for clique in cliques:
    if len(clique) == len(cliqueM):
        ZUC.append(clique)


# Affichage -----------------------------------

pos = creer_pos_pour_edges(edges)
options = {"edgecolors": "tab:gray", "node_size": 100, "alpha": 0.9}
nx.draw_networkx_edges(Gnx, pos=pos, width=1.0, alpha=0.5)

    # CouloirsVitaux

def afficheLesCouloirsVitaux():
    nx.draw_networkx_edges(
        Gnx,
        pos=pos,
        edgelist=couloirsVitales,
        width=3,
        alpha=1,
        edge_color="tab:red"
    )

    nx.draw_networkx_edges(Gnx, pos=pos, edgelist=suppDeList(edges, couloirsVitales), width=3, alpha=1)

    nx.draw_networkx_nodes(Gnx, pos=pos, nodelist=nodes, node_color="tab:gray", **options)

    affiche()

    # Caméra
def afficheLesCamera():
    nx.draw_networkx_edges(Gnx, pos=pos, edgelist=edges, width=3, alpha=1)

    nx.draw_networkx_nodes(Gnx, pos=pos, nodelist=ensemblesDomi, node_color="tab:red", **options)
    nx.draw_networkx_nodes(Gnx, pos=pos, nodelist=suppDeList(nodes, ensemblesDomi), node_color="tab:gray", **options)
    affiche()

def afficheInterSect():
    nx.draw_networkx_edges(Gnx, pos=pos, edgelist=edges, width=3, alpha=1)

    nx.draw_networkx_nodes(Gnx, pos=pos, nodelist=intersectionsCritiques, node_color="tab:red", **options)
    nx.draw_networkx_nodes(Gnx, pos=pos, nodelist=suppDeList(nodes, intersectionsCritiques), node_color="tab:gray", **options)
    affiche()

# ZUC

def afficheZuc():
    nx.draw_networkx_edges(Gnx, pos=pos, edgelist=edges, width=3, alpha=1)
    lst = []
    colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
    'tab:purple',
    'tab:brown',
    'tab:pink',
    'tab:olive',
    'tab:cyan'
    ]
    for i in range(len(ZUC)):
        color = colors[i % len(colors)]
        print(color)
        nx.draw_networkx_nodes(Gnx, pos=pos, nodelist=ZUC[i], node_color=color, **options)
        lst += ZUC[i]
    nx.draw_networkx_nodes(Gnx, pos=pos, nodelist=suppDeList(nodes, lst), node_color="tab:gray", **options)
    affiche()

def afficheGraph():
    nx.draw_networkx_edges(Gnx, pos=pos, edgelist=edges, width=3, alpha=1)
    
    nx.draw_networkx_nodes(Gnx, pos=pos, nodelist=nodes, node_color="tab:gray", **options)
    affiche()

def afficheInfo():
    print(
    "\n --------------------------------- Information sur le Graph ---------------------------------",
    "\n  ||                              ~~~~~~~~~~~~~~~~~~~~~~~~~~",
    "\n  || - Nom : ",  nom_bat, \
    "\n  || - Description : ", desc_bat ,
    "\n  || ",
    "\n  || - Intersection Critiques : ", intersectionsCritiques,
    "\n  || - Couloirs Vitaux : ", couloirsVitales,
    "\n  || - Est Connexe : ", connexe,
    "\n  || - Diametre : ", diametre,
    "\n  || - Emplacement des caméra : ", ensemblesDomi,
    "\n  || - Zone Ultra Connecté : ", ZUC,
    "\n  || - Densite : ", Densite,
    "\n  ||"
    "\n --------------------------------------------------------------------------------------------\n"
)
    

def start():
    Running = True
    while Running:
        print("\n Que Voulez-vous afficher ? :" \
        "\n [0] - Afficher le Batiment" \
        "\n [1] - Information sur le graph" \
        "\n [2] - Intersections Critiques" \
        "\n [3] - Emplacement optimisée des caméra" \
        "\n [4] - Zone à fort affluence" \
        "\n [5] - Couloirs vitaux" \
        "\n [6] - Quittez")

        response = input()

        match int(response):
            case 0:
                afficheGraph()
                Running = continuer()
            case 1:
                afficheInfo()
                Running = continuer()
            case 2:
                afficheInterSect()
                Running = continuer()
            case 3:
                afficheLesCamera()
                Running = continuer()
            case 4:
                afficheZuc()
                Running = continuer()
            case 5:
                afficheLesCouloirsVitaux()
                Running = continuer()
            case 6:
                Running = False
            case _:
                print("Mauvaise valeurs entrée")

start()
