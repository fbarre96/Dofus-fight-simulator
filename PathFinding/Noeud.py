"""@summary: déclare la classe Noeud, utile à PathFinder
"""
class Noeud:
    """@summary: Classe servant à l'algorithme de recherche de chemin A*"""

    def __init__(self, posX, posY, cout=0, heur=0):
        """@summary: Initialise un noeud du graphe.
        @posX: la cordonné x du noeud dans le graphe
        @type: int
        @posY: la cordonné y du noeud dans le graphe
        @type: int
        @cout: le coût calculé pour parvenir à ce noeud, 0 par défaut
        @type: int
        @heur: l'heuristique calculé pour parvenir à ce noeud, 0 par défaut
        @type: int"""

        self.posX = posX
        self.posY = posY
        self.cout = cout
        self.heur = heur
        