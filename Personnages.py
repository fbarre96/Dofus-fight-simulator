# -*- coding: utf-8 -*
"""
@summary: Rassembles les différents types de Personnages.
"""
from copy import deepcopy
import uuid

import Sort
from Etats.EtatBouclier import EtatBouclierPerLvl
from Effets.EffetInvoque import EffetInvoque
from IAs.DumbIA import DumbIA
from IAs.PasseIA import PasseIA
from IAs.JoueurIA import JoueurIA
import constantes
import Overlays


class Personnage(object):
    """@summary: Classe décrivant un personnage joueur de dofus."""

    def __init__(self, nomPerso, classe, lvl, team, caracsPrimaires,
                 caracsSecondaires, dommages, resistances, icone="", objIA=None):
        """@summary: Initialise un personnage.
        @classe: la classe du personnage (les 18 classes de Dofus).
                 Pour l'instant sert d'identifiant étant donné que 1v1 vs Poutch.
        @type: string
        @lvl: le niveau du personnage
        @type: int
        @team: le numéro d'équipe du personnage
        @type: int
        @caracsPrimaires: les caractéristiques primaires du perso
        (PA, PM, PO, vita, agi, chance, force, intel, pui, cc, sasa)
        @type: dict
        @caracsSecondaires: les caractéristiques secondaires du perso
        (RetPA, esquive pa, ret pm, esq pm, soins, tacle, fuite, ini, invocations, prospection)
        @type: dict
        @dommages: les dommages du perso
        (do, do cri, do neutre, do terre, do feu, do eau, do air, renvoi, maitrise d'arme,
                  pièges (fixe), pièges(puissance), poussée, Sorts, Arme, Distance, Mêlée)
        @type: dict
        @dommages: les résistances du perso
        (ré neutre, re per neutre, ré terre, ré per terre, ré feu, ré per feu, ré eau, ré per eau,
                                 ré air, ré per air, ré cc fixe, ré pou fixe, ré distance, ré mêlée)
        @type: dict
        @icone: le chemin de l'image pour afficher l'icône du personnage
        @type: string (nom de l'image. L'image doit faire moins de 30x30 pixels,
        se situer dans /image et porté le même nom que la classe une fois normalisé)
        """
        # pylint: disable=invalid-name
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
        self.doMaitriseArme = int(dommages.get("Maitrise d'arme", 0))
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

        self.vieMax = self.vie
        self.PMBase = int(self.PM)
        self.PABase = int(self.PA)
        self.nomPerso = nomPerso
        self.erosion = 10  # Erosion de base
        self.lvl = int(lvl)
        self.classe = classe
        self.uid = uuid.uuid4()
        self.sortsDebutCombat = []
        self.sorts, self.sortsDebutCombat = Personnage.chargerSorts(
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
        self.porteUid = None
        self.porteurUid = None
        self.checkLdv = True
        self.msgsPrevisu = []
        if objIA is None:
            objIA = JoueurIA()
        self.myIA = objIA

        if not icone.startswith("images/"):
            self.icone = ("images/"+icone)
        else:
            self.icone = (icone)
        self.icone = constantes.normaliser(self.icone)
        # Overlay affichange le nom de classe et sa vie restante
        self.overlay = Overlays.Overlay(self, Overlays.ColoredText(
            "nomPerso", (210, 105, 30)),
                                        Overlays.ColoredText("overlayTexte",
                                                             (224, 238, 238)),
                                        (56, 56, 56))

    def __deepcopy__(self, memo):
        toReturn = Personnage(self.nomPerso, self.classe, self.lvl, self.team,
                              {"PA": self.PA, "PM": self.PM, "PO": self.PO, "Vitalite": self.vie,
                               "Agilite": self.agi, "Chance": self.cha, "Force": self.fo,
                               "Intelligence": self.int, "Puissance": self.pui,
                               "Coups Critiques": self.cc, "Sagesse": self.sagesse},
                              {"Retrait PA": self.retPA, "Esquive PA": self.esqPA,
                               "Retrait PM": self.retPM, "Esquive PM": self.esqPM,
                               "Soins": self.soins, "Tacle": self.tacle, "Fuite": self.fuite,
                               "Initiative": self.ini, "Invocation": self.invocationLimite,
                               "Prospection": self.prospection},
                              {"Dommages": self.do, "Dommages critiques": self.doCri,
                               "Neutre": self.doNeutre, "Terre": self.doTerre, "Feu": self.doFeu,
                               "Eau": self.doEau, "Air": self.doAir, "Renvoi": self.doRenvoi,
                               "Maitrise d'arme": self.doMaitriseArme, "Pieges": self.doPieges,
                               "Pieges Puissance": self.doPiegesPui, "Poussee": self.doPou,
                               "Sorts": self.doSorts, "Armes": self.doArmes,
                               "Distance": self.doDist, "Melee": self.doMelee},
                              {"Neutre": self.reNeutre, "Neutre%": self.rePerNeutre,
                               "Terre": self.reTerre, "Terre%": self.rePerTerre, "Feu": self.reFeu,
                               "Feu%": self.rePerFeu, "Eau": self.reEau, "Eau%": self.rePerEau,
                               "Air": self.reAir, "Air%": self.rePerAir,
                               "Coups critiques": self.reCc, "Poussee": self.rePou,
                               "Distance": self.reDist, "Melee": self.reMelee},
                              self.icone)
        toReturn.sortsDebutCombat = self.sortsDebutCombat
        toReturn.posX = self.posX
        toReturn.posY = self.posY
        toReturn.PABase = self.PABase
        toReturn.PMBase = self.PMBase
        toReturn.vieMax = self.vieMax
        toReturn.uid = self.uid
        toReturn.sorts = deepcopy(self.sorts)
        toReturn.sortsDebutCombat = deepcopy(self.sortsDebutCombat)
        toReturn.etats = deepcopy(self.etats)
        toReturn.historiqueDeplacement = deepcopy(self.historiqueDeplacement)
        toReturn.posDebTour = self.posDebTour
        toReturn.posDebCombat = self.posDebCombat
        toReturn.invocateur = self.invocateur
        toReturn.porteUid = self.porteUid
        toReturn.porteurUid = self.porteurUid
        toReturn.checkLdv = self.checkLdv
        toReturn.invocations = deepcopy(self.invocations)
        toReturn.invocationLimite = self.invocationLimite
        toReturn.msgsPrevisu = deepcopy(self.msgsPrevisu)
        toReturn.myIA = self.myIA
        return toReturn

    def setOverlayText(self):
        """@summary: Change la valeur du texte dans l'overlay du perso
                     Ecrit X PV [X PB]
        """
        self.overlayTexte = str(self.vie) + " PV"
        boubou = self.getBoucliers()
        if boubou > 0:
            self.overlayTexte += " "+str(boubou)+" PB"

    def setOverlayTextGenerique(self, text):
        """@summary: Change la valeur du texte dans l'overlay du perso
                     Ecrit le texte donné en paramètre
        """
        self.overlayTexte = text

    def aEtatsRequis(self, etatsRequis):
        """@summary: Indique si le personnage possède les états donnés en paramètres.
        @etatsRequis: la liste des états à tester.
        si un ! se situe au début de la chaîne, il faut que l'état soit absent.
        @type: tableau de strings (noms d'états préfixé éventuellement par "!")


        @return: booléen valant True si tous les états requis sont sur le personnage, False sinon"""
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
                if (checkEtat.startswith("!") and aEtat) or \
                   (not checkEtat.startswith("!") and not aEtat):
                    # print "DEBUG : la cibleDirect n'a pas ou a l'etat requis :"+str(checkEtat)
                    return False
        return True

    @staticmethod
    def getSortRightLvl(lvl, tabSorts):
        """@summary: prend le sort dont le lvl requis est le plus élevé
                     mais reste inférieur au lvl donné
                     Méthode statique
        """
        closestLvlSort = None
        for sort in tabSorts[0:]:
            if sort.lvl <= lvl:
                if closestLvlSort is not None:
                    if closestLvlSort.lvl < sort.lvl:
                        closestLvlSort = sort
                else:
                    closestLvlSort = sort
        return closestLvlSort

    @staticmethod
    def chargerSorts(classe, lvl):
        """@summary: Méthode statique qui initialise les sorts du personnage selon sa classe.
        @classe: le nom de classe dont on souhaite récupérer les sorts
        @type: string

        @return: tableau de Sort"""
        sorts = []
        sortsDebutCombat = []
        if classe == "Stratege Iop":
            import Sorts.StrategeIop
            sortsDebutCombat += Sorts.StrategeIop.getSortsDebutCombat(lvl)
            sorts += Sorts.StrategeIop.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif classe == "Cadran de Xelor":
            import Sorts.CadranDeXelor
            sortsDebutCombat += Sorts.CadranDeXelor.getSortsDebutCombat(lvl)
            sorts += Sorts.CadranDeXelor.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif classe == "Balise de Rappel":
            import Sorts.BaliseDeRappel
            sortsDebutCombat += Sorts.BaliseDeRappel.getSortsDebutCombat(lvl)
            sorts += Sorts.BaliseDeRappel.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif classe == "Tonneau Attractif":
            import Sorts.TonneauAttractif
            sortsDebutCombat += Sorts.TonneauAttractif.getSortsDebutCombat(lvl)
            sorts += Sorts.TonneauAttractif.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif classe == "Tonneau Incapacitant":
            import Sorts.TonneauIncapacitant
            sortsDebutCombat += Sorts.TonneauIncapacitant.getSortsDebutCombat(lvl)
            sorts += Sorts.TonneauIncapacitant.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif classe == "Poutch":
            return sorts, sortsDebutCombat
        elif classe == "Lapino":
            import Sorts.Lapino
            sortsDebutCombat += Sorts.Lapino.getSortsDebutCombat(lvl)
            sorts += Sorts.Lapino.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif classe == "Lapino protecteur":
            import Sorts.Lapino_protecteur
            sortsDebutCombat += Sorts.Lapino_protecteur.getSortsDebutCombat(lvl)
            sorts += Sorts.Lapino_protecteur.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif classe == "Fiole":
            import Sorts.Fiole
            sortsDebutCombat += Sorts.Fiole.getSortsDebutCombat(lvl)
            sorts += Sorts.Fiole.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif classe == "Synchro":
            import Sorts.Synchro
            sortsDebutCombat += Sorts.Synchro.getSortsDebutCombat(lvl)
            sorts += Sorts.Synchro.getSorts(lvl)
            return sorts, sortsDebutCombat
        elif classe == "Xelor":
            import Sorts.Xelor
            sortsDebutCombat += Sorts.Xelor.getSortsDebutCombat(lvl)
            sorts += Sorts.Xelor.getSorts(lvl)
        elif classe == "Iop":
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
        elif classe == "Eniripsa":
            import Sorts.Eniripsa
            sortsDebutCombat += Sorts.Eniripsa.getSortsDebutCombat(lvl)
            sorts += Sorts.Eniripsa.getSorts(lvl)
        elif classe == "Pandawa":
            import Sorts.Pandawa
            sortsDebutCombat += Sorts.Pandawa.getSortsDebutCombat(lvl)
            sorts += Sorts.Pandawa.getSorts(lvl)
        sorts.append(Sort.Sort("Cawotte", 0, 4, 1, 6,
                               [EffetInvoque("Cawotte", False, cibles_possibles="",
                                             cible_non_requise=True)],
                               [], 0, 1, 1, 6, 0, "cercle", True,
                               description="Invoque une Cawotte"))
        totalNbSorts = len(sorts)
        i = 0
        while i < totalNbSorts:
            if sorts[i] is None:
                sorts.remove(sorts[i])
                totalNbSorts -= 1
                i -= 1
            i += 1
        return sorts, sortsDebutCombat

    def lancerSortsDebutCombat(self, niveau):
        """@summary: lance tous les sorts dans sortsDebutCombat
        """
        for sort in self.sortsDebutCombat:
            sort.lance(self.posX, self.posY, niveau, self.posX, self.posY)

    def ajoutHistoriqueDeplacement(self, posX=None, posY=None):
        """@summary: Ajoute la pos du joueur dans l'historique de déplacement
                     si posX ou posY est différent de None, l'ajoute à la place
        """
        if posX is None:
            posX = self.posX
        if posY is None:
            posY = self.posY
        self.historiqueDeplacement.append([posX, posY, 2])

    def bouge(self, niveau, nouvX, nouvY, ajouteHistorique=True):
        """@summary: téléporte le joueur sur la carte et stock
                    le déplacement dans l'historique de déplacement.
        @nouvX: la position d'arrivée en x.
        @type: int
        @nouvYx: la position d'arrivée en y.
        @type: int"""
        # test si la case d'arrivé est hors-map (compte comme un obstacle)
        if nouvX >= niveau.taille or nouvX < 0 or nouvY >= niveau.taille or nouvY < 0:
            return False, False
        elif niveau.structure[nouvY][nouvX].type != "v":
            return False, False
        joueurSurDestination = niveau.getJoueurSur(nouvX, nouvY)
        if joueurSurDestination is not None:
            return False, False
        if ajouteHistorique:
            self.ajoutHistoriqueDeplacement()
        self.posX = nouvX
        self.posY = nouvY
        if self.porteUid is not None:
            jPorte = niveau.getJoueurAvecUid(self.porteUid)
            jPorte.posX = nouvX
            jPorte.posY = nouvY
        if self.porteurUid is not None:
            jPorteur = niveau.getJoueurAvecUid(self.porteurUid)
            jPorteur.retirerEtats(niveau, ["Karcham", "Chamrak"])
            self.retirerEtats(niveau, ["Karcham", "Chamrak"])
            jPorteur.porteUid = None
            self.porteurUid = None
        nbPieges = len(niveau.pieges)
        i = 0
        piegeDeclenche = False
        # Priorité au nouveau piège:
        sauvegardeFile = niveau.fileEffets[:]
        niveau.fileEffets = []
        while i < nbPieges:
            piege = niveau.pieges[i]
            if piege.aPorteDeclenchement(nouvX, nouvY):
                piegeDeclenche = True
                for joueur in niveau.joueurs:
                    for etat in joueur.etats:
                        if etat.actif():
                            etat.triggerAvantPiegeDeclenche(
                                niveau, piege, self, joueur)

                for effet in piege.effets:
                    niveau.lancerEffet(effet, piege.centreX, piege.centreY,
                                       piege.nomSort, piege.centreX, piege.centreY, piege.lanceur)
                i -= 1
                niveau.pieges.remove(piege)
            i += 1
            nbPieges = len(niveau.pieges)
        # Verifie les entrées et sorties de glyphes:
        for glyphe in niveau.glyphes:
            if glyphe.actif():
                # Test Entre dans la glyphe
                if glyphe.aPorte(self.posX, self.posY):
                    for effet in glyphe.sortDeplacement.effets:
                        niveau.lancerEffet(effet, glyphe.centreX, glyphe.centreY,
                                           glyphe.nomSort, self.posX, self.posY, glyphe.lanceur)
                else:  # n'est pas dans la glyphe
                    if self.historiqueDeplacement:
                        dernierePos = self.historiqueDeplacement[-1]
                        # Test s'il était dans la glyphe avant

                        if glyphe.aPorte(dernierePos[0], dernierePos[1]):
                            for effet in glyphe.sortSortie.effets:
                                niveau.lancerEffet(
                                    effet, glyphe.centreX, glyphe.centreY, glyphe.nomSort,
                                    self.posX, self.posY, glyphe.lanceur)
        niveau.fileEffets = niveau.fileEffets + sauvegardeFile
        niveau.depileEffets()
        return True, piegeDeclenche

    def echangePosition(self, niveau, joueurCible, ajouteHistorique=True):
        """@summary: téléporte le joueur sur la carte et stock le déplacement
         dans l'historique de déplacement.
        @x: la position d'arrivée en x.
        @type: int
        @x: la position d'arrivée en y.
        @type: int"""
        # test si la case d'arrivé est hors-map (compte comme un obstacle)
        if niveau.getJoueurSur(joueurCible.posX, joueurCible.posY) is None:
            print("DEBUG : THIS SHOULD NOT BE POSSIBLE")
            return False, False
        if ajouteHistorique:
            self.ajoutHistoriqueDeplacement()
        joueurCible.ajoutHistoriqueDeplacement()
        depX = self.posX
        depY = self.posY
        self.posX = joueurCible.posX
        self.posY = joueurCible.posY
        joueurCible.posX = depX
        joueurCible.posY = depY
        nbPieges = len(niveau.pieges)
        i = 0
        piegeDeclenche = False
        # Priorité au nouveau piège:
        sauvegardeFile = niveau.fileEffets[:]
        niveau.fileEffets = []
        while i < nbPieges:
            piege = niveau.pieges[i]
            if piege.aPorteDeclenchement(depX, depY):
                piegeDeclenche = True
                for effet in piege.effets:
                    niveau.pieges.remove(piege)
                    i -= 1
                    niveau.lancerEffet(effet, piege.centreX, piege.centreY,
                                       piege.nomSort, piege.centreX, piege.centreY, piege.lanceur)
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

    def tpPosPrec(self, nbFois, niveau, lanceur, nomSort):
        """@summary: Téléporte le personnage à sa dernière position dans l'historique de déplacement
        @nbFois: Le nombre de retour en arrière à effectuer
        @type: int
        @niveau: la grille de jeu
        @type: Niveau
        @lanceur: le personnage à l'origine de cette action
        @type: Personnage
        @nomSort: le nom du sort à l'orginie de cette action
        @type: string"""
        for _ in range(nbFois):
            if self.historiqueDeplacement:
                pos = self.historiqueDeplacement[-1]
                del self.historiqueDeplacement[-1]
                niveau.gereDeplacementTF(
                    self, pos, lanceur, nomSort, ajouteHistorique=False)

    def aEtat(self, nomEtatCherche):
        """@summary: Indique si un personnage possède l'état donné
        @nomEtatCherche: Le nom de l'état cherché
        @type: string

        @return: booléen valant True si le personnage possède l'état , False sinon"""
        for etat in self.etats:
            if etat.nom == nomEtatCherche:
                return True
        return False

    def retirerEtats(self, niveau, nomsEtatCherche):
        """@summary: retire les états donné en paramètres
        @nomsEtatCherche: Les noms des états cherchés à supprimer
        @type: tableau de string"""
        i = 0
        print("Retire état "+str(nomsEtatCherche)+" de "+str(self.classe))
        nbEtats = len(self.etats)
        while i < nbEtats:
            if self.etats[i].nom in nomsEtatCherche:
                # Appliquer les fin de bonus et malus des do, pm, pa, po, pui et carac ici
                print(self.nomPerso+" sort de l'etat "+self.etats[i].nom)
                self.etats[i].triggerAvantRetrait(self)
                copyEtat = deepcopy(self.etats[i])
                del self.etats[i]
                i -= 1
                nbEtats = len(self.etats)
                for etat in self.etats:
                    if etat.actif():
                        etat.triggerApresRetrait(niveau, self, copyEtat)
            i += 1

    def getBoucliers(self):
        """@summary: Retourne la somme des points de bouclier
        """
        pbRestants = 0
        for etat in self.etats:
            if etat.actif():
                if isinstance(etat, EtatBouclierPerLvl):
                    pbRestants += etat.boostBouclier

        return pbRestants

    def soigne(self, soins, soigneur, shouldprint=True):
        """@summary: subit des dégâts de combats.
        Active les triggers d'états triggerAvantSubirDegats et triggerApresSubirDegats
        @soigneur: Le joueur soignant
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau
        @soins: Le nombre de points de soins calculés
        @type: int
        """
        for etat in self.etats:
            if etat.actif():
                soins = etat.triggerApresCalculSoins(soins, self, soigneur)
        soins = min(soins, self.vieMax-self.vie)
        self.vie += soins
        if shouldprint:
            print("+"+str(soins)+" PV")

    def subit(self, attaquant, niveau, degats, typeDegats, shouldprint=True):
        """@summary: subit des dégâts de combats.
        Active les triggers d'états triggerAvantSubirDegats et triggerApresSubirDegats
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

        pbRestants = 0
        for etat in self.etats:
            if etat.actif():
                if isinstance(etat, EtatBouclierPerLvl):
                    bouclierPrend = etat.boostBouclier - degats
                    if bouclierPrend > etat.boostBouclier:
                        degats -= etat.boostBouclier
                        etat.boostBouclier = 0
                        del etat
                    else:
                        etat.boostBouclier -= degats
                        degats = 0
                        pbRestants += etat.boostBouclier
        vieAEnlever = degats
        if self.vie - vieAEnlever < 0:
            vieAEnlever = self.vie

        self.vie -= vieAEnlever
        erosion = self.erosion
        if erosion > 50:  # L'érosion est capé à 50% dans le jeu
            erosion = 50
        elif erosion < 10:  # L'érosion est capé mini à 10% dans le jeu
            erosion = 10
        self.vieMax -= int(totalPerdu * (erosion/100))
        if self.vieMax < 0:
            self.vieMax = 0
        if self.vie > self.vieMax:
            self.vie = self.vieMax
        toprint = ""
        toprint = self.nomPerso+" a " + \
            str(self.vie) + "/"+str(self.vieMax)+" PV"
        if pbRestants > 0:
            toprint += " et "+str(pbRestants)+" PB"
        if shouldprint:
            print("-"+str(totalPerdu)+" PV")
            print(toprint)
        if self.vie <= 0:
            niveau.tue(self, attaquant)
        for etat in self.etats:
            if etat.actif():
                etat.triggerApresSubirDegats(
                    self, niveau, attaquant, totalPerdu)

    def finTour(self, niveau):
        """@summary: Termine le tour du personnage,
        récupération des PA et PM, sorts utilisés,
        activation du trigger d'état triggerFinTour
        @niveau: La grille de jeu
        @type: Niveau"""
        self.PM = self.PMBase
        self.PA = self.PABase
        for sort in self.sorts:
            sort.compteLancerParTour = 0
            sort.compteTourEntreDeux += 1
            sort.compteTourEntreDeux = min(sort.compteTourEntreDeux, sort.nbTourEntreDeux)
            sort.compteLancerParTourParJoueur = {}
        for etat in self.etats:
            if etat.actif():
                etat.triggerFinTour(self, niveau)

    def debutTour(self, niveau):
        """@summary: Débute le tour du personnage, déclenche glyphe,
        rafraîchit les états, les glyphes et l'historique de déplacement.
        @niveau: La grille de jeu
        @type: Niveau"""
        for glyphe in niveau.glyphes:
            if glyphe.actif():
                if glyphe.aPorte(self.posX, self.posY):
                    for effet in glyphe.sortMono.effets:
                        niveau.lancerEffet(effet, glyphe.centreX, glyphe.centreY,
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
        print("--------------------------------")
        print("Debut de tour de "+str(self.nomPerso)+".")
        print("PA : "+str(self.PA))
        print("PM : "+str(self.PM))
        print("PV : "+str(self.vie))

    def appliquerEtat(self, etat, lanceur, cumulMax=-1, niveau=None):
        """@summary: Applique un nouvel état sur le Personnage.
         Active le trigger d'état triggerInstantane
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
        for etatDejaApplique in self.etats:
            if etatDejaApplique.actif():
                etatDejaApplique.triggerAvantApplicationEtat(niveau, etat, lanceur, self)

        print(self.nomPerso+"  etat "+etat.nom+" ("+str(etat.duree)+" tours)")
        etat.lanceur = lanceur
        self.etats.append(etat)
        if self.etats[-1].actif():
            self.etats[-1].triggerInstantane(lanceur=lanceur,
                                             niveau=niveau, joueurCaseEffet=self)

    def changeDureeEffets(self, nbFois, niveau):
        """@summary: Réduit la durée des états sur le personnage
        @nbFois: le nombre de tours d'état réduit
        @type: int
        @niveau: La grille de jeu
        @type: Niveau"""
        for _ in range(abs(nbFois)):
            niveau.rafraichirEtats(self, False)

    def selectionSort(self, sort, niveau):
        """@summary: Verifie si le sort donné est selectionnable puis le selectionne.
        @sort: le sort a sélectionner
        @type: Sort
        @niveau: La grille de jeu
        @type: Niveau"""
        sortSelectionne = None
        coutPA = sort.coutPA
        if coutPA < 0:
            coutPA = 0
        if coutPA <= niveau.tourDe.PA:
            res, explication = sort.testLancableParJoueur(niveau.tourDe)
            if res:
                sortSelectionne = sort
            else:
                print(explication)

        else:
            print("PA insuffisant : coute "+str(coutPA) +
                  " mais "+str(niveau.tourDe.PA) + " restant.")
        return sortSelectionne

    def faitPorter(self, niveau, joueurPorte):
        """@summary: le joueur joueurPorteur porte joueurPorte
        """
        joueurPorte.ajoutHistoriqueDeplacement()
        joueurPorte.posX = self.posX
        joueurPorte.posY = self.posY
        self.porteUid = joueurPorte.uid
        joueurPorte.porteurUid = self.uid
        for etat in joueurPorte.etats:
            if etat.actif():
                etat.triggerApresPorte(niveau, self, joueurPorte)

    def faitLancer(self, niveau, cibleX, cibleY):
        """@summary: le joueur joueurPorteur lance joueurPorte
        """
        joueurSurCible = niveau.getJoueurSur(cibleX, cibleY)
        if niveau.structure[cibleY][cibleX].type == "v" and joueurSurCible is None:
            if self.porteUid is None:
                raise(Exception("IMPOSSIBLE pour "+str(self)+
                                " DE JETER UN JOUEUR S'IL N'EN PORTE PAS."))
            joueurPorte = niveau.getJoueurAvecUid(self.porteUid)
            joueurPorte.bouge(niveau, cibleX, cibleY, False)
            joueurPorte.retirerEtats(niveau, ["Karcham", "Chamrak"])
            self.retirerEtats(niveau, ["Karcham", "Chamrak"])
            joueurPorte.porteurUid = None
            self.porteUid = None
            for etat in joueurPorte.etats:
                if etat.actif():
                    etat.triggerApresLance(niveau, self, joueurPorte)

invocs_liste = {
    "Cadran de Xelor": Personnage("Cadran de Xelor", "Cadran de Xelor",
                                  100, 1, {"Vitalite": 1000}, {}, {}, {},
                                  "cadran_de_xelor.png", DumbIA()),
    "Cawotte": Personnage("Cawotte", "Cawotte", 0, 1,
                          {"Vitalite": 660}, {}, {}, {}, "cawotte.jpg", PasseIA()),
    "Synchro": Personnage("Synchro", "Synchro", 0, 1,
                          {"Vitalite": 1200}, {}, {}, {}, "synchro.png", PasseIA()),
    "Complice": Personnage("Complice", "Complice", 0, 1,
                           {"Vitalite": 650}, {}, {}, {}, "complice.png", PasseIA()),
    "Balise de Rappel": Personnage("Balise de Rappel", "Balise de Rappel",
                                   0, 1, {"Vitalite": 1000}, {}, {}, {},
                                   "balise_de_rappel.png", DumbIA()),
    "Balise Tactique": Personnage("Balise Tactique", "Balise Tactique",
                                  0, 1, {"Vitalite": 1000}, {}, {}, {},
                                  "balise_tactique.png", PasseIA()),
    "Stratege Iop": Personnage("Stratege Iop", "Stratège Iop", 0, 1,
                               {"Vitalite": 1385}, {}, {}, {}, "conquete.png", PasseIA()),
    "Double": Personnage("Double", "Double", 0, 1,
                         {"Vitalite": 1}, {}, {}, {}, "sram.png"),
    "Comploteur": Personnage("Comploteur", "Comploteur", 0, 1,
                             {"Vitalite": 1}, {}, {}, {}, "sram.png"),
    "Lapino": Personnage("Lapino", "Lapino",
                         0, 1, {"Vitalite": 1200, "PA":5, "PM":4},
                         {"Esquive PA":75, "Esquive PM":75}, {},
                         {"Neutre%":20, "Terre%":20, "Feu%":5, "Eau%":-5, "Air%":30},
                         "mot_d_amitie.jpg"),
    "Lapino protecteur": Personnage("Lapino protecteur", "Lapino protecteur",
                                    0, 1, {"Vitalite": 1200, "PA":5, "PM":4},
                                    {"Esquive PA":75, "Esquive PM":75}, {},
                                    {"Neutre%":10, "Terre%":15, "Feu%":0, "Eau%":-10, "Air%":25},
                                    "mot_d_affection.jpg"),
    "Fiole": Personnage("Fiole", "Fiole",
                        0, 1, {"Vitalite": 600, "PA":6, "PM":0},
                        {"Esquive PA":90, "Esquive PM":90}, {},
                        {"Neutre%":0, "Terre%":0, "Feu%":0, "Eau%":0, "Air%":0},
                        "mot_de_seduction.jpg", DumbIA()),
    "Tonneau Attractif": Personnage("Tonneau Attractif", "Tonneau Attractif",
                                    0, 1, {"Vitalite": 1315, "PA":8, "PM":-1},
                                    {"Esquive PA":52, "Esquive PM":52}, {},
                                    {"Neutre%":20, "Terre%":-10, "Feu%":20,
                                     "Eau%":-10, "Air%":30},
                                    "ivresse.jpg", DumbIA()),
    "Tonneau Incapacitant": Personnage("Tonneau Incapacitant", "Tonneau Incapacitant",
                                       0, 1, {"Vitalite": 1052, "PA":4, "PM":0},
                                       {"Esquive PA":0, "Esquive PM":0}, {},
                                       {"Neutre%":20, "Terre%":30, "Feu%":-10,
                                        "Eau%":20, "Air%":-10},
                                       "ebriete.jpg", DumbIA()),
}
