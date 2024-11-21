import numpy as np  # Bibliothèque pour la manipulation de tableaux et matrices
import pandas as pd  # Bibliothèque pour l'affichage et la manipulation de données sous forme de tableaux
import random as r  # Module pour les opérations aléatoires

class Ville:
    def __init__(self, nbNodes, nbStreet=0, adj_matrix=None):
        """
        Constructeur de la classe Ville. Initialise une ville avec un certain nombre de places (nœuds) et de rues.
        
        :param nbNodes: Nombre de places dans la ville (nombre de nœuds)
        :param nbStreet: Nombre de rues dans la ville (nombre d'arêtes)
        :param adj_matrix: Matrice d'adjacence optionnelle pour définir les connexions (rues) entre les places
        """
        self.nbNodes = nbNodes  # Nombre de places
        self.nodes = self.createNodes()  # Liste des places, nommées A, B, C, ...
        self.edges = set()  # Ensemble des rues (paires de nœuds connectés)
        self.nbLamp = 0  # Compteur du nombre de lampadaires
        self.lampadaires = [False] * self.nbNodes  # Liste pour suivre les places où des lampadaires sont placés (booléens)

        if adj_matrix is None:  # Si aucune matrice d'adjacence n'est fournie
            self.adj_matrix = self.new_matrix()  # Créer une nouvelle matrice d'adjacence vide (toutes les valeurs à 0)
            self.nbStreet = nbStreet  # Nombre de rues initialisé avec la valeur donnée
            self.createStreet()  # Générer les rues de manière aléatoire
        else:
            self.adj_matrix = adj_matrix  # Si une matrice d'adjacence est fournie, on l'utilise
            self.nbStreet = np.sum(adj_matrix) // 2  # Calcul du nombre de rues à partir de la matrice (chaque rue est comptée deux fois)

    def createNodes(self):
        """
        Crée une liste de nœuds (places) nommés A, B, C, ..., selon le nombre de places (nbNodes).
        :return: Liste des noms de places (par exemple ['A', 'B', 'C'])
        """
        return [chr(i) for i in range(ord('A'), ord('A') + self.nbNodes)]  # Génère une liste de lettres à partir du caractère 'A'

    
    def createStreet(self):
        """
        Crée un certain nombre de rues (connexions aléatoires entre les places) dans la ville.
        Utilise des échantillons aléatoires pour relier deux places à la fois, jusqu'à avoir le nombre requis de rues.
        S'il est impossible de créer suffisamment de rues, le processus s'arrête après 1000 tentatives.
        """
        attempts = 0  # Compteur d'essais pour éviter une boucle infinie
        while len(self.edges) < self.nbStreet:  # Tant qu'il n'y a pas suffisamment de rues
            u, v = r.sample(range(self.nbNodes), 2)  # Sélectionne deux nœuds au hasard
            if (u, v) not in self.edges and (v, u) not in self.edges:  # Vérifie que la rue n'existe pas déjà
                self.edges.add((u, v))  # Ajoute la rue à l'ensemble des rues
                self.adj_matrix[u][v] = self.adj_matrix[v][u] = 1  # Met à jour la matrice d'adjacence
            attempts += 1  # Incrémente le compteur d'essais
            if attempts > 1000:  # Si le nombre de tentatives dépasse 1000, on arrête pour éviter les boucles infinies
                print(f"Impossible de créer exactement {self.nbStreet} rues.")
                break
        self.checkIsolated()  # Vérifie que toutes les places sont bien connectées à au moins une rue

    def checkIsolated(self):
        """
        Vérifie que toutes les places ont au moins une connexion. Si une place est isolée (sans rue), 
        elle est connectée à une autre place non isolée au hasard.
        """
        for i in range(self.nbNodes):
            if np.sum(self.adj_matrix[i]) == 0:  # Si une place n'a aucune connexion
                while True:
                    new_connection = r.randint(0, self.nbNodes - 1)  # Sélectionne un autre nœud aléatoirement
                    if new_connection != i and np.sum(self.adj_matrix[new_connection]) > 0:  # Assure que le nœud sélectionné est valide
                        self.adj_matrix[i][new_connection] = self.adj_matrix[new_connection][i] = 1  # Crée une nouvelle connexion
                        break

    def new_matrix(self):
        """
        Crée une matrice d'adjacence vide (remplie de zéros) de taille nbNodes x nbNodes.
        :return: Matrice d'adjacence (tableau 2D numpy) initialisé à 0
        """
        return np.zeros((self.nbNodes, self.nbNodes), dtype=int)  # Retourne une matrice carrée de zéros


    def afficherMatrice(self):
        """
        Affiche la matrice d'adjacence sous forme de tableau, avec les noms des places en colonnes et en lignes.
        """
        df = pd.DataFrame(self.adj_matrix, index=self.nodes, columns=self.nodes)  # Crée un DataFrame pandas pour un affichage clair
        print(df)  # Affiche le tableau

    def afficherInfo(self):
        """
        Affiche le nombre de rues et le nombre de places de la ville.
        """
        print(f"\nNombre de rues : {self.nbStreet}")
        print(f"Nombre de places : {self.nbNodes}")

    def ruesSombre(self):
        """
        Calcule le nombre de rues non éclairées (représentées par la valeur 1 dans la matrice d'adjacence).
        :return: Nombre de rues non éclairées
        """
        return np.sum(self.adj_matrix == 1) // 2  # Compte les "1" dans la matrice, divisé par 2 (chaque rue est comptée deux fois)

    

    def afficherConnections(self):
        """
        Affiche les connexions (rues) de chaque place. Pour chaque place, elle montre à quelles autres places elle est reliée.
        """
        print("\nConnexions entre les places :")
        for i, node in enumerate(self.nodes):  # Pour chaque place
            connections = [self.nodes[j] for j in range(self.nbNodes) if self.adj_matrix[i][j] == 1]  # Liste des places connectées
            if connections:
                print(f"{node} est relié à : {', '.join(connections)}")  # Affiche les connexions

    def choisirPlaceLamp(self):
        """
        Algorithme pour placer des lampadaires sur les places. Choisit les places avec le plus de rues non éclairées 
        pour maximiser l'effet du lampadaire.
        """
        self.lampadaires = [False] * self.nbNodes  # Réinitialise la liste des lampadaires
        while np.any(self.adj_matrix == 1):  # Tant qu'il y a des rues non éclairées
            best_node = max(range(self.nbNodes), key=lambda i: np.sum(self.adj_matrix[i] == 1))  # Trouve la place avec le plus de rues non éclairées
            if not self.lampadaires[best_node]:  # Si cette place n'a pas encore de lampadaire
                self.placerLampadaire(best_node)  # Place un lampadaire
                self.lampadaires[best_node] = True  # Marque cette place comme ayant un lampadaire

    def placerLampadaire(self, node):
        """
        Place un lampadaire sur une place donnée et met à jour la matrice pour marquer les rues comme éclairées.
        :param node: La place où le lampadaire est placé
        """
        for j in range(self.nbNodes):
            if self.adj_matrix[node][j] == 1:  # Si la place est reliée à une autre place par une rue non éclairée
                self.adj_matrix[node][j] = self.adj_matrix[j][node] = 2  # Marque la rue comme éclairée (valeur 2)
        self.nbLamp += 1  # Incrémente le compteur de lampadaires placés
