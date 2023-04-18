# -*- coding: utf-8 -*
"""@summary: Décrit la classe Niveau qui orchestre tout se qui se passe dessus et les interactions.
"""

from copy import deepcopy
import pygame
from pygame.locals import Rect
import Personnages
import Zones
import constantes
import Overlays
from Effets.EffetGlyphe import EffetGlyphe
from Etats.Etat import Etat
from PathFinding.PathFinder import PathFinder
from PathFinding.Noeud import Noeud


class Case:
    """@summary: Classe décrivant une case de la grille du niveau."""

    def __init__(self, typ, hitbox):
        """@summary: initialise une case.
            @typ: le type de la case ("v" pour vide, ou "j" pour joueur)
            @type: string (de une lettre)
            @hitbox: la hitbox de la case.
            Possède une fonction pour savoir si un point est dans la case.
            @type: Rect (pygame.locals)
            """
        self.type = typ
        self.hitbox = hitbox
        self.effetsSur = []

class Niveau:
    """@summary: Classe permettant de créer un niveau"""

    def load_images(self):
        self.vide1 = pygame.image.load(constantes.image_vide_1).convert()
        self.vide2 = pygame.image.load(constantes.image_vide_2).convert()
        self.team1 = pygame.image.load(constantes.image_team_1).convert_alpha()
        self.team2 = pygame.image.load(constantes.image_team_2).convert_alpha()
        self.previsionDeplacement = pygame.image.load(constantes.image_prevision_deplacement).convert()
        self.previsionSort = pygame.image.load(constantes.image_prevision_sort).convert()
        self.previsionLdv = pygame.image.load(constantes.image_prevision_ldv).convert()
        self.previsionTacle = pygame.image.load(constantes.image_prevision_tacle).convert()
        self.zone = pygame.image.load(constantes.image_prevision_zone).convert()
    
    def __init__(self, fenetre, joueurs, font):
        """@summary: initialise le niveau.
            @fenetre: la fenêtre créé par pygame
            @type: fenêtre pygame
            @joueurs: tous les joueurs/mosntres qui doivent être placés
                      sur la carte au début du combat.
            @type: tableau de Personnage
            @font: décrit une police d'écriture pygame
            @type: Font de pygame"""
        if fenetre is None:
            return
        self.load_images()
        # Le double tableau qui décrit les lignes de case la grilel de jeus
        self.structure = None
        # le nombre de case sur un côté de la carte (carré)
        self.taille = constantes.taille_carte
        # Un tableau des cordonnées de départs possibles pour la team 1
        self.departT1 = [[6, 6], [5, 6]]
        # Un tableau des cordonnées de départs possibles pour la team 2
        self.departT2 = [[8, 8], [9, 8]]
        self.joueurs = sorted(joueurs, key=lambda x: x.ini, reverse=True)
        # Le joueur qui commence est à la position 0 du tableau des joueurs
        self.tourIndex = 0
        self.enPrevisu = False
        # Le joueur dont c'est le tour
        self.tourDe = self.joueurs[self.tourIndex]
        # liste des glyphes
        self.glyphes = []
        # liste des pièges
        self.pieges = []
        # liste des runes
        self.runes = []
        # File d'attente pour ordre explosion piège
        self.fifoExploPiege = []
        # File d'attente Effets:
        self.fileEffets = []
        self.bloquerFile = False
        self.fenetre = fenetre
        self.myfont = font
        # Generer la carte
        self.generer()
        # Initialise tous les joueurs
        self.initPersonnages()
        # path finding class
        self.pathfinder = PathFinder()
        self.cachedPrevisu = [None, 0, 0, None]
    
    def isPrevisu(self):
        return self.enPrevisu

    def setPrevisu(self, bVal):
        self.enPrevisu = bVal

    def __deepcopy__(self, memo):
        toReturn = Niveau(None, None, None)
        toReturn.fenetre = None
        toReturn.taille = self.taille
        toReturn.enPrevisu = self.enPrevisu
        toReturn.bloquerFile = self.bloquerFile
        toReturn.fileEffets = deepcopy(self.fileEffets)
        toReturn.joueurs = deepcopy(self.joueurs)
        toReturn.tourIndex = self.tourIndex
        toReturn.tourDe = toReturn.joueurs[toReturn.tourIndex]
        toReturn.structure = deepcopy(self.structure)
        toReturn.pieges = deepcopy(self.pieges)
        toReturn.runes = deepcopy(self.runes)
        toReturn.glyphes = deepcopy(self.glyphes)
        return toReturn

    def ajoutFileEffets(self, effet, joueurCaseEffet, joueurLanceur):
        """@summary: Ajout un effet sur la file.
        """
        self.fileEffets.append([effet, joueurCaseEffet, joueurLanceur])

    def depileEffets(self):
        """@summary: dépile tous les effet et les activent.
        """
        if not self.bloquerFile:
            self.bloquerFile = True
            nbEffets = len(self.fileEffets)
            while nbEffets > 0:
                rec = self.fileEffets[0]
                self.fileEffets.remove(self.fileEffets[0])
                rec[0].activerEffet(self, rec[1], rec[2])
                del rec
                nbEffets = len(self.fileEffets)
            self.bloquerFile = False

    def deplacement(self, mouseXY):
        """@summary: Le joueur dont c'est le tour a cliqué sur la carte sans sort sélectionné.
                      Un déplacement vers cette case est tenté
            @mouseXY: la position de la souris sur la fenêtre pygame
            @type: tableau [int,int] cordonnées x,y de la souris."""
        caseX, caseY = self.pixel2grid(mouseXY)
        if caseX >= constantes.taille_carte or caseY >= constantes.taille_carte or \
            caseY < 0 or caseX < 0:
            return False
        joueur = self.tourDe
        cases = self.pathfinder.pathFinding(self, caseX, caseY, joueur)
        # cases vaut None si aucun chemin n'a été trouvé par l'algorithme A*
        if cases is not None:
            # Les cases à parcourir pour se rendre
            # à la position souhaitée donnent un nombre de PM nécessaire.
            if len(cases) <= joueur.PM:
                # On effectue le déplacement
                for case in cases:
                    # Le joueur se déplace case par case et non pas en téléportation
                    if self.structure[case[1]][case[0]].type != "v":
                        print("La case ciblée est un mur")
                        break
                    elif self.getJoueurSur(case[0], case[1]) is not None:
                        print("La case ciblée est occupé")
                        break
                    nbPAPerdus, nbPMPerdus = self.calculTacle(joueur)
                    if joueur.PM - nbPMPerdus >= 1 and joueur.PA - nbPAPerdus >= 0:
                        if nbPMPerdus > 0:
                            print("Taclé, le joueur perd " +
                                  str(nbPMPerdus)+" PM et "+str(nbPAPerdus)+" PA")
                        joueur.PM -= nbPMPerdus + 1
                        joueur.PA -= nbPAPerdus
                        _, piegeDeclenche = joueur.bouge(
                            self, case[0], case[1])
                        if piegeDeclenche:
                            break
                    else:
                        print("Le joueur est complétement taclé !")
                print("PA : "+str(joueur.PA))
                print("PM : "+str(joueur.PM))
            else:
                print("Deplacement  impossible ("+str(joueur.PM)+" PM restants).")
        else:
            print("Deplacement impossible ("+str(joueur.PM)+" PM restants).")

    def pixel2grid(self, mouseXY):
        caseX = int(mouseXY[0]/constantes.taille_sprite)
        caseY = int(mouseXY[1]/constantes.taille_sprite)
        return caseX,caseY

    def calculTacle(self, fuyard, posX=None, posY=None):
        """@summary: calcul le nombre de PA et PM a utilisé
                     par le fuyard pour bouger.
        """
        if posX is None:
            posX = fuyard.posX
            posY = fuyard.posY
        tacleurs = []
        tacleurs.append(self.getJoueurSur(posX, posY+1, False))
        tacleurs.append(self.getJoueurSur(posX, posY-1, False))
        tacleurs.append(self.getJoueurSur(posX+1, posY, False))
        tacleurs.append(self.getJoueurSur(posX-1, posY, False))

        ratio = 1
        for tacleur in tacleurs:
            if tacleur is not None:
                if tacleur.uid != fuyard.uid and tacleur.team != fuyard.team:
                    tacle = tacleur.tacle
                    ratio *= float(fuyard.fuite + 2) / float(2*(tacle + 2))
        ratio = min(ratio, 1)
        ratio = max(ratio, 0)
        pmApresTacle = int(round(fuyard.PM * ratio))
        paApresTacle = int(round(fuyard.PA * ratio))
        return max(0, int(fuyard.PA - paApresTacle)), max(0, int(fuyard.PM - pmApresTacle))

    @staticmethod
    def getCasesAXDistanceDe(caseX, caseY, distance):
        """@summary: Méthode statique qui renvoie toutes les cases se trouvant
                     sur un anneau de rayon donné autour d'une case.
            @caseX: la coordonnée x de la case centrale
            @type: int
            @caseY: la coordonnée y de la case centrale
            @type: int
            @distance: le rayon de l'anneau dont l'on veut obtenir les cases
            @type: int

            @return:  Les cases sur l'anneau de rayon donné listées de
                      gauche à droite puis de haut en bas """
        departX = caseX
        departY = caseY
        # La variable qui sera renvoyée
        retour = []
        # Cas de base
        if distance == 0:
            return [[caseX, caseY]]

        # la logique de cette fonction est le parcours de l'anneau en partant du centre
        # et en s'en écartant progressivement.
        # pour chaque colonne, 2 cases sont sur le bon rayon
        # sauf sur les deux colonnes aux extrêmes de l'anneau où il n'y en a qu'une.
        # Ces deux colonne seront traitées séparemment des colonnes centrales.

        # Le delta représente l'écart au centre en cordonnée X,
        # Plus on s'éloigne du centre, plus l'écart en ordonnée se réduit
        delta = 0
        # Obligé de faire delta 0 (colonne centrale) a la main pour éviter
        # l'ajout de la ligne de delta +0 et delta -0
        # Test si la coordonnée x est dans le grille de jeu
        # if departX-delta >= 0:
        #     # Test si la case haute de la colonne centre de l'anneau est dans le grille de jeu
        #     if departY-distance+delta >= 0:
        #         retour.append([departX-delta, departY-distance+delta])
        #     # Test si la case basse de la colonne centre de l'anneau est dans le grille de jeu
        #     if departY+distance-delta < constantes.taille_carte:
        #         retour.append([departX-delta, departY+distance-delta])

        # # Eloignement du centre de 1 en 1 jusqu'au rayon donné -1
        # for delta in range(1, distance):
        #     # On test si la colonne souhaitée à gauche du centre est dans la grille de jeu
        #     if departX-delta >= 0:
        #         # On test si la ligne souhaitée en haut à gauche du centre est dans la grille de jeu
        #         if departY-distance+delta >= 0:
        #             retour.append([departX-delta, departY-distance+delta])
        #         # On test si la ligne souhaitée en bas à gauche du centre est dans la grille de jeu
        #         if departY+distance-delta < constantes.taille_carte:
        #             retour.append([departX-delta, departY+distance-delta])
        #     # On test si la colonne souhaitée à droite est dans la grille de jeu
        #     if departX+delta < constantes.taille_carte:
        #         # On test si la ligne souhaitée en haut à droite du centre est dans la grille de jeu
        #         if departY-distance+delta >= 0:
        #             retour.append([departX+delta, departY-distance+delta])
        #         # On test si la ligne souhaitée en bas à droite du centre est dans la grille de jeu
        #         if departY+distance-delta < constantes.taille_carte:
        #             retour.append([departX+delta, departY+distance-delta])
        # delta = distance
        # # Oblige de faire delta distance à la main car sur les colonnes les plus loins
        # #  du centre il ny à q'une ligne à ajouter.
        # # Test si la coordonnée x extême gauche est dans le grille de jeu
        # if departX-delta >= 0:
        #     # Test si la cooficherrdonnée y est dans le grille de jeu
        #     if departY-distance+delta >= 0:
        #         retour.append([departX-delta, departY-distance+delta])
        # # Test si la coordonnée extême drotie x est dans le grille de jeu
        # if departX+delta < constantes.taille_carte:
        #     # Test si la coordonnée y est dans le grille de jeu
        #     if departY-distance+delta >= 0:
        #         retour.append([departX+delta, departY-distance+delta])

        for delta in range(0, distance+1):
            retour.append([departX+distance-delta, departY+delta])
        for delta in range(1, distance+1):
            retour.append([departX-delta, departY+distance-delta])
        for delta in range(1, distance+1):
            retour.append([departX-distance+delta, departY-delta])
        for delta in range(1, distance):
            retour.append([departX+delta, departY-distance+delta])
        # Return Les cases trouvées
        return retour

    def afficherSorts(self):
        """@summary: Méthode qui affiche les icônes des sorts sur la fenêtre."""

        # Réinitialisation de la zone des sorts en noir
        if self.fenetre is None:
            return  # Pendant certaines prévisu (genre EffetPropage)
        if not self.tourDe.myIA.interactif:
            return
        pygame.draw.rect(self.fenetre, pygame.Color(0, 0, 0),
                         pygame.Rect(constantes.x_sorts, constantes.y_sorts,
                                     constantes.width_sorts, constantes.height_sorts))
        # Création d'une surface grise semi-transparente
        # pour la poser par dessus les sorts inutilisables
        # La surface avec la couche de transparance ALPHA
        surfaceGrise = pygame.Surface((30, 30), pygame.SRCALPHA)
        # Le tuple RGB + l'alpha
        surfaceGrise.fill((128, 128, 128, 128))

        posSortsX = constantes.x_sorts
        posSortsY = constantes.y_sorts
        # Pour chaque sort du joueur dont c'est le tour on va afficher
        # son icône + son état de jouabilité
        for sort in self.tourDe.sorts:
            if not sort.lancableParJoueur:
                continue
            # On ajoute l'overlay sur le sort,
            # l'overlay est ce qui s'affichera lorsque le sort sera survolé avec la souris.
            sort.vue = Overlays.VueForOverlay(self.fenetre, posSortsX, posSortsY, 30, 30, sort)
            # On tente de récupérer l'image du sort
            imageSort = pygame.image.load(
                sort.image).convert()  # charge l'image
            # colle l'image sur la zone
            self.fenetre.blit(imageSort, (posSortsX, posSortsY))
            # On récupère si le sort est jouable
            res, explication = sort.testLancableParJoueur(self.tourDe)
            # Si le sort n'est pas lançable alors:
            if not res:
                # On le grise
                self.fenetre.blit(surfaceGrise, (posSortsX, posSortsY))
                # Si c'est une question de nombre de tour entre deux lancé:
                if "avant prochain lance" in explication:
                    # On affiche le nombre de tour restant
                    delai = int(explication.split(":")[1])
                    delaiLabel = self.myfont.render(str(delai), 1, (0, 0, 0))
                    self.fenetre.blit(delaiLabel, (posSortsX, posSortsY))
            # Les sorts sont collés les uns à côtés des autres, séparés par 30 pixels
            posSortsX += 30
            # Si on est arrivé au bout de la fenêtre, on descend d'une ligne
            if posSortsX+30 > constantes.x_sorts+constantes.width_sorts:
                posSortsY += 30
                posSortsX = constantes.x_sorts

    def initPersonnages(self):
        """@summary: Initialise les joueurs sur le niveau (positionnement)."""
        placeT1 = 0
        placeT2 = 0
        for joueur in self.joueurs:
            # Placement différent entre les deux teams
            if joueur.team == 1:
                # On positionne le joueur sur le premier emplacement de spawn
                joueur.posX = self.departT1[placeT1][0]
                joueur.posY = self.departT1[placeT1][1]
                # Prochain spawn
                placeT1 += 1
                # On initialise l'historique de déplacement du joueur
                # avec sa pos de début de tour et début de combat
                joueur.posDebTour = [joueur.posX, joueur.posY]
                joueur.posDebCombat = [joueur.posX, joueur.posY]
            else:
                joueur.posX = self.departT2[placeT2][0]
                joueur.posY = self.departT2[placeT2][1]
                placeT2 += 1
                joueur.posDebTour = [joueur.posX, joueur.posY]
                joueur.posDebCombat = [joueur.posX, joueur.posY]
            joueur.lancerSortsDebutCombat(self)

    def rafraichirEtats(self, personnageARafraichir, debutTour=True):
        """@summary: met à jour les états du personnage. (diminution de durée restante),
                active le trigger triggerRafraichissement si un état débute et
                active triggerAvantRetrait si un état termine
        @personnage: le personnage dont on trouver les etats et les rafraichirs
        @type: Personnage
        @debutTour: Indique si le rafraichissement est dû au début de tour ou à un effet autre.
        @type: booléen."""
        for personnage in self.joueurs:
            i = 0
            nbEtats = len(personnage.etats)
            while i < nbEtats:
                # Baisse de la durée de vie si l'état était actif
                if personnage.etats[i].lanceur.uid == personnageARafraichir.uid:
                    if personnage.etats[i].actif():
                        personnage.etats[i].duree -= 1
                    # Si c'est un début de tour, le temps avant de début de l'état est diminué
                    if debutTour:
                        personnage.etats[i].debuteDans -= 1
                    # Si c'est finalement le tour de début de l'état et si l'état est actif,
                    # on active le trigger d'état de rafraichissement
                    if personnage.etats[i].debuteDans == 0:
                        if personnage.etats[i].actif():
                            personnage.etats[i].triggerRafraichissement(
                                personnage, self)
                    # Si c'est le tour de sortie de l'état on active
                    #  le trigger d'état d'avant retrait
                    if personnage.etats[i].duree == 0:
                        # Appliquer les fin de bonus et malus des do, pm, pa, po, pui et carac ici
                        print(personnage.nomPerso+" sort de l'etat " +
                              personnage.etats[i].nom)
                        personnage.etats[i].triggerAvantRetrait(personnage)
                        copyEtat = deepcopy(personnage.etats[i])
                        del personnage.etats[i]
                        i -= 1
                        nbEtats = len(personnage.etats)
                        for personnagePorteur in self.joueurs:
                            for etat in personnagePorteur.etats:
                                if etat.actif():
                                    etat.triggerApresRetrait(self, personnage,
                                                             personnagePorteur, copyEtat)
                i += 1

    def rafraichirGlyphes(self, duPersonnage):
        """@summary: Rafraîchit la durée des glyphes et supprime celles qui ne sont plus actives.
                    Cette fonction est appelé au début de chaque tour.
            @duPersonnage: On rafraîchit uniquement les glyphes posés par ce joueur.
            @type: Personnage"""
        i = 0
        longueurTab = len(self.glyphes)
        # Parcours des glyphes
        while i < longueurTab:
            # On teste si la glyphe appartient à celui qui vient de débuter son tour
            if self.glyphes[i].lanceur == duPersonnage:
                # Si la glyphe était active, on réduit sa durée
                if self.glyphes[i].actif():
                    self.glyphes[i].duree -= 1  #  Réduction du temps restant
                    # Test si la glyphe est terminée
                    if self.glyphes[i].duree <= 0:
                        # Si c'est le cas on la supprime
                        glyphe = self.glyphes[i]
                        for joueur in self.joueurs:
                            if self.glyphes[i].aPorte(joueur.posX, joueur.posY):
                                for effet in glyphe.sortSortie.effets:
                                    self.lancerEffet(
                                        effet, glyphe.centreX, glyphe.centreY, glyphe.nomSort,
                                        joueur.posX, joueur.posY, glyphe.lanceur)
                        del self.glyphes[i]
                        i -= 1
            # On recalcule la taille du tableau
            longueurTab = len(self.glyphes)
            i += 1

    def rafraichirRunes(self, duPersonnage):
        """@summary: Rafraîchit la durée des runes et supprime celles qui ne sont plus actives.
                    Cette fonction est appelé au début de chaque tour.
            @duPersonnage: On rafraîchit uniquement les runes posés par ce joueur.
            @type: Personnage"""
        i = 0
        longueurTab = len(self.runes)
        # Parcours des runes
        while i < longueurTab:
            # On teste si la rune appartient à celui qui vient de débuter son tour
            if self.runes[i].lanceur == duPersonnage:
                # Si la rune était active, on réduit sa durée
                if self.runes[i].actif():
                    self.runes[i].duree -= 1  #  Réduction du temps restant
                    # Test si la rune est terminée
                    if self.runes[i].duree <= 0:
                        # Si c'est le cas on l'active puis on la supprime
                        self.runes[i].activation(self)
                        del self.runes[i]
                        i -= 1
            # On recalcule la taille du tableau
            longueurTab = len(self.runes)
            i += 1

    def finTour(self, **kwargs):
        """@summary: Appelé lorsqu'un joueur finit son tour."""
        # On annonce au joueur la fin de son tour
        if self is not None:
            self.tourDe.finTour(self)
        if self.isPrevisu() and not kwargs.get("force", False):
            return
        # calcul du prochain joueur
        self.tourIndex = (self.tourIndex + 1) % len(self.joueurs)
        self.tourDe = self.joueurs[self.tourIndex]
        # On annonce au joueur son début de tour
        self.tourDe.debutTour(self)

    def tue(self, perso, meurtrier):
        """@summary: Tue instantanément le joueur donné en paramètre."""

        # Parcours des joueurs
        if perso is None:
            return False
        for joueur in self.joueurs:
            if joueur.uid == perso.uid:
                for etat in joueur.etats:
                    if etat.actif():
                        etat.triggerAvantMort(self, joueur, perso, meurtrier)
        print(perso.nomPerso+" est mort!")
        i = 0
        persosJoueursRestants = []
        tailleJoueurs = len(self.joueurs)
        doitPasserTour = False
        while i < tailleJoueurs:
            # Recherche du joueur à tuer
            if isinstance(self.joueurs[i], Personnages.Personnage):
                persosJoueursRestants.append(self.joueurs[i])
            if self.joueurs[i].uid == perso.uid:
                # Recherche de l'invocateur si c'est une invocation
                if perso.invocateur is not None:
                    # Supression de l'invoc dans la liste d'invoc du perso
                    for j, invocation in enumerate(perso.invocateur.invocations):
                        if invocation == perso:
                            del perso.invocateur.invocations[j]
                            break
                del self.joueurs[i]
                if self.tourIndex > i:
                    self.tourIndex -= 1
                elif self.tourIndex == i:
                    doitPasserTour = True
                i -= 1
                break
            i += 1
            tailleJoueurs = len(self.joueurs)
        if len(persosJoueursRestants) == 1:
            print("--------------------------------")
            print("Gagnant : "+str(persosJoueursRestants[0].nomPerso))
        elif not persosJoueursRestants:
            print("--------------------------------")
            print("Tous mort ! Egalité.")
        if doitPasserTour:
            self.finTour()
        return True

    def generer(self):
        """@summary: Méthode permettant de générer le niveau.
        On crée une liste générale, contenant une liste par ligne à afficher"""

        structureNiveau = []
        for i in range(self.taille):
            ligneNiveau = []
            for j in range(self.taille):
                coordX, coordY = self.grid2pixel(j, i)

                ligneNiveau.append(Case("v", pygame.draw.rect(self.fenetre, (0, 0, 0),
                                                              [coordX,
                                                               coordY,
                                                               constantes.taille_sprite,
                                                               constantes.taille_sprite])))
            # On ajoute la ligne à la liste du niveau
            structureNiveau.append(ligneNiveau)
        # On sauvegarde cette structure
        self.structure = structureNiveau

    def grid2pixel(self, x, y):
        coordX = x * constantes.taille_sprite
        coordY = y * constantes.taille_sprite
        return coordX,coordY

    def getJoueurSur(self, caseX, caseY, getInvisible=True):
        """@summary: Retourne le joueur se trouvant sur la case donnée.
        @caseX: La coordonnée x de la case dont on veut récupérer le joueur
        @type: int
        @caseY: La coordonnée y de la case dont on veut récupérer le joueur
        @type: int

        @return: Personnage si la case est occupée, None sinon"""
        for i, joueur in enumerate(self.joueurs):
            if not joueur.aEtat("Invisible") or getInvisible:
                if joueur.posX == caseX and joueur.posY == caseY:
                    return self.joueurs[i]
        return None

    def getVisualationJoueurSur(self, caseX, caseY):
        """@summary: Retourne le joueur affiché se trouvant sur la case donnée.
                     Diffère de getJoueurSur quand le joueur est invisible.
        @caseX: La coordonnée x de la case dont on veut récupérer le joueur
        @type: int
        @caseY: La coordonnée y de la case dont on veut récupérer le joueur
        @type: int

        @return: Personnage si la case est occupée, None sinon"""
        for i, joueur in enumerate(self.joueurs):
            if joueur.aEtat("Invisible") and self.tourDe.team != joueur.team:
                if joueur.derniere_action_posX == caseX and joueur.derniere_action_posY == caseY:
                    return self.joueurs[i]
            else:
                if joueur.posX == caseX and joueur.posY == caseY:
                    return self.joueurs[i]
        return None

    def joueursAvecEtat(self, nomEtatCherche):
        """@summary: Retourne les joueurs possédant un état donné.
        @nomEtatCherche: Le nom de l'état que les joueurs doivent posséder
        @type: string

        @return: Un tableau contenant les joueurs possédant l'état donné"""
        retourListePersonnages = []
        for joueur in self.joueurs:
            for etat in joueur.etats:
                if etat.nom == nomEtatCherche:
                    retourListePersonnages.append(joueur)
        return retourListePersonnages

    def invoque(self, invoc, caseX, caseY):
        """@summary: Invoque un nouveau joueur dans la partie
        @invoc: le joueur à invoquer
        @type: Personnage
        @caseX: la coordonnée x de la case sur laquelle le joueur sera invoqué.
        @type: int
        @caseY: la coordonnée y de la case sur laquelle le joueur sera invoqué.
        @type: int"""
        found = False
        for i in range(len(self.joueurs)):
            if self.joueurs[i] == self.tourDe:
                self.joueurs.insert(i+1, invoc)
                if not self.isPrevisu():
                    print("Invocation "+invoc.nomPerso)
                invoc.lancerSortsDebutCombat(self)
                found = True
                break
        if not found:
            raise Exception("Impossible d'invoquer si ce n'est pas votre tour.")
        else:
            invoc.bouge(self, caseX, caseY, False)

    def getZoneEffet(self, effet, caseX, caseY):
        """@summary: Retourne un tableau des cases présentes
                     dans la zone de l'effet donné.
                     Les cases sont triées par distances croissantes
                     par rapport au centre de l'effet.
        @effet: l'effet dont on prendra la zone
        @type: Effet
        @caseX: la coordonnée x de la case sur laquelle l'effet devrait être lancé.
        @type: int
        @caseY: la coordonnée y de la case sur laquelle l'effet devrait être lancé.
        @type: int

        @return: Tableau de coordonnées [int x,int y] cases sont triées par distances
                 croissantes par rapport au centre de l'effet."""
        tabCasesZone = []
        # La taille de la zone n'indique pas forcément la distance la plus lointaine au centre,
        # on parcourt donc toutes la carte en partant du centre
        if effet.isReverseTreatmentOrder():
            mrange = range(64, -1, -1)
        else:
            mrange = range(64)
        for tailleCercle in mrange:
            casesAXDistance = Niveau.getCasesAXDistanceDe(
                caseX, caseY, tailleCercle)
            for case in casesAXDistance:
                # Test si la case trouvée est à porté de l'effet.
                if effet.aPorteZone(caseX, caseY, case[0], case[1],
                                    self.tourDe.posX, self.tourDe.posY):
                    tabCasesZone.append(case)
        return tabCasesZone

    def getZonePorteSort(self, sort, posX0, posY0, poLanceur):
        """@summary: Retourne un tableau des cases présentes dans la portée du sort
                     Les cases sont triées par distances croissantes par rapport au
                     centre de l'effet.
        @sort: le sort dont on calcul les cases à portées
        @type: Sort
        @posX0: la coordonnée x de la case depuis laquelle le sort est lancé
        @type: int
        @posY0: la coordonnée y de la case depuis laquelle le sort est lancé
        @type: int
        @poLanceur: les points de portées supplémentaires du lanceur qui peuvent
                     influencer sur la portée du sort.
        @type: int

        @return: Tableau de coordonnées [int x,int y] cases sont triées par distances
                 croissantes par rapport au centre du sort."""
        tabCasesZone = []
        # La portée maximale * 2 (pour les sorts diagonales) donne la limite d'exploration des cases
        for tailleCercle in range(sort.POMin, sort.POMax*2+1):
            casesAXDistance = Niveau.getCasesAXDistanceDe(posX0, posY0, tailleCercle)
            for case in casesAXDistance:
                if sort.aPorte(posX0, posY0, case[0], case[1], poLanceur):
                    tabCasesZone.append(case)
        return tabCasesZone

    def getZoneDeplacementJoueur(self, joueur):
        """@summary: Retourne un tableau des cases présentes dans la portée de déplacement du joueur
                Les cases sont triées par distances croissantes par rapport au centre de l'effet.
        @joueur: le joueur dont on calcul les cases à porter de déplacement
        @type: Personnage

        @return: Tableau de coordonnées [int x,int y] cases sont triées par distances croissantes
                 par rapport au centre du joueur."""
        tabCasesZone = []
        # La portée maximale * 2 (pour les sorts diagonales) donne la limite d'exploration des cases
        for tailleCercle in range(1, joueur.PM+1):
            if joueur.aEtat("Invisible") and self.tourDe.team != joueur.team:
                casesAXDistance = Niveau.getCasesAXDistanceDe(
                    joueur.derniere_action_posX, joueur.derniere_action_posY, tailleCercle)
            else:
                casesAXDistance = Niveau.getCasesAXDistanceDe(
                    joueur.posX, joueur.posY, tailleCercle)
            for case in casesAXDistance:
                joueurSurCase = self.getJoueurSur(case[0], case[1])
                if case[1] > 0 and case[1] < len(self.structure) and case[0] > 0 and case[0] < len(self.structure[0]):
                    if (self.structure[case[1]][case[0]].type == "v" and joueurSurCase is None):
                        tabCasesZone.append(case)
                if joueurSurCase is not None:
                    if joueurSurCase.team != self.tourDe.team and joueurSurCase.aEtat("Invisible"):
                        tabCasesZone.append(case)
        return tabCasesZone

    def effectuerPousser(self, joueurCible, pousseur, nbCases, doDeg, coordonnes):
        """@summary: Fonction à appeler pour pousser un joueur.
        @joueurCible: Le joueur qui se fait pousser
        @type: Personnage
        @nbCases: le nombre de case dont il faut pousser la cible
        @type: int
        @coordonnes: Indique le point de direction de pousse
        @type: tuple

        @return: posPouX  -> int indiquant la coordonnée x d'arrivé après poussé
                ,posPouY -> int indiquant la coordonnée y d'arrivé après poussé
                ,nbFoisCogne -> int indiquant le nombre de case non déplacé pour cause d'obstacle"""

        nbFoisCogne = 0  # Nombre de cases obstacles cognés
        # calcul de poussé de nbCases
        fait = 0
        startPosX = joueurCible.posX
        startPosY = joueurCible.posY
        posPouX = -1
        posPouY = -1
        while fait < nbCases:
            # Calcul de la case d'arrivée après une poussée de 1 case
            posPouX = joueurCible.posX + coordonnes[0]
            if posPouX != joueurCible.posX:
                # test si la case d'arrivé est hors-map (compte comme un obstacle)
                aBouge, piegeDeclenche = joueurCible.bouge(
                    self, posPouX, joueurCible.posY, False)
                if not aBouge:
                    nbFoisCogne += 1
                if piegeDeclenche:
                    break
                fait += 1
            posPouY = joueurCible.posY + coordonnes[1]
            if posPouY != joueurCible.posY:
            # test si la case d'arrivé est hors-map (compte comme un obstacle)
                aBouge, piegeDeclenche = joueurCible.bouge(
                    self, joueurCible.posX, posPouY, False)
                if not aBouge:
                    nbFoisCogne += 1
                if piegeDeclenche:
                    break
                fait += 1
        if startPosX != joueurCible.posX or startPosY != joueurCible.posY:
            joueurCible.ajoutHistoriqueDeplacement(startPosX, startPosY)
        # Calcul des dégâts
        rStart = 6
        if doDeg:
            doPou = pousseur.doPou
            rePou = joueurCible.rePou
            # Intervention des états
            for etat in pousseur.etats:
                if etat.actif():
                    doPou, rePou = etat.triggerCalculPousser(
                        doPou, rePou, self, pousseur, joueurCible)
            for etat in joueurCible.etats:
                if etat.actif():
                    doPou, rePou = etat.triggerCalculPousser(
                        doPou, rePou, self, pousseur, joueurCible)
            # Calcul des dégâts
            total = (8+rStart*pousseur.lvl/50)*nbFoisCogne
            total = int(total)
            if total > 0:
                total += doPou
                vaSubir = total - rePou
                print(joueurCible.nomPerso+" perd " +
                      str(vaSubir) + "PV (do pou)")
                joueurCible.subit(pousseur, self, vaSubir, "doPou")
        return posPouX, posPouY, nbFoisCogne

    def pousser(self, effetPousser, joueurCible, pousseur, doDeg=True):
        """@summary: Fonction à appeler pour pousser un joueur.
        @nbCases: le nombre de case dont il faut pousser la cible
        @type: int
        @joueurCible: Le joueur qui se fait pousser
        @type: Personnage
        @pousseur: Le joueur qui va pousser
        @type: Personnage
        @doDeg: Indique si la poussé appliquera des dommages
                (L'attirance étant une poussé inversé, elle ne cause pas de dommage)
        @type: booléen, True pas défaut"""
        if joueurCible is not None:
            startX = joueurCible.posX
            startY = joueurCible.posY
            if effetPousser.coordonnees is not None:
                if not(effetPousser.coordonnees[0] == 0 and effetPousser.coordonnees[1] == 0):
                    posX, posY, nbCogne = self.effectuerPousser(
                        joueurCible, pousseur, effetPousser.nbCase, doDeg, effetPousser.coordonnees)
        if nbCogne < effetPousser.nbCase:
            for etat in joueurCible.etats:
                if etat.actif():
                    etat.triggerApresDeplacementForce(self, joueurCible, pousseur)
        
    def attire(self, effetAttire, joueurCible, attireur):
        """@summary: Fonction à appeler pour attirer un joueur.
        @nbCases: le nombre de case dont il faut attirer la cible
        @type: int
        @joueurCible: Le joueur qui se fait attirer
        @type: Personnage
        @attireur: Le joueur qui va attirer
        @type: Personnage"""

        self.pousser(effetAttire, joueurCible, attireur, False)

    def deplacementTFVersCaseVide(self, joueurBougeant, posAtteinte, ajouteHistorique):
        """@summary: Déplacement pouvant généré un téléfrag vers une case vide.
        @joueurBougeant: le joueur qui se déplace vers une case vide
        @type: Personnage
        @posAtteinte: La position que le joueur va atteindre
        @type: [int x, int y]
        @ajouteHistorique: indique si le déplacement compte dans l'historique.
                           (Le passif du téléfrag n'a pas l'historique du déplacement par exemple)
        @type: booléen"""

        joueurBougeant.bouge(
            self, posAtteinte[0], posAtteinte[1], ajouteHistorique)

    def activerGlyphe(self, nomSort):
        """@summary: Active une glyphe selon le nom du sort

        @nomSort: le nom du sort à l'origine de la glyphe a activer
        @type: string"""
        for glyphe in self.glyphes:
            if glyphe.nomSort == nomSort and glyphe.actif():
                casesDansPorte = self.getZonePorteSort(
                    glyphe.sortMono, glyphe.centreX, glyphe.centreY, 0)
                for effet in glyphe.sortMono.effets:
                    ciblesTraitees = []
                    for caseDansPorte in casesDansPorte:
                        if glyphe.aPorte(caseDansPorte[0], caseDansPorte[1]):
                            cibleDansPorte = self.getJoueurSur(
                                caseDansPorte[0], caseDansPorte[1])
                            if cibleDansPorte is not None:
                                if cibleDansPorte not in ciblesTraitees:
                                    _, cibles = self.lancerEffet(effet,
                                                                 glyphe.centreX,
                                                                 glyphe.centreY,
                                                                 glyphe.sortMono.nom,
                                                                 cibleDansPorte.posX,
                                                                 cibleDansPorte.posY,
                                                                 glyphe.lanceur)
                                    ciblesTraitees += cibles

    def deplacementTFVersCaseOccupee(self, joueurASwap, joueurBougeant,
                                     reelLanceur, nomSort, ajouteHistorique, genereTF):
        """@summary: Déplace le joueur en téléfrag vers une case avec un joueur.
        @joueurASwap: Le joueur qui occupe la case considéré comme occupé
        @type: Personnage
        @joueurBougeant: Le joueur qui se déplace en téléfrag vers la case occupé
        @type: string
        @reelLanceur: Le joueur étant à l'origine du téléfrag
        @type: Personnage
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @ajouteHistorique: Indique si le déplacement doit être conservé
                           dans l'historique de déplacement du joueur
        @type: booléen
        @genereTF: Indique si l'état téléfrag est placé pour les deux joueurs
        @type: booléen"""

        self.effectuerTF(joueurASwap, joueurBougeant, reelLanceur,
                         nomSort, ajouteHistorique, genereTF)
        # Si un téléfrag doit généré, il l'a été dans effectuerTF
        if genereTF:
            # Résultats d'un téléfrag (activation de glyphe, synchro, boost, et boost PA)
            for joueur in self.joueurs:
                for etat in joueur.etats:
                    if etat.actif():
                        etat.triggerApresTF(
                            self, joueurBougeant, joueurASwap, joueur, reelLanceur, nomSort)

    def effectuerTF(self, joueurASwap, joueurBougeant, reelLanceur,
                    nomSort, ajouteHistorique, genereTF):
        """@summary: Echange les joueurs en téléfrag.
        @joueurASwap: Le joueur qui occupe la case considéré comme occupé
        @type: Personnage
        @joueurBougeant: Le joueur qui se déplace en téléfrag vers la case occupé
        @type: string

        @reelLanceur: Le joueur étant à l'origine du téléfrag
        @type: Personnage
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @ajouteHistorique: Indique si le déplacement doit être conservé
                           dans l'historique de déplacement du joueur
        @type: booléen
        @genereTF: Indique si l'état téléfrag est placé pour les deux joueurs
        @type: booléen"""

        #joueurASwap.bouge(self,joueurBougeant.posX, joueurBougeant.posY,True)
        joueurBougeant.echangePosition(self, joueurASwap, ajouteHistorique)
        if genereTF:
            joueurBougeant.retirerEtats(self, "Telefrag")
            joueurASwap.retirerEtats(self, "Telefrag")
            joueurBougeant.appliquerEtat(Etat(
                "Telefrag", 0, 2, [nomSort], reelLanceur), reelLanceur, 1, self)
            joueurASwap.appliquerEtat(Etat(
                "Telefrag", 0, 2, [nomSort], reelLanceur), reelLanceur, 1, self)

    def gereDeplacementTF(self, joueurBougeant, posAtteinte, lanceur,
                          nomSort, ajouteHistorique=True, genereTF=True):
        """@summary: Fonction à appeler pour les déplacements pouvant créer un téléfrag.
        @joueurBougeant: Le joueur qui se déplace en téléfrag
        @type: string
        @posAtteinte: Les coordonnées de la case d'arrivée
        @type: [int x, int y]
        @lanceur: Le joueur étant à l'origine du téléfrag
        @type: Personnage
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @ajouteHistorique: Indique si le déplacement doit être conservé dans
                           l'historique de déplacement du joueur
        @type: booléen, True par défaut
        @genereTF: Indique si l'état téléfrag est placé pour les deux joueurs
        @type: booléen, True par défaut

        @return: Renvoie le joueur qui a été impliqué dans le téléfrag s'il existe, None sinon"""
        # Test hors-map
        if posAtteinte[1] < 0 or posAtteinte[1] >= constantes.taille_carte or \
           posAtteinte[0] < 0 or posAtteinte[0] >= constantes.taille_carte:
            return None
        # Test déplacement case vers vide
        joueurASwap = self.getJoueurSur(posAtteinte[0], posAtteinte[1])
        if self.structure[posAtteinte[1]][posAtteinte[0]].type == "v" \
           and joueurASwap is None:
            self.deplacementTFVersCaseVide(
                joueurBougeant, posAtteinte, ajouteHistorique)
            return None
        # Test si sa case d'arrivé est occupé par un joueur
        elif joueurASwap is not None:
            # Si C'est une invocation, c'est l'invocateur le réel lanceur
            if lanceur.invocateur is not None:
                reelLanceur = lanceur.invocateur
            else:
                reelLanceur = lanceur

            if joueurASwap != joueurBougeant:
                self.deplacementTFVersCaseOccupee(
                    joueurASwap, joueurBougeant, reelLanceur, nomSort, ajouteHistorique, genereTF)
                return joueurASwap
        else:
            print("Deplacement pas implemente")
        return None

    def appliquerEffetSansBoucleSurZone(self, effet, joueurLanceur, caseCibleX, caseCibleY,
                                        nomSort, ciblesTraitees, provX, provY):
        """@summary: Fonction qui applique un effet ayant une zone
                     sans la prendre en compte (les glyphes).
        @effet: L'effet qu'il faut appliquer
        @type: Effet
        @joueurLanceur: Le joueur à l'origine de l'effet
        @type: Personnage
        @caseCibleX: Coordonné x de la case ciblé
        @type: int
        @caseCibleY: Coordonné y de la case ciblé
        @type: int
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @ciblesTraitees: La liste des cibles déjà traitées pour cet effet
        @type: tableau de Personnage
        @provX: Coordonné x de la case d'origine de l'effet
        @type: int
        @provY: Coordonné y de la case d'origine de l'effet
        @type: int

        @return: Renvoie True si l'effet a été appliqué, False sinon"""
        if isinstance(effet, EffetGlyphe):
            effetALancer = deepcopy(effet)
            effetALancer.appliquerEffet(self, None, joueurLanceur,
                                        caseCibleX=caseCibleX, caseCibleY=caseCibleY,
                                        nom_sort=nomSort, cibles_traitees=ciblesTraitees,
                                        provX=provX, provY=provY)
            return True
        return False

    def appliquerEffetSurZone(self, zoneEffet, effet, joueurLanceur, joueurCibleDirect,
                              caseCibleX, caseCibleY, nomSort, ciblesTraitees, provX, provY):
        """@summary: Fonction qui applique un effet ayant une zone.
        @zoneEffet: la zone de l'effet
        @type: Effet
        @effet: L'effet qu'il faut appliquer
        @type: Effet
        @joueurLanceur: Le joueur à l'origine de l'effet
        @type: Personnage
        @joueurCibleDirect: Le joueur qui s'est fait ciblé pour lancé le sort
        @type: Personnage ou None si l'effet peut être fait au vide.
        @caseCibleX: Coordonné x de la case ciblé
        @type: int
        @caseCibleY: Coordonné y de la case ciblé
        @type: int
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @ciblesTraitees: La liste des cibles déjà traitées pour cet effet
        @type: tableau de Personnage
        @provX: Coordonné x de la case d'origine de l'effet
        @type: int
        @provY: Coordonné y de la case d'origine de l'effet
        @type: int
        @previsu: Un objet de type previsualisation a remplir
        @type: Previsu
        @return: -Renvoie True si l'effet a été appliqué, False sinon
                 -Les cibles traitées avec les nouveaux joueurs ajoutés dedans"""

        
        sestApplique = False
        # Pour chaque case dans la zone
        for caseEffet in zoneEffet:
            caseX = caseEffet[0]
            caseY = caseEffet[1]
            # récupération du joueur sur la case
            joueurCaseEffet = self.getJoueurSur(caseX, caseY)
            # Test si un joeuur est sur la case
            effetALancer = deepcopy(effet)
            msg, res = effet.estLancable(joueurLanceur, joueurCibleDirect)
            if not res:
                return False, ciblesTraitees
            if joueurCaseEffet is not None:

                # Si le joueur sur la case est une cible valide
                msg, estValide = effet.cibleValide(joueurLanceur, joueurCaseEffet,
                                                   ciblesTraitees)
                if not estValide:
                    if not self.isPrevisu():
                        print(msg)
                else:
                    # On appliquer l'effet
                    ciblesTraitees.append(joueurCaseEffet)
                    sestApplique = effetALancer.appliquerEffet(self, joueurCaseEffet, joueurLanceur,
                                                               caseCibleX=caseCibleX,
                                                               caseCibleY=caseCibleY,
                                                               nom_sort=nomSort,
                                                               cibles_traitees=ciblesTraitees,
                                                               provX=provX, provY=provY,
                                                               caseEffetX=caseX,
                                                               caseEffetY=caseY)
                    if sestApplique is None:
                        sestApplique = True
                    elif not isinstance(sestApplique, bool):
                        raise Exception(
                            "Retour d'effet inattendu : "+str(sestApplique))
                    # Peu import le type, l'etat requis est retire s'il est consomme
                    if effet.consommeEtat:
                        joueurCaseEffet.retirerEtats(self,
                                                     effet.etatRequisCibleDirect)
                        joueurCaseEffet.retirerEtats(self, effet.etatRequisCibles)
                        joueurLanceur.retirerEtats(self, effet.etatRequisLanceur)

            else:
                effetALancer.appliquerEffet(self, joueurCaseEffet, joueurLanceur,
                                            caseCibleX=caseCibleX, caseCibleY=caseCibleY,
                                            nom_sort=nomSort,
                                            cibles_traitees=ciblesTraitees,
                                            provX=provX, provY=provY, caseEffetX=caseX,
                                            caseEffetY=caseY)
                sestApplique = True

        return sestApplique, ciblesTraitees

    def lancerEffet(self, effet, provX, provY, nomSort, caseCibleX, caseCibleY, lanceur=None):
        """@summary: Fonction qui applique un effet.
        @effet: L'effet qu'il faut appliquer
        @type: Effet
        @provX: Coordonné x de la case d'origine de l'effet
        @type: int
        @provY: Coordonné y de la case d'origine de l'effet
        @type: int
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @caseCibleX: Coordonné x de la case ciblé
        @type: int
        @caseCibleY: Coordonné y de la case ciblé
        @type: int
        @lanceur: le lanceur de l'effet, None si le lanceur est sur provX;provY
        @type: Personnage, ou None
        @previsu: Un objet de type previsualisation a remplir
        @type: Previsu
        @return: -Renvoie True si l'effet a été appliqué, False sinon
                 -Les cibles traitées avec les nouveaux joueurs ajoutés dedans"""
        if lanceur is None:
            joueurLanceur = self.getJoueurSur(provX, provY)
        else:
            joueurLanceur = lanceur
        
        ciblesTraitees = []  # initialisation des cibles déjà traitées
        # Le joueur cible direct est celui ciblé pour lancer le sort.
        joueurCibleDirect = self.getJoueurSur(caseCibleX, caseCibleY)
        zoneEffet = self.getZoneEffet(effet, caseCibleX, caseCibleY)
        # Effet non boucles
        sestApplique = self.appliquerEffetSansBoucleSurZone(
            effet, joueurLanceur, caseCibleX, caseCibleY, nomSort, ciblesTraitees, provX, provY)
        if sestApplique:
            self.afficherSorts()
            return sestApplique, ciblesTraitees
        sestApplique, ciblesTraitees = self.appliquerEffetSurZone(zoneEffet, effet, joueurLanceur,
                                                                  joueurCibleDirect, caseCibleX,
                                                                  caseCibleY, nomSort,
                                                                  ciblesTraitees,
                                                                  provX, provY)
        return sestApplique, ciblesTraitees

    def getJoueurs(self, cibles):
        """@summary: Retourne les joueurs correspondant à une liste de classes.
        @cibles: la liste des classes dont on cherche les représentants.
        @type: string, chaque classe séparé par des "|"

        @return: Renvoie la liste des joueurs correspondant à la liste de classes donnée.
        """
        onCherche = cibles.split("|")
        retour = []
        for joueur in self.joueurs:
            if joueur.classe in onCherche:
                retour.append(joueur)
        return retour

    def getJoueurslesPlusProches(self, caseX, caseY, lanceur, zone=Zones.TypeZoneCercle(99),
                                 etatRequisCibles=None, ciblesPossibles=None, ciblesExclues=None,
                                 ciblesTraitees=None):
        """@summary: Retourne les joueurs correspondant aux critères donnés triés par proximité.
        @caseX: la coordonnée x de la case de départ de la recherche
        @type: int
        @caseY: la coordonnée y de la case de départ de la recherche
        @type: int
        @lanceur: le lanceur de la recherche
        @type: Personnage
        @zone: la zone de recherche, optionel:si pas de zone donnée, cherche sur toutes la carte
        @type: Zone
        @etatRequisCibles: la liste des états requis sur les cibles, optionnel.
        @type: tableau de string
        @ciblesPossibles: la liste des cibles possibles, optionnel
        @type: tableau de string
        @ciblesExclues: la liste des cibles exclues, optionnel
        @type: tableau de string
        @ciblesTraitees: la liste des cibles déjà traitées, optionnel
        @type: tableau de string

        @return: Renvoie la liste des joueurs correspondant aux crtères données triés par proximité.
        """
        if etatRequisCibles is None:
            etatRequisCibles = []
        if ciblesPossibles is None:
            ciblesPossibles = []
        if ciblesExclues is None:
            ciblesExclues = []
        if ciblesTraitees is None:
            ciblesTraitees = []
        joueursCasesZone = []
        for tailleCercle in range(64):
            casesAXDistance = self.getCasesAXDistanceDe(caseX, caseY, tailleCercle)
            # Pour chaque case à distance 0, puis 1, puis 2 etc...
            for case in casesAXDistance:
                # Si la case est dans le critère de zone
                if zone.testCaseEstDedans([caseX, caseY], case, None):
                    # S'il y a un joueur sur la case
                    joueur = self.getJoueurSur(case[0], case[1])
                    if joueur is not None:
                        # Test des conditions
                        if (joueur.team == lanceur.team and joueur != lanceur
                                                        and "Allies" in ciblesPossibles) \
                            or (joueur.team == lanceur.team and joueur == lanceur
                                and "Lanceur" in ciblesPossibles) \
                            or (joueur.team != lanceur.team and "Ennemis" in ciblesPossibles) \
                            or (joueur.classe in ciblesPossibles) \
                            or (joueur.invocateur is not None and "Invoc" in ciblesPossibles) \
                            or (lanceur.invocateur is not None and "Invocateur" in ciblesExclues
                                and joueur.uid == lanceur.invocateur.uid):
                            if not(joueur.classe in ciblesExclues or \
                                (joueur.uid == lanceur.uid and "Lanceur" in ciblesExclues) or\
                                (joueur.invocateur is not None and "Invoc" in ciblesExclues)):
                                # Test sur l'etat requis.
                                if joueur.aEtatsRequis(etatRequisCibles):
                                    # Test si le joueur ciblé à déjà été impacté
                                    if joueur not in ciblesTraitees:
                                        joueursCasesZone.append(joueur)
        return joueursCasesZone

    def afficher(self, fenetre, sortSelectionne, mouseXY):
        """@summary: Méthode permettant d'afficher le niveau"""
        # Chargement des images (seule celle de team contiennent de la transparence)
        
        # On parcourt la liste du niveau
        nLigne = 0
        tabCasesPrevi = []
        previsuToShow = []
        for ligne in self.structure:
            # Onparcourt les listes de lignes
            nCase = 0
            for sprite in ligne:
                # On calcule la position réelle en pixels
                pixelX,pixelY = self.grid2pixel(nCase, nLigne)
                if sprite.type == 'v':  # v = Vide
                    if (nCase+(nLigne*len(ligne))) % 2 == 0:
                        fenetre.blit(self.vide1, (pixelX, pixelY))
                    else:
                        fenetre.blit(self.vide2, (pixelX, pixelY))

                    # Afficher previsualation portee du sort selectionne
                    if sortSelectionne is not None:
                        # Previsu de la porte du sort, une case teste par tour de double boucle
                        if sortSelectionne.aPorte(self.tourDe.posX, self.tourDe.posY,
                                                  nCase, nLigne, self.tourDe.PO):
                            if not sortSelectionne.ldv or \
                               not self.tourDe.checkLdv or \
                               sortSelectionne.aLigneDeVue(self, self.tourDe.posX,
                                                           self.tourDe.posY, nCase, nLigne):
                                fenetre.blit(self.previsionSort, (pixelX, pixelY))
                            else:
                                fenetre.blit(self.previsionLdv, (pixelX, pixelY))
                        # Si la souris est sur la grille de jeu (et non pas dans les sorts)
                        if mouseXY[1] < constantes.y_sorts:
                            caseX, caseY = self.pixel2grid(mouseXY)
                            # Si on cible une case dans la porte du sort il faut afficher la zone
                            if sortSelectionne.aPorte(self.tourDe.posX, self.tourDe.posY,
                                                      caseX, caseY, self.tourDe.PO):
                                joueurCibleDirect = self.getJoueurSur(
                                    caseX, caseY)
                                if not sortSelectionne.chaine:
                                    tabEffets = sortSelectionne.effets
                                else:
                                    if sortSelectionne.effets:
                                        tabEffets = [sortSelectionne.effets[0]]
                                    else:
                                        tabEffets = []
                                # Liste des effets dont on va prévisualiser la zone.
                                for effet in tabEffets:
                                    if joueurCibleDirect is not None:
                                        if joueurCibleDirect.aEtatsRequis(
                                                effet.etatRequisCibleDirect):
                                            if effet.aPorteZone(caseX, caseY, nCase,
                                                                nLigne, self.tourDe.posX,
                                                                self.tourDe.posY):
                                                tabCasesPrevi.append(
                                                    [nCase, nLigne])
                                    else:
                                        if not effet.etatRequisCibleDirect:
                                            if effet.aPorteZone(caseX, caseY, nCase, nLigne, self.tourDe.posX, self.tourDe.posY) and effet.typeZone.showPrevisu:
                                                tabCasesPrevi.append(
                                                    [nCase, nLigne])
                                if self.cachedPrevisu[0] == sortSelectionne and \
                                   self.cachedPrevisu[1] == caseX and \
                                   self.cachedPrevisu[2] == caseY:
                                    previsuToShow = self.cachedPrevisu[3]
                                else:
                                    for joueur in self.joueurs:
                                        joueur.msgsPrevisu = []
                                    previsuToShow = sortSelectionne.lance(self.tourDe.posX,
                                                                          self.tourDe.posY,
                                                                          self, caseX, caseY,
                                                                          self.tourDe)
                                    self.cachedPrevisu = [
                                        sortSelectionne, caseX, caseY, previsuToShow]
                    # Afficher les cases glyphees
                    for glyphe in self.glyphes:
                        if glyphe.actif():
                            if glyphe.aPorte(nCase, nLigne):
                                pygame.draw.rect(fenetre, glyphe.couleur,
                                                 Rect(nCase*constantes.taille_sprite+1,
                                                      nLigne *constantes.taille_sprite+1,
                                                      constantes.taille_sprite-4,
                                                      constantes.taille_sprite-4))
                    for piege in self.pieges:
                        if piege.lanceur.team == self.tourDe.team or not piege.invisible:
                            if piege.aPorteDeclenchement(nCase, nLigne):
                                pygame.draw.rect(fenetre, piege.couleur,
                                                 Rect(nCase*constantes.taille_sprite+1,
                                                      nLigne * constantes.taille_sprite+1,
                                                      constantes.taille_sprite-4,
                                                      constantes.taille_sprite-4))
                            if piege.getDistanceDuPoint(nCase, nLigne) == 0:
                                piegeIcone = pygame.image.load(piege.icone).convert_alpha()
                                fenetre.blit(piegeIcone, (nCase*constantes.taille_sprite+1, nLigne *
                                                          constantes.taille_sprite+1))
                    for rune in self.runes:
                        if rune.centreX == nCase and rune.centreY == nLigne:
                            pygame.draw.rect(fenetre, rune.couleur,
                                             Rect(nCase*constantes.taille_sprite+1, nLigne *
                                                  constantes.taille_sprite+1,
                                                  constantes.taille_sprite-4,
                                                  constantes.taille_sprite-4))
                joueurOnCase = self.getJoueurSur(nCase, nLigne)
                if joueurOnCase is not None:
                    if joueurOnCase.aEtat("Invisible"):
                        if joueurOnCase.team == self.tourDe.team:
                            fenetre.blit(self.team1, (pixelX, pixelY))
                    else:
                        fenetre.blit(self.team1, (pixelX, pixelY))
                nCase += 1
            nLigne += 1

        # Affichage des cases dans la zone d'impact
        if sortSelectionne is not None:
            for case in tabCasesPrevi:
                pixelX, pixelY = self.grid2pixel(case[0], case[1])
                fenetre.blit(
                    self.zone, (pixelX, pixelY))
        else:
            # si pas de sort sélectionné et souris sur la grille on prévisualise un déplacement.
            if mouseXY[1] < constantes.y_sorts:
                caseX, caseY = self.pixel2grid(mouseXY)
                # Calcul du déplacement
                joueurPointe = self.getVisualationJoueurSur(caseX, caseY)
                if joueurPointe is None:
                    tabCasesPrevi = self.pathfinder.pathFinding(
                        self, caseX, caseY, self.tourDe)
                    if tabCasesPrevi is not None:
                        if len(tabCasesPrevi) <= self.tourDe.PM:
                            nbPATacle, nbPMTacle = self.calculTacle(self.tourDe)
                            cumulTacle = [0, 0]
                            for i, case in enumerate(tabCasesPrevi):
                                pxl_x, pxl_y = self.grid2pixel(case[0], case[1])
                                if nbPMTacle > 0 or nbPATacle > 0:
                                    cumulTacle[0] += nbPMTacle
                                    cumulTacle[1] += nbPATacle
                                if cumulTacle[0] + i+1 > self.tourDe.PM or \
                                   cumulTacle[1] > self.tourDe.PA:
                                    fenetre.blit(self.previsionTacle,
                                                 (pxl_x,
                                                  pxl_y))
                                else:
                                    fenetre.blit(self.previsionDeplacement,
                                                 (pxl_x,
                                                  pxl_y))
                                if cumulTacle[0] != 0 or cumulTacle[1] != 0:
                                    pixelX, pixelY = self.grid2pixel(caseX, caseY)
                                    self.tourDe.vue = Overlays.VueForOverlay(
                                        self.fenetre, pixelX,
                                        pixelY,
                                        30, 30, self.tourDe)
                                    self.tourDe.setOverlayTextGenerique(
                                        "-"+str(cumulTacle[0])+"PM\n-"+str(cumulTacle[1])+"PA")
                                    pixelX, pixelY = self.grid2pixel(self.tourDe.posX, self.tourDe.posY)
                                    self.tourDe.overlay.afficher(
                                        pixelX,
                                        pixelY)
                                nbPATacle, nbPMTacle = self.calculTacle(
                                    self.tourDe, case[0], case[1])
                else:
                    tabCasesPrevi = self.getZoneDeplacementJoueur(
                        joueurPointe)
                    if tabCasesPrevi is not None:
                        for case in tabCasesPrevi:
                            pixelX, pixelY = self.grid2pixel(case[0], case[1])
                            fenetre.blit(self.previsionDeplacement,
                                         (pixelX,
                                          pixelY))

        for jdp in previsuToShow:
            joueur = jdp
            pixelX, pixelY = self.grid2pixel(jdp.posX, jdp.posY)
            afficherLeJoueur = True
            if joueur.aEtat("Invisible"):
                if joueur.team != self.tourDe.team:
                    afficherLeJoueur = False
            if afficherLeJoueur:
                image = pygame.image.load(joueur.icone).convert_alpha()
                #image.fill((255, 255, 0, 10), None, pygame.BLEND_RGBA_MULT)
                fenetre.blit(image, (pixelX, pixelY))

        # Afficher joueurs
        for joueur in self.joueurs:
            pixelX, pixelY = self.grid2pixel(joueur.posX, joueur.posY)
            afficherLeJoueur = True
            if joueur.aEtat("Invisible"):
                if joueur.team != self.tourDe.team:
                    afficherLeJoueur = False
            if afficherLeJoueur:
                if joueur.team == 1:
                    fenetre.blit(self.team1, (pixelX, pixelY))
                else:
                    fenetre.blit(self.team2, (pixelX, pixelY))

                joueur.vue = Overlays.VueForOverlay(
                    self.fenetre, pixelX, pixelY, 30, 30, joueur)
                for joueurPrevisualiser in previsuToShow:
                    if joueurPrevisualiser.uid == joueur.uid:
                        if len(joueurPrevisualiser.msgsPrevisu) > 0:
                            joueur.setOverlayTextGenerique(
                                "\n".join(joueurPrevisualiser.msgsPrevisu))
                            pixelX, pixelY = self.grid2pixel(joueur.posX, joueur.posY)
                            joueur.overlay.afficher(
                                pixelX, pixelY)
                fenetre.blit(pygame.image.load(
                    joueur.icone).convert_alpha(), (pixelX, pixelY))
            else:
                pixelX, pixelY = self.grid2pixel(joueur.derniere_action_posX, joueur.derniere_action_posY)
                joueur.vue = Overlays.VueForOverlay(
                    self.fenetre, pixelX, pixelY, 30, 30, joueur)
                fenetre.blit(pygame.image.load(
                    joueur.icone).convert_alpha(), (pixelX, pixelY))

        # AfficherOverlays
        if mouseXY[1] > constantes.y_sorts:
            for sort in self.tourDe.sorts:
                if not sort.lancableParJoueur:
                    continue
                try:
                    if sort.vue.isMouseOver(mouseXY):
                        sort.overlay.afficher(sort.vue.posX, constantes.y_sorts)
                except AttributeError as exception:
                    print("Erreur Overlay de sort pour le sort :"+str(sort.nom)+\
                        " du joueur "+str(self.tourDe.classe)+" / "+str(exception))
        else:
            for joueur in self.joueurs:
                afficherLeJoueur = True
                if joueur.aEtat("Invisible"):
                    if joueur.team != self.tourDe.team:
                        afficherLeJoueur = False
                if joueur.vue.isMouseOver(mouseXY) and afficherLeJoueur:
                    if sortSelectionne is None:
                        joueur.setOverlayText()
                    pixelX, pixelY = self.grid2pixel(joueur.posX, joueur.posY)
                    joueur.overlay.afficher(
                        pixelX, pixelY)                    


    def poseGlyphe(self, glyphe):
        """@summary: Méthode permettant de poser une glyphe
        @glyphe: La glyphe à ajouter au niveau
        @type: Glyphe

        @return: L'indice d'ajout de la glype"""
        self.glyphes.append(glyphe)
        if glyphe.actif():
            casesDansPorte = self.getZonePorteSort(
                glyphe.sortMono, glyphe.centreX, glyphe.centreY, 0)
            for effet in glyphe.sortMono.effets:
                ciblesTraitees = []
                for caseDansPorte in casesDansPorte:
                    if glyphe.aPorte(caseDansPorte[0], caseDansPorte[1]):
                        cibleDansPorte = self.getJoueurSur(
                            caseDansPorte[0], caseDansPorte[1])
                        if cibleDansPorte is not None:
                            if cibleDansPorte not in ciblesTraitees:
                                _, cibles = self.lancerEffet(
                                    effet, glyphe.centreX, glyphe.centreY,
                                    glyphe.sortMono.nom, cibleDansPorte.posX,
                                    cibleDansPorte.posY, glyphe.lanceur)
                                ciblesTraitees += cibles
        return len(self.glyphes)-1

    def posePiege(self, piege):
        """@summary: Méthode permettant de poser un piège
        @piege: Le piège à ajouter au niveau
        @type: Piege

        @return: L'indice d'ajout du piège"""
        # Deux pièges ne peuvent pas être superposés.
        for piegeExistants in self.pieges:
            if piegeExistants.getDistanceDuPoint(piege.centreX, piege.centreY) == 0:
                return None
        # Ajout du piège
        self.pieges.append(piege)
        return len(self.pieges)-1

    def poseRune(self, rune):
        """@summary: Méthode permettant de poser une rune
        @rune: La rune à ajouter au niveau
        @type: Rune

        @return: L'indice d'ajout de la rune"""
        self.runes.append(rune)
        return len(self.runes)-1

    def getVoisins(self, noeud):
        """@summary: Retourne les cases vides existantes adjacentes à une case donnée
        @posX: La coordonnée x de la case dont on veut les voisins
        @type: int
        @posY: La coordonnée y de la case dont on veut les voisins
        @type: int

        @return: la liste des cases voisines vides à celle donnée"""
        voisins = []
        posToTest = []
        posX = noeud.posX
        posY = noeud.posY
        if posX > 0:
            posToTest.append([posX-1, posY])
        if posX < constantes.taille_carte-1:
            posToTest.append([posX+1, posY])
        if posY > 0:
            posToTest.append([posX, posY-1])
        if posY < constantes.taille_carte-1:
            posToTest.append([posX, posY+1])
        for pos in posToTest:
            if self.structure[pos[1]][pos[0]].type == "v":
                joueurSur = self.getJoueurSur(pos[0], pos[1])
                if joueurSur is None:
                    voisins.append(Noeud(pos[0], pos[1], 0, 0, noeud))
                else:
                    if joueurSur.aEtat("Invisible") and \
                    joueurSur.team != self.tourDe.team:
                        voisins.append(Noeud(pos[0], pos[1], 0, 0, noeud))
        return voisins

    def getJoueurAvecUid(self, uid):
        """@summary: retourne le joueur avvec l'uid donné"""
        for joueur in self.joueurs:
            if joueur.uid == uid:
                return joueur
        return None
        
