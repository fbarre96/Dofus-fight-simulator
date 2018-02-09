# -*- coding: utf-8 -*
import Personnages
import Zones
import constantes
import pygame
import Overlays
import Effets
import Etats
import Sort
from pygame.locals import *

class Noeud:
    """@summary: Classe servant à l'algorithme de recherche de chemin A*"""
    def __init__(self,x,y,cout=0,heur=0):
        """@summary: Initialise un noeud du graphe.
        @x: la cordonné x du noeud dans le graphe
        @type: int
        @y: la cordonné y du noeud dans le graphe
        @type: int
        @cout: le coût calculé pour parvenir à ce noeud, 0 par défaut
        @type: int
        @heur: l'heuristique calculé pour parvenir à ce noeud, 0 par défaut
        @type: int"""

        self.x = x
        self.y = y
        self.cout = cout
        self.heur = heur
    
def compare2Noeuds(n1, n2):
    """@summary: Fonction comparant deux noeuds du graphe.
        @n1: le premier noeud à comparer
        @type: Noeud
        @n2: le second noeud à comparer
        @type: Noeud
        @return: 1 si le premier noeud à la plus petite heuristique, -1 si le second à la plus petite heuristique et 0 si les deux sont égales"""

    if n1.heur < n2.heur:
        return 1
    elif n1.heur == n2.heur:
        return 0
    else:
        return -1

def ajoutTrie(liste,noeud):
        """@summary: Fonction ajoutant un noeud dans une liste triée.
        @liste: la liste de noeud trié
        @type: liste [Noeuds]
        @noeud: le noeud à insérer dans la liste triée.
        @type: Noeud"""

        liste.append(noeud)
        liste.sort(cmp=compare2Noeuds)

class Glyphe:
    """@summary: Classe décrivant une glyphe dans le jeu Dofus.
     Une glyphe est une zone au sol qui déclenche un effet sur les joueurs se trouvant dessus au début de leur tour."""
    def __init__(self, nomSort, sortMono, dureeGlyphe, centre_x, centre_y, lanceur, couleur):
        """@summary: Initialise une glyphe.
        @nomSort: le nom du sort à l'origine de la glyphe
        @type: string
        @sortMono: le sort qui va s'activer au début du tour du joueur qui se tient sur la glyphe. Le sort va être lancé sur le joueur dans la glyphe dont c'est le tour uniquement.
        @type: Sort
        @dureeGlyphe: Le nombre de début de tour du poseur que la glyphe va vivre
        @type: int
        @centre_x: la coordonnée x du centre de la zone de la glyphe.
        @type: int
        @centre_y: la coordonnée y du centre de la zone de la glyphe.
        @type: int
        @lanceur: le joueur ayant posé la glyphe.
        @type: Joueur
        @couleur: la coordonnée x du centre de la zone de la glyphe.
        @type: tuple (R,G,B)"""
        self.nomSort = nomSort
        self.sortMono = sortMono
        self.duree = dureeGlyphe
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.lanceur = lanceur
        self.couleur = couleur

    def actif(self):
        """@summary: Test si la glyphe est encore active
            @return: Retourne un booléen qui vaut vrai si la glyphe est encore active, faux sinon"""
        return self.duree > 0

class Case:
    """@summary: Classe décrivant une case de la grille du niveau."""
    def __init__(self, typ, hitbox):
        """@summary: initialise une case.
            @typ: le type de la case ("v" pour vide, ou "j" pour joueur) 
            @type: string (de une lettre)
            @hitbox: la hitbox de la case. Possède une fonction pour savoir si un point est dans la case.
            @type: Rect (pygame.locals)
            """
        self.type = typ
        self.hitbox = hitbox
        self.effetsSur = []

