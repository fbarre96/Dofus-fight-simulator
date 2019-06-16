"""@summary: Module introduisant la recherche de chemin A*
"""

from PathFinding.Noeud import Noeud


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class Key(object):
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


def compare2Noeuds(n1, n2):
    """@summary: Fonction comparant deux noeuds du graphe.
        @n1: le premier noeud à comparer
        @type: Noeud
        @n2: le second noeud à comparer
        @type: Noeud
        @return: 1 si le premier noeud à la plus petite heuristique,
                -1 si le second à la plus petite heuristique
                 0 si les deux sont égales"""

    if n1.heur < n2.heur:
        return 1
    elif n1.heur == n2.heur:
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
    liste.sort(key=cmp_to_key(compare2Noeuds))


class PathFinder:
    def __init__(self):
        self.cached_case_x = None
        self.cached_case_y = None
        self.cached_dest_x = None
        self.cached_dest_y = None
        self.cached_result = None

    def pathFinding(self, niveau, caseCibleX, caseCibleY, joueur):
        """@summary: Implémentation de l'algorithme A*. recherche de chemin depuis la position du joueur vers la case_cible
        @caseCibleX: La coordonnée x à laquelle on veut accéder
        @type: int
        @caseCibleY: La coordonnée y à laquelle on veut accéder
        @type: int
        @joueur: Le joueur qui veut se rendre sur la case cible depuis sa position
        @type: Personnage

        @return: la liste des cases composant le chemin pour accéder à la case cible depuis la position du joueur. None si aucun chemin n'a été trouvé"""
        if self.cached_dest_x == caseCibleX and self.cached_dest_y == caseCibleY and self.cached_case_x == joueur.posX and self.cached_case_y == joueur.posY:
            return self.cached_result
        self.cached_case_x = joueur.posX
        self.cached_case_y = joueur.posY
        self.cached_dest_x = caseCibleX
        self.cached_dest_y = caseCibleY

        # VOIR PSEUDO CODE WIKIPEDIA
        listeFermee = []
        listeOuverte = []
        if niveau.structure[caseCibleY][caseCibleX].type != "v":
            self.cached_result = None
            return None
        depart = Noeud(joueur.posX, joueur.posY)
        ajoutTrie(listeOuverte, depart)
        while len(listeOuverte) != 0:
            u = listeOuverte[-1]
            del listeOuverte[-1]
            if u.x == caseCibleX and u.y == caseCibleY:
                # reconstituerChemin(u,listeFermee)
                tab = []
                for case in listeFermee:
                    tab.append([case.x, case.y])
                if(len(tab) > 0):
                    if tab[0][0] == joueur.posX and tab[0][1] == joueur.posY:
                        del tab[0]
                tab.append([u.x, u.y])
                self.cached_result = tab
                return tab
            voisins = niveau.getVoisins(u.x, u.y)
            for v in voisins:
                v_existe_cout_inf = False
                for n in listeFermee+listeOuverte:
                    if n.x == v.x and n.y == v.y and n.cout < v.cout:
                        v_existe_cout_inf = True
                        break
                if not(v_existe_cout_inf):
                    v.cout = u.cout+1
                    v.heur = v.cout + \
                        (abs(v.x-caseCibleX)+abs(v.y-caseCibleY))
                    ajoutTrie(listeOuverte, v)
            listeFermee.append(u)
        print("Aucun chemin trouvee")
        self.cached_result = None
        return None
