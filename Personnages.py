# -*- coding: utf-8 -*
import Sort as Sort
import Zones as Zones
import Etats as Etats
from Effets.EffetInvoque import EffetInvoque
import constantes
import Overlays
import pygame
from pygame.locals import *
import json
from copy import deepcopy
import copy
import uuid



class Personnage(object):
    """@summary: Classe décrivant un personnage joueur de dofus."""

    def __init__(self, nomPerso, classe, lvl, team, caracsPrimaires, caracsSecondaires, dommages, resistances, icone=""):
        """@summary: Initialise un personnage.
        @classe: la classe du personnage (les 18 classes de Dofus). Pour l'instant sert d'identifiant étant donné que 1v1 vs Poutch.
        @type: string
        @lvl: le niveau du personnage
        @type: int
        @team: le numéro d'équipe du personnage
        @type: int
        @caracsPrimaires: les caractéristiques primaires du perso (PA, PM, PO, vita, agi, chance, force, intel, pui, cc, sasa)
        @type: dict
        @caracsSecondaires: les caractéristiques secondaires du perso (RetPA, esquive pa, ret pm, esq pm, soins, tacle, fuite, ini, invocations, prospection)
        @type: dict
        @dommages: les dommages du perso (do, do cri, do neutre, do terre, do feu, do eau, do air, renvoi, maitrise d'arme, pièges (fixe), pièges(puissance), poussée, Sorts, Arme, Distance, Mêlée)
        @type: dict
        @dommages: les résistances du perso (ré neutre, re per neutre, ré terre, ré per terre, ré feu, ré per feu, ré eau, ré per eau, ré air, ré per air, ré cc fixe, ré pou fixe, ré distance, ré mêlée)
        @type: dict
        @icone: le chemin de l'image pour afficher l'icône du personnage
        @type: string (nom de l'image. L'image doit faire moins de 30x30 pixels, se situer dans /image et porté le même nom que la classe une fois normalisé)
        """
        self.PA = int(caracsPrimaires.get("PA", 0))
        self.PM = int(caracsPrimaires.get("PM", 0))
        self.PO = int(caracsPrimaires.get("PO", 0))
        self.vie = int(caracsPrimaires.get("Vitalite", 1))
        self.agi = int(caracsPrimaires.get("Agilite", 0))
        self.cha = int(caracsPrimaires.get("Chance", 0))
        self.fo = int(caracsPrimaires.get("Force", 0))
        self.int = int(caracsPrimaires.get("Intelligence", 0))
        self.pui = int(caracsPrimaires.get("Puissance", 0))
        self.cc = int(caracsPrimaires.get("Coups Critiques", 0))
        # Aucune utilité dans le simulateur de combat
        self.sagesse = int(caracsPrimaires.get("Sagesse", 0))
        self.caracsPrimaires = caracsPrimaires

        self.retPA = int(caracsSecondaires.get("Retrait PA", 0))
        self.esqPA = int(caracsSecondaires.get("Esquive PA", 0))
        self.retPM = int(caracsSecondaires.get("Retrait PM", 0))
        self.esqPM = int(caracsSecondaires.get("Esquive PM", 0))
        self.soins = int(caracsSecondaires.get("Soins", 0))
        self.tacle = int(caracsSecondaires.get("Tacle", 0))
        self.fuite = int(caracsSecondaires.get("Fuite", 0))
        self.ini = int(caracsSecondaires.get("Initiative", 0))
        self.invocationLimite = int(caracsSecondaires.get("Invocation", 1))
        # Aucune utilité dans le simulateur de combat
        self.prospection = int(caracsSecondaires.get("Prospection", 0))
        self.caracsSecondaires = caracsSecondaires

        self.do = int(dommages.get("Dommages", 0))
        self.doCri = int(dommages.get("Dommages critiques", 0))
        self.doNeutre = int(dommages.get("Neutre", 0))
        self.doTerre = int(dommages.get("Terre", 0))
        self.doFeu = int(dommages.get("Feu", 0))
        self.doEau = int(dommages.get("Eau", 0))
        self.doAir = int(dommages.get("Air", 0))
        self.doRenvoi = int(dommages.get("Renvoi", 0))
        self.doMaitriseArme = int(dommages.get("Maitrise d'arme", 0))  # TODO
        self.doPieges = int(dommages.get("Pieges", 0))
        self.doPiegesPui = int(dommages.get("Pieges Puissance", 0))
        self.doPou = int(dommages.get("Poussee", 0))
        self.doSorts = int(dommages.get("Sorts", 0))
        self.doArmes = int(dommages.get("Armes", 0))
        self.doDist = int(dommages.get("Distance", 0))
        self.doMelee = int(dommages.get("Melee", 0))
        self.dommages = dommages

        self.reNeutre = int(resistances.get("Neutre", 0))
        self.rePerNeutre = int(resistances.get("Neutre%", 0))
        self.reTerre = int(resistances.get("Terre", 0))
        self.rePerTerre = int(resistances.get("Terre%", 0))
        self.reFeu = int(resistances.get("Feu", 0))
        self.rePerFeu = int(resistances.get("Feu%", 0))
        self.reEau = int(resistances.get("Eau", 0))
        self.rePerEau = int(resistances.get("Eau%", 0))
        self.reAir = int(resistances.get("Air", 0))
        self.rePerAir = int(resistances.get("Air%", 0))
        self.reCc = int(resistances.get("Coups critiques", 0))
        self.rePou = int(resistances.get("Poussee", 0))
        self.reDist = int(resistances.get("Distance", 0))
        self.reMelee = int(resistances.get("Melee", 0))
        self.resistances = resistances

        self._vie = self.vie
        self._PM = int(self.PM)
        self._PA = int(self.PA)
        self.nomPerso = nomPerso
        self.erosion = 10  # Erosion de base
        self.lvl = int(lvl)
        self.classe = classe
        self.uid = uuid.uuid4()
        self.sortsDebutCombat = []
        self.sorts, self.sortsDebutCombat = Personnage.ChargerSorts(
            self.classe, self.lvl)  # la liste des sorts du personnage
        self.posX = 0                                     # Sa position X sur la carte
        self.posY = 0                                     # Sa position Y sur la carte
        # La liste des états affectant le personange
        self.etats = []
        # Les déplacements effectués par le personnage dans ses 2 derniers tours
        self.historiqueDeplacement = []
        self.posDebTour = None
        self.posDebCombat = None
        self.invocateur = None
        self.invocations = []
        self.overlayTexte = ""
        self.team = int(team)

        self.msgsPrevisu = []

        if not(icone.startswith("images/")):
            self.icone = ("images/"+icone)
        else:
            self.icone = (icone)
        self.icone = constantes.normaliser(self.icone)
        # Overlay affichange le nom de classe et sa vie restante
        self.overlay = Overlays.Overlay(self, Overlays.ColoredText(
            "nomPerso", (210, 105, 30)), Overlays.ColoredText("overlayTexte", (224, 238, 238)), (56, 56, 56))

    def __deepcopy__(self, memo):
        toReturn = Personnage(self.nomPerso, self.classe, self.lvl, self.team,
                              {"PA": self.PA, "PM": self.PM, "PO": self.PO, "Vitalite": self.vie, "Agilite": self.agi, "Chance": self.cha,
                                  "Force": self.fo, "Intelligence": self.int, "Puissance": self.pui, "Coups Critiques": self.cc, "Sagesse": self.sagesse},
                              {"Retrait PA": self.retPA, "Esquive PA": self.esqPA, "Retrait PM": self.retPM, "Esquive PM": self.esqPM, "Soins": self.soins,
                               "Tacle": self.tacle, "Fuite": self.fuite, "Initiative": self.ini, "Invocation": self.invocationLimite, "Prospection": self.prospection},
                              {"Dommages": self.do, "Dommages critiques": self.doCri, "Neutre": self.doNeutre, "Terre": self.doTerre, "Feu": self.doFeu, "Eau": self.doEau, "Air": self.doAir, "Renvoi": self.doRenvoi,
                                  "Maitrise d'arme": self.doMaitriseArme, "Pieges": self.doPieges, "Pieges Puissance": self.doPiegesPui, "Poussee": self.doPou, "Sorts": self.doSorts, "Armes": self.doArmes, "Distance": self.doDist, "Melee": self.doMelee},
                              {"Neutre": self.reNeutre, "Neutre%": self.rePerNeutre, "Terre": self.reTerre, "Terre%": self.rePerTerre, "Feu": self.reFeu, "Feu%": self.rePerFeu, "Eau": self.reEau,
                               "Eau%": self.rePerEau, "Air": self.reAir, "Air%": self.rePerAir, "Coups critiques": self.reCc, "Poussee": self.rePou, "Distance": self.reDist, "Melee": self.reMelee},
                              self.icone)
        toReturn.sortsDebutCombat = self.sortsDebutCombat
        toReturn.posX = self.posX
        toReturn.posY = self.posY
        toReturn._PA = self._PA
        toReturn._PM = self._PM
        toReturn._vie = self._vie
        toReturn.uid = self.uid
        toReturn.sorts = deepcopy(self.sorts)
        toReturn.sortsDebutCombat = deepcopy(self.sortsDebutCombat)
        toReturn.etats = deepcopy(self.etats)
        toReturn.historiqueDeplacement = deepcopy(self.historiqueDeplacement)
        toReturn.posDebTour = self.posDebTour
        toReturn.posDebCombat = self.posDebCombat
        toReturn.invocateur = self.invocateur
        toReturn.invocations = deepcopy(self.invocations)
        toReturn.invocationLimite = self.invocationLimite
        toReturn.msgsPrevisu = deepcopy(self.msgsPrevisu)
        return toReturn

    def setOverlayText(self):
        self.overlayTexte = str(self.vie) + " PV"
        boubou = self.getBoucliers()
        if boubou > 0:
            self.overlayTexte += " "+str(boubou)+" PB"

    def setOverlayTextGenerique(self, text):
        self.overlayTexte = text

    def aEtatsRequis(self, etatsRequis):
        """@summary: Indique si le personnage possède les états donnés en paramètres.
        @etatsRequis: la liste des états à tester. si un ! se situe au début de la chaîne, il faut que l'état soit absent.
        @type: tableau de strings (noms d'états préfixé éventuellement par "!")


        @return: booléen valant True si tous les états requis sont sur le personnage, False sinon."""
        for checkEtat in etatsRequis:
            if checkEtat.strip() != "":
                # calcul du nom de l'état requis
                if checkEtat.startswith("!"):
                    etatRequis = checkEtat[1:]
                else:
                    etatRequis = checkEtat
                # Est-ce que le personnage possede l'état requis
                aEtat = self.aEtat(etatRequis)
                # Si test l'absence qu'on l'a ou si on test la présence et qu'on ne l'a pas
                if (checkEtat.startswith("!") and aEtat) or (not checkEtat.startswith("!") and not aEtat):
                    # print "DEBUG : la cibleDirect n'a pas ou a l'etat requis :"+str(checkEtat)
                    return False
        return True

    @staticmethod
    def getSortRightLvl(lvl, tab_sorts):
        closest_lvl_sort = None
        for sort in tab_sorts[0:]:
            if sort.lvl <= lvl:
                if closest_lvl_sort is not None:
                    if closest_lvl_sort.lvl < sort.lvl:
                        closest_lvl_sort = sort
                else:
                    closest_lvl_sort = sort
        return closest_lvl_sort

    @staticmethod
    def ChargerSorts(classe, lvl):
        """@summary: Méthode statique qui initialise les sorts du personnage selon sa classe.
        @classe: le nom de classe dont on souhaite récupérer les sorts
        @type: string

        @return: tableau de Sort"""
        sorts = []
        sortsDebutCombat = []
        if(classe == "Stratege Iop"):
            import Sorts.StrategeIop
            sortsDebutCombat += Sorts.StrategeIop.getSortsDebutCombat(lvl)
            sorts += Sorts.StrategeIop.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif(classe == "Cadran de Xelor"):
            import Sorts.CadranDeXelor
            sortsDebutCombat += Sorts.CadranDeXelor.getSortsDebutCombat(lvl)
            sorts += Sorts.CadranDeXelor.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif(classe == "Balise de Rappel"):
            import Sorts.BaliseDeRappel
            sortsDebutCombat += Sorts.BaliseDeRappel.getSortsDebutCombat(lvl)
            sorts += Sorts.BaliseDeRappel.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif classe == "Poutch":
            return sorts, sortsDebutCombat
        elif classe == "Synchro":
            import Sorts.Synchro
            sortsDebutCombat += Sorts.Synchro.getSortsDebutCombat(lvl)
            sorts += Sorts.Synchro.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif(classe == "Xelor"):
            import Sorts.Xelor
            sortsDebutCombat += Sorts.Xelor.getSortsDebutCombat(lvl)
            sorts += Sorts.Xelor.getSorts(lvl)
        elif(classe == "Iop"):
            import Sorts.Iop
            sortsDebutCombat += Sorts.Iop.getSortsDebutCombat(lvl)
            sorts += Sorts.Iop.getSorts(lvl)
        elif classe == "Cra":
            import Sorts.Cra
            sortsDebutCombat += Sorts.Cra.getSortsDebutCombat(lvl)
            sorts += Sorts.Cra.getSorts(lvl)
        elif classe == "Sram":
            import Sorts.Sram
            sortsDebutCombat += Sorts.Sram.getSortsDebutCombat(lvl)
            sorts += Sorts.Sram.getSorts(lvl)
        sorts.append(Sort.Sort("Cawotte",0,4,1,6,[EffetInvoque("Cawotte",False,cibles_possibles="", cible_requise=True)],[],0, 1,1,6,0,"cercle",True,description="Invoque une Cawotte")) 
        total_nb_sorts = len(sorts)
        i = 0
        while i < total_nb_sorts:
            if sorts[i] is None:
                sorts.remove(sorts[i])
                total_nb_sorts -= 1
                i -= 1
            i += 1
        return sorts, sortsDebutCombat

    def LancerSortsDebutCombat(self, niveau):
        for sort in self.sortsDebutCombat:
            sort.lance(self.posX, self.posY, niveau, self.posX, self.posY)

    def ajoutHistoriqueDeplacement(self, posX=None, posY=None):
        if posX is None:
            posX = self.posX
        if posY is None:
            posY = self.posY
        self.historiqueDeplacement.append([posX, posY, 2])

    def bouge(self, niveau, x, y, ajouteHistorique=True, canSwap=False):
        """@summary: téléporte le joueur sur la carte et stock le déplacement dans l'historique de déplacement.
        @x: la position d'arrivée en x.
        @type: int
        @x: la position d'arrivée en y.
        @type: int"""
        # test si la case d'arrivé est hors-map (compte comme un obstacle)
        if x >= niveau.taille or x < 0 or y >= niveau.taille or y < 0:
            return False, False
        elif niveau.structure[y][x].type != "v":
            return False, False
        if ajouteHistorique:
            self.ajoutHistoriqueDeplacement()
        niveau.structure[self.posY][self.posX].type = "v"
        niveau.structure[y][x].type = "j"
        self.posX = x
        self.posY = y

        nbPieges = len(niveau.pieges)
        i = 0
        piegeDeclenche = False
        # Priorité au nouveau piège:
        sauvegardeFile = niveau.fileEffets[:]
        niveau.fileEffets = []
        while i < nbPieges:
            piege = niveau.pieges[i]
            if piege.aPorteDeclenchement(x, y):
                piegeDeclenche = True
                for joueur in niveau.joueurs:
                    for etat in joueur.etats:
                        if etat.actif():
                            etat.triggerAvantPiegeDeclenche(
                                niveau, piege, self, joueur)

                for effet in piege.effets:
                    sestApplique, cibles = niveau.lancerEffet(
                        effet, piege.centre_x, piege.centre_y, piege.nomSort, piege.centre_x, piege.centre_y, piege.lanceur)
                i -= 1
                niveau.pieges.remove(piege)
            i += 1
            nbPieges = len(niveau.pieges)
        # Verifie les entrées et sorties de glyphes:
        for glyphe in niveau.glyphes:
            if glyphe.actif():
                # Test Entre dans la glyphe
                if glyphe.sortDeplacement.APorte(glyphe.centre_x, glyphe.centre_y, self.posX, self.posY, 0):
                    for effet in glyphe.sortDeplacement.effets:
                        niveau.lancerEffet(effet, glyphe.centre_x, glyphe.centre_y,
                                           glyphe.nomSort, self.posX, self.posY, glyphe.lanceur)
                else:  # n'est pas dans la glyphe
                    dernierePos = self.historiqueDeplacement[-1]
                    # Test s'il était dans la glyphe avant

                    if glyphe.sortDeplacement.APorte(glyphe.centre_x, glyphe.centre_y, dernierePos[0], dernierePos[1], 0):
                        for effet in glyphe.sortSortie.effets:
                            niveau.lancerEffet(
                                effet, glyphe.centre_x, glyphe.centre_y, glyphe.nomSort, self.posX, self.posY, glyphe.lanceur)
        niveau.fileEffets = niveau.fileEffets + sauvegardeFile
        niveau.depileEffets()
        return True, piegeDeclenche

    def echangePosition(self, niveau, joueurCible, ajouteHistorique=True):
        """@summary: téléporte le joueur sur la carte et stock le déplacement dans l'historique de déplacement.
        @x: la position d'arrivée en x.
        @type: int
        @x: la position d'arrivée en y.
        @type: int"""
        # test si la case d'arrivé est hors-map (compte comme un obstacle)
        if niveau.structure[joueurCible.posY][joueurCible.posX].type != "j":
            print("DEBUG : THIS SHOULD NOT BE POSSIBLE")
            return False, False
        if ajouteHistorique:
            self.ajoutHistoriqueDeplacement()
        joueurCible.ajoutHistoriqueDeplacement()
        x = self.posX
        y = self.posY
        self.posX = joueurCible.posX
        self.posY = joueurCible.posY
        joueurCible.posX = x
        joueurCible.posY = y
        nbPieges = len(niveau.pieges)
        i = 0
        piegeDeclenche = False
        # Priorité au nouveau piège:
        sauvegardeFile = niveau.fileEffets[:]
        niveau.fileEffets = []
        while i < nbPieges:
            piege = niveau.pieges[i]
            if piege.aPorteDeclenchement(x, y):
                piegeDeclenche = True
                for effet in piege.effets:
                    niveau.pieges.remove(piege)
                    i -= 1
                    sestApplique, cibles = niveau.lancerEffet(
                        effet, piege.centre_x, piege.centre_y, piege.nomSort, piege.centre_x, piege.centre_y, piege.lanceur)
            i += 1
            nbPieges = len(niveau.pieges)
        niveau.fileEffets = niveau.fileEffets + sauvegardeFile
        niveau.depileEffets()
        return True, piegeDeclenche

    def rafraichirHistoriqueDeplacement(self):
        """@summary: supprime les déplacements plus vieux que 2 tours"""
        i = 0
        longueurListe = len(self.historiqueDeplacement)
        while i < longueurListe:
            self.historiqueDeplacement[i][2] -= 1
            if self.historiqueDeplacement[i][2] == 0:
                del self.historiqueDeplacement[i]
                i -= 1
            i += 1
            longueurListe = len(self.historiqueDeplacement)

    def tpPosPrec(self, nb, niveau, lanceur, nomSort):
        """@summary: Téléporte le personnage à sa dernière position dans l'historique de déplacement.
        @nb: Le nombre de retour en arrière à effectuer
        @type: int
        @niveau: la grille de jeu
        @type: Niveau
        @lanceur: le personnage à l'origine de cette action
        @type: Personnage
        @nomSort: le nom du sort à l'orginie de cette action
        @type: string"""
        for i in range(nb):
            if(len(self.historiqueDeplacement) > 0):
                pos = self.historiqueDeplacement[-1]
                del self.historiqueDeplacement[-1]
                niveau.gereDeplacementTF(
                    self, pos, lanceur, nomSort, AjouteHistorique=False)

    def aEtat(self, nomEtatCherche):
        """@summary: Indique si un personnage possède l'état donné
        @nomEtatCherche: Le nom de l'état cherché
        @type: string

        @return: booléen valant True si le personnage possède l'état , False sinon"""
        for etat in self.etats:
            if etat.nom == nomEtatCherche:
                return True
        return False

    def retirerEtats(self, nomsEtatCherche):
        """@summary: retire les états donné en paramètres
        @nomsEtatCherche: Les noms des états cherchés à supprimer
        @type: tableau de string"""
        i = 0
        nbEtats = len(self.etats)
        while i < nbEtats:
            if self.etats[i].nom in nomsEtatCherche:
                # Appliquer les fin de bonus et malus des do, pm, pa, po, pui et carac ici
                print(self.nomPerso+" sort de l'etat "+self.etats[i].nom)
                self.etats[i].triggerAvantRetrait(self)
                del self.etats[i]
                i -= 1
                nbEtats = len(self.etats)
            i += 1

    def getBoucliers(self):
        pb_restants = 0
        for etat in self.etats:
            if etat.actif():
                if isinstance(etat, Etats.EtatBouclierPerLvl):
                    pb_restants += etat.boostBouclier

        return pb_restants

    def soigne(self, soigneur, niveau, soins, shouldprint=True):
        """@summary: subit des dégâts de combats. Active les triggers d'états triggerAvantSubirDegats et triggerApresSubirDegats
        @soigneur: Le joueur soignant
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau
        @soins: Le nombre de points de soins calculés
        @type: int
        """
        self.vie += soins
        if shouldprint:
            print("+"+str(soins)+" PV")

    def subit(self, attaquant, niveau, degats, typeDegats, shouldprint=True):
        """@summary: subit des dégâts de combats. Active les triggers d'états triggerAvantSubirDegats et triggerApresSubirDegats
        @attaquant: Le joueur attaquant
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau
        @degats: Le nombre de points de dégâts calculés par l'attaquant
        @type: int
        @typeDegats: Le type de dégâts à subir
        @type: string (feu , air, terre, eau, doPou)"""
        totalPerdu = degats
        for etat in self.etats:
            if etat.actif():
                etat.triggerAvantSubirDegats(
                    self, niveau, totalPerdu, typeDegats, attaquant)

        pb_restants = 0
        for etat in self.etats:
            if etat.actif():
                if isinstance(etat, Etats.EtatBouclierPerLvl):
                    bouclierPrend = etat.boostBouclier - degats
                    if bouclierPrend > etat.boostBouclier:
                        degats -= etat.boostBouclier
                        etat.boostBouclier = 0
                        del etat
                    else:
                        etat.boostBouclier -= degats
                        degats = 0
                        pb_restants += etat.boostBouclier
        vieAEnlever = degats
        if self.vie - vieAEnlever < 0:
            vieAEnlever = self.vie

        self.vie -= vieAEnlever
        erosion = self.erosion
        if erosion > 50:  # L'érosion est capé à 50% dans le jeu
            erosion = 50
        elif erosion < 10:  # L'érosion est capé mini à 10% dans le jeu
            erosion = 10
        self._vie -= int(totalPerdu * (erosion/100))
        if self._vie < 0:
            self._vie = 0
        if self.vie > self._vie:
            self.vie = self._vie
        toprint = ""
        toprint = self.nomPerso+" a "+str(self.vie) + "/"+str(self._vie)+" PV"
        if pb_restants > 0:
            toprint += " et "+str(pb_restants)+" PB"
        if shouldprint:
            print("-"+str(totalPerdu)+" PV")
            print(toprint)
        if self.vie <= 0:
            niveau.tue(self)
        for etat in self.etats:
            if etat.actif():
                etat.triggerApresSubirDegats(
                    self, niveau, attaquant, totalPerdu)

    def finTour(self, niveau):
        """@summary: Termine le tour du personnage, récupération des PA et PM, sorts utilisés, activation du trigger d'état triggerFinTour
        @niveau: La grille de jeu
        @type: Niveau"""
        self.PM = self._PM
        self.PA = self._PA
        for sort in self.sorts:
            sort.compteLancerParTour = 0
            sort.compteTourEntreDeux += 1
            sort.compteLancerParTourParJoueur = {}
        for etat in self.etats:
            if etat.actif():
                etat.triggerFinTour(self, niveau)

    def debutTour(self, niveau):
        """@summary: Débute le tour du personnage, déclenche glyphe, rafraîchit les états, les glyphes et l'historique de déplacement.
        @niveau: La grille de jeu
        @type: Niveau"""
        for glyphe in niveau.glyphes:
            if glyphe.actif():
                if glyphe.sortMono.APorte(glyphe.centre_x, glyphe.centre_y, self.posX, self.posY, 0):
                    for effet in glyphe.sortMono.effets:
                        niveau.lancerEffet(effet, glyphe.centre_x, glyphe.centre_y,
                                           glyphe.nomSort, self.posX, self.posY, glyphe.lanceur)
        niveau.rafraichirEtats(self)
        niveau.rafraichirGlyphes(self)
        niveau.rafraichirRunes(self)
        self.rafraichirHistoriqueDeplacement()
        for etat in self.etats:
            if etat.actif():
                etat.triggerDebutTour(self, niveau)

        self.posDebTour = [self.posX, self.posY]
        niveau.depileEffets()
        niveau.afficherSorts()
        print("Debut de tour de "+str(self.nomPerso)+".")
        print("PA : "+str(self.PA))
        print("PM : "+str(self.PM))
        print("PV : "+str(self.vie))

    def appliquerEtat(self, etat, lanceur, cumulMax=-1, niveau=None):
        """@summary: Applique un nouvel état sur le Personnage. Active le trigger d'état triggerInstantane
        @etat: l'état qui va être appliqué
        @type: Etat
        @lanceur: le lanceur de l'état
        @type: Personnage
        @niveau: La grille de jeu (optionnel)
        @type: Niveau"""
        if cumulMax != -1:
            count = 0
            for etatJoueur in self.etats:
                if etat.nom == etatJoueur.nom:
                    count += 1
            if count >= cumulMax:
                print("DEBUG : Cumul max atteint pour l'état "+etat.nom)
                return False
        print(self.nomPerso+"  etat "+etat.nom+" ("+str(etat.duree)+" tours)")
        etat.lanceur = lanceur
        self.etats.append(etat)
        if self.etats[-1].actif():
            self.etats[-1].triggerInstantane(lanceur=lanceur,
                                             niveau=niveau, joueurCaseEffet=self)

    def changeDureeEffets(self, n, niveau):
        """@summary: Réduit la durée des états sur le personnage
        @n: le nombre de tours d'état réduit
        @type: int
        @niveau: La grille de jeu
        @type: Niveau"""
        for i in range(abs(n)):
            niveau.rafraichirEtats(self, False)

    def selectionSort(self, sort, niveau):
        sortSelectionne = None
        coutPA = sort.getCoutPA(self)
        if coutPA < 0:
            coutPA = 0
        if (coutPA <= niveau.tourDe.PA):
            res, explication, coutPA = sort.estLancable(
                niveau, niveau.tourDe, None)
            if res == True:
                sortSelectionne = sort
            else:
                print(explication)

        else:
            print("PA insuffisant : coute "+str(coutPA) +
                  " mais "+str(niveau.tourDe.PA) + " restant.")
        return sortSelectionne

    def joue(self, event, niveau, mouse_xy, sortSelectionne):
        """@summary: Fonction appelé par la boucle principale pour demandé à un Personnage d'effectuer ses actions.
                     Dans la classe Personnage, c'est contrôle par utilisateur clavier/souris.
        @event: les évenements pygames survenus
        @type: Event pygame
        @niveau: La grille de jeu
        @type: Niveau
        @mouse_xy: Les coordonnées de la souris
        @type: int
        @sortSelectionne: Le sort sélectionné plus tôt dans la partie s'il y en a un
        @type: Sort

        @return: Le nouveau sortSelectionne éventuel"""

        # Clic souris
        if event.type == pygame.KEYDOWN:
            if event.key == K_F1:  # touche F1 = fin du tour
                sortSelectionne = None
                niveau.finTour()
            if event.key == K_ESCAPE:  # touche échap = déselection de sort.
                sortSelectionne = None
            if event.key >= K_1 and event.key <= K_9:
                aLance = niveau.tourDe.sorts[event.key - K_1]
                sortSelectionne = self.selectionSort(aLance, niveau)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicGauche, clicMilieu, clicDroit = pygame.mouse.get_pressed()
            # Clic gauche
            if clicGauche:
                # Clic gauche sort = tentative de sélection de sort
                if mouse_xy[1] > constantes.y_sorts:
                    for sort in niveau.tourDe.sorts:
                        if sort.vue.isMouseOver(mouse_xy):
                            sortSelectionne = self.selectionSort(sort, niveau)
                            break
                # Clic gauche grille de jeu = tentative de lancé un sort si un sort est selectionné ou tentative de déplacement sinon
                else:
                    # Un sort est selectionne
                    if sortSelectionne != None:
                        case_cible_x = int(
                            mouse_xy[0]/constantes.taille_sprite)
                        case_cible_y = int(
                            mouse_xy[1]/constantes.taille_sprite)
                        sortSelectionne.lance(
                            niveau.tourDe.posX, niveau.tourDe.posY, niveau, case_cible_x, case_cible_y)
                        sortSelectionne = None
                    # Aucun sort n'est selectionne: on pm
                    else:
                        niveau.Deplacement(mouse_xy)
            # Clic droit
            elif clicDroit:
                # Clic droit grille de jeu = affichage détaillé de l'état d'un personnage.
                if mouse_xy[1] < constantes.y_sorts:
                    case_x = int(mouse_xy[0]/constantes.taille_sprite)
                    case_y = int(mouse_xy[1]/constantes.taille_sprite)
                    joueurInfo = niveau.getJoueurSur(case_x, case_y)
                    if joueurInfo != None:
                        for etat in joueurInfo.etats:
                            if etat.actif():
                                print(joueurInfo.nomPerso+" est dans l'etat " +
                                      etat.nom+" ("+str(etat.duree)+")")
                            elif etat.debuteDans > 0:
                                print(joueurInfo.nomPerso+" sera dans l'etat " +
                                      etat.nom+" dans "+str(etat.debuteDans)+" tour(s)")
                    if sortSelectionne != None:
                        sortSelectionne = None
        return sortSelectionne


