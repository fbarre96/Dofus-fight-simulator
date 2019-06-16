from Etats.Etat import Etat

class EtatBoostSortCarac(Etat):
    """@summary: Classe décrivant un état qui modifie la valeur d'une Sort."""
    def __init__(self, nom, debDans,duree, nomSort, nomAttributCarac, boostCarac,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int
        @nomSort: Le sort dont les caracs doivent être modifiées
        @type: str
        @nomAttributCarac: Le nom de l'attribut a boost
        @type: string qui doit être dans les attribut de la classe Personnage
        @boostCarac: le gain de Caractéristique a appliqué
        @type: int (négatif ou positif)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nomAttributCarac = nomAttributCarac
        self.boostCarac = boostCarac
        self.nomSort = nomSort
        super().__init__(nom,  debDans,duree,lanceur,desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostSortCarac(self.nom, self.debuteDans, self.duree, self.nomSort,self.nomAttributCarac, self.boostCarac, self.lanceur,self.desc)

    def triggerRafraichissement(self, personnage,niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit (au début de chaque tour ou quand sa durée est modifiée).
                     Les points de porté sont reboostés à chaque rafraîchissement de l'état.
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        self.triggerInstantane(joueurCaseEffet=personnage)

    def __getSortToUpdate(self, perso):
        for sort in perso.sorts:
            if sort.nom == self.nomSort:
                return sort
    
    def triggerInstantane(self,**kwargs):
        """@summary: Un trigger appelé au moment ou un état est appliqué.
                     change la carac du joueur selon le boost carac et le nom de l'attribut a boost
        @kwargs: les options non prévisibles selon les états.
        @type: **kwargs"""
        personnage = kwargs.get("joueurCaseEffet")
        sortToUpdate = self.__getSortToUpdate(personnage)
        caracValue = getattr(sortToUpdate,self.nomAttributCarac)
        setattr(sortToUpdate,self.nomAttributCarac,caracValue + self.boostCarac)
        print("Modification du sort "+sortToUpdate.nom+" "+self.nomAttributCarac+":"+str(caracValue)+" -> "+str(caracValue + self.boostCarac) )
        niveau = kwargs.get("niveau",None)
        if niveau is not None:
            niveau.afficherSorts()
    def triggerAvantRetrait(self,personnage):
        """@summary: Un trigger appelé au moment ou un état va être retirés.
                     Retire la vitalité bonus lorsque l'état se termine
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        sortToUpdate = self.__getSortToUpdate(personnage)
        caracValue = getattr(sortToUpdate,self.nomAttributCarac) 
        setattr(sortToUpdate,self.nomAttributCarac,caracValue - self.boostCarac)
        print("Fin de modification du sort "+sortToUpdate.nom+" "+self.nomAttributCarac+":"+str(caracValue)+" -> "+str(caracValue - self.boostCarac) )
