from Etats.Etat import Etat

class EtatModSoinPer(Etat):
    """@summary: Classe décrivant un état qui multiplie par un pourcentage les soins totaux que devrait subir le porteur."""
    def __init__(self, nom, debDans, duree, pourcentage, provenance="",lanceur=None,desc=""):
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
        self.provenance = provenance
        super(EtatModSoinPer, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatModSoinPer(self.nom, self.debuteDans,self.duree,  self.pourcentage,self.provenance, self.lanceur,self.desc)

    def triggerApresCalculSoins(self, total,cible,attaquant):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués lorsque des dommages ont terminé d'être calculé.
                     Modifie les dégâts par un pourcentage si les dommages sont des dommages de sort (pas de poussé)
        @total: Le total de dégâts qui va être infligé.
        @type: int

        @return: la nouvelle valeur du total de dégâts."""
        if self.provenance == "Allies" and cible.team != attaquant.team:
            return total
        if self.provenance == "Ennemis" and cible.team == attaquant.team:
            return total    
        
        return int((total * self.pourcentage)/100)