class PersonnageMur(Personnage):
    """@summary: Classe décrivant un montre de type MUR immobile (cawotte, cadran de Xelor...). hérite de Personnage"""

    def __init__(self, *args):
        """@summary: Initialise un personnage Mur, même initialisation que Personange
        @args: les arguments donnés, doivent être les mêmes que Personnage
        @type:*args"""
        super(PersonnageMur, self).__init__(*args)

    def deepcopy(self):
        """@summary: Clone le personnageMur
        @return: le clone"""
        cp = PersonnageMur(self.nomPerso, self.classe, self.lvl, self.team, self.caracsPrimaires,
                           self.caracsSecondaires, self.dommages, self.resistances, self.icone)
        cp.sorts, cp.sortsDebutCombat = Personnage.ChargerSorts(
            cp.classe, cp.lvl)
        return cp

    def joue(self, event, niveau, mouse_xy, sortSelectionne):
        """@summary: Fonction appelé par la boucle principale pour demandé à un PersonnageMur d'effectuer ses actions.
                     Dans la classe PersonnageMur, c'est fin de tour immédiate sans action.
        @event: les évenements pygames survenus
        @type: Event pygame
        @niveau: La grille de jeu
        @type: Niveau
        @mouse_xy: Les coordonnées de la souris
        @type: int
        @sortSelectionne: Le sort sélectionné plus tôt dans la partie s'il y en a un
        @type: Sort"""
        print("Tour de "+(niveau.tourDe.nomPerso))
        niveau.finTour()


