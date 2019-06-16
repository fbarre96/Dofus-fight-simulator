from Etats.Etat import Etat

class EtatBoostSortsPer(Etat):
    """@summary: Classe décrivant un état qui multiplie par un pourcentage les dégats totaux des sorts que devrait donné le lanceur."""
    def __init__(self, nom, debDans, duree, pourcentage,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @pourcentage: le pourcentage de modification des dégâts qui seront subis.
        @type: int (pourcentage)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.pourcentage = pourcentage
        super(EtatBoostSortsPer, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostSortsPer(self.nom, self.debuteDans,self.duree,  self.pourcentage, self.lanceur,self.desc)

    def triggerApresCalculDegats(self,total,typeDeg,cible,attaquant):
        if typeDeg != "arme":
            return int((total * self.pourcentage)/100)
        else:
            return total
