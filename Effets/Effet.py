# -*- coding: utf-8 -*
"""
@summary: Décrit un Effet de sort générique, déclare les fonctions stub
"""
import Zones

class Effet(object):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
                 Cette classe est 'abstraite' et doit être héritée."""

    def __init__(self, **kwargs):
        """@summary: Initialise un Effet.
        @kwargs: Options de l'effets
        , possibilitées: etat_requis (string séparé par |, aucun par défaut),
                        etat_requis_cibles (string séparé par |, aucun par défaut),
                        etat_requis_lanceur (string séparé par |, aucun par défaut),
                        consomme_etat (booléen, Faux par défaut),
                        cibles_possibles (string, "Allies|Ennemis|Lanceur" par défaut)
                        cibles_exclues (string, aucune par défaut)
                        cible_non_requise (booléen, Faux par défaut).
                                    Indique si l'effet peut être lancé s'il n'a pas de cible direct
                                    (autrement dit si le sort est lancé sur une case vide).
                        zone (Zone, Zones.TypeZoneCercle(0) par défaut = sort mono cible)
        @type: **kwargs"""
        self.etatRequisCibleDirect = kwargs.get('etat_requis', "").split("|")
        if self.etatRequisCibleDirect[-1] == "":
            self.etatRequisCibleDirect = []
        self.etatRequisCibles = kwargs.get('etat_requis_cibles', "").split("|")
        if self.etatRequisCibles[-1] == "":
            self.etatRequisCibles = []
        self.etatRequisLanceur = kwargs.get('etat_requis_lanceur', "").split("|")
        if self.etatRequisLanceur[-1] == "":
            self.etatRequisLanceur = []
        self.consommeEtat = kwargs.get('consomme_etat', False)
        self.ciblesPossibles = kwargs.get(
            'cibles_possibles', "Allies|Ennemis|Lanceur").split("|")
        self.ciblesExclues = kwargs.get('cibles_exclues', "").split("|")
        self.ciblesPossiblesDirect = kwargs.get('cibles_possibles_direct',
                                                "|".join(self.ciblesPossibles)).split("|")
        self.cibleNonRequise = kwargs.get('cible_non_requise', False)
        self.typeZone = kwargs.get('zone', Zones.TypeZoneCercle(0))
        self.pile = kwargs.get("pile", True)
        self.kwargs = kwargs

    def setCritique(self, val):
        """
        @summary: indique à l'effet qu'il a été lancé avec un sort qui a été critique
        @val: la nouvelle valeur pour le booléen critique
        @type: bool
        """
        self.kwargs["isCC"] = val

    def isCC(self):
        """
        @summary: demance à l'effet s'il a été lancé avec un sort qui a été critique
        @return: bool
        """
        return self.kwargs.get("isCC", False)

    def setPrevisu(self, val):
        """
        @summary: indique à l'effet qu'il est lancé dans le cadre d'une prévisualisation
        @val: la nouvelle valeur pour le booléen isPrevisu
        @type: bool
        """
        self.kwargs["isPrevisu"] = val

    def isPrevisu(self):
        """
        @summary: demance à l'effet s'il a été lancé pour une prévisualisation
        @return: bool
        """
        return self.kwargs.get("isPrevisu", False)

    def setNomSortTF(self, val):
        """
        @summary: indique à l'effet le nom du sort a l'origine du téléfrag
        @val: la nouvelle valeur pour le nom du sort
        @type: string
        """
        self.kwargs["nomSortTF"] = val

    def getNomSortTF(self):
        """
        @summary: demance à l'effet le nom du sort à l'origine du téléfrag
        @return: le nom du sort
        """
        return self.kwargs.get("nomSortTF", "")

    def isReverseTreatmentOrder(self):
        """
        @summary: demande à l'effet s'il doit rechercher ses cibles dans le sens inverse.
                  Depuis l'extérieur vers l'intérieur.
        @return: un booléen
        """
        return self.kwargs.get("reversedTreatmentOrder", False)

    def __deepcopy__(self, memo):
        """
        @summary: implémente une copie profonde de l'état
        @return: Renvoie une copie profonde exacte de l'effet
        """
        return Effet(**self.kwargs)

    def setDegatsSubits(self, valPerdu, typeDegats):
        """
        @summary: indique à l'effet les degats subits et le type de dégats
        @valPerdu: Le nombre de points de vie perdus
        @type: int
        @typeDegats: Le type des dégats
        @type: str (Air, Terre, Feu, Eau, Arme...)
        @return: un booléen
        """
        self.kwargs["degatsSubits"] = valPerdu
        self.kwargs["typeDegats"] = typeDegats

    def getDegatsSubits(self):
        """
        @summary: retourne la valeur de degats subits et le type de degats
        @return: renvoie un tuple (degats subits, type de dégats) avec type (int, str)
                défaut est (0,"")
        """
        return self.kwargs.get("degatsSubits", 0), self.kwargs.get("typeDegats", "")

    def estLancable(self, joueurLanceur, joueurCibleDirect):
        # pylint: disable=unused-argument
        """@summary: Test si un effet peut etre lance selon les options de l'effets.
        @joueurLanceur: Le joueur lançant l'effet
        @type: Personnage
        @joueurCible: Le joueur dans la zone d'effet testé
        @type: Personnage
        @joueurCibleDirect: Le joueur sur lequel l'effet est lancé
                            à la base (peut-être identique à joueurCible.
        @type: Personnage ou None
        @ciblesDejaTraitees: Les cibles déjà touchées par l'effet
        @type: tableau de Personnage
        @return: booléen indiquant vrai si la cible est valide, faux sinon"""
        msg = ""
        # Test si une cible direct n'existe pas si l'effet doit être jouée
        if (joueurCibleDirect is None and not self.cibleNonRequise):
            msg = "DEBUG : Invalide : Cible direct non renseigne et pas faire au vide"
            return msg, False
        # Test si un état est requis sur la cible direct et qu'une cible direct existe
        # une liste est vraie si elle n'est pas vide
        if (joueurCibleDirect is None and self.etatRequisCibleDirect):
            msg = "DEBUG : Invalide : Cible direct non renseigne et etatRequis "+ \
                "pour cible direct (" + str(self.etatRequisCibleDirect)+")"
            return msg, False
        if not joueurLanceur.aEtatsRequis(self.etatRequisLanceur):
            msg = "DEBUG : Invalide :etatRequis pour lanceur non present" + \
                str(self.etatRequisLanceur)+" n'est pas présent sur le lanceur"
            return msg, False
        if joueurCibleDirect is not None:
            if not((joueurCibleDirect.team == joueurLanceur.team and \
                joueurCibleDirect.uid != joueurLanceur.uid and \
                "Allies" in self.ciblesPossiblesDirect) \
                    or \
                (joueurCibleDirect.team != joueurLanceur.team and \
                joueurCibleDirect.uid != joueurLanceur.uid and \
                "Ennemis" in self.ciblesPossiblesDirect) \
                    or \
                (joueurCibleDirect.team == joueurLanceur.team and \
                joueurCibleDirect.uid == joueurLanceur.uid and \
                "Lanceur" in self.ciblesPossiblesDirect) \
                    or \
                (joueurCibleDirect.classe in self.ciblesPossiblesDirect) \
                    or \
                (joueurCibleDirect.invocateur is not None and \
                "Invoc" in self.ciblesPossiblesDirect) \
                    or \
                (joueurCibleDirect.invocateur is not None and \
                joueurCibleDirect.invocateur.uid == joueurCibleDirect.uid and \
                "Invocateur" in self.ciblesPossiblesDirect)):

                msg = "DEBUG : Invalide : Cible Direct non possible "+\
                        str(joueurCibleDirect.classe)+"/"+str(self.ciblesPossiblesDirect)
                return msg, False
            # Test si la cible firect n'est pas une case vide qu'il a bien les états requis
            if not joueurCibleDirect.aEtatsRequis(self.etatRequisCibleDirect):
                msg = "DEBUG : Invalide :etatRequis pour cible direct non present"
                return msg, False
        return msg, True

    def cibleValide(self, joueurLanceur, joueurCible, ciblesDejaTraitees):
        """@summary: Test si un joueur cible est un cible valide selon les options de l'effets.
        @joueurLanceur: Le joueur lançant l'effet
        @type: Personnage
        @joueurCible: Le joueur dans la zone d'effet testé
        @type: Personnage
        @joueurCibleDirect: Le joueur sur lequel l'effet est lancé
                            à la base (peut-être identique à joueurCible.
        @type: Personnage ou None
        @ciblesDejaTraitees: Les cibles déjà touchées par l'effet
        @type: tableau de Personnage
        @return: booléen indiquant vrai si la cible est valide, faux sinon"""

        # Test si la cible est dans les cibles possibles
        msg = ""
        if joueurCible is None:
            joueurCibleTeam = -1
            joueurCibleUid = -1
            joueurCibleClasse = ""
            joueurCibleInvocateur = ""
        else:
            joueurCibleTeam = joueurCible.team
            joueurCibleUid = joueurCible.uid
            joueurCibleClasse = joueurCible.classe
            joueurCibleInvocateur = joueurCible.invocateur

        if (joueurCibleTeam == joueurLanceur.team and joueurCibleUid != joueurLanceur.uid
                and "Allies" in self.ciblesPossibles) \
            or (joueurCibleTeam == joueurLanceur.team and joueurCibleUid == joueurLanceur.uid
                and "Lanceur" in self.ciblesPossibles) \
            or (joueurCibleTeam != joueurLanceur.team and "Ennemis" in self.ciblesPossibles) \
            or (joueurCibleClasse in self.ciblesPossibles) \
            or (joueurCibleInvocateur is not None and "Invoc" in self.ciblesPossibles) \
            or (joueurLanceur.invocateur is not None and "Invocateur" in self.ciblesPossibles
                and joueurCibleUid == joueurLanceur.invocateur.uid):
            # Test si la cible est exclue
            if joueurCibleClasse in self.ciblesExclues \
               or (joueurCibleUid == joueurLanceur.uid and "Lanceur" in self.ciblesExclues) \
               or (joueurCibleInvocateur is not None and "Invoc" in self.ciblesExclues) \
               or (joueurLanceur.invocateur is not None and "Invocateur" in self.ciblesExclues
                       and joueurCibleUid == joueurLanceur.invocateur.uid):
                if joueurCibleClasse != "":
                    msg = "DEBUG : Invalide : Cible Exclue "+\
                        str(joueurCibleClasse)+"/"+str(self.ciblesExclues)
                    return msg, False
            # Test si la cible est déjà traitée
            if joueurCible in ciblesDejaTraitees:
                msg = "DEBUG : Invalide : Cible deja traitee "+\
                    str(joueurCible) + str(ciblesDejaTraitees)
                return msg, False
            # Test si la cible est une case vide et que l'effet ne nécessite pas d'etat pour la cibl
            # une liste est vraie si elle n'est pas vide
            if joueurCible is None and self.etatRequisCibles:
                msg = "DEBUG : Invalide : Cible  non renseigne et etatRequis pour cible"
                return msg, False
            # Test si la cible n'est pas une case vide qu'il a bien les états requis
            if joueurCible is not None:
                if not joueurCible.aEtatsRequis(self.etatRequisCibles):
                    msg = "DEBUG : Invalide :etatRequis pour cible non present"
                    return msg, False

            # La cible a passé tous les tests
            return msg, True
        msg = "DEBUG : Invalide : Cible "+ joueurCibleClasse + \
                " pas dans la liste des cibles possibles ("+str(self.ciblesPossibles)+")"
        return msg, False

    def aPorteZone(self, departZoneX, departZoneY, testDansZoneX, testDansZoneY, joueurX, joueurY):
        """@summary: Test si une case appartient à une zone donnée.
                     Wrapper pour la fonction testCaseEstDedans polymorphique.
        @departZoneX: L'abcisse de la case de départ de la zone,
                      souvent le centre et souvent le centre de l'effet
        @type: int
        @departZoneY: L'ordonnée de la case de départ de la zone,
                      souvent le centre et souvent le centre de l'effet
        @type: int
        @testDansZoneX: L'abcisse de la case dont ou souhait savoir si elle est dans la zone'
        @type: int
        @testDansZoneY: L'ordonnée de la case dont ou souhait savoir si elle est dans la zone'
        @type: int
        @joueurX: L'abcisse de la case sur laquelle le joueur lançant l'effet se trouve.
                  Utile pour certaines zones dépendants de la position du lanceur.
        @type: int
        @joueurY: L'ordonnée de la case sur laquelle le joueur lançant l'effet se trouve.
                  Utile pour certaines zones dépendants de la position du lanceur.
        @type: int
        @return: booléen indiquant vrai si la case testée est dans la zone, faux sinon"""

        # Le lanceur peut pas etre dans la zone si y a le - a la fin du type zone
        toRet = self.typeZone.testCaseEstDedans([departZoneX, departZoneY],
                                                [testDansZoneX, testDansZoneY],
                                                [joueurX, joueurY])
        return toRet

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        # pylint: disable=unused-argument
        """@summary: Applique les modifications sur le jeu créées par l'effet.
        @niveau: la grille de simulation de combat.
        @type: Niveau
        @joueurCaseEffet: Le joueur sur se tenant sur une case de la zone d'effet traitée.
        @type: Personnage
        @joueurLanceur: Le joueur ayant lancé l'effet
        @type: Personnage
        @kwargs: Les paramètres optionnels supplémentaires pour chaque effet.s
        @type: **kwargs"""

        # Comportement neutre non défini
        niveau.ajoutFileEffets(self)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        # pylint: disable=unused-argument
        """@summary: activer un effet. Appeler dans Niveau.depileEffets"""
        print("Activation non définie")

    def afficher(self):
        """@summary: Affiche un effet dans la console (DEBUG)"""
        print("Effet etatRequis:"+self.etatRequisCibleDirect +
              " consommeEtat:"+str(self.consommeEtat) +
              " ciblesPossibles:"+str(self.ciblesPossibles) +
              " cibles_exclues:"+str(self.ciblesExclues))
