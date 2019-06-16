from Etats.Etat import Etat

class EtatBoostBaseDeg(Etat):
    """@summary: Classe décrivant un état qui modifie les dégâts de base d'un sort pour le porteur."""
    def __init__(self, nom,  debDans, duree,nomSort,boostbaseDeg,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @nomSort: le nom du sort dont les dégâts de base seront boostés
        @type: string
        @boostbaseDeg: le gain de dommage de base pour le sort concerné
        @type: int (négatif ou positif)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.boostbaseDeg = boostbaseDeg
        self.nomSort=nomSort
        super().__init__(nom, debDans,duree, lanceur,desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostBaseDeg(self.nom,  self.debuteDans, self.duree, self.nomSort, self.boostbaseDeg,self.lanceur,self.desc)

    def triggerAvantCalculDegats(self,dommages, baseDeg, caracs, nomSort):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués lorsque des dommages sont en train d'être calculés.
             Les dégâts de base du sort sont boostés si le nom du sort correspond à l'état
        @dommages: La somme des dommages bonus qui ont été calculé jusque là (panoplie et autres états)
        @type: int
        @baseDeg: Le dégât de base aléatoire qui a été calculé jusque là (jet aléatoire plus autres états)
        @type: int
        @caracs: La somme de point de caractéristiques calculé jusque là (panoplie et autres états)
        @type: int
        @nomSort: Le sort qui est provoque les dégâts. (utile pour les états modifiant les dégâts de base d'un seul sort)
        @type: string

        @return: la nouvelle valeur dommages, la nouvelle valeur dégâts de base, la nouvelle valeur point de caractéristiques."""
        if nomSort == self.nomSort:
            baseDeg += self.boostbaseDeg
        return dommages, baseDeg, caracs

class EtatBoostBaseDegLvlBased(EtatBoostBaseDeg):
    """@summary: Classe décrivant un état qui modifie les dégâts de base d'un sort pour le porteur selon son lvl.
    Hérite de EtatBoostBaseDeg"""
    def __init__(self, nom,  debDans, duree,nomSort,boostbaseDeg,lanceur=None,desc=""):
        super().__init__(nom, debDans,duree,boostbaseDeg,nomSort, lanceur,desc)
    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostBaseDegLvlBased(self.nom,  self.debuteDans, self.duree, self.nomSort, self.boostbaseDeg,self.lanceur,self.desc)    
    def triggerAvantCalculDegats(self,dommages, baseDeg, caracs, nomSort):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués lorsque des dommages sont en train d'être calculés.
             Les dégâts de base du sort sont boostés si le nom du sort correspond à l'état
        @dommages: La somme des dommages bonus qui ont été calculé jusque là (panoplie et autres états)
        @type: int
        @baseDeg: Le dégât de base aléatoire qui a été calculé jusque là (jet aléatoire plus autres états)
        @type: int
        @caracs: La somme de point de caractéristiques calculé jusque là (panoplie et autres états)
        @type: int
        @nomSort: Le sort qui est provoque les dégâts. (utile pour les états modifiant les dégâts de base d'un seul sort)
        @type: string

        @return: la nouvelle valeur dommages, la nouvelle valeur dégâts de base, la nouvelle valeur point de caractéristiques."""
        if nomSort == self.nomSort:
            baseDeg += int((self.boostbaseDeg/100.0)*(self.lanceur.lvl))
        return dommages, baseDeg, caracs