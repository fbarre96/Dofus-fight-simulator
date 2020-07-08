# -*- coding: utf-8 -*
"""@summary: Regroupe toutes les classes liées aux Sorts.
"""
from copy import deepcopy
from Effets.Effet import Effet
import random
import os
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
        self.lvl = int(lvl)
        self.coutPA = int(coutPA)
        self.POMin = int(POMin)
        self.POMax = int(POMax)
        self.effets = tableauEffets
        self.effetsCC = tableauEffetsCC
        self.POMod = int(POMod)
        self.typeLancer = typeLancer
        self.probaCC = int(probaCC)
        self.ldv = ldv
        nomImageSort = "images/"+constantes.normaliser(nom.lower())+".jpg"
        if os.path.isfile(nomImageSort):
            self.image = nomImageSort
        else:
            self.image = "images/undefined.jpg"
        self.hitbox = None
        self.chaine = kwargs.get("chaine", True)
        self.nbLancerParTour = int(nbLancerParTour)
        self.nbLancerParTourParJoueur = int(nbLancerParTourParJoueur)
        self.nbTourEntreDeux = int(nbTourEntreDeux)
        if self.nbTourEntreDeux > 0:
            self.nbLancerParTour = 1
            self.nbLancerParTourParJoueur = 1
        self.compteLancerParTour = 0
        self.compteLancerParTourParJoueur = {}
        self.compteTourEntreDeux = nbTourEntreDeux
        self.description = kwargs.get("description", "")
        self.lancableParJoueur = kwargs.get("lancableParJoueur", True)
        self.overlay = Overlays.Overlay(self, Overlays.ColoredText(
            "nom", (210, 105, 30)), Overlays.ColoredText(
                "description", (224, 238, 238)), (56, 56, 56))
    
    @classmethod
    def getCaracList(cls):
        return ["lvl", "coutPA", "POMin", "POMax", "POMod", "probaCC", "ldv", "nbTourEntreDeux"]

    def __deepcopy__(self, memo):
        toReturn = Sort(self.nom, self.lvl, self.coutPA, self.POMin, self.POMax,
                        self.effets, self.effetsCC, self.probaCC,
                        self.nbLancerParTour, self.nbLancerParTourParJoueur,
                        self.nbTourEntreDeux, self.POMod, self.typeLancer, self.ldv, lancableParJoueur=self.lancableParJoueur)
        toReturn.description = self.description
        toReturn.compteTourEntreDeux = self.compteTourEntreDeux
        toReturn.compteLancerParTourParJoueur = self.compteLancerParTourParJoueur
        toReturn.chaine = self.chaine
        toReturn.hitbox = self.hitbox
        toReturn.image = self.image
        return toReturn

    @classmethod
    def craftSort(cls, sortInfos):
        sortsLevels = []
        for i in range(1, 4):
            if str(i) not in sortInfos.keys():
                continue
            s = sortInfos[str(i)]
            tabEffets = []
            for effet in s["Effets"]:
                craftedEffet = Effet.effectFactory(effet)
                tabEffets.append(craftedEffet)
            tabEffetsCritiques = []
            for effet in s["EffetsCritiques"]:
                tabEffetsCritiques.append(Effet.effectFactory(effet))
            cc = int(s["Autres"]["Probabilit\u00e9 de coup critique"][:-1])
            if s["Autres"].get("Lancer en diagonale", "Non") == "Oui":
                typeLance = "diagonale"
            elif s["Autres"].get("Lancer en ligne", "Non") == "Oui":
                typeLance = "ligne"
            else:
                typeLance = "cercle"
            lvl = int(s["level"]) if s["level"] != "N/A" else 201
            newSort = Sort(
                    sortInfos["nom"], int(lvl), int(s["PA"]),\
                    int(s["PO_min"]), int(s["PO_max"]),\
                    tabEffets, tabEffetsCritiques,\
                    cc, int(s["Autres"].get("Nb. de lancers par tour", 1)),\
                    int(s["Autres"].get("Nb. de lancers par tour par joueur", 1)),\
                    int(s["Autres"].get("Nb. de tours entre deux lancers", 0)),\
                    int(1 if s["Autres"].get("Portée modifiable", "Non") == "Oui" else 0),\
                    typeLance, s["Autres"].get("Ligne de vue", "Non") == "Oui",\
                    desc=sortInfos["desc"],\
                    chaine=s["Autres"].get("Chaîné", "Oui") == "Oui",\
                    lancableParJoueur=sortInfos.get("lancableParJoueur", True)\
                )
            if sortInfos["nom"] == "Activation de Brume":
                print("debg")
            sortsLevels.append(newSort)
        return sortsLevels

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

    def testLancableParJoueur(self, joueurLanceur):
        """@summary: vérifie si les conditions de lancabilité du joueur. Sans cible
        """
        res, delaiRestant = self.testLancableDelai()
        if not res:
            return False, "Delai avant prochain lance:"+str(delaiRestant)
        res = self.testLancablePA(joueurLanceur)
        if not res:
            return False, "Pa insuffisant"
        res = self.testLancableCeTour()
        if not res:
            return False, "Ce sort ne peut plus etre utilise ce tour."
        return True, ""

    def estLancableSurCible(self, niveau, joueurLanceur, cibleX, cibleY):
        """@summary: vérifie si les conditions de lancabilité du joueur. Sans cible et avec cible
        """
        res, msg = self.testLancableParJoueur(joueurLanceur)
        if not res:
            return False, msg
        res = self.aPorte(joueurLanceur.posX, joueurLanceur.posY, cibleX, cibleY, joueurLanceur.PO)
        if not res:
            return False, "Pas la porté requise"
        joueurCible = niveau.getJoueurSur(cibleX, cibleY)
        if self.ldv and not self.aLigneDeVue(niveau, joueurLanceur.posX, joueurLanceur.posY,
                                             cibleX, cibleY):
            if joueurLanceur.checkLdv:
                return False, "Pas de ligne de vue."
        if joueurCible is not None:
            if not self.testLancableCeTourSurJoueur(joueurCible):
                return False, "Ce sort ne peut plus etre utilise sur ce personnage ce tour."
        res, msg = self.testLancableForEffets(joueurLanceur, joueurCible)
        if not res:
            return False, msg
        return True, ""

    def testLancablePA(self, lanceur):
        """@summary: Renvoie True si le cout en PA du sort est inférieur au nb de PA du lanceur
        """
        coutPA = self.coutPA
        if coutPA < 0:
            coutPA = 0
        return coutPA <= lanceur.PA

    def testLancableCeTour(self):
        """@summary: Renvoie True si le sort n'a pas atteint sa limite de lancer par tour
        """
        return self.compteLancerParTour < self.nbLancerParTour

    def testLancableCeTourSurJoueur(self, joueurCible):
        """@summary: Renvoie True si le sort n'a pas atteint sa limite de lancer par tour par joueur
        """
        if joueurCible is not None:
            if not joueurCible in self.compteLancerParTourParJoueur:
                self.compteLancerParTourParJoueur[joueurCible] = 0
            compte = self.compteLancerParTourParJoueur[joueurCible]
            return compte < self.nbLancerParTourParJoueur
        return True

    def testLancableDelai(self):
        """@summary: Renvoie True si le sort a dépassé son délai de cooldown
        """
        calcul = self.nbTourEntreDeux-self.compteTourEntreDeux
        res = calcul <= 0
        return res, calcul

    def testLancableForEffets(self, joueurLanceur, joueurCibleDirect):
        """@summary: Renvoie True si les effets du sort ont validé la cible.
        """
        raisons = []
        for effet in self.effets:
            msg, res = effet.estLancable(joueurLanceur, joueurCibleDirect)
            if not res:
                if self.chaine:
                    return False, "Un effet a échoué et le sort est chainé. Raison :"+str(msg)
                else:
                    raisons.append(msg)
            else:
                if not self.chaine:
                    return True, "Un effet a réussi et le sort n'est pas chainé"
        if self.chaine:
            return True, "Tous les effets ont réussi et le sort est chainé"
        return False, "Aucun effet n'a réussi et le sort n'est pas chainé. Raisons :"+str(msg)

    def marquerLancer(self, joueurCible):
        """@summary: compte le sort dans les lancers autorisés par tour.
        """
        self.compteLancerParTour += 1
        if joueurCible is not None:
            self.compteLancerParTourParJoueur[joueurCible] += 1
        self.compteTourEntreDeux = 0

    def lance(self, origineX, origineY, niveau, caseCibleX, caseCibleY,
              caraclanceur=None):
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
        isPrevisu = niveau.isPrevisu()
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
        if caraclanceur.porteurUid is not None:
            if niveau.tourDe.uid == caraclanceur.porteurUid:
                caraclanceur = niveau.getJoueurAvecUid(caraclanceur.porteurUid)
        elif caraclanceur.porteUid is not None:
            if niveau.tourDe.uid == caraclanceur.porteUid:
                caraclanceur = niveau.getJoueurAvecUid(caraclanceur.porteUid)

        if self.ldv and not self.aLigneDeVue(niveau, origineX, origineY, caseCibleX, caseCibleY):
            if caraclanceur.checkLdv and not isPrevisu:
                print("Pas de ligne de vue !")
                return niveau.joueurs
        # Get toutes les cases dans la zone d'effet
        joueurCible = niveau.getJoueurSur(caseCibleX, caseCibleY)
        # Test si la case est bien dans la portée du sort
        if self.aPorte(origineX, origineY, caseCibleX, caseCibleY, caraclanceur.PO):
            if not isPrevisu:
                print(caraclanceur.nomPerso+" lance :"+self.nom)
            # Test si le sort est lançable
            # (cout PA suffisant, délai et nombre d'utilisations par tour et par cible)
            res, explication = self.estLancableSurCible(niveau, caraclanceur,
                                                        caseCibleX, caseCibleY)
            if res:
                # Lancer du sort
                if not isPrevisu:
                    caraclanceur.PA -= self.coutPA
                    self.marquerLancer(joueurCible)
                    print(caraclanceur.nomPerso+": -"+str(self.coutPA) +
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
                    effet.setSort(self)
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
            if niveau.structure[cumulY][cumulX].type != "v" or \
                   niveau.getJoueurSur(cumulX, cumulY) is not None:
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
