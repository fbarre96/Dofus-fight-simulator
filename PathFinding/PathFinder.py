"""@summary: Module introduisant la recherche de chemin A*
"""

from PathFinding.Noeud import Noeud


def cmpToKey(mycmp):
    'Convert a cmp= function into a key= function'
    class Key():
        """@summary: Classe servant à déclarer une clé de comparaison
        """
        def __init__(self, obj, *args):
            # pylint: disable=unused-argument
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return Key


def compare2Noeuds(noeud1, noeud2):
    """@summary: Fonction comparant deux noeuds du graphe.
        @noeud1: le premier noeud à comparer
        @type: Noeud
        @noeud2: le second noeud à comparer
        @type: Noeud
        @return: 1 si le premier noeud à la plus petite heuristique,
                -1 si le second à la plus petite heuristique
                 0 si les deux sont égales"""

    if noeud1.heur < noeud2.heur:
        return 1
    elif noeud1.heur == noeud2.heur:
        return 0
    else:
        return -1


def ajoutTrie(liste, noeud):
    """@summary: Fonction ajoutant un noeud dans une liste triée.
    @liste: la liste de noeud trié
    @type: liste [Noeuds]
    @noeud: le noeud à insérer dans la liste triée.
    @type: Noeud"""
    for i,noeud_in_liste in enumerate(liste):
        if compare2Noeuds(noeud, noeud_in_liste) != -1:
            liste.insert(i, noeud)
            return
    liste.append(noeud)

class PathFinder:
    """@summary: Classe implémentant l'algorithme A*
    """
    def __init__(self):
        self.cachedCaseX = None
        self.cachedCaseY = None
        self.cachedDestX = None
        self.cachedDestY = None
        self.cachedResult = None

    def pathFinding(self, niveau, caseCibleX, caseCibleY, joueur):
        """@summary: Implémentation de l'algorithme A*.
                    recherche de chemin depuis la position du joueur vers la case_cible
        @caseCibleX: La coordonnée posX à laquelle on veut accéder
        @type: int
        @caseCibleY: La coordonnée posY à laquelle on veut accéder
        @type: int
        @joueur: Le joueur qui veut se rendre sur la case cible depuis sa position
        @type: Personnage

        @return: la liste des cases composant le chemin pour accéder à la case cible
         depuis la position du joueur. None si aucun chemin n'a été trouvé"""
        if self.cachedDestX == caseCibleX and self.cachedDestY == caseCibleY and \
           self.cachedCaseX == joueur.posX and self.cachedCaseY == joueur.posY:
            return self.cachedResult
        self.cachedCaseX = joueur.posX
        self.cachedCaseY = joueur.posY
        self.cachedDestX = caseCibleX
        self.cachedDestY = caseCibleY

        # VOIR PSEUDO CODE WIKIPEDIA
        listeFermee = []
        listeOuverte = []
        joueurSurCase = niveau.getJoueurSur(caseCibleX, caseCibleY)
        if niveau.structure[caseCibleY][caseCibleX].type != "v" or joueurSurCase is not None:
            self.cachedResult = None
            return None
        depart = Noeud(joueur.posX, joueur.posY)
        ajoutTrie(listeOuverte, depart)
        noeudOuvert = None
        while listeOuverte:
            if noeudOuvert is not None:
                listeOuverte.remove(noeudOuvert)
            noeudOuvert = listeOuverte[0]

            if noeudOuvert.posX == caseCibleX and noeudOuvert.posY == caseCibleY:
                path = []
                current = noeudOuvert
                while current is not None:
                    path.append([current.posX, current.posY])
                    current = current.parent
                path.remove(path[-1])
                self.cachedResult = path[::-1]
                return path[::-1] # Return reversed path
            voisins = niveau.getVoisins(noeudOuvert)
            for voisin in voisins:
                vExisteCoutInf = False
                for noeud2Listes in listeFermee+listeOuverte:
                    if noeud2Listes.posX == voisin.posX and noeud2Listes.posY == voisin.posY \
                       and noeud2Listes.cout < voisin.cout:
                        vExisteCoutInf = True
                        break
                if not vExisteCoutInf:
                    voisin.cout = noeudOuvert.cout+1
                    voisin.heur = voisin.cout + \
                        (abs(voisin.posX-caseCibleX)+abs(voisin.posY-caseCibleY))
                    ajoutTrie(listeOuverte, voisin)
            listeFermee.append(noeudOuvert)
        print("Aucun chemin trouvee")
        self.cachedResult = None
        return None
