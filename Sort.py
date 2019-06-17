# -*- coding: utf-8 -*
"""@summary: Regroupe toutes les classes liées aux Sorts.
"""
from copy import deepcopy

import random

import constantes
import Overlays


class Sort:
    """@summary: Décrit un sort.
    """

    def __init__(self, nom, lvl, coutPA, POMin, POMax, tableauEffets, tableauEffetsCC,
                 probaCC, nbLancerParTour, nbLancerParTourParJoueur, nbTourEntreDeux,
                 POMod, typeLancer, ldv, **kwargs):
        # pylint: disable=invalid-name
        self.nom = nom
        self.lvl = lvl
        self.coutPA = coutPA
        self.POMin = POMin
        self.POMax = POMax
        self.effets = tableauEffets
        self.effetsCC = tableauEffetsCC
        self.POMod = POMod
        self.typeLancer = typeLancer
        self.probaCC = probaCC
        self.ldv = ldv
        self.image = "images/"+constantes.normaliser(nom.lower())+".jpg"
        self.hitbox = None
        self.chaine = kwargs.get("chaine", True)
        self.nbLancerParTour = nbLancerParTour
        self.nbLancerParTourParJoueur = nbLancerParTourParJoueur
        self.nbTourEntreDeux = nbTourEntreDeux
        self.compteLancerParTour = 0
        self.compteLancerParTourParJoueur = {}
        self.compteTourEntreDeux = nbTourEntreDeux
        self.description = kwargs.get("description", "")
        self.overlay = Overlays.Overlay(self, Overlays.ColoredText(
            "nom", (210, 105, 30)), Overlays.ColoredText(
                "description", (224, 238, 238)), (56, 56, 56))

    def __deepcopy__(self, memo):
        toReturn = Sort(self.nom, self.lvl, self.coutPA, self.POMin, self.POMax,
                        self.effets, self.effetsCC, self.probaCC,
                        self.nbLancerParTour, self.nbLancerParTourParJoueur,
                        self.nbTourEntreDeux, self.POMod, self.typeLancer, self.ldv)
        toReturn.description = self.description
        toReturn.compteTourEntreDeux = self.compteTourEntreDeux
        toReturn.compteLancerParTourParJoueur = self.compteLancerParTourParJoueur
        toReturn.chaine = self.chaine
        toReturn.hitbox = self.hitbox
        toReturn.image = self.image
        return toReturn

    def aPorte(self, j1x, j1y, ciblex, cibley, PO):
        """@summary: calcul si le point j1 et a portée du point cible
                     avec la portée du sort + les PO du joueurs
                     si la portée du sort est modifiable uniquement.
        """
        # pylint: disable=invalid-name
        distanceX = abs(ciblex-j1x)
        distanceY = abs(cibley-j1y)
        distance = distanceX+distanceY
        sortPoMin = self.POMin
        sortPoMax = self.POMax+(self.POMod*PO)
        if self.typeLancer == "ligne":
            if distanceX > 0 and distanceY > 0:
                return False
        elif self.typeLancer == "diagonale":
            if distanceY != distanceX:
                return False
            sortPoMin *= 2
            sortPoMax *= 2
        return sortPoMin <= distance <= sortPoMax

    def estLancable(self, joueurLanceur, joueurCible):
        """@summary: vérifie si le sort est lancable
                     et vérifie si chaque effet est lancable
        """
        res, msg, coutPA = self.sortEstLancable(joueurCible)
        if not res:
            return res, msg, coutPA
        for effet in self.effets:
            res, msg = effet.estLancable(joueurLanceur, joueurCible)
            if not res:
                return res, msg, coutPA
        return True, msg, coutPA

    def sortEstLancable(self, joueurCible):
        """@vérifie si le sort est lancable sur la cible.
                     check cout en PA et les limites de lancer par tour
        """
        coutPA = self.coutPA
        if self.compteTourEntreDeux >= self.nbTourEntreDeux:
            if self.compteLancerParTour < self.nbLancerParTour:
                if joueurCible is not None:
                    if not joueurCible in self.compteLancerParTourParJoueur:
                        self.compteLancerParTourParJoueur[joueurCible] = 0
                    compte = self.compteLancerParTourParJoueur[joueurCible]
                    if compte < self.nbLancerParTourParJoueur:
                        return True, "", coutPA
                    return False, "Ce sort ne peut plus etre utilise sur ce personnage ce tour.", 0
                return True, "", coutPA
            return False, "Ce sort ne peut plus etre utilise ce tour.", 0
        msg = "Delai avant prochain lance:"+str(self.nbTourEntreDeux-self.compteTourEntreDeux)
        return False, msg, 0

    def marquerLancer(self, joueurCible):
        """@summary: compte le sort dans les lancers autorisés par tour.
        """
        self.compteLancerParTour += 1
        if joueurCible is not None:
            self.compteLancerParTourParJoueur[joueurCible] += 1
        self.compteTourEntreDeux = 0

    def lance(self, origineX, origineY, niveau, caseCibleX, caseCibleY,
              caraclanceur=None, isPrevisu=False):
        """@summary: Lance un sort
        @origineX: la pos x d'où est lancé le sort
        @type: int
        @origineY: la pos y d'où est lancé le sort
        @type: int
        @niveau: La grille de jeu
        @type: Niveau
        @caseCibleX: La coordonnée x de la case cible du sort
        @type: int
        @caseCibleY: La coordonnée y de la case cible du sort
        @type: int
        @caraclanceur: le personnage dont les caractéristiques doivent être prise
        pour infliger les dégâts de sort. Optionnel : self est pris à la place
        @type: Personnage (ou None pour prendre le lanceur)"""
        caseCibleX = int(caseCibleX)
        caseCibleY = int(caseCibleY)
        if self.ldv and not self.aLigneDeVue(niveau, origineX, origineY, caseCibleX, caseCibleY):
            print("Pas de ligne de vue !")
            return niveau.joueurs
        saveLanceur = None
        if isPrevisu:
            save = niveau
            niveau = deepcopy(niveau)
            if caraclanceur is not None:
                saveLanceur = caraclanceur
                for joueur in niveau.joueurs:
                    if joueur.uid == caraclanceur.uid:
                        caraclanceur = joueur

        caraclanceur = caraclanceur if caraclanceur is not None else niveau.getJoueurSur(
            origineX, origineY)
        # Get toutes les cases dans la zone d'effet
        joueurCible = niveau.getJoueurSur(caseCibleX, caseCibleY)
        # Test si la case est bien dans la portée du sort
        if self.aPorte(origineX, origineY, caseCibleX, caseCibleY, caraclanceur.PO):
            if not isPrevisu:
                print(caraclanceur.nomPerso+" lance :"+self.nom)
            # Test si le sort est lançable
            # (cout PA suffisant, délai et nombre d'utilisations par tour et par cible)
            res, explication, coutPA = self.estLancable(caraclanceur, joueurCible)
            if res:
                # Lancer du sort
                if not isPrevisu:
                    caraclanceur.PA -= coutPA
                    self.marquerLancer(joueurCible)
                    print(caraclanceur.nomPerso+": -"+str(coutPA) +
                          " PA (reste "+str(caraclanceur.PA)+"PA)")
                chanceCC = caraclanceur.cc + self.probaCC
                randomVal = round(random.random(), 2)
                isCC = False
                if self.probaCC != 0 and not isPrevisu:
                    isCC = (randomVal*100 <= chanceCC)

                if isCC and not isPrevisu:  # TOFIX : PREVISUALISATION IMPOSSIBLE POUR CC
                    print("Coup Critique !")
                    effetsSort = self.effetsCC
                else:
                    effetsSort = self.effets
                sestApplique = True
                # Application des effets
                for effet in effetsSort:
                    effet.setCritique(isCC)
                    effet.setPrevisu(isPrevisu)
                    # Test si les effets sont dépendants les uns à la suite des autres
                    if self.chaine:
                        if sestApplique:  # Si l'effet a été appliqué, on continue
                            sestApplique, _ = niveau.lancerEffet(
                                effet, origineX, origineY, self.nom,
                                caseCibleX, caseCibleY, caraclanceur)
                    else:
                        sestApplique, _ = niveau.lancerEffet(
                            effet, origineX, origineY, self.nom, caseCibleX,
                            caseCibleY, caraclanceur)
                    # Apres application d'un effet sur toutes les cibles:
            else:
                if not isPrevisu:
                    print(explication)
        else:
            if not isPrevisu:
                print("Cible hors de porte")
        niveau.depileEffets()
        toReturn = None
        if isPrevisu:
            toReturn = deepcopy(niveau.joueurs)
            del niveau
            niveau = save
            if saveLanceur is not None:
                caraclanceur = saveLanceur
        #  réaffiche les sorts pour marquer les sorts qui ne sont plus utilisables
        niveau.afficherSorts()
        return toReturn

    def aLigneDeVue(self, niveau, posX0, posY0, posX1, posY1):
        """@summary: calcul si la pos 0 à la la lidgne de vue sur la pos 1
           @return: booléen
        """
        ldv = True
        distanceX = abs(posX1 - posX0)
        distanceY = abs(posY1 - posY0)
        cumulX = posX0
        cumulY = posY0
        cumulN = -1 + distanceX + distanceY
        xInc = 1 if posX1 > posX0 else -1
        yInc = 1 if posY1 > posY0 else -1
        error = distanceX - distanceY
        distanceX *= 2
        distanceY *= 2

        if error > 0:
            cumulX += xInc
            error -= distanceY
        elif error < 0:
            cumulY += yInc
            error += distanceX
        else:
            cumulX += xInc
            error -= distanceY
            cumulY += yInc
            error += distanceX
            cumulN -= 1

        while cumulN > 0 and ldv:
            if niveau.structure[cumulY][cumulX].type != "v":
                ldv = False
            else:
                if error > 0:
                    cumulX += xInc
                    error -= distanceY
                elif error < 0:
                    cumulY += yInc
                    error += distanceX
                else:
                    cumulX += xInc
                    error -= distanceY
                    cumulY += yInc
                    error += distanceX
                    cumulN -= 1
                cumulN -= 1
        return ldv
