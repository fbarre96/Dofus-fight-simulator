from Etats.Etat import Etat

class EtatBoostCaracFixe(Etat):
    """@summary: Classe décrivant un état qui modifie la valeur d'une caractéristique."""
    def __init__(self, nom, debDans,duree, nomAttributCarac, boostCarac,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int
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
        super().__init__(nom,  debDans,duree,lanceur,desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostCaracFixe(self.nom, self.debuteDans, self.duree, self.nomAttributCarac, self.boostCarac, self.lanceur,self.desc)

    def triggerInstantane(self,**kwargs):
        """@summary: Un trigger appelé au moment ou un état est appliqué.
                     change la carac du joueur selon le boost carac et le nom de l'attribut a boost
        @kwargs: les options non prévisibles selon les états.
        @type: **kwargs"""
        personnage = kwargs.get("joueurCaseEffet")
        caracValue = getattr(personnage,self.nomAttributCarac)
        setattr(personnage,self.nomAttributCarac,caracValue + self.boostCarac)
        print("Modification de "+self.nomAttributCarac+":"+str(caracValue)+" -> "+str(caracValue + self.boostCarac) )

    def triggerRafraichissement(self, personnage,niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit (au début de chaque tour ou quand sa durée est modifiée).
                     Les points de porté sont reboostés à chaque rafraîchissement de l'état.
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        self.triggerInstantane(joueurCaseEffet=personnage)
    
    def triggerAvantRetrait(self,personnage):
        """@summary: Un trigger appelé au moment ou un état va être retirés.
                     Retire la vitalité bonus lorsque l'état se termine
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        caracValue = getattr(personnage,self.nomAttributCarac)
        setattr(personnage,self.nomAttributCarac,caracValue - self.boostCarac)
        print("Fin de modification de "+self.nomAttributCarac+":"+str(caracValue)+" -> "+str(caracValue - self.boostCarac) )

    def triggerFinTour(self,personnage,niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour termine.
                     Active un effet à la fin du tour du personnage ciblant la position du personnage qui finit son tour, le lanceur peut être lui-même ou le lanceur de l'effet.
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau"""
        if self.nomAttributCarac in ["PA","PM"]:
            caracValue = getattr(personnage,self.nomAttributCarac)
            setattr(personnage,self.nomAttributCarac,caracValue + self.boostCarac)

class EtatBoostCaracPer(Etat):
    """@summary: Classe décrivant un état qui modifie la valeur d'une caractéristique selon un pourcentage."""
    def __init__(self, nom, debDans,duree, nomAttributCarac, boostCaracPer,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int
        @nomAttributCarac: Le nom de l'attribut a boost
        @type: string qui doit être dans les attribut de la classe Personnage
        @boostCaracPer: le gain de Caractéristique a appliqué
        @type: int (négatif ou positif)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nomAttributCarac = nomAttributCarac
        self.boostCaracPer = boostCaracPer
        self.boostCarac = 0
        super().__init__(nom,  debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostCaracPer(self.nom, self.debuteDans, self.duree, self.nomAttributCarac, self.boostCaracPer, self.lanceur, self.desc)

    def triggerRafraichissement(self, personnage,niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit (au début de chaque tour ou quand sa durée est modifiée).
                     Les points de porté sont reboostés à chaque rafraîchissement de l'état.
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        self.triggerInstantane(joueurCaseEffet=personnage)

    def triggerInstantane(self,**kwargs):
        """@summary: Un trigger appelé au moment ou un état est appliqué.
                     change la carac du joueur selon le boost carac et le nom de l'attribut a boost
        @kwargs: les options non prévisibles selon les états.
        @type: **kwargs"""
        personnage = kwargs.get("joueurCaseEffet")
        caracValue = getattr(personnage,self.nomAttributCarac)
        pourcentageBoost = self.boostCaracPer
        self.boostCarac = int(caracValue * (pourcentageBoost/100.0))
        setattr(personnage,self.nomAttributCarac,caracValue + self.boostCarac)
        if self.nomAttributCarac == "vie":
            personnage.vieMax += self.boostCarac
        print("Modification de "+self.nomAttributCarac+":"+str(caracValue)+" -> "+str(caracValue + self.boostCarac) +" ("+str(self.boostCaracPer)+"%)")
    
    def triggerAvantRetrait(self,personnage):
        """@summary: Un trigger appelé au moment ou un état va être retirés.
                     Retire la vitalité bonus lorsque l'état se termine
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        caracValue = getattr(personnage,self.nomAttributCarac)
        setattr(personnage,self.nomAttributCarac,caracValue - self.boostCarac)
        if self.nomAttributCarac == "vie":
            personnage.vieMax -= self.boostCarac
        print("Fin de modification de "+self.nomAttributCarac+":"+str(caracValue)+" -> "+str(caracValue - self.boostCarac) +" ("+str(self.boostCaracPer)+"%)")
