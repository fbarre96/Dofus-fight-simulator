# -*- coding: utf-8 -*
"""@summary: Rassemble toutes les classes liées aux Overlay
"""
import pygame
from pygame.locals import Rect


class ColoredText(object):
    """@summary: Classe décrivant un texte coloré"""

    def __init__(self, texte, couleur):
        """@summary: Initialise un texte coloré
        @texte: le texte
        @type: string
        @couleur: la couleur à donner au texte
        @type: (R,G,B)"""
        self.texte = texte
        self.couleur = couleur


class Overlay(object):
    """@summary: Classe l'affiche de l'overlay"""
    pygame.font.init()
    fontTitre = pygame.font.SysFont("monospace", 15, True)
    fontContenu = pygame.font.SysFont("monospace", 15)

    def __init__(self, myobject, titre, contenu, couleurFond=(100, 100, 100, 128)):
        """@summary: initialise un overlay.
        @myobject: l'objet ayant un attribut "titre" de type ColoredText
                    et un attribut "contenu" de type ColoredText
        @type: Object
        @titre: le titre de l'overlay
        @type: string
        @contenu: le contenu de l'overlay
        @type: string
        @couleurFond: La couleur de fond de l'overlay RGBA (100,100,100,128 par défaut)
        @type: (R,G,B,A)
        """
        self.couleurFond = couleurFond
        self.titre = titre
        self.contenu = contenu
        self.myobject = myobject
        self.fenetre = None

    def render(self, texte, font, maxWidth):
        """@summary: initialise un overlay.
        @myobject: l'objet ayant un attribut "titre" de type
                    ColoredText et un attribut "contenu" de type ColoredText
        @type: Object
        @texte: le texte que l'on veut faire rentrer dans l'overlay
        @type: string
        @font: la police dans laquelle on veut afficher le texte
        @type: pygame font
        @maxWidth: la largeur maximale souhaitée pour le texte finale
                    (des sauts de lignes sotn ajoutés pour réduire la largeur)
        @type: int

        @return: -le tableau de ligne de texte qui rentreront dans la largeur demandées.
                 -la hauteur calculé une fois affiché
                 -la largeur calculé une fois affiché"""
        i = 0
        lignesTexte = []
        buff = ""
        calcWidth = 0
        # Pout toutes les lettres dans le texte à affiché
        while i < len(texte):
            # Quel taille fait la lettre dans la police donnée
            width, _ = font.size(texte[i])
            # Si la lettre ne rentre pas, retour à la ligne
            if width+calcWidth > maxWidth:
                calcWidth = 0
                lignesTexte.append(buff)
                buff = ""
            else:
                calcWidth += width
                buff += texte[i]
                i += 1
        # Ajout de la dernière ligne qui n'a pas atteint la taille maximale
        lignesTexte.append(buff)
        calcWidth, calcHeight = font.size(lignesTexte[0])
        return lignesTexte, calcHeight*len(lignesTexte), calcWidth

    def afficher(self, posX, posY):
        """@summary: affiche l'overlay sur la position donnée
        @posX: la coordonnée x du pixel sur lequel se trouvera
                le coin supérieur gauche de l'overlay.
        @type: int
        @posY: la coordonnée y du pixel sur lequel se trouvera
                le coin supérieur gauche de l'overlay.
        @type: int

        @return: -le tableau de ligne de texte qui rentreront dans la largeur demandées.
                 -la hauteur calculé une fois affiché
                 -la largeur calculé une fois affiché"""

        maxWidth = 215  # largeur de l'overlay
        # titre de l'overlay
        titreTexte = getattr(self.myobject, self.titre.texte)
        #  contenu de l'overlay
        contenuTexte = getattr(self.myobject, self.contenu.texte)
        # Conversion en string si ce n'est pas déjà le cas.
        if not isinstance(titreTexte, str):
            titreTexte = str(titreTexte)
        if not isinstance(contenuTexte, str):
            contenuTexte = str(contenuTexte)
        # Découpage du titre pour qu'il rendre dans l'overlay
        lignesTitre, heightTitre, widthTitre = self.render(
            titreTexte, Overlay.fontTitre, maxWidth)
        # Découpage du contenu pour qu'il rendre dans l'overlay
        lignesContenu, heightContenu, widthContenu = self.render(
            contenuTexte, Overlay.fontContenu, maxWidth)
        # calcul des dimensions de l'overlay
        height = heightTitre + heightContenu
        width = widthTitre if widthTitre > widthContenu else widthContenu
        # Affichage du background de l'overlay
        background = pygame.Surface(
            (width+10, height+10), pygame.SRCALPHA)   # per-pixel alpha
        # notice the alpha value in the color
        background.fill(self.couleurFond)
        # Calcul de la position de l'overlay si la souris est trop à droite de l'écran.
        posToPutX = posX
        if posToPutX+maxWidth+10 >= self.fenetre.get_width():
            posToPutX = self.fenetre.get_width() - maxWidth-10

        ###Affichage###
        # collage du fond
        self.fenetre.blit(background, (posToPutX, (posY-height-10)))
        nextHeight = 0
        # collage du titre découpé
        for ligne in lignesTitre:
            titreSurface = Overlay.fontTitre.render(
                ligne, 1, self.titre.couleur)
            # +5 et -10 pour avoir un padding
            self.fenetre.blit(titreSurface, (posToPutX +
                                             5, (posY-height-10)+5+nextHeight))
            nextHeight += titreSurface.get_height()
        # collage du contenu découpé
        for ligne in lignesContenu:
            contenuSurface = Overlay.fontTitre.render(
                ligne, 1, self.contenu.couleur)
            # +5 et -10 spour avoir un padding
            self.fenetre.blit(contenuSurface, (posToPutX +
                                               5, (posY-height-10)+5+nextHeight))
            nextHeight += titreSurface.get_height()


class VueForOverlay(object):
    """@summary: Classe provoquant un affichage d'overlay quand survolé par la souris"""

    def __init__(self, fenetre, posX, posY, width, height, objectWithOverlay):
        """@summary: initialise une vue déclenchant un overlay.
        @fenetre: la fenêtre pygame
        @type: pygame fenêtre
        @posX: la position posX du composant
        @type: int
        @posY: la position posY du composant
        @type: int
        @width: la largeur du composant
        @type: int
        @height: la hauteur du composant
        @type: int
        @objectWithOverlay: l'object qui a un attribut overlay de type Overlay
        @type: Object"""
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.fenetre = fenetre
        self.hitbox = Rect(posX, posY, width, height)
        self.objectWithOverlay = objectWithOverlay
        self.objectWithOverlay.overlay.fenetre = fenetre

    def isMouseOver(self, mouseXY):
        """@summary: Indique si la souris survole le composant
        @mouseXY: la position de la souris
        @type: tableau de coordonnée [int x, int y]

        @return: True si les coordonnées passées en paramètres sont sur le composant décrit"""
        return self.hitbox.collidepoint(mouseXY)
