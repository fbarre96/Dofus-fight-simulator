from Etats.Etat import Etat

class EtatActiveSort(Etat):
    """@summary: Classe décrivant un état qui active un sort à chaque tour actif."""
    def __init__(self, nom, debDans,duree, sort,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int
        
        @sort: le sort qui sera lancé au rafraîchissement de l'effet
        @type: Sort
        
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.sort = sort
        super(EtatActiveSort, self).__init__(nom,debDans, duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatActiveSort(self.nom, self.debuteDans,self.duree,  self.sort, self.lanceur,self.desc)

    def triggerRafraichissement(self, personnage,niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit (au début de chaque tour ou quand sa durée est modifiée).
                     Le sort est lancé à ce moment.
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        self.sort.lance(personnage.posX,personnage.posY,niveau,personnage.posX,personnage.posY)
