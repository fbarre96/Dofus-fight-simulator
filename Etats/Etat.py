# -*- coding: utf-8 -*
"""@summary: Décrit un état de base qui sera appliqué à un personnage."""


class Etat:
    """@summary: Classe décrivant un état.
                 Cette classe est utile pour les états 'passifs' qui sont seulement
                 là pour vérification de présense.
                 Mais elle doit être héritée par tous les autres types d'états."""
    subclasses = []
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    @classmethod
    def getListEtat(cls):
        return [str(classe.__name__) for classe in cls.subclasses]+["Etat"]
    
    @classmethod
    def getObjectFromName(cls, name):
        for classe in cls.subclasses:
            if str(classe.__name__) == name:
                return classe("nom etat", 0, 1)
        return cls("nom etat", 0, 1)

    @classmethod
    def craftFromInfos(cls, infos):
        return Etat(infos["nom"], infos["debuteDans"], infos["duree"], None, infos["desc"])
        
    @classmethod
    def factory(cls, etat_infos, **kwargs):
        if isinstance(etat_infos, dict):
            for classe in cls.subclasses + [Etat]:
                if classe.__name__ == etat_infos["etatType"]:
                    return classe.craftFromInfos(etat_infos)
        else:
            raise TypeError("Etat factory attend un etat sous forme de json dict")

    def getAllInfos(self):
        ret = {}
        ret["etatType"] = self.__class__.__name__
        ret["nom"] = self.nom
        ret["duree"] = self.duree
        ret["debuteDans"] = self.debuteDans
        ret["desc"] = self.desc
        return ret

    def __str__(self):
        return self.nom+" ("+str(self.duree)+(" tours)" if int(self.duree) > 1 else " tour)")
    
    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nomLbl = ttk.Label(frame, text="Nom:")
        nomLbl.grid(row=0, column=0, sticky="e")
        self.nomEntry = ttk.Entry(frame, width=40)
        self.nomEntry.delete(0, 'end')
        self.nomEntry.insert(0, self.nom)
        self.nomEntry.grid(row=0, column=1, sticky="w")
        ret["nom"] = self.nomEntry
        debDansLbl = ttk.Label(frame, text="Débute dans ? tours:")
        debDansLbl.grid(row=1, column=0, sticky="e")
        self.debDansSpinbox = tk.Spinbox(frame, from_=0, to=999, width=4)
        self.debDansSpinbox.delete(0, 'end')
        self.debDansSpinbox.insert(0, int(self.debuteDans))
        self.debDansSpinbox.grid(row=1, column=1, sticky="w")
        ret["debuteDans"] = self.debDansSpinbox
        dureeLbl = ttk.Label(frame, text="Durée:")
        dureeLbl.grid(row=2, column=0, sticky="e")
        self.dureeSpinbox = tk.Spinbox(frame, from_=-1, to=999, width=4)
        self.dureeSpinbox.delete(0, 'end')
        self.dureeSpinbox.insert(0, int(self.duree))
        self.dureeSpinbox.grid(row=2, column=1, sticky="w")
        ret["duree"] = self.dureeSpinbox
        descLbl = ttk.Label(frame, text="Description:")
        descLbl.grid(row=3, column=0, sticky="e")
        self.descEntry = ttk.Entry(frame, width=100)
        self.descEntry.delete(0, 'end')
        self.descEntry.insert(0, self.desc)
        self.descEntry.grid(row=3, column=1, sticky="w")
        ret["desc"] = self.descEntry
        frame.pack()
        return ret


    def __init__(self, nom, debDans, duree, lanceur=None, desc=""):
        """@summary: Initialise un état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nom = nom
        self.duree = int(duree)
        self.debuteDans = int(debDans)
        self.description = desc
        self.lanceur = lanceur
        self.desc = desc

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return Etat(self.nom, self.debuteDans, self.duree, self.lanceur, self.desc)

    def actif(self):
        """@summary: Test si un état est actif.
        @return: Un booléen qui vaut vrai si l'état est actif, faux sinon."""
        return self.debuteDans <= 0 and self.duree != 0

    def triggerAvantPiegeDeclenche(self, niveau, piege, joueurDeclencheur, porteur):
        """@summary: Un trigger appelé pour tous les joueurs lorsqu'un joueur déclenche un piège.
                     Cet état de base ne fait rien (comportement par défaut hérité).
        @niveau: La grille de jeu en cours
        @type: Niveau
        @piege: Le piège qui a été déclenché
        @type: Piege
        @joueurDeclencheur: Le personnage qui a déclenché le piège
        @type: Personnage
        @porteur: Le personnage qui porte l'état dont le trigger s'est activé
        @type: Personnage"""
        # pylint: disable=unused-argument
        return

    def triggerApresTF(self, niveau, joueurOrigineTF, joueurEchangeTF, porteur,
                       reelLanceur, nomSort):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé pour tous les joueurs lorsqu'un joueur déclenche un téléfrag
                     Cet état de base ne fait rien (comportement par défaut hérité).
        @niveau: La grille de jeu en cours
        @type: Niveau
        @joueurOrigineTF: Le joueur qui se déplace en téléfrag
        @type: Personnage
        @joueurEchangeTF: Le personnage qui a va être échangé au cours du téléfrag
        @type: Personnage
        @reelLanceur: Le personnage qui à lancer le sort à l'origine du téléfrag
        @type: Personnage
        @nomSort: Le nom du sort qui a provoqué le téléfrag
        @type: str
        """
        return

    def triggerRafraichissement(self, personnage, niveau):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit
                     (au début de chaque tour ou quand sa durée est modifiée).
                     Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        return

    def triggerAvantCalculDegats(self, dommages, baseDeg, caracs, nomSort, minjet, maxjet):
        # pylint: disable=unused-argument
        """@summary:
            Un trigger appelé pour tous les états des 2 joueurs impliqués lorsque des dommages
            sont en train d'être calculés.
            Utile pour les modifications de données de calcul de sorts
            (caractéristiques et dégâts de base du sort)
            Cet état de base ne fait rien d'autres que renvoyées les paramètres
            (comportement par défaut hérité).
        @dommages: La somme des dommages bonus qui ont été calculé jusque là
                   (panoplie et autres états)
        @type: int
        @baseDeg: Le dégât de base aléatoire qui a été calculé jusque là
                  \n(jet aléatoire plus autres états)
        @type: int
        @caracs: La somme de point de caractéristiques calculé jusque là
                 (panoplie et autres états)
        @type: int
        @nomSort: Le sort qui est provoque les dégâts.
                  (utile pour les états modifiant les dégâts de base d'un seul sort)
        @type: string

        @return: la nouvelle valeur dommages, la nouvelle valeur dégâts de base,
                 la nouvelle valeur point de caractéristiques."""
        return dommages, baseDeg, caracs

    def triggerApresCalculDegats(self, total, typeDeg, cible, attaquant):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués
                     lorsque des dommages ont terminé d'être calculé.
                     Utile pour les modifications du total de dégâts calculés.
                     Cet état de base ne fait rien d'autres que renvoyées le même total
                     (comportement par défaut hérité).
        @total: Le total de dégâts qui va être infligé.
        @type: int
        @typeDeg: Le type de dégâts qui va être infligé
        @type: string

        @return: la nouvelle valeur du total de dégâts."""
        return total

    def triggerApresCalculSoins(self, total, cible, attaquant):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués
                     lorsque des dommages ont terminé d'être calculé.
                     Utile pour les modifications du total de dégâts calculés.
                     Cet état de base ne fait rien d'autres que renvoyées le même total
                     (comportement par défaut hérité).
        @total: Le total de dégâts qui va être infligé.
        @type: int
        @typeDeg: Le type de dégâts qui va être infligé
        @type: string

        @return: la nouvelle valeur du total de dégâts."""
        return total

    def triggerApresChangementDeVie(self, porteur, niveau):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé orsque la vie du porteur a changé.
                     Cet état de base ne fait rien.

        @return: rien"""
        

    def triggerAvantSubirDegats(self, cibleAttaque, niveau, totalPerdu, typeDegats, attaquant):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé pour tous les états du joueur attaqué
                     lorsque des dommages vont être subits.
                     Utile pour la réaction à une attaque.
                     N'est pas censé être utilisé pour modifier les dégâts.
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
        return

    def triggerApresSubirDegats(self, cibleAttaque, niveau, attaquant, totalPerdu):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé pour tous les états du joueur attaqué
                     lorsque des dommages viennent d'être subits.
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
        return

    def triggerDebutTour(self, personnage, niveau):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour commence.
                     Utile pour les états déclenchant un effet au début de tour par exemple.
                     Cet état de base ne fait rien.(comportement par défaut hérité).
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: Personnage grille de jeu
        @type: Niveau"""
        return

    def triggerFinTour(self, personnage, niveau):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour termine.
                     Utile pour les états déclenchant un effet en fin de tour par exemple.
                     Cet état de base ne fait rien.(comportement par défaut hérité).
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau"""
        return

    def triggerCalculPousser(self, doPou, rePou, niveau, pousseur, joueurCible):
        # pylint: disable=unused-argument
        """@summary:
        Un trigger appelé pour tous les états du pousseur qui aura poussé sa cible.
        Utile pour les états modifiant la caractéristique nombre de dommage de poussées.
        Cet état de base ne fait rien d'aute que retourner les dommages de poussés
        déjà passé en paramètre. (comportement par défaut hérité).
        @doPou: La caractéristique dommage de poussée du pousseur +
                les états l'ayant déjà éventuellement modifiée.
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
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé au moment ou un état est appliqué.
                     Utile pour les états qui ont un comportement immédiat.
                     Cet état de base ne fait rien (comportement par défaut hérité).
        @kwargs: les options non prévisibles selon les états.
        @type: **kwargs"""
        return

    def triggerAvantRetrait(self, personnage):
        # pylint: disable=unused-argument
        """@summary:
        Un trigger appelé au moment ou un état va être retirés.
        Utile pour les modifications de caractéristiques qui disparaissent à la fin de l'état
        Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        return

    def triggerApresRetrait(self, niveau, personnage, porteur, etatRetire):
        # pylint: disable=unused-argument
        """@summary:
        Un trigger appelé au moment ou un état va être retirés.
        Utile pour les modifications de caractéristiques qui disparaissent à la fin de l'état
        Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        return

    def triggerAvantMort(self, niveau, porteur, mouru, meurtrier):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé pour tous les états des joueurs
                     lorsque un perso meurt.
                     Active un effet ciblant le meurtier ou la victime ou le porteur avant la mort
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
        return
    def triggerAvantApplicationEtat(self, niveau, nouvelEtat, joueurLanceur, joueurCible):
        # pylint: disable=unused-argument
        """@summary: Un trigger appelé pour le joueur qui obtient un nouvel état.
                     Active un effet sur le lanceur ou la cible"""
        return

    def triggerApresDeplacementForce(self, niveau, deplace, deplaceur):
        # pylint: disable=unused-argument
        """@summary:
        Un trigger appelé au moment ou un personnage se fait porté
        Utile pour les modifications de caractéristiques qui disparaissent à la fin de l'état
        Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        return

    def triggerApresPorte(self, niveau, porteur, porte):
        # pylint: disable=unused-argument
        """@summary:
        Un trigger appelé au moment ou un personnage se fait porté
        Utile pour les modifications de caractéristiques qui disparaissent à la fin de l'état
        Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        return

    def triggerApresLance(self, niveau, lanceur, celuiLance):
        # pylint: disable=unused-argument
        """@summary:
        Un trigger appelé au moment ou un personnage se fait porté
        Utile pour les modifications de caractéristiques qui disparaissent à la fin de l'état
        Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        return
