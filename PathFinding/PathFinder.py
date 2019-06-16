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
    liste.append(noeud)
    liste.sort(key=cmpToKey(compare2Noeuds))


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
        if niveau.structure[caseCibleY][caseCibleX].type != "v":
            self.cachedResult = None
            return None
        depart = Noeud(joueur.posX, joueur.posY)
        ajoutTrie(listeOuverte, depart)
        while listeOuverte:
            noeudOuvert = listeOuverte[-1]
            del listeOuverte[-1]
            if noeudOuvert.posX == caseCibleX and noeudOuvert.posY == caseCibleY:
                # reconstituerChemin(noeudOuvert,listeFermee)
                tab = []
                for case in listeFermee:
                    tab.append([case.posX, case.posY])
                if tab:
                    if tab[0][0] == joueur.posX and tab[0][1] == joueur.posY:
                        del tab[0]
                tab.append([noeudOuvert.posX, noeudOuvert.posY])
                self.cachedResult = tab
                return tab
            voisins = niveau.getVoisins(noeudOuvert.posX, noeudOuvert.posY)
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
