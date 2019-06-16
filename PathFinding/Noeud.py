
class Noeud:
    """@summary: Classe servant à l'algorithme de recherche de chemin A*"""

    def __init__(self, x, y, cout=0, heur=0):
        """@summary: Initialise un noeud du graphe.
        @x: la cordonné x du noeud dans le graphe
        @type: int
        @y: la cordonné y du noeud dans le graphe
        @type: int
        @cout: le coût calculé pour parvenir à ce noeud, 0 par défaut
        @type: int
        @heur: l'heuristique calculé pour parvenir à ce noeud, 0 par défaut
        @type: int"""

        self.x = x
        self.y = y
        self.cout = cout
        self.heur = heur