class PersonnageSansPM(Personnage):
    """@summary: Classe décrivant un personange pouvant faire des actions mais sans chercher à se déplacer (Stratege iop). hérite de Personnage"""

    def __init__(self, *args):
        """@summary: Initialise un personnage sans PM, même initialisation que Personange
        @args: les arguments donnés, doivent être les mêmes que Personnage
        @type:*args"""
        super(PersonnageSansPM, self).__init__(*args)

    def deepcopy(self):
        """@summary: Clone le PersonnageSansPM
        @return: le clone"""
        cp = PersonnageSansPM(self.nomPerso, self.classe, self.lvl, self.team, self.caracsPrimaires,
                              self.caracsSecondaires, self.dommages, self.resistances, self.icone)
        cp.sorts, cp.sortsDebutCombat = Personnage.ChargerSorts(
            cp.classe, cp.lvl)
        return cp

    def joue(self, event, niveau, mouse_xy, sortSelectionne):
        """@summary: Fonction appelé par la boucle principale pour demandé à un PersonnageSansPM d'effectuer ses actions.
                     Dans la classe PersonnageSansPM, lancer son seul sort sur lui-même et terminé son tour (comportement temporaire).
        @event: les évenements pygames survenus
        @type: Event pygame
        @niveau: La grille de jeu
        @type: Niveau
        @mouse_xy: Les coordonnées de la souris
        @type: int
        @sortSelectionne: Le sort sélectionné plus tôt dans la partie s'il y en a un
        @type: Sort"""
        self.sorts[0].lance(niveau.tourDe.posX,
                            niveau.tourDe.posY, niveau, self.posX, self.posY)
        niveau.finTour()



