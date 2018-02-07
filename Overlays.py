import pygame
from pygame.locals import *
class ColoredText(object):
    def __init__(self,texte,couleur):
        self.texte = texte
        self.couleur = couleur
class Overlay(object):
    pygame.font.init()
    fontTitre = pygame.font.SysFont("monospace", 15,True)
    fontContenu = pygame.font.SysFont("monospace", 15)
    def __init__(self,myobject,titre,contenu,couleurFond=(100,100,100,128)):
        self.couleurFond = couleurFond
        self.titre=titre
        self.contenu=contenu
        self.myobject = myobject
        self.fenetre = None

    def render(self, texte, font, maxWidth):
        i=0
        lignesTexte=[]
        buff=""
        calcWidth = 0
        nextWidth = 0
        h=0
        while i < len(texte):
            w,h=font.size(texte[i])
            if w+calcWidth > maxWidth:
                calcWidth = 0
                lignesTexte.append(buff)
                buff = ""
            else:
                calcWidth+=w
                buff+=texte[i]
                i+=1
        lignesTexte.append(buff)
        calcWidth,calcHeight = font.size(lignesTexte[0])
        return lignesTexte,calcHeight*len(lignesTexte),calcWidth

    def afficher(self,x,y):
        maxWidth = 215
        titreTexte = getattr(self.myobject, self.titre.texte)
        contenuTexte = getattr(self.myobject, self.contenu.texte)
        if not type(titreTexte) is str and not type(titreTexte) is unicode:
            titreTexte = str(titreTexte)
        if not type(contenuTexte) is str and not type(contenuTexte) is unicode:
            contenuTexte = str(contenuTexte)
        lignesTitre,heightTitre,widthTitre=self.render(titreTexte,Overlay.fontTitre,maxWidth)
        lignesContenu,heightContenu,widthContenu=self.render(contenuTexte,Overlay.fontContenu,maxWidth)
        height = heightTitre + heightContenu
        width = widthTitre if widthTitre>widthContenu else widthContenu
        background = pygame.Surface((width+10  ,height+10), pygame.SRCALPHA)   # per-pixel alpha
        background.fill(self.couleurFond)                      # notice the alpha value in the color
        pos_to_put_x = x
        if pos_to_put_x+maxWidth+10 >= self.fenetre.get_width():
            pos_to_put_x = self.fenetre.get_width() - maxWidth-10
        self.fenetre.blit(background, (pos_to_put_x,(y-height-10)))
        nextHeight = 0
        for ligne in lignesTitre:
            titreSurface=Overlay.fontTitre.render(ligne, 1, self.titre.couleur)
            self.fenetre.blit(titreSurface, (pos_to_put_x+5, (y-height-10)+5+nextHeight))
            nextHeight+=titreSurface.get_height()
        for ligne in lignesContenu:
            contenuSurface=Overlay.fontTitre.render(ligne, 1, self.contenu.couleur)
            self.fenetre.blit(contenuSurface, (pos_to_put_x+5, (y-height-10)+5+nextHeight))
            nextHeight+=titreSurface.get_height()
class VueForOverlay(object):
    def __init__(self,fenetre,x,y,width,height,objectWithOverlay):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.fenetre=fenetre
        self.hitbox = Rect(x, y, width, height)
        self.objectWithOverlay = objectWithOverlay
        self.objectWithOverlay.overlay.fenetre = fenetre
    def isMouseOver(self,mouse_xy):
        return self.hitbox.collidepoint(mouse_xy)
    def printOverlay(self,mouse_xy):
        if not self.isMouseOver(mouse_xy):
            return None
        titre = objectToOverlay.overlay.titre
        description = objectToOverlay.overlay.description
