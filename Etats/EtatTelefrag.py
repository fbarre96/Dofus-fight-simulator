from Etats.Etat import Etat

class EtatTelefrag(Etat):
    """@summary: Classe décrivant un état Téléfrag."""
    def __init__(self, nom,  debDans,duree, nomSort, lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @nomSort: le nom du sort qui à générer le téléfrag
        @type: string

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nomSort = nomSort
        super(EtatTelefrag, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatTelefrag(self.nom, self.debuteDans,self.duree,  self.nomSort,self.lanceur,self.desc)