INVOCS = {
        "Cadran de Xelor": PersonnageSansPM("Cadran de Xelor", "Cadran de Xelor", 100, 1, {"Vitalite": 1000}, {}, {}, {}, "cadran_de_xelor.png"),
        "Cawotte": PersonnageMur("Cawotte", "Cawotte", 0, 1, {"Vitalite": 800}, {}, {}, {}, "cawotte.png"),
        "Synchro": PersonnageMur("Synchro", "Synchro", 0, 1, {"Vitalite": 1200}, {}, {}, {}, "synchro.png"),
        "Complice": PersonnageMur("Complice", "Complice", 0, 1, {"Vitalite": 650}, {}, {}, {}, "complice.png"),
        "Balise de Rappel": PersonnageSansPM("Balise de Rappel", "Balise de Rappel", 0, 1, {"Vitalite": 1000}, {}, {}, {}, "balise_de_rappel.png"),
        "Balise Tactique": PersonnageMur("Balise Tactique", "Balise Tactique", 0, 1, {"Vitalite": 1000}, {}, {}, {}, "balise_tactique.png"),
        "Stratege Iop": PersonnageMur("Stratege Iop", "Stratège Iop", 0, 1, {"Vitalite": 1385}, {}, {}, {}, "conquete.png"),
        "Double": Personnage("Double", "Double", 0, 1, {"Vitalite": 1}, {}, {}, {}, "sram.png"),
        "Comploteur": Personnage("Comploteur", "Comploteur", 0, 1, {"Vitalite": 1}, {}, {}, {}, "sram.png"),
    }