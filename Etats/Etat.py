# -*- coding: utf-8 -*
"""@summary: Décrit un état de base qui sera appliqué à un personnage."""


class Etat():
    """@summary: Classe décrivant un état.
                 Cette classe est utile pour les états 'passifs' qui sont seulement
                 là pour vérification de présense.
                 Mais elle doit être héritée par tous les autres types d'états."""

    def __init__(self, nom, debDans, duree, lanceur=None, tabCarac=None, desc=""):
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
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nom = nom
        self.duree = duree
        self.debuteDans = debDans
        if tabCarac is None:
            self.tabCarac = []
        else:
            self.tabCarac = tabCarac
        self.description = desc
        self.lanceur = lanceur
        self.desc = desc

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return Etat(self.nom, self.debuteDans, self.duree, self.lanceur, self.tabCarac, self.desc)

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

    def triggerAvantCalculDegats(self, dommages, baseDeg, caracs, nomSort):
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
        