# -*- coding: utf-8 -*
import Sort
import Effets
import Zones
class Etat(object):
    """@summary: Classe décrivant un état.
                 Cette classe est utile pour les états 'passifs' qui sont seulement là pour vérification de présense.
                  Mais elle doit être héritée par tous les autres types d'états."""
    def __init__(self, nom, debDans, duree, lanceur=None,tabCarac=[],desc=""):
        """@summary: Initialise un état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nom = nom
        self.duree = duree
        self.debuteDans = debDans
        self.tabCarac = tabCarac
        self.description = desc
        self.lanceur = lanceur
        self.desc = desc

    def __deepcopy__(self,memo):
        return self.deepcopy()

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return Etat(self.nom, self.debuteDans, self.duree, self.lanceur,self.tabCarac, self.desc)

    def actif(self):
        """@summary: Test si un état est actif.
        @return: Un booléen qui vaut vrai si l'état est actif, faux sinon."""
        return self.debuteDans <= 0 and self.duree != 0

    def triggerRafraichissement(self,personnage,niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit (au début de chaque tour ou quand sa durée est modifiée).
                     Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        pass
    def triggerAvantCalculDegats(self, dommages, baseDeg, caracs,nomSort):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués lorsque des dommages sont en train d'être calculés.
                     Utile pour les modifications de données de calcul de sorts (caractéristiques et dégâts de base du sort)
                     Cet état de base ne fait rien d'autres que renvoyées les paramètres (comportement par défaut hérité).
        @dommages: La somme des dommages bonus qui ont été calculé jusque là (panoplie et autres états)
        @type: int
        @baseDeg: Le dégât de base aléatoire qui a été calculé jusque là (jet aléatoire plus autres états)
        @type: int
        @caracs: La somme de point de caractéristiques calculé jusque là (panoplie et autres états)
        @type: int
        @nomSort: Le sort qui est provoque les dégâts. (utile pour les états modifiant les dégâts de base d'un seul sort)
        @type: string

        @return: la nouvelle valeur dommages, la nouvelle valeur dégâts de base, la nouvelle valeur point de caractéristiques."""
        return dommages,baseDeg,caracs
    def triggerApresCalculDegats(self,total,typeDeg,cible,attaquant):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués lorsque des dommages ont terminé d'être calculé.
                     Utile pour les modifications du total de dégâts calculés.
                     Cet état de base ne fait rien d'autres que renvoyées le même tolal (comportement par défaut hérité).
        @total: Le total de dégâts qui va être infligé.
        @type: int
        @typeDeg: Le type de dégâts qui va être infligé
        @type: string

        @return: la nouvelle valeur du total de dégâts."""
        return total
    def triggerApresCalculSoins(self,total,cible,attaquant):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués lorsque des dommages ont terminé d'être calculé.
                     Utile pour les modifications du total de dégâts calculés.
                     Cet état de base ne fait rien d'autres que renvoyées le même tolal (comportement par défaut hérité).
        @total: Le total de dégâts qui va être infligé.
        @type: int
        @typeDeg: Le type de dégâts qui va être infligé
        @type: string

        @return: la nouvelle valeur du total de dégâts."""
        return total
    def triggerAvantSubirDegats(self,cibleAttaque,niveau,totalPerdu,typeDegats,attaquant):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué lorsque des dommages vont être subits.
                     Utile pour la réaction à une attaque. N'est pas censé être utilisé pour modifier les dégâts.
                     Cet état de base ne fait rien.(comportement par défaut hérité).
        @cibleAttaque: le joueur qui va subir les dégâts
        @type: joueur
        @niveau: La grille de jeu
        @type: Niveau
        @totalPerdu: Le total de vie que le joueur va subir.
        @type: int
        @typeDeg:  Le type de dégâts qui va être subit
        @type: string
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        pass
    def triggerApresSubirDegats(self,cibleAttaque,niveau,attaquant, totalPerdu):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué lorsque des dommages viennent d'être subits.
                     Utile pour la réaction à une attaque.
                     Cet état de base ne fait rien.(comportement par défaut hérité).
        @cibleAttaque: le joueur qui a subit les dégâts
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage
        @totalPerdu: Le total de degats subits par le perso
        @type: int"""
        pass
    def triggerDebutTour(self,personnage,niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour commence.
                     Utile pour les états déclenchant un effet au début de tour par exemple.
                     Cet état de base ne fait rien.(comportement par défaut hérité).
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: Personnage grille de jeu
        @type: Niveau"""
        pass
    def triggerFinTour(self,personnage,niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour termine.
                     Utile pour les états déclenchant un effet en fin de tour par exemple.
                     Cet état de base ne fait rien.(comportement par défaut hérité).
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau"""
        pass
    def triggerCoutPA(self, sort, coutPAActuel):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque le coût en PA d'un sort doit être calculé.
                     Utile pour les états réduisant le coût en PA d'un sort par exemple.
                     Cet état de base ne fait rien d'aute que retourner le coût en PA passé en paramètre.(comportement par défaut hérité).
        @sort: le sort dont on cherche à calculer le coût en poitn d'action.
        @type: Sort
        @coutPAActuel: le coût du sort avant le trigger (calculé et réduit selon les éventuels états précedents.)
        @type: int

        @return: Le nouveau coût en PA"""
        return coutPAActuel
    def triggerCalculPousser(self,doPou,rePou, niveau,pousseur,joueurCible):
        """@summary: Un trigger appelé pour tous les états du pousseur qui aura poussé sa cible contre un obstacle.
                     Utile pour les états modifiant la caractéristique nombre de dommage de poussées.
                     Cet état de base ne fait rien d'aute que retourner les dommages de poussés déjà passé en paramètre.(comportement par défaut hérité).
        @doPou: La caractéristique dommage de poussée du pousseur + les états l'ayant déjà éventuellement modifiée.
        @type: int
        @niveau: La grille de jeu
        @type: Niveau
        @pousseur: Le joueur qui à pousser
        @type: Personnage
        @joueurCible: Le joueur qui s'est fait pousser
        @type: Personnage

        @return: La nouvelle valeur de dommage de poussé"""
        return doPou, rePou
    def triggerInstantane(self, **kwargs):
        """@summary: Un trigger appelé au moment ou un état est appliqué.
                     Utile pour les états qui ont un comportement immédiat.
                     Cet état de base ne fait rien (comportement par défaut hérité).
        @kwargs: les options non prévisibles selon les états.
        @type: **kwargs"""
        pass
    def triggerAvantRetrait(self,personnage):
        """@summary: Un trigger appelé au moment ou un état va être retirés.
                     Utile pour les modifications de caractéristiques qui disparaissent à la fin de l'état
                     Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        pass

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
        #print "Rafraichissement de active sort : "+personnage.classe+" lance "+self.sort.nom + " sur sa pose."
        self.sort.lance(personnage.posX,personnage.posY,niveau,personnage.posX,personnage.posY)

class EtatRedistribuerPer(Etat):
    """@summary: Classe décrivant un état qui redistribue en partie les dégâts subits autour du personnage endommagé"""
    def __init__(self, nom, debDans,duree, pourcentage,cibles, tailleZone,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int
        
        @pourcentage: le pourcentage des gégâts qui sera redistribué
        @type: int
        @cibles: la liste des cibles qui peuvent être touchés par la redistribution
        @type: string, les cibles séparées par des '|'
        @tailleZone: le rayon du cercle de redistribution
        @type: int

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.pourcentage = pourcentage
        self.tailleZone = tailleZone
        self.cibles = cibles
        super(EtatRedistribuerPer, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatRedistribuerPer(self.nom, self.debuteDans,self.duree,  self.pourcentage, self.cibles, self.tailleZone, self.lanceur,self.desc)

    def triggerApresSubirDegats(self,cibleAttaque,niveau,attaquant,totalPerdu):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué lorsque des dommages vont être subits.
                     Redistribue une partie des dégâts qui vont être subit dans la zone définit.
        @cibleAttaque: le joueur qui va subir les dégâts
        @type: joueur
        @niveau: La grille de jeu
        @type: Niveau
        @totalPerdu: Le total de vie que le joueur va subir.
        @type: int
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        totalPerdu = int(totalPerdu*(self.pourcentage/100.0))
        effetRedistribution = Effets.EffetDegats(totalPerdu,totalPerdu,"renvoie",zone=Zones.TypeZoneCercle(self.tailleZone),bypassDmgCalc=True,cibles_possibles=self.cibles,cibles_exclues="Lanceur")
        niveau.lancerEffet(effetRedistribution,cibleAttaque.posX,cibleAttaque.posY,"Redistribution", cibleAttaque.posX,cibleAttaque.posY)
        

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
        super(EtatBoostCaracFixe, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostCaracFixe(self.nom, self.debuteDans, self.duree, self.nomAttributCarac, self.boostCarac, self.lanceur,self.desc)

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
        setattr(personnage,self.nomAttributCarac,caracValue + self.boostCarac)
        print("Modification de "+self.nomAttributCarac+":"+str(caracValue)+" -> "+str(caracValue + self.boostCarac) )
    
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
        super(EtatBoostCaracPer, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostCaracPer(self.nom, self.debuteDans, self.duree, self.nomAttributCarac, self.boostCaracPer, self.lanceur,self.desc)

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
            personnage._vie += self.boostCarac
        print("Modification de "+self.nomAttributCarac+":"+str(caracValue)+" -> "+str(caracValue + self.boostCarac) +" ("+str(self.boostCaracPer)+"%)")
    
    def triggerAvantRetrait(self,personnage):
        """@summary: Un trigger appelé au moment ou un état va être retirés.
                     Retire la vitalité bonus lorsque l'état se termine
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        caracValue = getattr(personnage,self.nomAttributCarac)
        setattr(personnage,self.nomAttributCarac,caracValue - self.boostCarac)
        if self.nomAttributCarac == "vie":
            personnage._vie -= self.boostCarac
        print("Fin de modification de "+self.nomAttributCarac+":"+str(caracValue)+" -> "+str(caracValue - self.boostCarac) +" ("+str(self.boostCaracPer)+"%)")

class EtatBouclierPerLvl(Etat):
    """@summary: Classe décrivant un état qui modifie les points de bouclier par niveau."""
    def __init__(self, nom, debDans,duree,  boostBouclier,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @boostPA: le gain de Vita
        @type: int (négatif ou positif)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.boostBouclier = boostBouclier
        super(EtatBouclierPerLvl, self).__init__(nom,debDans, duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBouclierPerLvl(self.nom, self.debuteDans,self.duree,  self.boostBouclier, self.lanceur,self.desc)

    def triggerRafraichissement(self, personnage,niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit (au début de chaque tour ou quand sa durée est modifiée).
                     Les points de vitas sont boostés dès le rafraîchessement de l'état.
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        self.triggerInstantane(joueurCaseEffet=personnage)

    def triggerInstantane(self,**kwargs):
        """@summary: Un trigger appelé au moment ou un état est appliqué.
                     change le bouclier du joueur selon le boost Vita
        @kwargs: les options non prévisibles selon les états.
        @type: **kwargs"""
        personnage = kwargs.get("joueurCaseEffet")
        pourcentageBoost = self.boostBouclier
        self.boostBouclier = int(personnage.lvl * (pourcentageBoost/100.0))
        print("Modification de bouclier:"+str(self.boostBouclier))

    def triggerAvantRetrait(self,personnage):
        """@summary: Un trigger appelé au moment ou un état va être retirés.
                     Retire les points de bouclier bonus lorsque l'état se termine
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        print("Modification de bouclier: -"+str(self.boostBouclier))



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
        super(EtatBoostBaseDeg, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
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

class EtatLanceSortSiSubit(Etat):
    """@summary: Classe décrivant un état qui fait active un sort si le porteur subit des dégâts."""
    def __init__(self, nom, debDans,duree,  sort, lanceurDuSort,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @sort: le sort qui sera lancé lorsque des dégâts seront subits
        @type: Sort
        @lanceurDuSort: Le lanceur du sort parmis Porteur,Attaquant
        @type: str
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.sort = sort
        self.lanceurDuSort = lanceurDuSort
        super(EtatLanceSortSiSubit, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatLanceSortSiSubit(self.nom, self.debuteDans,self.duree,  self.sort,self.lanceurDuSort, self.lanceur,self.desc)

    def triggerApresSubirDegats(self,cibleAttaque,niveau,attaquant,totalPerdu):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué lorsque des dommages viennent d'être subits.
                     Le personnage subissant les dégâts lance le sort donné.
        @cibleAttaque: le joueur qui a subit les dégâts
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        if self.lanceurDuSort == "Porteur":
            self.sort.lance(cibleAttaque.posX,cibleAttaque.posY, niveau, cibleAttaque.posX, cibleAttaque.posY)
        elif self.lanceurDuSort == "Attaquant":
            self.sort.lance(attaquant.posX, attaquant.posY, niveau, attaquant.posX, attaquant.posY)

class EtatEffetFinTour(Etat):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur termine son tour."""
    def __init__(self, nom,  debDans,duree, effet, nomSort,quiLancera,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @effet: l'effet qui sera lancé lorsque le joueur terminera son tour
        @type: Effet
        @nomSort: le nom de sort à l'origine de l'effet
        @type: string
        @quiLancera: Le Personnage qui lancera l'effet
        @type: string ("lanceur" pour que le lanceur soit le poseur de l'état ou "cible" pour que ce soit celui qui possède l'état)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        super(EtatEffetFinTour, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetFinTour(self.nom, self.debuteDans,self.duree,  self.effet,self.nomSort,self.quiLancera, self.lanceur,self.desc)

    def triggerFinTour(self,personnage,niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour termine.
                     Active un effet à la fin du tour du personnage ciblant la position du personnage qui finit son tour, le lanceur peut être lui-même ou le lanceur de l'effet.
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau"""
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet,personnage.posX,personnage.posY,self.nomSort, personnage.posX, personnage.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet,personnage.posX,personnage.posY,self.nomSort, personnage.posX, personnage.posY, personnage)

class EtatEffetDebutTour(Etat):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur débute son tour."""
    def __init__(self, nom,  debDans,duree, effet, nomSort,quiLancera,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @effet: l'effet qui sera lancé lorsque le joueur terminera son tour
        @type: Effet
        @nomSort: le nom de sort à l'origine de l'effet
        @type: string
        @quiLancera: Le Personnage qui lancera l'effet
        @type: string ("lanceur" pour que le lanceur soit le poseur de l'état ou "cible" pour que ce soit celui qui possède l'état)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        super(EtatEffetDebutTour, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetDebutTour(self.nom, self.debuteDans,self.duree,  self.effet,self.nomSort,self.quiLancera, self.lanceur,self.desc)

    def triggerDebutTour(self,personnage,niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour commence.
                     Active un effet au début du tour ciblant la case du personnage dont le tour débute avec comme lanceur le personnage dont le tour débute  ou le lanceur de l'effet.
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: Personnage grille de jeu
        @type: Niveau"""
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet,personnage.posX,personnage.posY,self.nomSort, personnage.posX, personnage.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet,personnage.posX,personnage.posY,self.nomSort, personnage.posX, personnage.posY, personnage)

class EtatRetourCaseDepart(Etat):
    """@summary: Classe décrivant un état qui renvoie le porteur à sa case de début de tour lorsqu'il termine son tour."""
    def __init__(self, nom, debDans, duree, lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        super(EtatRetourCaseDepart, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatRetourCaseDepart(self.nom, self.debuteDans,self.duree, self.lanceur,self.desc)

    def triggerFinTour(self,personnage,niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour termine.
                     Le personnage retourne à sa case de début de tour lorsque son tour se termine
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau"""
        niveau.gereDeplacementTF(personnage,personnage.posDebTour,personnage,self.nom,AjouteHistorique=True)

class EtatCoutPA(Etat):
    """@summary: Classe décrivant un état qui modifie le coût en PA d'un des sorts du porteur."""
    def __init__(self, nom, debDans,duree,  nomSortAffecte,modCoutPA, lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @nomSortAffecte: le nom de sort dont le coût en PA sera modifié
        @type: string
        @modCoutPA: l'augmentation du coût en PA
        @type: int

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.modCoutPA = modCoutPA
        self.nomSortAffecte = nomSortAffecte
        super(EtatCoutPA, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatCoutPA(self.nom, self.debuteDans,self.duree,  self.nomSortAffecte, self.modCoutPA,self.lanceur,self.desc)

    def triggerCoutPA(self, sort, coutPAActuel):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque le coût en PA d'un sort doit être calculé.
                     Renvoie le coût du sort en PA modifié si le sort dont le coût est en train d'être calculé correspond au sort que cet état modifie.
        @sort: le sort dont on cherche à calculer le coût en point d'action.
        @type: Sort
        @coutPAActuel: le coût du sort avant le trigger (calculé et réduit selon les éventuels états précedents.)
        @type: int

        @return: Le nouveau coût en PA"""
        if sort.nom == self.nomSortAffecte:
            coutPAActuel += self.modCoutPA
        return coutPAActuel

class EtatModDegPer(Etat):
    """@summary: Classe décrivant un état qui multiplie par un pourcentage les dégâts totaux que devrait subir le porteur."""
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
        super(EtatModDegPer, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatModDegPer(self.nom, self.debuteDans,self.duree,  self.pourcentage,self.provenance, self.lanceur,self.desc)

    def triggerApresCalculDegats(self, total,typeDeg,cible,attaquant):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués lorsque des dommages ont terminé d'être calculé.
                     Modifie les dégâts par un pourcentage si les dommages sont des dommages de sort (pas de poussé)
        @total: Le total de dégâts qui va être infligé.
        @type: int
        @typeDeg: Le type de dégâts qui va être infligé
        @type: string

        @return: la nouvelle valeur du total de dégâts."""
        if self.provenance == "Allies" and cible.team != attaquant.team:
            return total
        if self.provenance == "Ennemis" and cible.team == attaquant.team:
            return total    
        if typeDeg != "doPou":
            return int((total * self.pourcentage)/100)
        return total

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

class EtatContre(Etat):
    """@summary: Classe décrivant un état qui renvoie une partie des dégâts subits au corps à corps."""
    def __init__(self, nom, debDans,duree, pourcentage, tailleZone,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @pourcentage: le pourcentage des dégâts subits au corps-à-corps x qui seront répartis
        @type: int (pourcentage)
        @tailleZone: la rayon du cercle-zone dans laquelle les dégâts subits seront réinfligés en partie
        @type: int 

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.pourcentage = pourcentage
        self.tailleZone = tailleZone
        super(EtatContre, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatContre(self.nom, self.debuteDans,self.duree,  self.pourcentage, self.tailleZone, self.lanceur,self.desc)

    def triggerAvantSubirDegats(self,cibleAttaque,niveau,totalPerdu,typeDegats,attaquant):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué lorsque des dommages vont être subits.
                     Redistribue une partie des dégâts qui vont être subit au corps-à-corps sur la zone définit.
        @cibleAttaque: le joueur qui va subir les dégâts
        @type: joueur
        @niveau: La grille de jeu
        @type: Niveau
        @totalPerdu: Le total de vie que le joueur va subir.
        @type: int
        @typeDeg:  Le type de dégâts qui va être subit
        @type: string
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        if cibleAttaque.team != attaquant.team:
            distance = abs(attaquant.posX-cibleAttaque.posX)+abs(attaquant.posY-cibleAttaque.posY)
            if distance == 1:
                if typeDegats.lower() in ["terre","eau","air","feu","neutre"]:
                    retour = int(((self.pourcentage/100)*totalPerdu) + cibleAttaque.doRenvoi)
                    s=Sort.Sort("Contre",0,0,0,1,[Effets.EffetDegats(retour,retour,typeDegats,zone=Zones.TypeZoneCercle(self.tailleZone),cibles_possibles="Ennemis", bypassDmgCalc=True)],[],0,99,99,0,0,"cercle",False)
                    s.lance(cibleAttaque.posX,cibleAttaque.posY, niveau, attaquant.posX, attaquant.posY)

class EtatEffetSiSubit(Etat):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur subit des dégâts."""
    def __init__(self, nom,  debDans,duree,effet,nomSort,quiLancera,typeDeg="",lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @effet: l'effet qui s'activera lors d'un dégât subit
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui subira l'effet 
        @type: string ("lanceur" ou "cible")

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        self.typeDeg = typeDeg
        super(EtatEffetSiSubit, self).__init__(nom,debDans, duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiSubit(self.nom, self.debuteDans,self.duree,  self.effet, self.nomSort,self.quiLancera,self.typeDeg,self.lanceur,self.desc)

    def triggerAvantSubirDegats(self,cibleAttaque,niveau,totalPerdu,typeDegats,attaquant):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué lorsque des dommages vont être subits.
                     Active un effet ciblant le lanceur ou la cible avant de subir les dégâts
        @cibleAttaque: le joueur qui va subir les dégâts
        @type: joueur
        @niveau: La grille de jeu
        @type: Niveau
        @totalPerdu: Le total de vie que le joueur va subir.
        @type: int
        @typeDeg:  Le type de dégâts qui va être subit
        @type: string
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        if totalPerdu >0 and (self.typeDeg == typeDegats or self.typeDeg==""):
            if self.quiLancera == "lanceur":
                niveau.lancerEffet(self.effet,attaquant.posX,attaquant.posY,self.nomSort, attaquant.posX, attaquant.posY, self.lanceur)
            elif self.quiLancera == "cible":
                niveau.lancerEffet(self.effet,cibleAttaque.posX,cibleAttaque.posY,self.nomSort, attaquant.posX, attaquant.posY, attaquant)
class EtatEffetSiPousse(Etat):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur se fait pousser."""
    def __init__(self, nom,  debDans,duree,effet,nomSort,quiLancera,lanceur=None,desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devra passé pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra passé pour que l'état se désactive.
        @type: int

        @effet: l'effet qui s'activera lors d'une poussé
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui subira l'effet 
        @type: string ("lanceur" ou "cible")

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        super(EtatEffetSiPousse, self).__init__(nom,debDans, duree, lanceur,desc)

    def deepcopy(self):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiPousse(self.nom, self.debuteDans,self.duree,  self.effet, self.nomSort,self.quiLancera,self.lanceur,self.desc)

    def triggerCalculPousser(self,doPou,rePou,niveau,pousseur,cibleAttaque):
        """@summary: Un trigger appelé pour tous les états du pousseur qui aura poussé sa cible contre un obstacle.
                     Active un effet sur le lanceur ou la cible au choix si le joueur portant l'état est poussé
        @doPou: La caractéristique dommage de poussée du pousseur + les états l'ayant déjà éventuellement modifiée.
        @type: int
        @niveau: La grille de jeu
        @type: Niveau
        @pousseur: Le joueur qui à pousser
        @type: Personnage
        @joueurCible: Le joueur qui s'est fait pousser
        @type: Personnage

        @return: La nouvelle valeur de dommage de poussé"""
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet,self.lanceur.posX,cibleAttaque.posY,self.nomSort, cibleAttaque.posX, cibleAttaque.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet,cibleAttaque.posX,cibleAttaque.posY,self.nomSort, cibleAttaque.posX, cibleAttaque.posY, cibleAttaque)
        return doPou,rePou
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
