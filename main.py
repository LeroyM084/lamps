# main.py

import ville
import numpy as np
import argparse
import networkx as nx
import matplotlib.pyplot as plt

def dessiner_graphe(city):
    """
    Dessine le graphe de la ville en utilisant la matrice d'adjacence.
    - Les nœuds avec un lampadaire sont en orange, les autres en bleu clair.
    - Les arêtes non éclairées sont en noir, les arêtes éclairées sont en jaune.
    
    :param city: Objet Ville contenant la configuration des lampadaires et de la matrice d'adjacence
    """
    # Utilise la matrice d'adjacence de la ville
    matrix = city.adj_matrix

    # Crée un graphe vide
    G = nx.Graph()

    # Ajoute les nœuds avec une couleur spécifique selon la présence de lampadaires
    n = matrix.shape[0]
    # Si un lampadaire est présent à l'index i, le nœud est en orange; sinon, en bleu clair.
    node_colors = ['yellow' if city.lampadaires[i] else 'darkgrey' for i in range(n)]
    for i in range(n):
        # Ajoute le nœud en utilisant des lettres comme noms (A, B, C, ...)
        G.add_node(chr(i + ord('A')))

    # Ajouter les arêtes et définir leur couleur
    edges = []       # Liste des arêtes
    edge_colors = [] # Liste des couleurs d'arêtes correspondantes
    for i in range(n):
        for j in range(i + 1, n):  # Parcours des paires de nœuds (i, j) pour éviter les doublons
            if matrix[i, j] == 1:
                # Arête non éclairée (noir)
                G.add_edge(chr(i + ord('A')), chr(j + ord('A')))
                edges.append((chr(i + ord('A')), chr(j + ord('A'))))
                edge_colors.append('black')
            elif matrix[i, j] == 2:
                # Arête éclairée (jaune)
                G.add_edge(chr(i + ord('A')), chr(j + ord('A')))
                edges.append((chr(i + ord('A')), chr(j + ord('A'))))
                edge_colors.append('orange')

    # Dessiner le graphe avec la mise en page de NetworkX et les couleurs assignées
    pos = nx.spring_layout(G)  # Positionnement des nœuds avec l'algorithme spring
    nx.draw(G, pos, with_labels=True, edge_color=edge_colors, node_color=node_colors, node_size=700, font_size=12, width=2)
    plt.show()

def creationVille(rounds, nodes, edges=None, allConnected=False):
    """
    Fonction pour optimiser le placement des lampadaires dans une ville.
    Exécute plusieurs essais pour trouver la configuration optimale de lampadaires.
    
    :param rounds: Nombre de tentatives pour trouver la meilleure configuration
    :param nodes: Nombre de places dans la ville (nombre de nœuds)
    :param edges: Nombre de rues dans la ville (nombre d'arêtes), ignoré si allConnected est True
    :param allConnected: Si True, toutes les places sont connectées à chaque autre place
    """
    # Création de la ville de référence, soit avec un graphe complet (allConnected) ou avec un nombre donné de rues
    if allConnected:
        matrix = np.ones((nodes, nodes), dtype=int)  # Matrice complète de connexions
        np.fill_diagonal(matrix, 0)  # Pas de connexion d'un nœud à lui-même
        reference_city = ville.Ville(nodes, adj_matrix=matrix)
    else:
        reference_city = ville.Ville(nodes, edges)  # Ville avec un nombre de rues donné

    # Affiche les informations et connexions de la ville
    reference_city.afficherInfo()
    reference_city.afficherConnections()




    test_city = ville.Ville(nodes, adj_matrix=reference_city.adj_matrix.copy()) #Création d'un objet ville avec comme matrice la matrice de reference
    test_city.choisirPlaceLamp()  # Place les lampadaires de manière optimisée

    dessiner_graphe(test_city)


def main():
    """
    Point d'entrée du programme. Utilise argparse pour obtenir les arguments d'entrée :
    - Nombre de places (obligatoire)
    - Nombre de rues (optionnel)
    - Option pour connecter toutes les places
    """
    parser = argparse.ArgumentParser(description='Optimisation du placement des lampadaires dans une ville')
    parser.add_argument('nbNodes', type=int, help='Nombre de places dans la ville')
    parser.add_argument('--street', type=int, help='Nombre approximatif de rues', default=None)
    parser.add_argument('rounds', type=int, help="Nombre de rounds d'essais")
    parser.add_argument('--allConnected', action='store_true', help='Toutes les places sont connectées')

    # Extraction des arguments fournis par l'utilisateur
    args = parser.parse_args()

    # Vérification de compatibilité des options allConnected et street
    if args.allConnected and args.street is not None:
        print("Attention : --street est ignoré quand --allConnected est utilisé.")

    # Appel de la fonction d'optimisation avec les arguments fournis
    opti(args.rounds, args.nbNodes, args.street, args.allConnected)

# Lancement du programme si le fichier est exécuté directement
if __name__ == "__main__":
    main()