class Niveau:
    """@summary: Classe permettant de créer un niveau"""
    def __init__(self, fenetre, joueurs,font):
        """@summary: initialise le niveau.
            @fenetre: la fenêtre créé par pygame
            @type: fenêtre pygame
            @joueurs: tous les joueurs/mosntres qui doivent être placé sur la carte au début du combat.
            @type: tableau de Joueur
            @font: décrit une police d'écriture pygame
            @type: Font de pygame"""

        #Le double tableau qui décrit les lignes de case la grilel de jeus
        self.structure = None
        #le nombre de case sur un côté de la carte (carré)
        self.taille = constantes.taille_carte
        #Un tableau des cordonnées de départs possibles pour la team 1
        self.departT1 = [[5,5]]
        #Un tableau des cordonnées de départs possibles pour la team 2
        self.departT2 = [[8,8]]
        self.joueurs = joueurs
        #Le joueur qui commence est à la position 0 du tableau des joueurs
        self.tourIndex = 0
        #Le joueur dont c'est le tour
        self.tourDe = self.joueurs[self.tourIndex]
        #liste des glyphes
        self.glyphes=[]
        self.fenetre = fenetre
        self.myfont = font
        #Generer la carte
        self.generer()
        #Initialise tous les joueurs
        self.initJoueurs()

    

    def Deplacement(self, mouse_xy):
        """@summary: Le joueur dont c'est le tour a cliqué sur la carte sans sort sélectionné.
                      Un déplacement vers cette case est tenté
            @mouse_xy: la position de la souris sur la fenêtre pygame
            @type: tableau [int,int] cordonnées x,y de la souris."""
        case_x = mouse_xy[0]/constantes.taille_sprite
        case_y = mouse_xy[1]/constantes.taille_sprite
        joueur = self.tourDe
        cases = self.pathFinding(case_x,case_y,joueur)
        #cases vaut None si aucun chemin n'a été trouvé par l'algorithme A*
        if cases != None:
            #Les cases à parcourir pour se rendre à la position souhaitée donnent un nombre de PM nécessaire.
            if len(cases)<=joueur.PM:
                #On effectue le déplacement
                joueur.PM -= len(cases)
                self.structure[joueur.posY][joueur.posX].type = "v"
                for case in cases:
                    #Le joueur se déplace case par case et non pas en téléportation
                    joueur.bouge(case[0],case[1])
                self.structure[joueur.posY][joueur.posX].type = "j"
                print "PA : "+str(joueur.PA)
                print "PM : "+str(joueur.PM)
            else:
                print "Deplacement  impossible ("+str(joueur.PM)+" PM restants)."
        else:
            print "Deplacement impossible ("+str(joueur.PM)+" PM restants)."

    @staticmethod
    def getCasesAXDistanceDe(case_x,case_y,distance):
        """@summary: Méthode statique qui renvoie toutes les cases se trouvant sur un anneau de rayon donné autour d'une case.
            @case_x: la coordonnée x de la case centrale
            @type: int
            @case_y: la coordonnée y de la case centrale
            @type: int
            @distance: le rayon de l'anneau dont l'on veut obtenir les cases
            @type: int

            @return:  Les cases sur l'anneau de rayon donné listées gauche à droite puis de haut en bas """
        departX = case_x
        departY = case_y
        #La variable qui sera renvoyée
        retour = []
        # Cas de base
        if distance == 0:
            return [[case_x,case_y]]

        #la logique de cette fonction est le parcours de l'anneau en partant du centre et en s'en écartant progressivement.
        # pour chaque colonne, 2 cases sont sur le bon rayon sauf sur les deux colonnes aux extrêmes de l'anneau où il n'y en a qu'une. 
        #Ces deux colonne seront traitées séparemment des colonnes centrales. 

        #Le delta représente l'écart au centre en cordonnée X, Plus on s'éloigne du centre, plus l'écart en ordonnée se réduit
        delta = 0
        #Obligé de faire delta 0 (colonne centrale) a la main pour éviter l'ajout de la ligne de delta +0 et delta -0
        #Test si la coordonnée x est dans le grille de jeu
        if departX-delta >=0:
            #Test si la case haute de la colonne centre de l'anneau est dans le grille de jeu
            if departY-distance+delta>=0:
                retour.append([departX-delta, departY-distance+delta])
            #Test si la case basse de la colonne centre de l'anneau est dans le grille de jeu
            if departY+distance-delta<constantes.taille_carte:
                retour.append([departX-delta, departY+distance-delta])

        #Eloignement du centre de 1 en 1 jusqu'au rayon donné -1
        for delta in xrange(1,distance):
            #On test si la colonne souhaitée à gauche du centre est dans la grille de jeu
            if departX-delta >=0:
                #On test si la ligne souhaitée en haut à gauche du centre est dans la grille de jeu
                if departY-distance+delta>=0:
                    retour.append([departX-delta, departY-distance+delta])
                #On test si la ligne souhaitée en bas à gauche du centre est dans la grille de jeu
                if departY+distance-delta<constantes.taille_carte:
                    retour.append([departX-delta, departY+distance-delta])
            #On test si la colonne souhaitée à droite est dans la grille de jeu
            if departX+delta < constantes.taille_carte:
                #On test si la ligne souhaitée en haut à droite du centre est dans la grille de jeu
                if departY-distance+delta>=0:
                    retour.append([departX+delta, departY-distance+delta])
                #On test si la ligne souhaitée en bas à droite du centre est dans la grille de jeu
                if departY+distance-delta<constantes.taille_carte:
                    retour.append([departX+delta, departY+distance-delta])

        delta=distance
        #Oblige de faire delta distance à la main car sur les colonnes les plus loins du centre il ny à q'une ligne à ajouter.
        #Test si la coordonnée x extême gauche est dans le grille de jeu
        if departX-delta >=0:
            #Test si la coordonnée y est dans le grille de jeu
            if departY-distance+delta>=0:
                retour.append([departX-delta, departY-distance+delta])
        #Test si la coordonnée extême drotie x est dans le grille de jeu
        if departX+delta >=0:
            #Test si la coordonnée y est dans le grille de jeu
            if departY-distance+delta>=0:
                retour.append([departX+delta, departY-distance+delta])

        #Return Les cases trouvées
        return retour

    def afficherSorts(self):
        """@summary: Méthode qui affiche les icônes des sorts sur la fenêtre."""

        #Réinitialisation de la zone des sorts en noir
        pygame.draw.rect(self.fenetre, pygame.Color(0, 0, 0), pygame.Rect(constantes.x_sorts, constantes.y_sorts, constantes.width_sorts, constantes.height_sorts))
        #Création d'une surface grise semi-transparente pour la poser par dessus les sorts inutilisables
        surfaceGrise = pygame.Surface((30   ,30), pygame.SRCALPHA)   # La surface avec la couche de transparance ALPHA
        surfaceGrise.fill((128,128,128,128))                         # Le tuple RGB + l'alpha
        
        x = constantes.x_sorts
        y = constantes.y_sorts
        #Pour chaque sort du joueur dont c'est le tour on va afficher son icône + son état de jouabilité
        for sort in self.tourDe.sorts:
            #On ajoute l'overlay sur le sort, l'overlay est ce qui s'affichera lorsque le sort sera survolé avec la souris.
            sort.vue = Overlays.VueForOverlay(self.fenetre, x, y, 30, 30,sort)
            #On tente de récupérer l'image du sort
            try:
                imageSort = pygame.image.load(sort.image).convert() # charge l'image
                self.fenetre.blit(imageSort, (x,y))                 # colle l'image sur la zone 
            except:
                pass
            #On récupère si le sort est jouable
            res,explication,coutPA = sort.estLancable(self,self.tourDe,None)
            #Si le sort n'est pas lançable alors:
            if res == False:
                #On le grise
                self.fenetre.blit(surfaceGrise, (x,y))
                #Si c'est une question de nombre de tour entre deux lancé:
                if "avant prochain lance" in explication:
                    #On affiche le nombre de tour restant
                    delai = int(explication.split(":")[1])
                    delaiLabel = self.myfont.render(str(delai), 1, (0,0,0))
                    self.fenetre.blit(delaiLabel, (x, y))
            #Les sorts sont collés les uns à côtés des autres, séparés par 30 pixels
            x+=30
            #Si on est arrivé au bout de la fenêtre, on descend d'une ligne
            if(x+30>constantes.x_sorts+constantes.width_sorts):
                y+=30
                x=constantes.x_sorts
    
    def initJoueurs(self):
        """@summary: Initialise les joueurs sur le niveau (positionnement)."""
        placeT1 = 0
        placeT2 = 0
        for joueur in self.joueurs:
            #Placement différent entre les deux teams
            if joueur.team == 1:
                #On positionne le joueur sur le premier emplacement de spawn
                joueur.posX = self.departT1[placeT1][0]
                joueur.posY = self.departT1[placeT1][1]
                #Prochain spawn
                placeT1+=1
                #On initialise l'historique de déplacement du joueur avec sa pos de début de tour et début de combat
                joueur.posDebTour = [joueur.posX, joueur.posY]
                joueur.posDebCombat = [joueur.posX, joueur.posY]
            else:
                joueur.posX = self.departT2[placeT2][0]
                joueur.posY = self.departT2[placeT2][1]
                placeT2+=1
                joueur.posDebTour = [joueur.posX, joueur.posY]
                joueur.posDebCombat = [joueur.posX, joueur.posY]
            self.structure[joueur.posY][joueur.posX].type="j"

    def rafraichirGlyphes(self, duJoueur):
        """@summary: Rafraîchit la durée des glyphes et supprime celles qui ne sont plus actives.
                    Cette fonction est appelé au début de chaque tour.
            @duJoueur: On rafraîchit uniquement les glyphes posés par ce joueur.
            @type: Joueur"""
        i=0
        longueurTab = len(self.glyphes)
        #Parcours des glyphes
        while i < longueurTab:
            #On teste si la glyphe appartient à celui qui vient de débuter son tour
            if self.glyphes[i].lanceur == duJoueur:
                #Si la glyphe était active, on réduit sa durée
                if self.glyphes[i].actif():
                    self.glyphes[i].duree -= 1 # Réduction du temps restant
                    #Test si la glyphe est terminée
                    if(self.glyphes[i].duree <= 0):
                        #Si c'est le cas on la supprime
                        del self.glyphes[i]
                        i-=1
            #On recalcule la taille du tableau
            longueurTab = len(self.glyphes)
            i+=1
    
    def finTour(self):
        """@summary: Appelé lorsqu'un joueur finit son tour."""
        #On annonce au joueur la fin de son tour
        self.tourDe.finTour(self)
        #calcul du prochain joueur
        self.tourIndex = (self.tourIndex + 1) % len(self.joueurs)
        self.tourDe = self.joueurs[self.tourIndex]
        #On annonce au joueur son début de tour
        self.tourDe.debutTour(self)
        
    def tue(self, perso):
        """@summary: Tue instantanément le joueur donné en paramètre."""
        print perso.classe+" est mort!"
        #Parcours des joueurs
        i= 0 
        while i < xrange(len(self.joueurs)):
            #Recherche du joueur à tuer
            if self.joueurs[i] == perso:
                #On supprime son existence
                self.structure[perso.posY][perso.posX].type="v"
                del self.joueurs[i]
                i-=1
                break
            i+=1

    def generer(self):
        """@summary: Méthode permettant de générer le niveau.
        On crée une liste générale, contenant une liste par ligne à afficher""" 

        structure_niveau=[]
        for i in xrange(self.taille):
            ligne_niveau = []
            for j in xrange(self.taille):
                x = j * constantes.taille_sprite
                y = i * constantes.taille_sprite
                #Toutes les cases sont initialisées à vide
                ligne_niveau.append(Case("v", pygame.draw.rect(self.fenetre, (0,0,0), [x , y, constantes.taille_sprite, constantes.taille_sprite])))
            #On ajoute la ligne à la liste du niveau
            structure_niveau.append(ligne_niveau)
        #On sauvegarde cette structure
        self.structure = structure_niveau

    def getJoueurSur(self, case_x,case_y):
        """@summary: Retourne le joueur se trouvant sur la case donnée.
        @case_x: La coordonnée x de la case dont on veut récupérer le joueur
        @type: int
        @case_y: La coordonnée y de la case dont on veut récupérer le joueur
        @type: int

        @return: Joueur si la case est occupée, None sinon""" 
        for i,joueur in enumerate(self.joueurs):
            if joueur.posX == case_x and joueur.posY == case_y:
                return self.joueurs[i]
        return None

    def joueursAvecEtat(self,nomEtatCherche):
        """@summary: Retourne les joueurs possédant un état donné.
        @nomEtatCherche: Le nom de l'état que les joueurs doivent posséder
        @type: string

        @return: Un tableau contenant les joueurs possédant l'état donné""" 
        retourListeJoueurs = []
        for joueur in self.joueurs:
            for etat in joueur.etats:
                if etat.nom == nomEtatCherche:
                    retourListeJoueurs.append(joueur)
        return retourListeJoueurs

    def invoque(self,invoc,case_x,case_y):
        """@summary: Invoque un nouveau joueur dans la partie
        @invoc: le joueur à invoquer
        @type: Joueur
        @case_x: la coordonnée x de la case sur laquelle le joueur sera invoqué.
        @type: int
        @case_y: la coordonnée y de la case sur laquelle le joueur sera invoqué.
        @type: int""" 
        print "Invocation "+invoc.classe
        self.structure[case_y][case_x].type = "j"
        invoc.posX = case_x
        invoc.posY = case_y
        for i in xrange(len(self.joueurs)):
            if self.joueurs[i] == self.tourDe:
                self.joueurs.insert(i+1, invoc)
                break

    def getZoneEffet(self, effet, case_x,case_y):
        """@summary: Retourne un tableau des cases présentes dans la zone de l'effet donné.
                     Les cases sont triées par distances croissantes par rapport au centre de l'effet.
        @effet: l'effet dont on prendra la zone
        @type: Effet
        @case_x: la coordonnée x de la case sur laquelle l'effet devrait être lancé.
        @type: int
        @case_y: la coordonnée y de la case sur laquelle l'effet devrait être lancé.
        @type: int

        @return: Tableau de coordonnées [int x,int y] cases sont triées par distances croissantes par rapport au centre de l'effet.""" 
        tab_cases_zone = []
        x0 = case_x
        y0 = case_y
        # La taille de la zone n'indique pas forcément la distance la plus lointaine au centre, on parcourt donc toutes la carte en partant du centre
        for tailleCercle in xrange(64):
            casesAXDistance = Niveau.getCasesAXDistanceDe(case_x,case_y,tailleCercle)
            for case in casesAXDistance:
                # Test si la case trouvée est à porté de l'effet.
                if effet.APorteZone(case_x,case_y,case[0],case[1], self.tourDe.posX, self.tourDe.posY):
                    tab_cases_zone.append(case)
        return tab_cases_zone

    def getZonePorteSort(self, sort, x0, y0, poLanceur):
        """@summary: Retourne un tableau des cases présentes dans la portée du sort
                     Les cases sont triées par distances croissantes par rapport au centre de l'effet.
        @sort: le sort dont on calcul les cases à portées
        @type: Sort
        @x0: la coordonnée x de la case depuis laquelle le sort est lancé
        @type: int
        @y0: la coordonnée y de la case depuis laquelle le sort est lancé
        @type: int
        @poLanceur: les points de portées supplémentaires du lanceur qui peuvent influencer sur la portée du sort.
        @type: int

        @return: Tableau de coordonnées [int x,int y] cases sont triées par distances croissantes par rapport au centre du sort.""" 
        tab_cases_zone = []
        #La portée maximale * 2 (pour les sorts diagonales) donne la limite d'exploration des cases
        for tailleCercle in xrange(sort.POMin,sort.POMax*2+1):
            casesAXDistance = Niveau.getCasesAXDistanceDe(x0,y0,tailleCercle)
            for case in casesAXDistance:
                if sort.APorte(x0,y0,case[0],case[1], poLanceur):
                    tab_cases_zone.append(case)
        return tab_cases_zone    

    def __determinerSensPousser(self,joueurCible,depuisX,depuisY):
        """@summary: Retourne des données permettant de calculer le sens dans lequel un joueur sera poussé.
        @joueurCible: le joueur qui va être poussé
        @type: Joueur
        @depuisX: la coordonnée x depuis laquelle le joueur se fait poussé. Si None est donné, c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        @type: int
        @depuisY: la coordonnée y depuis laquelle le joueur se fait poussé. Si None est donné, c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        @type: int

        @return: horizontal (booléen vrai si la poussé se fait vers la gauche ou la droite), positif (1 si la poussé est vers le bas -1 si vers le haut).""" 
        
        #On ne peut pas pousser le pousseur
        if depuisY == joueurCible.posY and depuisX == joueurCible.posX:
            return None,None
        #Si None est donné, c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        if depuisY == None:
            depuisY = self.tourDe.posY-1
        if depuisX == None:
            depuisX = self.tourDe.posX
        #Calcul de la direction de la poussée
        horizontal = not (joueurCible.posX == depuisX)
        if horizontal and joueurCible.posX > depuisX:
            positif = 1
        elif (not horizontal) and joueurCible.posY > depuisY:
            positif = 1
        else:
            positif = -1 
        return horizontal,positif

    def __effectuerPousser(self,joueurCible,doDeg,posPouX,posPouY,D,pousseur):
        """@summary: Déplace la cible après les calculs de poussé.
        @joueurCible: le joueur qui va être poussé
        @type: Joueur
        @doDeg: Indique si la poussé appliquera des dommages (L'attirance étant une poussé inversé, elle ne cause pas de dommage)
        @type: booléen
        @posPouX: la coordonnée x sur laquelle le joueur poussé va arriver (voir la fonction __calculerArrivePousser)
        @type: int
        @posPouY: la coordonnée y sur laquelle le joueur poussé va arriver (voir la fonction __calculerArrivePousser)
        @type: int
        @D: le nombre de cases que le joueur aurait dû parcourir mais qui ont été bloqué par un obstacle (voir la fonction __calculerArrivePousser)
        @type: int
        @pousseur: Le joueur qui pousse
        @type: Joueurs""" 

        #Déplacement du joueur
        self.structure[joueurCible.posY][joueurCible.posX].type = "v"
        joueurCible.bouge(posPouX,posPouY)
        self.structure[joueurCible.posY][joueurCible.posX].type = "j"
        #Calcul des dégâts
        R = 6
        if doDeg:
            doPou = pousseur.doPou
            # Intervention des états
            for etat in pousseur.etats:
                if etat.actif():
                    doPou = etat.triggerCalculPousser(doPou,self,pousseur,joueurCible)
            for etat in joueurCible.etats:
                if etat.actif():
                    doPou = etat.triggerCalculPousser(doPou,self,pousseur,joueurCible)
            # Calcul des dégâts
            total = (8+R*pousseur.lvl/50)*D+doPou
            if total > 0:
                print joueurCible.classe+" perd "+ str(total) + "PV (do pou)"
                joueurCible.subit(pousseur,self,total,"doPou")

    def pousser(self, nbCases, joueurCible,pousseur,doDeg=True,depuisX=None,depuisY=None):
        """@summary: Fonction à appeler pour pousser un joueur.
        @nbCases: le nombre de case dont il faut pousser la cible
        @type: int
        @joueurCible: Le joueur qui se fait pousser
        @type: Joueur
        @pousseur: Le joueur qui va pousser
        @type: Joueur
        @doDeg: Indique si la poussé appliquera des dommages (L'attirance étant une poussé inversé, elle ne cause pas de dommage)
        @type: booléen, True pas défaut
        @depuisX: la coordonnée x depuis laquelle le joueurCible se fera pousser,Si non renseigné None, ce sera la position du pousseur.
        @type: int
        @depuisY: la coordonnée y depuis laquelle le joueurCible se fera pousser,Si non renseigné None, ce sera la position du pousseur.
        @type: int"""
        horizontal,positif = self.__determinerSensPousser(joueurCible,depuisX,depuisY)
        if horizontal != None:
            posPouX,posPouY,D = self.__calculerArrivePousser(joueurCible, nbCases, int(horizontal), positif)
            self.__effectuerPousser(joueurCible,doDeg,posPouX,posPouY,D,pousseur)
        
    def __calculerArrivePousser(self, joueurCible, nbCases, horizontal, positif):
        """@summary: Fonction à appeler pour pousser un joueur.
        @joueurCible: Le joueur qui se fait pousser
        @type: Joueur
        @nbCases: le nombre de case dont il faut pousser la cible
        @type: int
        @horizontal: Indique si la poussé est horizontal ou verticales
        @type: booléen
        @positif: 1 si la poussé est vers la droite ou le bas, -1 si vers la gauche ou le hauts
        @type: int

        @return: posPouX  -> int indiquant la coordonnée x d'arrivé après poussé
                 ,posPouY -> int indiquant la coordonnée y d'arrivé après poussé
                 ,D       -> int indiquant le nombre de case non déplacé pour cause d'obstacle"""

        D = 0     #Nombre de cases obstacles cognés
        _posPouX = joueurCible.posX # position X validé pendant la poussé
        _posPouY = joueurCible.posY # position Y validé pendant la poussé
        #calcul de poussé de nbCases
        for fait in xrange(nbCases):
            #Calcul de la case d'arrivée après une poussée de 1 case
            posPouX = _posPouX # Variable temporaire pour tester l'arrivée X
            posPouY = _posPouY # Variable temporaire pour tester l'arrivée Y
            posPouX = posPouX + (1*positif*horizontal)
            posPouY = posPouY + (1*positif*((horizontal+1)%2))
            # test si la case d'arrivé est hors-map (compte comme un obstacle)
            if posPouX >= self.taille or posPouX < 0 or posPouY >= self.taille or posPouY < 0:
                D+=1 # Un obstacle tapé
                posPouY = _posPouY # La position n'est pas validé
                posPouX = _posPouX
            # test si la case d'arrivée n'est pas vide
            #Cas séparé de l'autre car indexError si hors-map
            elif self.structure[posPouY][posPouX].type != "v":
                D+=1 # Un obstacle tapé
                posPouY = _posPouY # La position n'est pas validé
                posPouX = _posPouX
            # Sinon la poussé
            else:
                _posPouX = posPouX # La position d'arrivé est bien sauvegardé
                _posPouY = posPouY
        return posPouX,posPouY,D

    def attire(self, nbCases, joueurCible, attireur):
        """@summary: Fonction à appeler pour attirer un joueur.
        @nbCases: le nombre de case dont il faut attirer la cible
        @type: int
        @joueurCible: Le joueur qui se fait attirer
        @type: Joueur
        @attireur: Le joueur qui va attirer
        @type: Joueur"""

        #Calcul du sens de l'attirence
        distanceX = abs(joueurCible.posX - attireur.posX)
        distanceY = abs(joueurCible.posY - attireur.posY)
        horizontal = distanceX > distanceY
        if horizontal:
            positif = joueurCible.posX > attireur.posX
        else:
            positif = joueurCible.posY > attireur.posY
        #Pour attirer, on peut pousser la cible vers non et ne pas compter les dégâts.
        if horizontal and positif:
            self.pousser(nbCases,joueurCible,attireur,False,joueurCible.posX+1,joueurCible.posY)
        elif horizontal:
            self.pousser(nbCases,joueurCible,attireur,False,joueurCible.posX-1,joueurCible.posY)
        elif not horizontal and positif:
            self.pousser(nbCases,joueurCible,attireur,False,joueurCible.posX,joueurCible.posY+1)
        else:
            self.pousser(nbCases,joueurCible,attireur,False,joueurCible.posX,joueurCible.posY-1)

    def __deplacementTFVersCaseVide(self,joueurBougeant, posAtteinte,AjouteHistorique):
        """@summary: Déplacement pouvant généré un téléfrag vers une case vide.
        @joueurBougeant: le joueur qui se déplace vers une case vide
        @type: Joueur
        @posAtteinte: La position que le joueur va atteindre
        @type: [int x, int y]
        @AjouteHistorique: indique si le déplacement compte dans l'historique. (Le passif du téléfrag n'a pas l'historique du déplacement par exemple)
        @type: booléen"""
        self.structure[posAtteinte[1]][posAtteinte[0]].type = "j"
        self.structure[joueurBougeant.posY][joueurBougeant.posX].type = "v"
        if AjouteHistorique:
            #La fonction bouge ajoute automatiquement à l'historique
            joueurBougeant.bouge(posAtteinte[0], posAtteinte[1])
        else:
            joueurBougeant.posX = posAtteinte[0]
            joueurBougeant.posY = posAtteinte[1]

    def __boostApresTF(self,nomSort,reelLanceur):
        """@summary: Tous les boost après un téléfrag sont généré ici
        @nomSort: le nom du sort à l'origine du Téléfrag
        @type: string
        @reelLanceur: Le joueur étant à l'origine du Téléfrag
        @type: Joueur"""

        #BoostSynchro
        synchros = self.getJoueurs("Synchro")
        for synchro in synchros:
            if not synchro.aEtat(nomSort) and nomSort != "Rembobinage" and not synchro.aEtat("DejaBoost"):
                synchro.appliquerEtat(Etats.Etat("Boost Synchro "+nomSort,0,-1, reelLanceur),reelLanceur)
                synchro.appliquerEtat(Etats.Etat("DejaBoost",0,1,[nomSort], reelLanceur),reelLanceur)
        #BoostGlas
        reelLanceur.appliquerEtat(Etats.EtatCoutPA("Glas",0,-1,u"Glas",-1),reelLanceur)

    def __exploserSynchro(self,synchro,reelLanceur):
        """@summary: Explose la synchro du xélor si elle est téléfragé
        @synchro: la synchro
        @type: Joueur de classe synchro
        @reelLanceur: Le joueur étant à l'origine de la synchro (le niveau du xélor est prit en compte dans les dégâts)
        @type: Joueur"""

        nbTF = 0 # Nombre de téléfrag qui boost la synchro
        for etat in synchro.etats:
            if etat.nom.startswith("Boost Synchro"):
                nbTF+=1
        #Explosion
        synchro.lanceSort(Sort.Sort("Fin_des_temps",0,0,0,[Effets.EffetDegats(int(reelLanceur.lvl*1.90)*(nbTF*2-1),int(reelLanceur.lvl*1.90)*(nbTF*2-1),"air",zone=Zones.TypeZoneCercle(3),cibles_possibles="Ennemis")], 99,99,0,0,"cercle"),self,synchro.posX,synchro.posY)
        self.tue(synchro)

    def __glypheActiveTF(self,reelLanceur,nomSort):
        """@summary: Active les glyphes qui s'activent après un téléfrag (Instabilité_temporelle)
        @reelLanceur: Le joueur étant à l'origine du téléfrag
        @type: Joueur
        @nomSort: le nom du sort qui est jeté
        @type: string"""
        for glyphe in self.glyphes:
            if glyphe.nomSort == "Instabilite_temporelle" and glyphe.actif() and reelLanceur == glyphe.lanceur and glyphe.sortMono.nom != nomSort:
                casesDansPorte = self.getZonePorteSort(glyphe.sortMono, glyphe.centre_x, glyphe.centre_y,0)
                for effet in glyphe.sortMono.effets:
                    ciblesTraitees = []
                    for caseDansPorte in casesDansPorte:
                        cibleDansPorte = self.getJoueurSur(caseDansPorte[0],caseDansPorte[1])
                        if cibleDansPorte != None:
                            if cibleDansPorte not in ciblesTraitees:
                                sestApplique, cibles=self.lancerEffet(effet,glyphe.centre_x,glyphe.centre_y, glyphe.sortMono.nom, cibleDansPorte.posX, cibleDansPorte.posY, glyphe.lanceur)
                                ciblesTraitees += cibles

    def __deplacementTFVersCaseOccupee(self, joueurASwap,joueurBougeant, posAtteinte, reelLanceur,nomSort, AjouteHistorique,genereTF):
        """@summary: Déplace le joueur en téléfrag vers une case avec un joueur.
        @joueurASwap: Le joueur qui occupe la case considéré comme occupé
        @type: Joueur
        @joueurBougeant: Le joueur qui se déplace en téléfrag vers la case occupé
        @type: string
        @posAtteinte: Les coordonnées de la case d'arrivée
        @type: [int x, int y]
        @reelLanceur: Le joueur étant à l'origine du téléfrag
        @type: Joueur
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @AjouteHistorique: Indique si le déplacement doit être conservé dans l'historique de déplacement du joueur
        @type: booléen
        @genereTF: Indique si l'état téléfrag est placé pour les deux joueurs
        @type: booléen"""

        self.__effectuerTF(joueurASwap,joueurBougeant,posAtteinte,reelLanceur,nomSort,AjouteHistorique,genereTF)
        #Si un téléfrag doit généré, il l'a été dans effectuerTF
        if genereTF:
            #Résultats d'un téléfrag (activation de glyphe, synchro, boost, et boost PA)
            #Si le xelor est pas deja boostPA par ce sort, rembo ne peut pas boost PA

            #Boost PA
            if not reelLanceur.aEtat(nomSort) and nomSort != "Rembobinage":
                reelLanceur.appliquerEtat(Etats.Etat("BoostPA",0,1,[2],reelLanceur),reelLanceur)
                reelLanceur.appliquerEtat(Etats.Etat(nomSort,0,1,["Telefrag"],reelLanceur),reelLanceur)
            #Boost Glas, Synchro
            self.__boostApresTF(nomSort,reelLanceur)
            #Test Explosion synchro
            if ("Synchro" == joueurBougeant.classe) and not reelLanceur.aEtat("Faille_temporelle"):
                self.__exploserSynchro(joueurBougeant,reelLanceur)
            elif ("Synchro" == joueurASwap.classe) and not reelLanceur.aEtat("Faille_temporelle"):
                self.__exploserSynchro(joueurASwap,reelLanceur)
            #Activation des glyphes qui s'activent après un téléfrag
            self.__glypheActiveTF(reelLanceur,nomSort)
 

    def __effectuerTF(self, joueurASwap,joueurBougeant,posAtteinte,reelLanceur,nomSort,AjouteHistorique,genereTF):
        """@summary: Echange les joueurs en téléfrag.
        @joueurASwap: Le joueur qui occupe la case considéré comme occupé
        @type: Joueur
        @joueurBougeant: Le joueur qui se déplace en téléfrag vers la case occupé
        @type: string
        @posAtteinte: Les coordonnées de la case d'arrivée
        @type: [int x, int y]
        @reelLanceur: Le joueur étant à l'origine du téléfrag
        @type: Joueur
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @AjouteHistorique: Indique si le déplacement doit être conservé dans l'historique de déplacement du joueur
        @type: booléen
        @genereTF: Indique si l'état téléfrag est placé pour les deux joueurs
        @type: booléen"""
        joueurASwap.bouge(joueurBougeant.posX, joueurBougeant.posY)
        if AjouteHistorique:
            joueurBougeant.bouge(posAtteinte[0], posAtteinte[1])
        else:
            joueurBougeant.posX = posAtteinte[0]
            joueurBougeant.posY = posAtteinte[1]
        if genereTF:
            joueurBougeant.retirerEtats("Telefrag")
            joueurASwap.retirerEtats("Telefrag")
            joueurBougeant.appliquerEtat(Etats.Etat("Telefrag",0,2,[nomSort],reelLanceur),reelLanceur)
            joueurASwap.appliquerEtat(Etats.Etat("Telefrag",0,2,[nomSort],reelLanceur),reelLanceur)

    def gereDeplacementTF(self, joueurBougeant, posAtteinte, lanceur, nomSort, AjouteHistorique=True, genereTF=True):
        """@summary: Fonction à appeler pour les déplacements pouvant créer un téléfrag.
        @joueurBougeant: Le joueur qui se déplace en téléfrag
        @type: string
        @posAtteinte: Les coordonnées de la case d'arrivée
        @type: [int x, int y]
        @lanceur: Le joueur étant à l'origine du téléfrag
        @type: Joueur
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @AjouteHistorique: Indique si le déplacement doit être conservé dans l'historique de déplacement du joueur
        @type: booléen, True par défaut
        @genereTF: Indique si l'état téléfrag est placé pour les deux joueurs
        @type: booléen, True par défaut

        @return: Renvoie le joueur qui a été impliqué dans le téléfrag s'il existe, None sinon"""

        #Test hors-map
        if posAtteinte[1]<0 or posAtteinte[1]>=constantes.taille_carte or posAtteinte[0]<0 or posAtteinte[0]>=constantes.taille_carte:
            return None
        #Test déplacement case vers vide
        if self.structure[posAtteinte[1]][posAtteinte[0]].type == "v":
            self.__deplacementTFVersCaseVide(joueurBougeant, posAtteinte,AjouteHistorique)
            return None
        #Test si sa case d'arrivé est occupé par un joueur
        elif self.structure[posAtteinte[1]][posAtteinte[0]].type == "j":
            #Si C'est une invoccation, c'est l'invocateur le réel lanceur
            if lanceur.invocateur != None:
                reelLanceur = lanceur.invocateur
            else:
                reelLanceur = lanceur

            joueurSwap = joueurASwap = self.getJoueurSur(posAtteinte[0],posAtteinte[1])
            if joueurASwap != joueurBougeant:
                self.__deplacementTFVersCaseOccupee(joueurASwap,joueurBougeant, posAtteinte, reelLanceur,nomSort, AjouteHistorique,genereTF)
                return joueurASwap
        else:
            print "Deplacement pas implemente"
        return None

    def __appliquerEffetSansBoucleSurZone(self,effet,joueurLanceur,case_cible_x,case_cible_y,nomSort,ciblesTraitees,prov_x,prov_y):
        """@summary: Fonction qui applique un effet ayant une zone sans la prendre en compte (les glyphes).
        @effet: L'effet qu'il faut appliquer
        @type: Effet
        @joueurLanceur: Le joueur à l'origine de l'effet
        @type: Joueur
        @case_cible_x: Coordonné x de la case ciblé
        @type: int
        @case_cible_y: Coordonné y de la case ciblé
        @type: int
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @ciblesTraitees: La liste des cibles déjà traitées pour cet effet
        @type: tableau de Joueur
        @prov_x: Coordonné x de la case d'origine de l'effet
        @type: int
        @prov_y: Coordonné y de la case d'origine de l'effet
        @type: int

        @return: Renvoie True si l'effet a été appliqué, False sinon"""
        if type(effet) == type(Effets.EffetGlyphe(None,None,None,None)):
            effet.appliquerEffet(self,None,joueurLanceur, case_cible_x=case_cible_x, case_cible_y=case_cible_y, nom_sort=nomSort, cibles_traitees=ciblesTraitees, prov_x=prov_x, prov_y=prov_y)
            return True
        return False

    def __appliquerEffetSurZone(self,zoneEffet,effet,joueurLanceur,joueurCibleDirect,case_cible_x,case_cible_y,nomSort,ciblesTraitees,prov_x,prov_y):
        """@summary: Fonction qui applique un effet ayant une zone.
        @zoneEffet: la zone de l'effet
        @type: Effet
        @effet: L'effet qu'il faut appliquer
        @type: Effet
        @joueurLanceur: Le joueur à l'origine de l'effet
        @type: Joueur
        @joueurCibleDirect: Le joueur qui s'est fait ciblé pour lancé le sort
        @type: Joueur ou None si l'effet peut être fait au vide.
        @case_cible_x: Coordonné x de la case ciblé
        @type: int
        @case_cible_y: Coordonné y de la case ciblé
        @type: int
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @ciblesTraitees: La liste des cibles déjà traitées pour cet effet
        @type: tableau de Joueur
        @prov_x: Coordonné x de la case d'origine de l'effet
        @type: int
        @prov_y: Coordonné y de la case d'origine de l'effet
        @type: int

        @return: -Renvoie True si l'effet a été appliqué, False sinon
                 -Les cibles traitées avec les nouveaux joueurs ajoutés dedans"""

        sestApplique = False
        #Pour chaque case dans la zone
        for case_effet in zoneEffet:
            case_x = case_effet[0]
            case_y = case_effet[1]
            joueurCaseEffet = self.getJoueurSur(case_x, case_y) # récupération du joueur sur la case
            #Test si un joeuur est sur la case
            if joueurCaseEffet != None:
                #Si le joueur sur la case est une cible valide
                if effet.cibleValide(joueurLanceur, joueurCaseEffet,joueurCibleDirect,ciblesTraitees):
                    #On appliquer l'effet
                    ciblesTraitees.append(joueurCaseEffet)
                    effet.appliquerEffet(self,joueurCaseEffet,joueurLanceur, case_cible_x=case_cible_x, case_cible_y=case_cible_y, nom_sort=nomSort, cibles_traitees=ciblesTraitees, prov_x=prov_x, prov_y=prov_y)
                    sestApplique = True
                    #Peu import le type, l'etat requis est retire s'il est consomme
                    if effet.consommeEtat:
                        joueurCaseEffet.retirerEtats(effet.etatRequisCibleDirect)
                        joueurCaseEffet.retirerEtats(effet.etatRequisCibles)
            else:
                if effet.faireAuVide:
                    effet.appliquerEffet(self,None,joueurLanceur, case_cible_x=case_cible_x, case_cible_y=case_cible_y, nom_sort=nomSort, cibles_traitees=ciblesTraitees, prov_x=prov_x, prov_y=prov_y)
                    sestApplique = True
        return sestApplique, ciblesTraitees

    def lancerEffet(self, effet, prov_x, prov_y, nomSort, case_cible_x, case_cible_y, lanceur=None):
        """@summary: Fonction qui applique un effet.
        @effet: L'effet qu'il faut appliquer
        @type: Effet
        @prov_x: Coordonné x de la case d'origine de l'effet
        @type: int
        @prov_y: Coordonné y de la case d'origine de l'effet
        @type: int
        @nomSort: Le nom du sort qui a généré le téléfrag
        @type: string
        @case_cible_x: Coordonné x de la case ciblé
        @type: int
        @case_cible_y: Coordonné y de la case ciblé
        @type: int
        @lanceur: le lanceur de l'effet, None si le lanceur est sur prov_x;prov_y
        @type: Joueur, ou None

        @return: -Renvoie True si l'effet a été appliqué, False sinon
                 -Les cibles traitées avec les nouveaux joueurs ajoutés dedans"""

        if lanceur == None:
            joueurLanceur = self.getJoueurSur(prov_x,prov_y)
        else:
            joueurLanceur = lanceur
        ciblesTraitees = [] # initialisation des cibles déjà traitées
        joueurCibleDirect = self.getJoueurSur(case_cible_x, case_cible_y) # Le joueur cible direct est celui ciblé pour lancer le sort.
        #Si l'effet est lancé dynamiquement sur le lanceur, calcul de la pos cible
        if type(effet) is Effets.EffetDegatsPosLanceur or type(effet) is Effets.EffetTeleportePosPrecLanceur:
            case_cible_x = joueurLanceur.posX
            case_cible_y = joueurLanceur.posY

        zoneEffet = self.getZoneEffet(effet, case_cible_x,case_cible_y)
        #Effet non boucles
        sestApplique = self.__appliquerEffetSansBoucleSurZone(effet,joueurLanceur,case_cible_x,case_cible_y,nomSort,ciblesTraitees,prov_x,prov_y)
        if sestApplique == True:
            return sestApplique,ciblesTraitees
        return self.__appliquerEffetSurZone(zoneEffet,effet,joueurLanceur,joueurCibleDirect,case_cible_x,case_cible_y,nomSort,ciblesTraitees,prov_x,prov_y)

    def getJoueurs(self, cibles):
        """@summary: Retourne les joueurs correspondant à une liste de classes.
        @cibles: la liste des classes dont on cherche les représentants.
        @type: string, chaque classe séparé par des "|"

        @return: Renvoie la liste des joueurs correspondant à la liste de classes donnée.
        """
        onCherche = cibles.split("|")
        retour = []
        #if (joueurCaseEffet.team == joueurLanceur.team and joueurCaseEffet != joueurLanceur and effet.faireAuxAllies) or (joueurCaseEffet.team == joueurLanceur.team and joueurCaseEffet == joueurLanceur and effet.faireAuLanceur) or (joueurCaseEffet.team != joueurLanceur.team and effet.faireAuxEnnemis):
        for joueur in self.joueurs:
            if joueur.classe in onCherche:
                retour.append(joueur)
        return retour

    def getJoueurslesPlusProches(self, case_x,case_y,lanceur,zone=Zones.TypeZoneCercle(99),etatRequisCibles=[],ciblesPossibles=[],ciblesExclues=[],ciblesTraitees=[]):
        """@summary: Retourne les joueurs correspondant aux critères donnés triés par proximité.
        @case_x: la coordonnée x de la case de départ de la recherche 
        @type: int
        @case_y: la coordonnée y de la case de départ de la recherche 
        @type: int
        @lanceur: le lanceur de la recherche
        @type: Joueur
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

        @return: Renvoie la liste des joueurs correspondant aux cirtères données triés par proximité.
        """

        joueurs_cases_zone = []
        x0 = case_x
        y0 = case_y
        for tailleCercle in xrange(64):
            casesAXDistance = self.getCasesAXDistanceDe(case_x,case_y,tailleCercle)
            #Pour chaque case à distance 0, puis 1, puis 2 etc...
            for case in casesAXDistance:
                #Si la case est dans le critère de zone
                if zone.testCaseEstDedans([case_x,case_y],case,None):
                    # S'il y a un joueur sur la case
                    joueur = self.getJoueurSur(case[0],case[1])
                    if joueur != None:
                        #Test des conditions 
                        if (joueur.team == lanceur.team and joueur != lanceur and "Allies" in ciblesPossibles) or (joueur.team == lanceur.team and joueur == lanceur and "Lanceur" in ciblesPossibles) or (joueur.team != lanceur.team and "Ennemis" in ciblesPossibles) or (joueur.classe in ciblesPossibles):
                            if not(joueur.classe in ciblesExclues or (joueur.classe == lanceur.classe and "Lanceur" in ciblesExclues)):
                                #Test sur l'etat requis.
                                if joueur.aEtatsRequis(etatRequisCibles):
                                    #Test si le joueur ciblé à déjà été impacté
                                    if joueur not in ciblesTraitees:
                                        joueurs_cases_zone.append(joueur)
        return joueurs_cases_zone

    def afficher(self, fenetre, sortSelectionne, mouse_xy):
        """@summary: Méthode permettant d'afficher le niveau"""

        #Chargement des images (seule celle de team contiennent de la transparence)
        vide1 = pygame.image.load(constantes.image_vide_1).convert()
        vide2 = pygame.image.load(constantes.image_vide_2).convert()
        team1 = pygame.image.load(constantes.image_team_1).convert_alpha()
        team2 = pygame.image.load(constantes.image_team_2).convert_alpha()
        prevision = pygame.image.load(constantes.image_prevision).convert()
        zone = pygame.image.load(constantes.image_zone).convert()
        glyphe_ou_piege = pygame.image.load(constantes.image_team_1).convert()
        #On parcourt la liste du niveau
        num_ligne = 0
        tab_cases_previ = []
        
        for ligne in self.structure:
            #Onparcourt les listes de lignes
            num_case = 0
            for sprite in ligne:
                #On calcule la position réelle en pixels
                x = num_case * constantes.taille_sprite
                y = num_ligne * constantes.taille_sprite
                if sprite.type == 'v' or sprite.type == 'j':          #v = Vide, j = joueur
                    if (num_case+(num_ligne*len(ligne)))%2 == 0:
                        fenetre.blit(vide1, (x,y))
                    else:
                        fenetre.blit(vide2, (x,y))
                    #Afficher les cases glyphees
                    for glyphe in self.glyphes:
                        if glyphe.actif():
                            if glyphe.sortMono.APorte(glyphe.centre_x, glyphe.centre_y, num_case, num_ligne, 0):
                                pygame.draw.rect(fenetre, glyphe.couleur, Rect(num_case*constantes.taille_sprite+1, num_ligne*constantes.taille_sprite+1,constantes.taille_sprite-2,constantes.taille_sprite-2))

                    #Afficher previsualation portee du sort selectionne
                    if sortSelectionne != None:
                        #Previsu de la porte du sort, une case teste par tour de double boucle
                        if sortSelectionne.APorte(self.tourDe.posX, self.tourDe.posY, num_case,num_ligne, self.tourDe.PO):
                            fenetre.blit(prevision, (x,y))
                        #Si la souris est sur la grille de jeu (et non pas dans les sorts)
                        if mouse_xy[1] < constantes.y_sorts:
                            case_x = mouse_xy[0]/constantes.taille_sprite
                            case_y = mouse_xy[1]/constantes.taille_sprite
                            #Si on cible une case dans la porte du sort il faut afficher la zone effet
                            if sortSelectionne.APorte(self.tourDe.posX, self.tourDe.posY, case_x,case_y, self.tourDe.PO):
                                joueurCibleDirect = self.getJoueurSur(case_x,case_y)
                                if sortSelectionne.chaine == False:
                                    tabEffets = sortSelectionne.effets
                                else:
                                    if len(sortSelectionne.effets)>0:
                                        tabEffets = [sortSelectionne.effets[0]]
                                    else:
                                        tabEffets=[]
                                #Liste des effets dont on va prévisualiser la zone.
                                for effet in tabEffets:
                                    if joueurCibleDirect != None:
                                        if joueurCibleDirect.aEtatsRequis(effet.etatRequisCibleDirect):
                                            if effet.APorteZone(case_x,case_y,num_case,num_ligne, self.tourDe.posX, self.tourDe.posY):
                                                tab_cases_previ.append([num_case,num_ligne])
                                    else:
                                        if len(effet.etatRequisCibleDirect)==0:
                                            if effet.APorteZone(case_x,case_y,num_case,num_ligne, self.tourDe.posX, self.tourDe.posY):
                                                tab_cases_previ.append([num_case,num_ligne])

                num_case+=1
            num_ligne+=1
        
        #Affichage des cases dans la zone d'impact
        if sortSelectionne != None:
            for case in tab_cases_previ:
                fenetre.blit(zone, (case[0]*constantes.taille_sprite,case[1]*constantes.taille_sprite))
        else:
            # si pas de sort sélectionné et souris sur la grille on prévisualise un déplacement.
            if mouse_xy[1] < constantes.y_sorts:
                case_x = mouse_xy[0]/constantes.taille_sprite
                case_y = mouse_xy[1]/constantes.taille_sprite
                #Calcul du déplacement
                tab_cases_previ = self.pathFinding(case_x,case_y,self.tourDe)
                if tab_cases_previ != None:
                    if len(tab_cases_previ) <= self.tourDe.PM:
                        for case in tab_cases_previ:
                            fenetre.blit(prevision, (case[0]*constantes.taille_sprite,case[1]*constantes.taille_sprite))


        #Afficher joueurs
        for joueur in self.joueurs:
            x = joueur.posX*constantes.taille_sprite
            y = joueur.posY*constantes.taille_sprite
            if joueur.team == 1:    
                fenetre.blit(team1, (x,y))
            else:
                fenetre.blit(team2, (x,y))
            joueur.vue = Overlays.VueForOverlay(self.fenetre, x, y, 30, 30,joueur)
            fenetre.blit(pygame.image.load(joueur.icone).convert_alpha(), (x,y))

        #AfficherOverlays
        if mouse_xy[1] > constantes.y_sorts:
            for sort in self.tourDe.sorts:
                if sort.vue.isMouseOver(mouse_xy):
                    sort.overlay.afficher(sort.vue.x,constantes.y_sorts)
        else:
            for joueur in self.joueurs:
                if joueur.vue.isMouseOver(mouse_xy):
                    joueur.overlay.afficher(joueur.posX*constantes.taille_sprite,joueur.posY*constantes.taille_sprite)

    def poseGlyphe(self,glyphe):
        """@summary: Méthode permettant de poser une glyphe
        @glyphe: La glyphe à ajouté au niveau
        @type: Glyphe

        @return: L'indice d'ajout de la glype"""
        self.glyphes.append(glyphe)
        return len(self.glyphes)-1



    def getVoisins(self,x,y):
        """@summary: Retourne les cases vides existantes adjacentes à une case donnée
        @x: La coordonnée x de la case dont on veut les voisins
        @type: int
        @y: La coordonnée y de la case dont on veut les voisins
        @type: int

        @return: la liste des cases voisines vides à celle donnée"""
        voisins = []
        if x > 0:
            if self.structure[y][x-1].type == "v":
                voisins.append(Noeud(x-1,y))
        if x < constantes.taille_carte-1:
            if self.structure[y][x+1].type == "v":
                voisins.append(Noeud(x+1,y))
        if y > 0:
            if self.structure[y-1][x].type == "v":
                voisins.append(Noeud(x,y-1))
        if y < constantes.taille_carte-1:
            if self.structure[y+1][x].type == "v":
                voisins.append(Noeud(x,y+1))
        return voisins

    def pathFinding(self, case_cible_x, case_cible_y, joueur):
        """@summary: Implémentation de l'algorithme A*. recherche de chemin depuis la position du joueur vers la case_cible
        @case_cible_x: La coordonnée x à laquelle on veut accéder
        @type: int
        @case_cible_y: La coordonnée y à laquelle on veut accéder
        @type: int
        @joueur: Le joueur qui veut se rendre sur la case cible depuis sa position
        @type: Joueur

        @return: la liste des cases composant le chemin pour accéder à la case cible depuis la position du joueur. None si aucun chemin n'a été trouvé"""

        # VOIR PSEUDO CODE WIKIPEDIA
        listeFermee = []
        listeOuverte = []
        if self.structure[case_cible_y][case_cible_x].type != "v":
            return None
        depart = Noeud(joueur.posX, joueur.posY)
        ajoutTrie(listeOuverte,depart)
        while len(listeOuverte) != 0:
            u = listeOuverte[-1]
            del listeOuverte[-1]
            if u.x == case_cible_x and u.y == case_cible_y:
                #reconstituerChemin(u,listeFermee)
                tab = []
                for case in listeFermee:
                    tab.append([case.x,case.y])
                if(len(tab)>0):
                    if tab[0][0] == joueur.posX and tab[0][1] == joueur.posY:
                        del tab[0]
                tab.append([u.x,u.y])
                return tab
            voisins = self.getVoisins(u.x,u.y)
            for v in voisins:
                v_existe_cout_inf = False
                for n in listeFermee+listeOuverte:
                    if n.x == v.x and n.y == v.y and n.cout < v.cout:
                        v_existe_cout_inf= True
                        break
                if not(v_existe_cout_inf):
                    v.cout = u.cout+1
                    v.heur = v.cout + (abs(v.x-case_cible_x)+abs(v.y-case_cible_y))
                    ajoutTrie(listeOuverte,v)
            listeFermee.append(u)
        print "Aucun chemin trouvee"
        return None
