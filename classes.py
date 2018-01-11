# -*- coding: utf-8 -*
from zones import *
from constantes import *
import pygame
from pygame.locals import *
import random
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

class Etat(object):
    def __init__(self, nom, debDans, duree, lanceur=None,tabCarac=[],desc=""):
        self.nom = nom
        self.duree = duree
        self.debuteDans = debDans
        self.tabCarac = tabCarac
        self.description = desc
        self.lanceur = lanceur
        self.desc = desc
    def deepcopy(self):
        return Etat(self.nom, self.debuteDans, self.duree, self.lanceur,self.tabCarac, self.desc)

    def actif(self):
        return self.debuteDans <= 0 and self.duree != 0

    def triggerRafraichissement(self,personnage,niveau):
        pass
    def triggerAvantCalculDegats(self, dommages, baseDeg, caracs,nomSort):
        return dommages,baseDeg,caracs
    def triggerApresCalculDegats(self,total,typeDeg):
        return total
    def triggerAvantSubirDegats(self,cibleAttaque,niveau,totalPerdu,typeDegats,attaquant):
        pass
    def triggerApresSubirDegats(self,cibleAttaque,niveau,attaquant):
        pass
    def triggerDebutTour(self,personnage,niveau):
        pass
    def triggerFinTour(self,personnage,niveau):
        pass
    def triggerCoutPA(self, sort, coutPAActuel):
        return coutPAActuel
    def triggerCalculPousser(self,doPou,niveau,pousseur,joueurCible):
        return doPou
    def triggerInstantane(self, **kwargs):
        pass
    def triggerAvantRetrait(self,personnage):
        pass

class EtatActiveSort(Etat):
    def __init__(self, nom, debDans,duree, sort,lanceur=None,desc=""):
        self.sort = sort
        super(EtatActiveSort, self).__init__(nom,debDans, duree, lanceur,desc)

    def deepcopy(self):
        return EtatActiveSort(self.nom, self.debuteDans,self.duree,  self.sort, self.lanceur,self.desc)

    def triggerRafraichissement(self, personnage,niveau):
        #print "Rafraichissement de active sort : "+personnage.classe+" lance "+self.sort.nom + " sur sa pose."
        personnage.lanceSort(self.sort,niveau,personnage.posX,personnage.posY)

class EtatRedistribuerPer(Etat):
    def __init__(self, nom, debDans,duree, pourcentage, tailleZone,lanceur=None,desc=""):
        self.pourcentage = pourcentage
        self.tailleZone = tailleZone
        super(EtatRedistribuerPer, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        return EtatRedistribuerPer(self.nom, self.debuteDans,self.duree,  self.pourcentage, self.tailleZone, self.lanceur,self.desc)

    def triggerAvantSubirDegats(self,cibleAttaque,niveau,totalPerdu,typeDegats,attaquant):
        cibleAttaque.lanceSort(Sort("Redistribution",0,0,0,[EffetDegats(totalPerdu,totalPerdu,typeDegats,zone=TypeZoneCercle(self.tailleZone),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur")],99,99,0,0,"cercle"), niveau, cibleAttaque.posX, cibleAttaque.posY)

class EtatBoostPA(Etat):
    def __init__(self, nom, debDans,duree,  boostPA,lanceur=None,desc=""):
        self.boostPA = boostPA
        super(EtatBoostPA, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        return EtatBoostPA(self.nom, self.debuteDans,self.duree,  self.boostPA, self.lanceur,self.desc)

    def triggerRafraichissement(self, personnage,niveau):
        self.triggerInstantane(joueurCaseEffet=personnage)
    def triggerInstantane(self,**kwargs):
        personnage = kwargs.get("joueurCaseEffet")
        personnage.PA += self.boostPA
        print "Modification de PA:"+str(self.boostPA)
        print "PA : "+str(personnage.PA)
        print "PM : "+str(personnage.PM)

class EtatBoostPM(Etat):
    def __init__(self, nom, debDans,duree,  boostPM,lanceur=None,desc=""):
        self.boostPM = boostPM
        super(EtatBoostPM, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        return EtatBoostPM(self.nom, self.debuteDans, self.duree, self.boostPM, self.lanceur,self.desc)

    def triggerRafraichissement(self, personnage,niveau):
         self.triggerInstantane(joueurCaseEffet=personnage)

    def triggerInstantane(self,**kwargs):
        personnage = kwargs.get("joueurCaseEffet")
        personnage.PM += self.boostPM
        print "Modification de PM:"+str(self.boostPM)
        print "PA : "+str(personnage.PA)
        print "PM : "+str(personnage.PM)

class EtatBoostPO(Etat):
    def __init__(self, nom, debDans,duree,  boostPO,lanceur=None,desc=""):
        self.boostPO = boostPO
        super(EtatBoostPO, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        return EtatBoostPO(self.nom, self.debuteDans, self.duree, self.boostPO, self.lanceur,self.desc)

    def triggerRafraichissement(self, personnage,niveau):
         self.triggerInstantane(joueurCaseEffet=personnage)

    def triggerInstantane(self,**kwargs):
        personnage = kwargs.get("joueurCaseEffet")
        personnage.PM += self.boostPO
        print "Modification de PO:"+str(self.boostPO)

class EtatBoostVita(Etat):
    def __init__(self, nom, debDans,duree,  boostVita,lanceur=None,desc=""):
        self.boostVita = boostVita
        super(EtatBoostVita, self).__init__(nom,debDans, duree, lanceur,desc)

    def deepcopy(self):
        return EtatBoostVita(self.nom, self.debuteDans,self.duree,  self.boostVita, self.lanceur,self.desc)

    def triggerRafraichissement(self, personnage,niveau):
        self.triggerInstantane(joueurCaseEffet=personnage)

    def triggerInstantane(self,**kwargs):
        personnage = kwargs.get("joueurCaseEffet")
        pourcentageBoost = self.boostVita
        self.boostVita = int(personnage._vie * (pourcentageBoost/100.0))
        personnage.vie += self.boostVita
        print "Modification de Vitalite:"+str(self.boostVita)

    def triggerAvantRetrait(self,personnage):
        personnage.vie -= self.boostVita
        print "Modification de Vitalite: -"+str(self.boostVita)

class EtatBoostDoPou(Etat):
    def __init__(self, nom,  debDans, duree,boostDoPou,lanceur=None,desc=""):
        self.boostDoPou = boostDoPou
        super(EtatBoostDoPou, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        return EtatBoostDoPou(self.nom, self.debuteDans,self.duree,  self.boostDoPou, self.lanceur,self.desc)

    def triggerCalculPousser(self,doPou,niveau, pousseur, joueurCible):
        return doPou+self.boostDoPou

class EtatBoostDommage(Etat):
    def __init__(self, nom, debDans, duree, boostDommage,lanceur=None,desc=""):
        self.boostDommage = boostDommage
        super(EtatBoostDommage, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        return EtatBoostDommage(self.nom,  self.debuteDans,self.duree, self.boostDommage, self.lanceur,self.desc)

    def triggerAvantCalculDegats(self,dommages, baseDeg, caracs,nomSort):
        return dommages+self.boostDommage, baseDeg, caracs
class EtatBoostPerDommageSorts(Etat):
    def __init__(self, nom, debDans, duree, boostDommage,lanceur=None,desc=""):
        self.boostDommage = boostDommage
        super(EtatBoostPerDommageSorts, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        return EtatBoostPerDommageSorts(self.nom,  self.debuteDans,self.duree, self.boostDommage, self.lanceur,self.desc)

    def triggerApresCalculDegats(self, total,typeDeg):
        if typeDeg != "doPou":
            return total+int(total*(self.boostDommage/100.0))
        return total
class EtatBoostPuissance(Etat):
    def __init__(self, nom, debDans,duree,  boostPuissance,lanceur=None,desc=""):
        self.boostPuissance = boostPuissance
        super(EtatBoostPuissance, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        return EtatBoostPuissance(self.nom,  self.debuteDans, self.duree,self.boostPuissance, self.lanceur,self.desc)

    def triggerAvantCalculDegats(self,dommages, baseDeg, caracs,nomSort):
        return dommages, baseDeg, caracs+self.boostPuissance

class EtatBoostBaseDeg(Etat):
    def __init__(self, nom,  debDans, duree,nomSort,boostbaseDeg,lanceur=None,desc=""):
        self.boostbaseDeg = boostbaseDeg
        self.nomSort=nomSort
        super(EtatBoostBaseDeg, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        return EtatBoostBaseDeg(self.nom,  self.debuteDans, self.duree, self.nomSort, self.boostbaseDeg,self.lanceur,self.desc)

    def triggerAvantCalculDegats(self,dommages, baseDeg, caracs, nomSort):
        if nomSort == self.nomSort:
            baseDeg += self.boostbaseDeg
        return dommages, baseDeg, caracs

class EtatLanceSortSiSubit(Etat):
    def __init__(self, nom, debDans,duree,  sort,lanceur=None,desc=""):
        self.sort = sort
        super(EtatLanceSortSiSubit, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        return EtatLanceSortSiSubit(self.nom, self.debuteDans,self.duree,  self.sort, self.lanceur,self.desc)

    def triggerApresSubirDegats(self,cibleAttaque,niveau,attaquant):
        cibleAttaque.lanceSort(self.sort, niveau, cibleAttaque.posX, cibleAttaque.posY)

class EtatEffetFinTour(Etat):
    def __init__(self, nom,  debDans,duree, effet, nomSort,quiLancera,lanceur=None,desc=""):
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        super(EtatEffetFinTour, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        return EtatEffetFinTour(self.nom, self.debuteDans,self.duree,  self.effet,self.nomSort,self.quiLancera, self.lanceur,self.desc)

    def triggerFinTour(self,personnage,niveau):
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet,personnage.posX,personnage.posY,self.nomSort, personnage.posX, personnage.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet,personnage.posX,personnage.posY,self.nomSort, personnage.posX, personnage.posY, personnage)

class EtatEffetDebutTour(Etat):
    def __init__(self, nom,  debDans,duree, effet, nomSort,quiLancera,lanceur=None,desc=""):
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        super(EtatEffetDebutTour, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        return EtatEffetDebutTour(self.nom, self.debuteDans,self.duree,  self.effet,self.nomSort,self.quiLancera, self.lanceur,self.desc)

    def triggerDebutTour(self,personnage,niveau):
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet,personnage.posX,personnage.posY,self.nomSort, personnage.posX, personnage.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet,personnage.posX,personnage.posY,self.nomSort, personnage.posX, personnage.posY, personnage)

class EtatRetourCaseDepart(Etat):
    def __init__(self, nom, debDans, duree, lanceur=None,desc=""):
        super(EtatRetourCaseDepart, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        return EtatRetourCaseDepart(self.nom, self.debuteDans,self.duree, self.lanceur,self.desc)

    def triggerFinTour(self,personnage,niveau):
        niveau.gereDeplacementTF(personnage,personnage.posDebTour,personnage,self.nom,AjouteHistorique=True)

class EtatCoutPA(Etat):
    def __init__(self, nom, debDans,duree,  nomSortAffecte,modCoutPA, lanceur=None,desc=""):
        self.modCoutPA = modCoutPA
        self.nomSortAffecte = nomSortAffecte
        super(EtatCoutPA, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        return EtatCoutPA(self.nom, self.debuteDans,self.duree,  self.nomSortAffecte, self.modCoutPA,self.lanceur,self.desc)

    def triggerCoutPA(self, sort, coutPAActuel):
        if sort.nom == self.nomSortAffecte:
            coutPAActuel += self.modCoutPA
        return coutPAActuel

class EtatModDegPer(Etat):
    def __init__(self, nom, debDans, duree, pourcentage, lanceur=None,desc=""):
        self.pourcentage = pourcentage
        super(EtatModDegPer, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        return EtatModDegPer(self.nom, self.debuteDans,self.duree,  self.pourcentage,self.lanceur,self.desc)

    def triggerApresCalculDegats(self, total,typeDeg):
        if typeDeg != "doPou":
            return (total * self.pourcentage)/100
        return total
class EtatContre(Etat):
    def __init__(self, nom, debDans,duree, pourcentage, tailleZone,lanceur=None,desc=""):
        self.pourcentage = pourcentage
        self.tailleZone = tailleZone
        super(EtatContre, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        return EtatContre(self.nom, self.debuteDans,self.duree,  self.pourcentage, self.tailleZone, self.lanceur,self.desc)

    def triggerAvantSubirDegats(self,cibleAttaque,niveau,totalPerdu,typeDegats,attaquant):
        if cibleAttaque.team != attaquant.team:
            distance = abs(attaquant.posX-cibleAttaque.posX)+abs(attaquant.posY-cibleAttaque.posY)
            if distance == 1:
                cibleAttaque.lanceSort(Sort("Contre",0,0,0,[EffetDegats(totalPerdu,totalPerdu,typeDegats,zone=TypeZoneCercle(self.tailleZone),cibles_possibles="Ennemis")],99,99,0,0,"cercle"), niveau, self.posX, self.posY)

class EtatRepousserSiSubit(Etat):
    def __init__(self, nom, debDans,duree, nbCase,lanceur=None,desc=""):
        self.nbCase = nbCase
        super(EtatRepousserSiSubit, self).__init__(nom, duree, debDans,lanceur,desc)

    def deepcopy(self):
        return EtatRepousserSiSubit(self.nom, self.debuteDans,self.duree,  self.nbCase,self.lanceur,self.desc)

    def triggerAvantSubirDegats(self,cibleAttaque,niveau,totalPerdu,typeDegats,attaquant):
        niveau.pousser(self.nbCase,attaquant,cibleAttaque, True, cibleAttaque.posX, cibleAttaque.posY)

class EtatEffetSiSubit(Etat):
    def __init__(self, nom,  debDans,duree,effet,nomSort,quiLancera,typeDeg="",lanceur=None,desc=""):
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        self.typeDeg = typeDeg
        super(EtatEffetSiSubit, self).__init__(nom,debDans, duree, lanceur,desc)

    def deepcopy(self):
        return EtatEffetSiSubit(self.nom, self.debuteDans,self.duree,  self.effet, self.nomSort,self.quiLancera,self.typeDeg,self.lanceur,self.desc)

    def triggerAvantSubirDegats(self,cibleAttaque,niveau,totalPerdu,typeDegats,attaquant):
        if totalPerdu >0 and (self.typeDeg == typeDegats or self.typeDeg==""):
            if self.quiLancera == "lanceur":
                niveau.lancerEffet(self.effet,attaquant.posX,attaquant.posY,self.nomSort, attaquant.posX, attaquant.posY, self.lanceur)
            elif self.quiLancera == "cible":
                niveau.lancerEffet(self.effet,cibleAttaque.posX,cibleAttaque.posY,self.nomSort, attaquant.posX, attaquant.posY, attaquant)
class EtatEffetSiPousse(Etat):
    def __init__(self, nom,  debDans,duree,effet,nomSort,quiLancera,lanceur=None,desc=""):
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        super(EtatEffetSiPousse, self).__init__(nom,debDans, duree, lanceur,desc)

    def deepcopy(self):
        return EtatEffetSiPousse(self.nom, self.debuteDans,self.duree,  self.effet, self.nomSort,self.quiLancera,self.lanceur,self.desc)

    def triggerCalculPousser(self,doPou,niveau,pousseur,cibleAttaque):
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet,self.lanceur.posX,cibleAttaque.posY,self.nomSort, cibleAttaque.posX, cibleAttaque.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet,cibleAttaque.posX,cibleAttaque.posY,self.nomSort, cibleAttaque.posX, cibleAttaque.posY, cibleAttaque)
        return doPou
class EtatTelefrag(Etat):
    def __init__(self, nom,  debDans,duree, nomSort, lanceur=None,desc=""):
        self.nomSort = nomSort
        super(EtatTelefrag, self).__init__(nom,  debDans,duree,lanceur,desc)

    def deepcopy(self):
        return EtatTelefrag(self.nom, self.debuteDans,self.duree,  self.nomSort,self.lanceur,self.desc)

    def triggerAvantRetrait(self, personnage):
        if self.nomSort == "Momification":
            self.lanceur.appliquerEtat(EtatBoostPuissance("Momification",0,2,100,self.lanceur),self.lanceur)

class Effet(object):
    def __init__(self,**kwargs):
        self.etatRequisCibleDirect = kwargs.get('etat_requis',"").split("|")
        if self.etatRequisCibleDirect[-1] == "":
            self.etatRequisCibleDirect = []
        self.etatRequisCibles = kwargs.get('etat_requis_cibles',"").split("|")
        if self.etatRequisCibles[-1] == "":
            self.etatRequisCibles = []
        self.consommeEtat = kwargs.get('consomme_etat',False)
        self.ciblesPossibles = kwargs.get('cibles_possibles',"Allies|Ennemis|Lanceur").split("|")
        self.ciblesExclues = kwargs.get('cibles_exclues',"").split("|")
        self.faireAuVide = kwargs.get('faire_au_vide',False)
        self.typeZone = kwargs.get('zone',TypeZoneCercle(0))

    def cibleValide(self, joueurLanceur, joueurCible,joueurCibleDirect, ciblesDejaTraitees):
        if (joueurCible.team == joueurLanceur.team and joueurCible != joueurLanceur and "Allies" in self.ciblesPossibles) or (joueurCible.team == joueurLanceur.team and joueurCible == joueurLanceur and "Lanceur" in self.ciblesPossibles) or (joueurCible.team != joueurLanceur.team and "Ennemis" in self.ciblesPossibles) or (joueurCible.classe in self.ciblesPossibles):
            if joueurCible.classe in self.ciblesExclues or (joueurCible.classe == joueurLanceur.classe and "Lanceur" in self.ciblesExclues):
                #print "DEBUG : Invalide : Cible Exclue"
                return False
            if joueurCible in ciblesDejaTraitees:
                #print "DEBUG : Invalide : Cible deja traitee"
                return False
            if (joueurCibleDirect == None and len(self.etatRequisCibleDirect)!=0):
                #print "DEBUG : Invalide : Cible direct non renseigne et etatRequis pour cible direct ("+str(self.etatRequisCibleDirect)+")"
                return False
            if (joueurCibleDirect == None and not self.faireAuVide):
                #print "DEBUG : Invalide : Cible direct non renseigne et pas faire au vide"
                return False    
            if (joueurCible == None and len(self.etatRequisCibles)!=0):
                #print "DEBUG : Invalide : Cible  non renseigne et etatRequis pour cible"
                return False
            if joueurCible != None:
                if not joueurCible.aEtatsRequis(self.etatRequisCibles):
                    #print "DEBUG : Invalide :etatRequis pour cible non present"
                    return False
            if joueurCibleDirect != None:
                if not joueurCibleDirect.aEtatsRequis(self.etatRequisCibleDirect):
                    #print "DEBUG : Invalide :etatRequis pour cible direct non present"
                    return False
            return True
        #print u"DEBUG : Invalide : Cible "+joueurCible.classe +u" pas dans la liste des cibles possibles ("+unicode(self.ciblesPossibles)+u")"
        return False

    def APorteZone(self, departZone_x,departZone_y, testDansZone_x,testDansZone_y, j_x, j_y):
        #Le lanceur peut pas etre dans la zone si y a le - a la fin du type zone
        return self.typeZone.testCaseEstDedans([departZone_x,departZone_y],[testDansZone_x,testDansZone_y],[j_x,j_y])

    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        print "Effet non existant"

    def afficher(self):
        print "Effet etatRequis:"+self.etatRequisCibleDirect + " consommeEtat:"+str(self.consommeEtat)+" ciblesPossibles:"+str(self.ciblesPossibles)+" cibles_exclues:"+str(self.ciblesExclues)

class EffetDegats(Effet):
    def __init__(self,int_minJet,int_maxJet,str_typeDegats, **kwargs):
        self.minJet = int_minJet
        self.maxJet = int_maxJet
        self.typeDegats = str_typeDegats
        super(EffetDegats, self).__init__(**kwargs)
    def appliquerDegats(self,niveau,joueurCaseEffet, joueurLanceur,nomSort):
        if joueurCaseEffet == None:
            return None
        baseDeg=random.randrange(self.minJet,self.maxJet+1)
        carac = joueurLanceur.pui
        dos = 0
        if self.typeDegats == "eau":
            carac+=joueurLanceur.cha
            dos += joueurLanceur.doCha
        elif self.typeDegats == "air":
            carac+=joueurLanceur.agi
            dos += joueurLanceur.doAgi
        elif self.typeDegats == "terre":
            carac+=joueurLanceur.fo
            dos += joueurLanceur.doFo
        elif self.typeDegats == "feu":
            carac+=joueurLanceur.int
            dos += joueurLanceur.doInt
        dos += joueurLanceur.do
        #Etats du lanceur
        total = 0
        for etat in joueurLanceur.etats:
            if etat.actif():
                dos,baseDeg,carac = etat.triggerAvantCalculDegats(dos,baseDeg,carac,nomSort)
        total += baseDeg + (baseDeg * ((carac) / 100)) + dos
        #appliquer les effets des etats sur les degats total du joueur cible
        for etat in joueurLanceur.etats:
            if etat.actif():
                total = etat.triggerApresCalculDegats(total,self.typeDegats)

        for etat in joueurCaseEffet.etats:
            if etat.actif():
                total = etat.triggerApresCalculDegats(total,self.typeDegats)
        if total < 0:
            total = 0
        print joueurCaseEffet.classe+" perd "+ str(total) + "PV"
        joueurCaseEffet.subit(joueurLanceur,niveau,total,self.typeDegats)
        return total
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        self.appliquerDegats(niveau,joueurCaseEffet, joueurLanceur,kwargs.get("nom_sort",""))
class EffetVolDeVie(EffetDegats):
    def __init__(self,int_minJet,int_maxJet,str_typeDegats, **kwargs):
        super(EffetVolDeVie, self).__init__(int_minJet,int_maxJet,str_typeDegats,**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        total = super(EffetVolDeVie, self).appliquerDegats(niveau,joueurCaseEffet, joueurLanceur,kwargs.get("nom_sort"))
        print joueurLanceur.classe+" vol "+ str(total/2) + "PV" 
        joueurLanceur.vie += (total/2)
        if joueurLanceur.vie > joueurLanceur._vie:
            joueurLanceur.vie = joueurLanceur._vie

class EffetDegatsPosLanceur(EffetDegats):
    def __init__(self,int_minJet,int_maxJet,str_typeDegats, **kwargs):
        super(EffetDegatsPosLanceur, self).__init__(int_minJet,int_maxJet,str_typeDegats,**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurLanceur = niveau.getJoueurSur(kwargs.get("prov_x"),kwargs.get("prov_y"))
        total = super(EffetDegatsPosLanceur, self).appliquerDegats(niveau,joueurCaseEffet, joueurLanceur,str(kwargs.get("nom_sort")))
class EffetTue(Effet):
    def __init__(self, **kwargs):
        super(EffetTue , self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.tue(joueurCaseEffet)
class EffetRetPA(Effet):
    def __init__(self,int_retrait, **kwargs):
        self.retrait = int_retrait
        super(EffetRetPA, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        print joueurCaseEffet.classe+" -"+ str(self.retrait) + "PA"
        
class EffetRetPM(Effet):
    def __init__(self,int_retrait, **kwargs):
        self.retrait = int_retrait
        super(EffetRetPM, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        print joueurCaseEffet.classe+" -"+ str(self.retrait) + "PM"
class EffetPropage(Effet):
    def __init__(self,sort_sort,zone_zone, **kwargs):
        self.zone = zone_zone
        self.sort = sort_sort
        super(EffetPropage, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurCaseEffet.appliquerEtat(Etat("temporaire",0,1),joueurLanceur)
        joueursAppliquables = niveau.getJoueurslesPlusProches(joueurCaseEffet.posX,joueurCaseEffet.posY,joueurLanceur,self.zone,["!temporaire"],self.ciblesPossibles)
        if len(joueursAppliquables)>0:
            joueurCaseEffet.lanceSort(self.sort,niveau, joueursAppliquables[0].posX, joueursAppliquables[0].posY,joueurLanceur)
class EffetEtat(Effet):
    def __init__(self, etat_etat, **kwargs):
        self.etat = etat_etat
        super(EffetEtat, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        etatCopier = self.etat.deepcopy()
        joueurCaseEffet.appliquerEtat(etatCopier,joueurLanceur, niveau)
class EffetGlyphe(Effet):
    def __init__(self,sort_sort,int_duree,str_nom, tuple_couleur, **kwargs):
        self.sort = sort_sort
        self.duree = int_duree
        self.nom = str_nom
        self.couleur = tuple_couleur
        super(EffetGlyphe, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        nouvelleGlyphe = Glyphe(self.nom, self.sort, self.duree, kwargs.get("case_cible_x"), kwargs.get("case_cible_y"), joueurLanceur,self.couleur)
        glypheID = niveau.poseGlyphe(nouvelleGlyphe)
        
class EffetPousser(Effet):
    def __init__(self,int_nbCase, **kwargs):
        self.nbCase = int_nbCase
        super(EffetPousser, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        if joueurCaseEffet != None:
            niveau.pousser(self.nbCase,joueurCaseEffet,joueurLanceur,True, kwargs.get("case_cible_x"), kwargs.get("case_cible_y"))
        
class EffetRepousser(Effet):
    def __init__(self,int_nbCase, **kwargs):
        self.nbCase = int_nbCase
        super(EffetRepousser, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.pousser(self.nbCase,joueurCaseEffet,joueurLanceur)
        
class EffetAttire(Effet):
    def __init__(self,int_nbCase, **kwargs):
        self.nbCase = int_nbCase
        super(EffetAttire, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        if not(joueurCaseEffet.posX == joueurLanceur.posX and joueurCaseEffet.posY == joueurLanceur.posY):
            niveau.attire(self.nbCase,joueurCaseEffet,joueurLanceur)

class EffetAttireAttaquant(Effet):
    def __init__(self,int_nbCase, **kwargs):
        self.nbCase = int_nbCase
        super(EffetAttireAttaquant, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.attire(self.nbCase,joueurLanceur,joueurCaseEffet)

class EffetAttireAllies(Effet):
    def __init__(self,int_nbCase, **kwargs):
        self.nbCase = int_nbCase
        super(EffetAttireAllies, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        if joueurCaseEffet.team == joueurLanceur.team:
            niveau.attire(self.nbCase,joueurCaseEffet,joueurLanceur)
        
class EffetDureeEtats(Effet):
    def __init__(self,int_deXTours, **kwargs):
        self.deXTours = int_deXTours
        super(EffetDureeEtats, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurCaseEffet.changeDureeEffets(self.deXTours, niveau)
class EffetRetireEtat(Effet):
    def __init__(self,str_nomEtat, **kwargs):
        self.nomEtat = str_nomEtat
        super(EffetRetireEtat, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurCaseEffet.retirerEtats(self.nomEtat)
class EffetTeleportePosPrec(Effet):
    def __init__(self,int_nbCase, **kwargs):
        self.nbCase = int_nbCase
        super(EffetTeleportePosPrec, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurCaseEffet.tpPosPrec(self.nbCase,niveau,joueurLanceur, kwargs.get("nom_sort"))

class EffetTeleportePosPrecLanceur(Effet):
    def __init__(self,int_nbCase,**kwargs):
        self.nbCase = int_nbCase
        super(EffetTeleportePosPrecLanceur, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurLanceur = niveau.getJoueurSur(kwargs.get("prov_x"),kwargs.get("prov_y"))
        joueurCaseEffet.tpPosPrec(self.nbCase,niveau,joueurLanceur, kwargs.get("nom_sort"))
                      
class EffetTeleporteDebutTour(Effet):
    def __init__(self, **kwargs):
        super(EffetTeleporteDebutTour, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.gereDeplacementTF(joueurCaseEffet,joueurCaseEffet.posDebTour,joueurLanceur,"Renvoi",AjouteHistorique=True)
        
class EffetTpSym(Effet):
    def __init__(self, **kwargs):
        super(EffetTpSym, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        distanceX = (joueurCaseEffet.posX-joueurLanceur.posX)
        distanceY = (joueurCaseEffet.posY-joueurLanceur.posY)
        arriveeX = joueurCaseEffet.posX+distanceX
        arriveeY = joueurCaseEffet.posY+distanceY
        niveau.gereDeplacementTF(joueurLanceur,[arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"),AjouteHistorique=True)
        
class EffetTpSymSelf(Effet):
    def __init__(self, **kwargs):
        super(EffetTpSymSelf, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        distanceX = (joueurCaseEffet.posX-joueurLanceur.posX)
        distanceY = (joueurCaseEffet.posY-joueurLanceur.posY)
        arriveeX = joueurLanceur.posX-distanceX
        arriveeY = joueurLanceur.posY-distanceY
        niveau.gereDeplacementTF(joueurCaseEffet,[arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"), AjouteHistorique=True)
        
class EffetTpSymCentre(Effet):
    def __init__(self, **kwargs):
        super(EffetTpSymCentre, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        distanceX = (joueurCaseEffet.posX-kwargs.get("case_cible_x"))
        distanceY = (joueurCaseEffet.posY-kwargs.get("case_cible_y"))
        arriveeX = kwargs.get("case_cible_x")-distanceX
        arriveeY = kwargs.get("case_cible_y")-distanceY
        joueurTF = niveau.gereDeplacementTF(joueurCaseEffet,[arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"), AjouteHistorique=True)
        if joueurTF != None:
            kwargs.get("cibles_traitees").append(joueurTF)
        
class EffetEtatSelf(Effet):
    def __init__(self,etat_etat, **kwargs):
        self.etat = etat_etat
        super(EffetEtatSelf, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        etatCopier = self.etat.deepcopy()
        joueurLanceur.appliquerEtat(etatCopier,joueurLanceur)
        
class EffetEntiteLanceSort(Effet):
    def __init__(self,str_nomEntites,sort_sort, **kwargs):
        self.nomEntites = str_nomEntites
        self.sort = sort_sort
        super(EffetEntiteLanceSort, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueursLanceurs = niveau.getJoueurs(self.nomEntites)
        for joueur in joueursLanceurs:
            joueur.lanceSort(self.sort,niveau, joueur.posX, joueur.posY)
        
class EffetEchangePlace(Effet):
    def __init__(self, **kwargs):
        super(EffetEchangePlace, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        genereTF = kwargs.get("generer_TF",False)
        joueurTF = niveau.gereDeplacementTF(joueurLanceur,[joueurCaseEffet.posX, joueurCaseEffet.posY], joueurLanceur, kwargs.get("nom_sort"), True,genereTF)
        if joueurTF != None:
            kwargs.get("cibles_traitees").append(joueurTF)
        
class EffetTp(Effet):
    def __init__(self, **kwargs):
        super(EffetTp, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.structure[joueurLanceur.posY][joueurLanceur.posX].type = "v"
        niveau.structure[kwargs.get("case_cible_y")][kwargs.get("case_cible_x")].type = "j"
        joueurLanceur.bouge(kwargs.get("case_cible_x"),kwargs.get("case_cible_y"))
        

class EffetInvoque(Effet):
    def __init__(self, str_nomInvoque, **kwargs):
        self.nomInvoque = str_nomInvoque
        super(EffetInvoque, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        invoc = Niveau.INVOCS[self.nomInvoque].deepcopy()
        invoc.invocateur = joueurLanceur
        invoc.team = joueurLanceur.team
        invoc.lvl = joueurLanceur.lvl
        niveau.invoque(invoc,kwargs.get("case_cible_x"),kwargs.get("case_cible_y"))

class Noeud:
    def __init__(self,x,y,cout=0,heur=0):
        self.x = x
        self.y = y
        self.cout = cout
        self.heur = heur
    
def compare2Noeuds(n1, n2):
    if n1.heur < n2.heur:
        return 1
    elif n1.heur == n2.heur:
        return 0
    else:
        return -1

class Glyphe:
    def __init__(self, nomSort, sortMono, dureeGlyphe, centre_x, centre_y, lanceur, couleur):
        self.nomSort = nomSort
        self.sortMono = sortMono
        self.duree = dureeGlyphe
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.lanceur = lanceur
        self.couleur = couleur
    def actif(self):
        return self.duree > 0

class Personnage(object):

    def __init__(self, classe, v,f,a,c,i,p,d,df,da,dc,di,dp,pm,pa,po,lvl,team=1,icone=""):
        self.vie = int(v)
        self.fo = int(f)
        self.agi = int(a)
        self.cha = int(c)
        self.int = int(i)
        self.pui = int(p)
        self.do = int(d)
        self.doFo = int(df)
        self.doAgi = int(da)
        self.doCha = int(dc)
        self.doInt = int(di)
        self.doPou = int(dp)
        self.PM = int(pm)
        self.PA = int(pa)
        self.PO = int(po)
        self._vie = self.vie
        self._fo = int(f)
        self._agi = int(a)
        self._cha = int(c)
        self._int = int(i)
        self._pui = int(p)
        self._do = int(d)
        self._doFo = int(df)
        self._doAgi = int(da)
        self._doCha = int(dc)
        self._doInt = int(di)
        self._PM = int(pm)
        self._PA = int(pa)
        self._PO = int(po)
        self.lvl = int(lvl)
        self.classe = classe
        self.sorts = Personnage.ChargerSorts(self.classe)
        self.posX = 0
        self.posY = 0
        self.etats = []
        self.historiqueDeplacement = []
        self.posDebTour = None
        self.invocateur = None
        self.team = int(team)
        if not(icone.startswith("images/")):
            self.icone = ("images/"+icone)
        else:
            self.icone = (icone)
        self.icone=normaliser(self.icone)
        self.overlay = Overlay(self,ColoredText("classe",(210,105,30)),ColoredText("vie",(224,238,238)),(56,56,56))

    def aEtatsRequis(self,etatsRequis):
        for checkEtat in etatsRequis:
            if checkEtat.strip() != "":
                if checkEtat.startswith("!"):
                    etatsRequis = checkEtat[1:]
                else:
                    etatsRequis = checkEtat
                aEtat = self.aEtat(etatsRequis)
                if (checkEtat.startswith("!") and aEtat) or (not checkEtat.startswith("!") and not aEtat):
                    #print "DEBUG : la cibleDirect n'a pas ou a l'etat requis :"+str(checkEtat)
                    return False
        return True

    @staticmethod
    def ChargerSorts(classe):
        sorts = []
        retourParadoxe = Sort(u"Retour Paradoxe",0,0,0,[EffetTpSymCentre(zone=TypeZoneCercle(99),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis_cibles="ParadoxeTemporel",consomme_etat=True)],99,99,0,0,"cercle")
        activationInstabiliteTemporelle = Sort(u"Activation Instabilité Temporelle",0,0,3,[EffetTeleportePosPrec(1)], 99,99,0,0,"cercle")
        activationParadoxeTemporel = Sort(u"Paradoxe Temporel", 0,0,0,[EffetTpSymCentre(zone=TypeZoneCercle(4),cibles_possibles="Allies|Ennemis",cibles_exclues=u"Lanceur|Xélor|Synchro"),EffetEtat(Etat("ParadoxeTemporel",0,2),zone=TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur|Xelor|Synchro"), EffetEtatSelf(EtatActiveSort("RetourParadoxe",1,1,retourParadoxe),cibles_possibles="Lanceur")],99,99,0,0,"cercle")
        if(classe==u"Stratège Iop"):
            sorts.append(Sort("Strategie_iop",0,0,0,[EffetEtat(EtatRedistribuerPer("Stratégie Iop",0,-1, 50,2))],99,99,0,0,"cercle"))
            return sorts
        elif(classe==u"Cadran de Xélor"):
            sorts.append(Sort("Synchronisation",0,0,0,[EffetDegats(100,130,"feu",zone=TypeZoneCercleSansCentre(4), cibles_possibles="Ennemis|Lanceur",etat_requis_cibles="Telefrag"),EffetEtat(EtatBoostPA("Synchronisation",0,2,2),zone=TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Lanceur",etat_requis_cibles="Telefrag")],99,99,0,0,"cercle"))
            return sorts
        elif(classe==u"Synchro"):
            sorts.append(Sort(u"Début des Temps",0,0,0,[EffetEtat(EtatBoostPA("Synchro",1,1,-1),zone=TypeZoneCercle(99),cibles_possibles="Xelor")],99,99,0,0,"cercle"))
            return sorts
        elif(classe==u"Balise de Rappel"):
            sorts.append(Sort("Rappel",0,0,0,[EffetEchangePlace(zone=TypeZoneCercle(99),cibles_possibles="Cra"), EffetTue(zone=TypeZoneCercle(99),cibles_possibles="Lanceur")],99,99,0,0,"cercle"))
        elif classe == u"Poutch":
            return sorts
        elif(classe==u"Xélor"):
            sorts.append(Sort(u"Ralentissement",2,1,6,[EffetDegats(8,9,"eau"),EffetRetPA(1),EffetRetPA(1,cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag")],4,2,0,1,"cercle",description=u"Occasionne des dommages Eau et retire 1 PA à la cible. Retire 1 PA supplémentaire aux ennemis dans l'état Téléfrag. Le retrait de PA ne peut pas être désenvoûté."))
            sorts.append(Sort(u"Souvenir",4,1,6,[EffetDegats(26,30,"terre"),EffetTeleportePosPrec(1)], 3,2,0,1,"ligne",description=u"Occasionne des dommages Terre et téléporte la cible à sa position précédente."))
            sorts.append(Sort(u"Aiguille",4,1,8,[EffetDegats(25,29,"feu"),EffetRetPA(1),EffetRetPA(2,etat_requis_cibles="Telefrag",consomme_etat=True)], 3,2,0,1,"cercle", description=u"Occasionne des dommages Feu et retire 1 PA à la cible. Retire des PA supplémentaires aux ennemis dans l'état Téléfrag. Le retrait de PA ne peut pas être désenvoûté. Retire l'état Téléfrag."))
            sorts.append(Sort(u"Rouage",3,1,7,[EffetDegats(12,14,"eau"),EffetEtatSelf(EtatBoostPA("Rouage",1,1,1))], 2,99,0,1,"cercle",chaine=True,description="Occasionne des dommages Eau. Le lanceur gagne 1 PA au tour suivant."))
            sorts.append(Sort(u"Téléportation",2,1,5,[EffetTpSym()], 1,1,3,0,"cercle",description=u"Téléporte le lanceur symétriquement par rapport à la cible. Le lanceur gagne 2 PA pour 1 tour à chaque fois qu’il génère un Téléfrag. Le temps de relance est supprimé quand un Téléfrag est généré ou consommé. Un Téléfrag est généré lorsqu'une entité prend la place d'une autre."))
            sorts.append(Sort(u"Retour Spontané",1,0,7,[EffetTeleportePosPrec(1)], 3,3,0,1,"cercle",description=u"Le lanceur revient à sa position précédente."))
            sorts.append(Sort(u"Flétrissement",3,1,6,[EffetDegats(26,29,"air"),EffetDegats(10,10,"air",etat_requis_cibles="Telefrag")], 3,2,0,1,"ligne",description=u"Occasionne des dommages Air en ligne. Occasionne des dommages supplémentaires aux ennemis dans l'état Téléfrag."))
            sorts.append(Sort(u"Dessèchement",4,1,6,[EffetDegats(38,42,"air"),EffetEtat(EtatEffetDebutTour(u"Dessèchement", 1,1,EffetDegats(44,48,"air",zone=TypeZoneCercleSansCentre(2)),"Dessechement","lanceur"))], 2,1,0,0,"ligne",description=u"Occasionne des dommages Air. Au prochain tour du lanceur, la cible occasionne des dommages autour d'elle."))
            sorts.append(Sort(u"Rembobinage",2,0,6,[EffetEtat(EtatRetourCaseDepart("Bobine",0,1),cibles_possibles="Allies|Lanceur")], 1,1,3, 0, "ligne",description=u"À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour."))
            sorts.append(Sort(u"Renvoi",3,1,6,[EffetTeleporteDebutTour()], 1,1,2, 0, "ligne",description=u"Téléporte la cible ennemie à sa cellule de début de tour."))
            sorts.append(Sort(u"Rayon Obscur",5,1,6,[EffetDegats(37,41,"terre"),EffetDegats(37,41,"terre",cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag",consomme_etat=True)], 3,2,0,0,"ligne",description=u"Occasionne des dommages Terre en ligne. Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag. Retire l'état Téléfrag."))
            sorts.append(Sort(u"Rayon Ténebreux",3,1,5,[EffetDegats(19,23,"terre"),EffetDegats(19,23,"terre",zone=TypeZoneCercleSansCentre(2),etat_requis="Telefrag")], 3,2,0,0,"ligne",description=u"Occasionne des dommages Terre. Si la cible est dans l'état Téléfrag, occasionne des dommages Terre en zone autour d'elle."))
            sorts.append(Sort(u"Complice",2,1,5,[EffetInvoque("Complice",cibles_possibles="",faire_au_vide=True),EffetTue(cibles_possibles=u"Cadran de Xélor|Complice",zone=TypeZoneCercleSansCentre(99))], 1,1,0,0,"cercle",chaine=True,description=u"Invoque un Complice statique qui ne possède aucun sort. Il est tué si un autre Complice est invoqué."))
            sorts.append(Sort(u"Cadran de Xélor",3,1,5,[EffetInvoque(u"Cadran de Xélor",cibles_possibles="",faire_au_vide=True),EffetTue(cibles_possibles=u"Cadran de Xélor|Complice",zone=TypeZoneCercleSansCentre(99))], 1,1,4,0,"cercle",chaine=True,description=u"Invoque un Cadran qui occasionne des dommages Feu en zone et retire des PA aux ennemis dans l'état Téléfrag. Donne des PA aux alliés autour de lui et dans l'état Téléfrag."))
            sorts.append(Sort(u"Gelure",2,2,5,[EffetDegats(11,13,"air",cibles_possibles="Ennemis|Lanceur"), EffetTeleportePosPrec(1)], 3,2,0,1,"cercle",description=u"Occasionne des dommages Air aux ennemis. Téléporte la cible à sa position précédente."))
            sorts.append(Sort(u"Perturbation",2,1,4,[EffetDegats(9,11,"feu",cibles_possibles="Ennemis|Lanceur"), EffetTpSymSelf()], 3,2,0,0,"ligne", chaine=False,description=u"Occasionne des dommages Feu et téléporte la cible symétriquement par rapport au lanceur."))
            sorts.append(Sort(u"Sablier de Xélor",2,1,7,[EffetDegats(15,17,"feu"),EffetRetPA(2),EffetDegats(15,17,"feu",zone=TypeZoneCercleSansCentre(2),etat_requis="Telefrag"),EffetRetPA(2,zone=TypeZoneCercleSansCentre(2),etat_requis="Telefrag")], 3,1,0,1,"ligne",description=u"Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue. Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone. Le retrait de PA ne peut pas être désenvoûté."))
            sorts.append(Sort(u"Distorsion Temporelle",4,0,0,[EffetDegats(26,30,"air",zone=TypeZoneCarre(1),cibles_possibles="Ennemis"),EffetTeleportePosPrec(1,zone=TypeZoneCarre(1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur")], 1,1,0,0,"cercle",description=u"Occasionne des dommages Air aux ennemis. Téléporte les cibles à leur position précédente."))
            sorts.append(Sort(u"Vol du Temps",4,1,5,[EffetDegats(27,30,"eau"),EffetEtatSelf(EtatBoostPA("Vol du Temps",1,1,1))], 3,2,0,0,"cercle",chaine=True,description=u"Occasionne des dommages Eau à la cible. Le lanceur gagne 1 PA au début de son prochain tour."))
            sorts.append(Sort(u"Pétrification",5,1,7,[EffetDegats(34,38,"eau"),EffetEtatSelf(EtatCoutPA("Petrification",0,2,"Petrification",-1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag")], 3,2,0,1,"ligne",description=u"Occasionne des dommages Eau et retire des PA. Si la cible est dans l'état Téléfrag, le coût en PA du sort est réduit pendant 2 tours."))
            sorts.append(Sort(u"Flou",2,1,3,[EffetEtat(EtatBoostPA("Flou",0,1,-2),zone=TypeZoneCercle(3)),EffetEtat(EtatBoostPA("Flou",1,1,2),zone=TypeZoneCercle(3))], 1,1,3,0,"cercle",description=u"Retire des PA en zone le tour en cours. Augmente les PA en zone le tour suivant."))
            sorts.append(Sort(u"Conservation",3,0,5,[EffetEtat(EtatModDegPer("Conservation",0,1,150),cibles_possibles="Allies|Lanceur"),EffetEtat(EtatModDegPer("Conservation",1,1,70),cibles_possibles="Allies|Lanceur")], 1,1,3,0,"cercle",description=u"Augmente les dommages subis par l'allié ciblé ou le lanceur de 50%% pour le tour en cours. Au tour suivant, la cible réduit les dommages subis de 30%%."))
            sorts.append(Sort(u"Poussière Temporelle",4,0,6,[EffetDegats(34,37,"feu",cibles_possibles="Ennemis"), EffetDegats(34,37,"feu",zone=TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"), EffetTpSymCentre(zone=TypeZoneCercleSansCentre(2),etat_requis="Telefrag")], 2,2,0,1,"cercle",description=u"Occasionne des dommages Feu. Si la cible est dans l'état Téléfrag, les dommages sont occasionnés en zone et les entités à proximité sont téléportées symétriquement par rapport au centre de la zone d'effet."))
            sorts.append(Sort(u"Suspension Temporelle",4,1,4,[EffetDegats(27,31,"feu"),EffetDureeEtats(1,etat_requis="Telefrag",consomme_etat=True)], 3,2,0,0,"ligne",description=u"Occasionne des dommages Feu sur les ennemis. Réduit la durée des effets sur les cibles ennemies dans l'état Téléfrag et retire l'état."))
            sorts.append(Sort(u"Raulebaque",2,0,0,[EffetTeleportePosPrec(1,zone=TypeZoneCercle(99))], 1,1,2, 0, "cercle",description=u"Replace tous les personnages à leurs positions précédentes."))
            sorts.append(Sort(u"Instabilité Temporelle",3,0,7,[EffetGlyphe(activationInstabiliteTemporelle,2,u"Instabilité Temporelle",(255,255,0),zone=TypeZoneCercle(3),faire_au_vide=True)], 1,1,4,1,"cercle",description=u"Pose un glyphe qui renvoie les entités à leur position précédente. Les effets du glyphe sont également exécutés lorsque le lanceur génère un Téléfrag."))
            sorts.append(Sort(u"Démotivation",3,1,5,[EffetDegats(23,26,"terre",cibles_possibles="Ennemis"),EffetDureeEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True)], 3,2,0,0,"diagonale",description=u"Occasionne des dommages Terre aux ennemis en diagonale. Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état."))
            sorts.append(Sort(u"Pendule",5,1,5,[EffetTpSym(),EffetDegatsPosLanceur(48,52,"air",zone=TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis"), EffetTeleportePosPrecLanceur(1,cibles_possibles="Lanceur")], 2,1,0,0,"cercle",chaine=True,description=u"Le lanceur se téléporte symétriquement par rapport à la cible et occasionne des dommages Air en zone sur sa cellule de destination. Il revient ensuite à sa position précédente."))
            sorts.append(Sort(u"Paradoxe Temporel",3,0,0,[EffetEntiteLanceSort(u"Complice|Cadran de Xélor",activationParadoxeTemporel)], 1,1,2,0,"cercle",description=u"Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran). Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles. Fixe le temps de relance de Cadran de Xélor et de Complice à 1."))
            sorts.append(Sort(u"Faille Temporelle",3,0,0,[EffetEchangePlace(zone=TypeZoneCercle(99),cibles_possibles=u"Cadran de Xélor|Complice",generer_TF=True),EffetEtat(EtatEffetFinTour("Retour faille temporelle", 1,1,EffetTeleportePosPrec(1),"Fin faille Temporelle","cible")), EffetEtat(Etat("Faille_temporelle",0,1),zone=TypeZoneCercle(99),cibles_possibles="Xelor")], 1,1,3,0,"cercle",description=u"Le lanceur échange sa position avec celle du Complice (ou du Cadran). À la fin du tour, le Complice (ou le Cadran) revient à sa position précédente. La Synchro ne peut pas être déclenchée pendant la durée de Faille Temporelle."))
            sorts.append(Sort(u"Synchro",2,1,4,[EffetInvoque("Synchro",cibles_possibles="",faire_au_vide=True)], 1,1,3,0,"cercle",description=u"Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour. La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag. Elle n'est pas affectée par les effets de Rembobinage. À partir du tour suivant son lancer, son invocateur perd 1 PA."))
            sorts.append(Sort(u"Contre",2,0,6,[EffetEtat(EtatContre("Contre",0,2, 50,1),zone=TypeZoneCercle(2),cibles_possibles="Allies|Lanceur")], 1,1,5,0,"cercle", description=u"Renvoie une partie des dommages subis en mêlée à l'attaquant."))
            sorts.append(Sort(u"Bouclier Temporel",3,0,3,[EffetEtat(EtatEffetSiSubit("Bouclier temporel",0,1, EffetTeleportePosPrec(1),"Bouclier Temporel","lanceur",""))], 1,1,3,0,"cercle",description=u"Si la cible subit des dommages, son attaquant revient à sa position précédente."))
            sorts.append(Sort(u"Fuite",1,0,5,[EffetEtat(EtatEffetDebutTour("Fuite", 1,1,EffetTeleportePosPrec(1),"Fuite","cible"))], 4,2,0,0,"cercle",description=u"Téléporte la cible sur sa position précédente au début du prochain tour du lanceur."))
            sorts.append(Sort(u"Horloge",5,1,6,[EffetVolDeVie(36,39,"eau"),EffetEtatSelf(EtatBoostPA("Horloge",1,1,1)),EffetRetPA(4,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)], 3,2,0,0,"ligne", chaine=True,description=u"Vole de vie dans l'élément Eau. Le lanceur gagne 1 PA au début de son prochain tour. Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état. Le retrait de PA ne peut pas être désenvoûté."))
            sorts.append(Sort(u"Clepsydre",4,1,3,[EffetDegats(30,34,"eau"),EffetEtatSelf(EtatBoostPA("Clepsydre",1,1,2),etat_requis="Telefrag",consomme_etat=True)], 2,2,0,0,"cercle", chaine=True,description=u"Occasionne des dommages Eau. Si la cible est dans l'état Téléfrag, le lanceur gagne 2 PA au prochain tour. Retire l'état Téléfrag."))
            sorts.append(Sort(u"Frappe de Xélor",3,1,3,[EffetDegats(23,27,"terre",cibles_possibles="Ennemis"), EffetTpSymSelf()], 3,2,0,0,"cercle",chaine=False,description=u"Occasionne des dommages Terre aux ennemis. Téléporte la cible symétriquement par rapport au lanceur du sort."))
            sorts.append(Sort(u"Engrenage",4,1,5,[EffetDegats(38,42,"terre",zone=TypeZoneLignePerpendiculaire(1),cibles_possibles="Ennemis"), EffetTpSymCentre(zone=TypeZoneLignePerpendiculaire(1))], 2,2,0,0,"ligne",chaine=False,description=u"Occasionne des dommages Terre et téléporte les cibles symétriquement par rapport au centre de la zone d'effet."))
            sorts.append(Sort(u"Momification",2,0,0,[EffetEtat(EtatBoostPM("Momification",0,1,2)),EffetEtat(EtatTelefrag("Telefrag",0,2,"Momification"),zone=TypeZoneCercle(99)),EffetEtat(EtatBoostDommage("Momie",0,1,-99999999))], 1,1,3,0,"cercle",description=u"Le lanceur ne peut plus occasionner de dommages avec ses sorts élémentaires et gagne 2 PM pendant 1 tour. Fixe l'état Téléfrag à tous les alliés et ennemis pendant 2 tours. Quand l'état Téléfrag est retiré, le lanceur gagne 100 Puissance pendant 2 tours."))
            sorts.append(Sort(u"Glas",2,0,0,[], 1,1,3,0,"cercle",description=u"Occasionne des dommages Neutre aux ennemis autour de chaque entité dans l'état Téléfrag. Plus le lanceur a de vie, plus les dommages sont importants. Retire l'état Téléfrag."))
        elif(classe==u"Iop"):
            activationRassemblement= Sort(u"AttireAllies",0,0,0,[EffetAttireAllies(2,zone=TypeZoneCroix(3))],99,99,0,0,"cercle")
            activationFriction= Sort(u"Attire",0,0,0,[EffetAttire(1,zone=TypeZoneCroix(99))],99,99,0,0,"cercle")
            sorts.append(Sort(u"Pression",3,1,3,[EffetDegats(21,25,"terre")], 99,3,0,0,"cercle",description=u"Occasionne des dommages Terre et applique un malus d'Érosion."))
            sorts.append(Sort(u"Tannée",4,1,7,[EffetDegats(30,34,"air",zone=TypeZoneLignePerpendiculaire(1)),EffetRetPM(3,zone=TypeZoneLignePerpendiculaire(1))], 2,2,0,0,"ligne",description=u"Occasionne des dommages Air en zone et retire des PM."))
            sorts.append(Sort(u"Bond",5,1,6,[EffetTp(cibles_possibles="",faire_au_vide=True),EffetEtat(EtatModDegPer("Bond",0,1,115),zone=TypeZoneCercle(1),cibles_possibles="Ennemis")], 1,1,2,0,"cercle",description=u"Téléporte sur la case ciblée. Augmente les dommages reçus par les ennemis situés sur les cases adjacentes."))
            sorts.append(Sort(u"Détermination",2,0,0,[EffetEtat(Etat("Indeplacable",0,1)),EffetEtat(EtatModDegPer("Determination",0,1,75))], 1,1,2,0,"cercle",description="Fixe l'état Indéplaçable et réduit 25%% des dommages subis pendant 1 tour. Ne peut pas être désenvoûté."))
            sorts.append(Sort(u"Intimidation",2,1,2,[EffetDegats(11,13,"terre"),EffetRepousser(4)], 3,2,0,0,"ligne",description=u"Occasionne des dommages Neutre sur les ennemis et repousse la cible."))
            sorts.append(Sort(u"Menace",3,1,3,[EffetDegats(26,28,"eau"),EffetAttire(2)], 3,2,0,0,"cercle",description=u"Occasionne des dommages Eau et attire la cible. Le lanceur gagne des points de bouclier."))
            sorts.append(Sort(u"Déferlement",3,1,3,[EffetDegats(17,19,"eau"),EffetAttireAttaquant(2)], 3,2,0,0,"ligne",description=u"Occasionne des dommages Eau aux ennemis et rapproche le lanceur de la cible. Le lanceur gagne des points de bouclier."))
            sorts.append(Sort(u"Conquête",3,1,6,[EffetInvoque("Stratège Iop",cible_possibles="",faire_au_vide=True),EffetEtat(EtatRedistribuerPer("Strategie iop",0,-1, 50,2))], 1,1,3,0,"ligne",description=u"Invoque un épouvantail qui redistribue à proximité (2 cases) 50%% des dommages qu'il subit."))
            sorts.append(Sort(u"Epée_Divine",3,0,0,[EffetDegats(21,23,"air",zone=TypeZoneCroix(3),cibles_possibles="Ennemis"), EffetEtat(EtatBoostDommage("Epee Divine",0,4,20),zone=TypeZoneCroix(3),cibles_possibles="Allies|Lanceur")], 2,2,0,0,"cercle",chaine=False,description=u"Occasionne des dommages Air et augmente les dommages des alliés ciblés."))
            sorts.append(Sort(u"Fendoir",5,1,4,[EffetDegats(40,44,"eau",zone=TypeZoneCroix(1))], 2,2,0,0,"cercle",description=u"Occasionne des dommages Eau en zone. Applique des points de bouclier pour chaque ennemi touché."))
            sorts.append(Sort(u"Épée Destructrice",4,1,5,[EffetDegats(32,36,"feu",zone=TypeZoneLignePerpendiculaire(1))], 2,2,0,0,"ligne",description=u"Occasionne des dommages Feu et réduit la probabilité que la cible occasionne des coups critiques."))
            sorts.append(Sort(u"Anneau Destructeur",3,0,2,[EffetDegats(26,30,"air",zone=TypeZoneAnneau(3)), EffetAttire(1,zone=TypeZoneAnneau(3))], 2,2,0,0,"cercle",description=u"Occasionne des dommages Air en anneau et attire les cibles."))
            sorts.append(Sort(u"Massacre",2,1,7,[EffetEtat(EtatRedistribuerPer("Massacre",0,2,50,1))], 1,1,3,0,"cercle",description=u"Lorsque la cible ennemie reçoit des dommages de sorts, elle occasionne 50% de ces dommages aux entités au contact."))
            sorts.append(Sort(u"Rassemblement",2,1,6,[EffetEtat(EtatLanceSortSiSubit("Rassemblement",0,1,activationRassemblement))], 1,1,2,0,"cercle",description=u"La cible attire ses alliés à proximité (2 cases) lorsqu'elle est attaquée."))
            sorts.append(Sort(u"Souffle",2,2,8,[EffetPousser(1,zone=TypeZoneCroix(1),faire_au_vide=True)],1,1,2,0,"cercle",description=u"Repousse les alliés et les ennemis situés autour de la cellule ciblée."))
            sorts.append(Sort(u"Violence",2,0,0,[EffetAttire(1,zone=TypeZoneCercle(2),cibles_possibles="Allies|Ennemis"),EffetEtat(EtatBoostDoPou("Violence",0,1,50))],1,1,0,0,"cercle",description=u"Attire les entités à proximité et augmente les dommages de poussée et le Tacle pour chaque ennemi dans la zone d'effet."))
            sorts.append(Sort(u"Concentration",2,1,1,[EffetDegats(20,24,"terre")],4,3,0,0,"ligne",description=u"Occasionne des dommages Terre. Les dommages sont augmentés contre les Invocations."))
            sorts.append(Sort(u"Accumulation",3,0,4,[EffetDegats(28,32,"terre",cibles_possibles="Ennemis"),EffetEtat(EtatBoostBaseDeg("Accumulation",0,3,"Accumulation",15),cibles_possibles="Lanceur")],2,1,0,0,"ligne",chaine=False,description=u"Occasionne des dommages Terre. Si le sort est lancé sur soi, le sort n'occasionne pas de dommages et ils sont augmentés pour les prochains lancers."))
            sorts.append(Sort(u"Couper",3,1,4,[EffetDegats(18,22,"feu",zone=TypeZoneLigne(3)),EffetRetPM(3,zone=TypeZoneLigne(3))],2,2,0,1,"ligne",description=u"Occasionne des dommages Feu et retire des PM."))
            sorts.append(Sort(u"Fracture",4,1,4,[EffetDegats(26,30,"air",zone=TypeZoneLigneJusque(0))],2,2,0,0,"ligne",description=u"Occasionne des dommages Air jusqu'à la cellule ciblée. Applique un malus d'Érosion."))
            sorts.append(Sort(u"Friction",2,0,5,[EffetEtat(EtatLanceSortSiSubit("Friction",0,2,activationFriction))],1,1,3,0,"cercle",description=u"La cible se rapproche de l'attaquant si elle reçoit des dommages issus de sorts. Nécessite d'être aligné avec la cible."))
            sorts.append(Sort(u"Coup pour coup",2,1,3,[EffetEtat(EtatRepousserSiSubit("Coup_pour_coup",0,2,2))],1,1,3,0,"cercle",description=u"La cible est repoussée de 2 cases à chaque fois qu'elle attaque le lanceur."))
            sorts.append(Sort(u"Duel",3,1,1,[],1,1,4,0,"cercle",description=u"Retire leurs PM à la cible et au lanceur, leur applique l'état Pesanteur et les rend invulnérable aux dommages à distance. Ne fonctionne que si lancé sur un ennemi."))
            sorts.append(Sort(u"Emprise",3,1,1,[],1,1,4,0,"cercle",description=u"Retire tous les PM de l'ennemi ciblé mais le rend invulnérable."))
            sorts.append(Sort(u"Épée du Jugement",4,1,5,[EffetDegats(20,28,"air"),EffetVolDeVie(10,12,"feu")],3,2,0,0,"cercle",description=u"Occasionne des dommages Air et vole de la vie dans l'élément Feu sans ligne de vue."))
            sorts.append(Sort(u"Condamnation",3,1,6,[
                EffetDegats(33,37,"feu",zone=TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_2",consomme_etat=False),
                EffetDegats(33,37,"air",zone=TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_2",consomme_etat=True),
                EffetEtat(Etat("Condamnation_lancer_2",0,-1),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=True),
                EffetDegats(23,27,"feu",zone=TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=False),
                EffetDegats(23,27,"air",zone=TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=True),
                EffetEtat(Etat("Condamnation_lancer_1",0,-1),etat_requis_cibles="!Condamnation_lancer_2")
                ],3,2,0,0,"cercle",chaine=False,description=u"Occasionne des dommages Air et Feu. Les dommages sont appliqués lorsque le sort est lancé sur une autre cible. Peut se cumuler 2 fois sur une même cible."))
            sorts.append(Sort(u"Puissance",3,0,6,[EffetEtat(EtatBoostPuissance("Puissance",0,2,300))],1,1,4,0,"cercle",description=u"Augmente la Puissance de la cible."))
            sorts.append(Sort(u"Vertu",4,0,0,[EffetEtat(EtatBoostPuissance("Vertu",0,2,-150),zone=TypeZoneCercle(1))],1,1,3,0,"cercle",description=u"Applique un bouclier zone mais réduit la Puissance du lanceur."))
            sorts.append(Sort(u"Précipitation",2,0,6,[EffetEtat(EtatBoostPA("Precipite",0,1,5)),EffetEtat(EtatBoostPA("Sortie de Precipitation",1,1,-3))],1,1,2,0,"cercle",description=u"Augmente les PA de la cible pour le tour en cours mais lui retire des PA le tour suivant. Interdit l'utilisation des armes et du sort Colère de Iop."))
            sorts.append(Sort(u"Agitation",2,0,5,[EffetEtat(EtatBoostPM("Agitation",0,1,2))],2,2,0,0,"cercle",description=u"Augmente les PM et la Fuite pour le tours en cours."))
            sorts.append(Sort(u"Tempête de Puissance",3,3,5,[EffetDegats(30,34,"feu")],3,2,0,0,"cercle",description=u"Occasionne des dommages Feu."))
            sorts.append(Sort(u"Tumulte",4,2,5,[EffetDegats(19,21,"feu",zone=TypeZoneCroix(1))],1,1,1,0,"cercle",description=u"Occasionne des dommages Feu en zone. Plus le nombre de cibles est important, plus les dommages sont importants.*"))
            sorts.append(Sort(u"Épée Céleste",4,0,4,[EffetDegats(36,40,"air",zone=TypeZoneCercle(2))],2,2,0,0,"ligne",description=u"Occasionne des dommages Air en zone."))
            sorts.append(Sort(u"Zénith",5,1,3,[EffetDegats(75,81,"air",zone=TypeZoneLigne(4))],1,1,0,0,"ligne",description=u"Occasionne des dommages Air en zone. Les dommages sont augmentés pour chaque PM disponible lorsque le sort est lancé."))
            sorts.append(Sort(u"Vitalité",3,0,6,[EffetEtat(EtatBoostVita("Vitalite",0,4,20))],1,1,2,0,"cercle",description=u"Augmente temporairement les PV de la cible en pourcentage. Le bonus de PV est plus faible sur les alliés que sur le lanceur."))
            sorts.append(Sort(u"Endurance",4,1,1,[EffetDegats(34,38,"eau")],3,2,0,0,"cercle",description="Occasionne des dommages Eau. Applique des points de bouclier au lanceur."))
            sorts.append(Sort(u"Épée de Iop",4,1,6,[EffetDegats(37,41,"terre",zone=TypeZoneCroix(3),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",faire_au_vide=True)],2,2,0,0,"ligne",description=u"Occasionne des dommages Terre en croix.")) 
            sorts.append(Sort(u"Pugilat",2,1,4,[EffetDegats(9,11,"terre",zone=TypeZoneCroix(1)),EffetEtatSelf(EtatBoostBaseDeg("Pugilat",0,1,"Pugilat",15))],4,1,0,0,"cercle",description=u"Occasionne des dommages Terre en zone. Les dommages sont augmentés pendant 1 tour après chaque lancer.")) 
            sorts.append(Sort(u"Épée du Destin",4,1,1,[EffetDegats(38,42,"feu"),EffetEtatSelf(EtatBoostBaseDeg("Epee_du_destin", 2,1,u"Épée du Destin",30))], 1,1,2,0,"ligne",description=u"Occasionne des dommages Feu. Les dommages sont augmentés à partir du second lancer.")) 
            sorts.append(Sort(u"Sentence",2,1,6,[EffetDegats(13,16,"feu"),EffetEtat(EtatEffetFinTour("Sentence", 1,1,EffetDegats(13,16,"feu",zone=TypeZoneCercle(2)),"Sentence","lanceur"))], 3,1,0,0,"ligne",description=u"Occasionne des dommages Feu. Occasionne des dommages Feu supplémentaires en zone à la fin du tour de la cible.")) 
            sorts.append(Sort(u"Colère de Iop",7,1,1,[EffetDegats(81,100,"terre"),EffetEtatSelf(EtatBoostBaseDeg("Colere_de_Iop", 3,1,u"Colère de Iop",110))], 1,1,3,0,"ligne",description=u"Occasionne des dommages Terre. Augmente les dommages du sort au troisième tour après son lancer.")) 
            sorts.append(Sort(u"Fureur",3,1,1,[EffetDegats(19,21,"terre"),EffetEtatSelf(EtatBoostBaseDeg("Fureur", 1,2,"Fureur",40))], 1,1,0,0,"ligne",description=u"Occasionne des dommages Terre. Les dommages sont augmentés à chaque lancer du sort, mais ce bonus est perdu si le sort n'est pas relancé."))
        elif classe==u"Crâ":
            sorts.append(Sort(u"Flèche Magique",3,1,12,[EffetDegats(19,21,"air"),EffetEtat(EtatBoostPO("Fleche Magique",1,1,-2)),EffetEtatSelf(EtatBoostPO("Fleche Magique",0,1,2))],3,2,0,1,"cercle",description=u"Occasionne des dommages Air et vole la portée de la cible."))
            sorts.append(Sort(u"Flèche de Concentration",3,3,8,[EffetDegats(28,32,"air"),EffetAttireAttaquant(1)],2,1,0,1,"cercle",description=u"Occasionne des dommages Air et attire vers la cible."))
            sorts.append(Sort(u"Flèche de Recul",3,1,8,[EffetDegats(25,28,"air"),EffetRepousser(4)],2,1,0,0,"ligne",description=u"Occasionne des dommages Air aux ennemis et pousse la cible."))
            sorts.append(Sort(u"Flèche Érosive",3,1,3,[EffetDegats(19,24,"terre")],3,2,0,0,"ligne",description=u"Occasionne des dommages Terre et applique un malus d'Érosion."))
            sorts.append(Sort(u"Flèche de Dispersion",3,1,12,[EffetPousser(2,zone=TypeZoneCroix(2),faire_au_vide=True)],1,1,2,1,"cercle",description=u"Pousse les ennemis et alliés, même s'ils sont bloqués par d'autres entités."))
            sorts.append(Sort(u"Représailles",4,2,5,[EffetEtat(EtatBoostPM("Immobilise",1,1,-100))],1,1,5,0,"ligne",description=u"Immobilise la cible."))
            sorts.append(Sort(u"Flèche Glacée",3,3,6,[EffetDegats(12,13,"feu"),EffetRetPA(2)],99,2,0,1,"cercle",description=u"Occasionne des dommages Feu et retire des PA."))
            sorts.append(Sort(u"Flèche Paralysante",5,2,6,[EffetDegats(39,42,"feu",zone=TypeZoneCroix(1)),EffetRetPA(4,zone=TypeZoneCroix(1))],1,1,0,0,"cercle",description=u"Occasionne des dommages Feu et retire des PA."))
            sorts.append(Sort(u"Flèche Enflammée",4,1,8,[EffetDegats(33,35,"feu",zone=TypeZoneLigne(5)),EffetPousser(1,zone=TypeZoneLigne(5))],2,2,0,1,"ligne",description=u"Occasionne des dommages Feu et pousse les cibles présentes dans la zone d'effet du sort."))
            sorts.append(Sort(u"Flèche Repulsive",3,2,5,[EffetDegats(28,32,"feu",zone=TypeZoneLignePerpendiculaire(1)),EffetPousser(1,zone=TypeZoneLignePerpendiculaire(1))],2,2,0,0,"ligne",description=u"Occasionne des dommages Feu et repousse de 1 case."))
            sorts.append(Sort(u"Tir Éloigne",3,0,0,[EffetEtat(EtatBoostPO("Tir_eloigne",0,4,6),zone=TypeZoneCercle(3))],1,1,5,0,"cercle",description=u"Augmente la portée des cibles présentes dans la zone d'effet."))
            sorts.append(Sort(u"Acuité Absolue",5,0,0,[EffetEtat(Etat("Desactive_ligne_de_vue",0,1))],1,1,4,0,"cercle",description=u"Tous les sorts du Crâ peuvent être lancés au travers des obstacles."))
            sorts.append(Sort(u"Flèche d'Expiation",4,8,10,[EffetDegats(35,37,"eau"),EffetEtat(Etat("Pesanteur",1,1)),EffetEtatSelf(EtatBoostBaseDeg(u"Fleche_d_expiation",0,-1,u"Flèche d'Expiation",36))],1,1,3,1,"cercle",description=u"Occasionne des dommages Eau, augmente les dommages du sort tous les 3 tours et empêche la cible d'utiliser des sorts de déplacement."))
            sorts.append(Sort(u"Flèche de Rédemption",3,6,8,[EffetDegats(19,22,"eau"),EffetEtatSelf(EtatBoostBaseDeg("Fleche_de_redemption",1,1,u"Flèche de Rédemption",12))],3,2,0,1,"cercle",description=u"Occasionne des dommages Eau qui sont augmentés si le sort est relancé le tour suivant."))
            sorts.append(Sort(u"Oeil de Taupe",3,5,10,[EffetVolDeVie(16,18,"eau",zone=TypeZoneCercle(3)),EffetEtat(EtatBoostPO("Oeil_de_taupe",1,3,-3),zone=TypeZoneCercle(3)),EffetRetireEtat("Invisibilite",zone=TypeZoneCercle(3))],1,1,4,1,"cercle",description=u"Réduit la portée des personnages ciblés, vole de la vie dans l'élément Eau et repère les objets invisibles dans sa zone d'effet."))
            sorts.append(Sort(u"Flèche Écrasante",3,5,7,[EffetDegats(34,38,"feu",zone=TypeZoneCroixDiagonale(1)),EffetEtat(Etat("Pesanteur",1,1),zone=TypeZoneCroixDiagonale(1))],1,1,3,1,"cercle",description=u"Occasionne des dommages Feu et applique l'état Pesanteur."))
            sorts.append(Sort(u"Tir Critique",2,0,6,[EffetEtat(Etat("Tir_critique",0,4))],1,1,5,1,"cercle",description=u"Augmente la probabilité de faire un coup critique."))
            sorts.append(Sort(u"Balise de Rappel",2,1,5,[EffetInvoque("Balise_de_rappel",cibles_possibles="",faire_au_vide=True)],1,1,2,0,"cercle",description=u"Invoque une balise qui échange sa position avec celle du lanceur (au début du prochain tour)."))
            sorts.append(Sort(u"Flèche d'Immobilisation",2,1,6,[EffetDegats(10,11,"eau"),EffetEtat(EtatBoostPM("Fleche_d_immobilisation",1,1,-1)),EffetEtatSelf(EtatBoostPM("Fleche_d_immobilisation",0,1,1))],4,2,0,1,"cercle",description=u"Occasionne des dommages Eau et vole des PM à la cible."))
            sorts.append(Sort(u"Flèche Assaillante",3,2,6,[EffetDegats(33,37,"eau",cibles_possibles="Ennemis"),EffetRepousser(1,cibles_possibles="Ennemis"),EffetAttireAttaquant(1,cibles_possibles="Allies")],3,2,0,1,"ligne",description=u"Occasionne des dommages Eau sur les ennemis et le lanceur recule de 1 case. Sur un allié : rapproche le lanceur de 1 case."))
            sorts.append(Sort(u"Flèche Punitive",4,6,8,[EffetDegats(29,31,"terre"),EffetEtatSelf(EtatBoostBaseDeg("Fleche_punitive",0,-1,u"Flèche Punitive",30))],1,1,2,1,"cercle",description=u"Occasionne des dommages Terre et augmente les dommages du sort tous les 2 tours."))
            sorts.append(Sort(u"Flèche du Jugement",5,5,7,[EffetDegats(64,68,"terre")],2,1,0,1,"cercle",description=u"Occasionne des dommages Terre. Plus le pourcentage de PM du personnage au lancement du sort est important, plus les dommages occasionnés sont importants."))
            sorts.append(Sort(u"Tir Puissant",3,0,6,[EffetEtat(EtatBoostPuissance("Tir_puissant",0,3,250))],1,1,6,1,"cercle",description=u"Augmente les dommages des sorts."))
            sorts.append(Sort(u"Balise Tactique",1,1,10,[EffetInvoque("Balise_tactique",cibles_possibles="", faire_au_vide=True)],1,1,2,1,"cercle",description=u"Invoque une Balise qui peut servir d'obstacle et de cible. La Balise subit 2 fois moins de dommages des alliés."))
            sorts.append(Sort(u"Flèche Harcelante",3,1,12,[EffetDegats(13,15,"air")],1,1,2,1,"cercle",description=u"Occasionne des dommages Air sans ligne de vue."))
            sorts.append(Sort(u"Flèche Massacrante",3,4,8,[EffetDegats(19,22,"air"),EffetEtatSelf(EtatBoostBaseDeg("Fleche_massacrante",1,1,u"Flèche Massacrante",10))],3,2,0,1,"ligne",description=u"Occasionne des dommages Air. Les dommages du sort sont augmentés au tour suivant."))
            sorts.append(Sort(u"Flèche Empoisonnée",3,1,10,[EffetRetPM(4),EffetEtat(EtatEffetDebutTour("Fleche_empoisonnee", 1,2,EffetDegats(17,18,"terre"),"Fleche_empoisonnee","lanceur"))],4,1,0,1,"cercle",description=u"Occasionne des dommages Neutre sur plusieurs tours et retire des PM."))
            sorts.append(Sort(u"Flèche Persecutrice",3,5,8,[EffetDegats(15,17,"feu"),EffetDegats(15,17,"air")],99,2,0,1,"ligne",description=u"Occasionne des dommages Air et Feu."))
            sorts.append(Sort(u"Flèche Tyrannique",4,2,7,[EffetEtat(EtatEffetSiPousse("Fleche_tyrannique_air",0,2, EffetDegats(12,12,"air"),"Fleche_tyrannique","lanceur")),EffetEtat(EtatEffetSiSubit("Fleche_tyrannique_feu",0,2, EffetDegats(12,12,"feu"),"Fleche_tyrannique","doPou","lanceur"))],99,1,0,1,"ligne",description=u"Occasionne des dommages Air si la cible est poussée. Occasionne des dommages Feu si la cible subit des dommages de poussée."))
            sorts.append(Sort(u"Flèche Destructrice",4,5,8,[EffetDegats(30,32,"terre"),EffetEtat(EtatBoostDommage(u"Flèche destructrice",1,1,-60))],99,2,0,1,"cercle",description=u"Occasionne des dommages Terre et réduit les dommages occasionnés par la cible."))
            sorts.append(Sort(u"Tir de Barrage",4,4,8,[EffetDegats(29,33,"terre"),EffetRepousser(2)],3,2,0,1,"cercle",description=u"Occasionne des dommages Terre et repousse la cible."))
            sorts.append(Sort(u"Flèche Absorbante",4,6,8,[EffetVolDeVie(29,31,"air")],3,2,0,1,"cercle",description=u"Vole de la vie dans l'élément Air."))
            sorts.append(Sort(u"Flèche Dévorante",3,1,6,[
                EffetDegats(70,74,"air",zone=TypeZoneCercle(99),etat_requis_cibles="Fleche_devorante_lancer_3",consomme_etat=True),
                EffetEtat(Etat("Fleche_devorante_lancer_3",0,-1),etat_requis_cibles="Fleche_devorante_lancer_2",consomme_etat=True),
                EffetDegats(52,56,"air",zone=TypeZoneCercle(99),etat_requis_cibles="Fleche_devorante_lancer_2",consomme_etat=True),
                EffetEtat(Etat("Fleche_devorante_lancer_2",0,-1),etat_requis_cibles="Fleche_devorante_lancer_1",consomme_etat=True),
                EffetDegats(34,38,"air",zone=TypeZoneCercle(99),etat_requis_cibles="Fleche_devorante_lancer_1",consomme_etat=True),
                EffetEtat(Etat("Fleche_devorante_lancer_1",0,-1),etat_requis_cibles="!Fleche_devorante_lancer_2|!Fleche_devorante_lancer_3")
                ],2,1,0,1,"cercle",chaine=False,description=u"Occasionne des dommages Air. Les dommages sont appliqués lorsque le sort est lancé sur une autre cible. Peut se cumuler 3 fois sur une même cible."))
            sorts.append(Sort(u"Flèche cinglante",2,1,9,[EffetRepousser(2)],4,2,0,1,"ligne",description=u"Applique de l'Érosion aux ennemis et repousse de 2 cases."))
            sorts.append(Sort(u"Flèche de_repli",1,2,5,[EffetPousser(1,zone=TypeZoneCercleSansCentre(5),cible_possibles="Lanceur")],4,2,0,1,"ligne",description=u"Le lanceur du sort recule de 2 cases."))
            sorts.append(Sort(u"Flèche ralentissante",4,1,8,[EffetRetPA(3,zone=TypeZoneCercle(2)),EffetDegats(36,38,"eau",zone=TypeZoneCercle(2))],2,1,0,1,"ligne",description=u"Occasionne des dommages Eau et retire des PA en zone."))
            sorts.append(Sort(u"Flèche percutante",2,1,6,[EffetDegats(6,10,"eau"),EffetEtat(EtatEffetFinTour("Fleche_percutante_retardement", 1,1,EffetDegats(6,10,"eau",zone=TypeZoneCercleSansCentre(2)),"Fleche_percutante_retardement","lanceur")),EffetEtat(EtatEffetFinTour("Fleche_percutante_retardementPA", 1,1,EffetRetPA(2,zone=TypeZoneCercleSansCentre(2)),"Fleche_percutante_retardementPA","lanceur"))],2,1,0,1,"cercle",description=u"Occasionne des dommages Eau. À la fin de son tour, la cible occasionne des dommages Eau et retire des PA en cercle de taille 2 autour d'elle."))
            sorts.append(Sort(u"Flèche explosive",4,1,8,[EffetDegats(36,40,"feu",zone=TypeZoneCercle(3))],2,1,0,1,"cercle",description=u"Occasionne des dommages Feu en zone."))
            fleche_fulminante=Sort(u"Flèche Fulminante",4,1,8,[EffetDegats(39,42,"feu",cibles_possibles="Ennemis|Balise_tactique"),EffetEtatSelf(EtatBoostBaseDeg("Fleche_Fulminante_boost",0,1,u"Flèche Fulminante Rebond",10))],1,1,0,1,"cercle",description=u"Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
            fleche_fulminante_rebond=Sort(u"Flèche Fulminante Rebond",0,0,99,[EffetDegats(39,42,"feu",cibles_possibles="Ennemis|Balise_tactique"),EffetEtatSelf(EtatBoostBaseDeg("Fleche_Fulminante_boost",0,1,u"Flèche Fulminante Rebond",10))],999,999,0,0,"cercle",description=u"Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
            fleche_fulminante.effets.append(EffetPropage(fleche_fulminante_rebond,TypeZoneCercle(2),cibles_possibles="Ennemis|Balise_tactique"))
            fleche_fulminante_rebond.effets.append(EffetPropage(fleche_fulminante_rebond,TypeZoneCercle(2),cibles_possibles="Ennemis|Balise_tactique"))
            sorts.append(fleche_fulminante)
            sorts.append(Sort(u"Maîtrise de l'arc",2,0,6,[EffetEtat(EtatBoostDommage("Maitrise de l'arc",0,3,60))],1,1,5,1,"cercle",description=u"Augmente les dommages."))
            sorts.append(Sort(u"Sentinelle",4,0,0,[EffetEtatSelf(EtatBoostPerDommageSorts("Sentinelle",1,1,30)),EffetEtatSelf(EtatBoostPM("Sentinelle",1,1,-100))],1,1,4,0,"cercle",description=u"Au tour suivant, le lanceur perd tous ses PM mais gagne un bonus de dommages."))
        sorts.append(Sort(u"Cawotte",4,1,6,[EffetInvoque("Cawotte",cibles_possibles="", faire_au_vide=True)], 1,1,6,0,"cercle",description=u"Invoque une Cawotte")) 
        
        return sorts
    def bouge(self, x,y):
        self.historiqueDeplacement.append([self.posX,self.posY,2])
        self.posX = x
        self.posY = y


    def rafraichirHistoriqueDeplacement(self):
        i = 0
        longueurListe = len(self.historiqueDeplacement)
        while i < longueurListe:
            self.historiqueDeplacement[i][2] -= 1 
            if self.historiqueDeplacement[i][2] == 0:
                del self.historiqueDeplacement[i]
                i-=1
            i+=1
            longueurListe = len(self.historiqueDeplacement)


    def tpPosPrec(self, nb, niveau, lanceur, nomSort):
        for i in xrange(nb):
            if(len(self.historiqueDeplacement)>0):
                pos = self.historiqueDeplacement[-1]
                del self.historiqueDeplacement[-1]
                niveau.gereDeplacementTF(self,pos,lanceur,nomSort,AjouteHistorique=False)
                

    def deepcopy(self):
        cp = Personnage(self.classe, self.vie, self.fo, self.agi, self.cha, self.int, self.pui,self.do,self.doFo,self.doAgi,self.doCha,self.doInt,self.doPou,self.PM,self.PA,self.PO,self.lvl,self.team,self.icone)
        cp.sorts = Personnage.ChargerSorts(cp.classe)
        return cp


    def rafraichirEtats(self,niveau,debutTour=True):
        i = 0
        nbEtats = len(self.etats)
        while i < nbEtats:
            if self.etats[i].actif():
                  self.etats[i].duree -= 1
            if debutTour:
                self.etats[i].debuteDans -= 1
            if self.etats[i].debuteDans == 0:
                if self.etats[i].actif():
                    self.etats[i].triggerRafraichissement(self,niveau)
            if self.etats[i].duree == 0:
                #Appliquer les fin de bonus et malus des do, pm, pa, po, pui et carac ici
                print self.classe+" sort de l'etat "+self.etats[i].nom
                self.etats[i].triggerAvantRetrait(self)
                del self.etats[i]
                i-=1
                nbEtats = len(self.etats)
            i+=1

    def aEtat(self,nomEtatCherche):
        for etat in self.etats:
            if etat.nom == nomEtatCherche:
                return True
        return False

    def retirerEtats(self, nomsEtatCherche):
        i = 0
        nbEtats = len(self.etats)
        while i < nbEtats:
            if self.etats[i].nom in nomsEtatCherche:
                #Appliquer les fin de bonus et malus des do, pm, pa, po, pui et carac ici
                print self.classe+" sort de l'etat "+self.etats[i].nom
                self.etats[i].triggerAvantRetrait(self)
                del self.etats[i]
                i-=1
                nbEtats = len(self.etats)
            i+=1

    def subit(self,attaquant, niveau, degats,typeDegats):
        totalPerdu = degats
        if self.vie - degats < 0:
            totalPerdu = self.vie
        for etat in self.etats:
            if etat.actif():
                etat.triggerAvantSubirDegats(self,niveau,totalPerdu,typeDegats,attaquant)
                
        self.vie -= totalPerdu
        print self.classe+" a "+str(self.vie) +" PV restant."
        if self.vie <= 0:
            niveau.tue(self)
        else:
            for etat in self.etats:
                if etat.actif():
                    etat.triggerApresSubirDegats(self,niveau,attaquant)

    def finTour(self,niveau):
        self.PM = self._PM
        self.PA = self._PA
        for sort in self.sorts:
            sort.compteLancerParTour = 0
            sort.compteTourEntreDeux+=1
            sort.compteLancerParTourParJoueur = {}
        for etat in self.etats:
            if etat.actif():
                etat.triggerFinTour(self,niveau)
        for glyphe in niveau.glyphes:
            if glyphe.actif():
                if glyphe.sortMono.APorte(glyphe.centre_x, glyphe.centre_y,self.posX,self.posY, 0):
                    for effet in glyphe.sortMono.effets:
                        niveau.lancerEffet(effet,glyphe.centre_x,glyphe.centre_y,glyphe.nomSort, self.posX, self.posY, glyphe.lanceur)

    def debutTour(self,niveau):     
        self.rafraichirEtats(niveau)
        niveau.rafraichirGlyphes(self)
        self.rafraichirHistoriqueDeplacement()
        for etat in self.etats:
            if etat.actif():
                etat.triggerDebutTour(self,niveau)
        self.posDebTour = [self.posX, self.posY]
        niveau.afficherSorts()
        print "Debut de tour."
        print "PA : "+str(self.PA)
        print "PM : "+str(self.PM)
        print "PV : "+str(self.vie)


    def appliquerEtat(self,etat,lanceur, niveau=None):
        print self.classe+"  etat "+etat.nom+" ("+str(etat.duree)+" tours)"
        etat.lanceur = lanceur
        self.etats.append(etat)
        if self.etats[-1].actif():
            self.etats[-1].triggerInstantane(lanceur=lanceur,niveau=niveau,joueurCaseEffet=self)
    def changeDureeEffets(self, n, niveau):
        for i in xrange(abs(n)):
            self.rafraichirEtats(niveau,False)

    def lanceSort(self, sort,niveau, case_cible_x, case_cible_y, caraclanceur=None):
        caraclanceur = caraclanceur if caraclanceur != None else self
        #Get toutes les cases dans la zone d'effet
        joueurCible=niveau.getJoueurSur(case_cible_x,case_cible_y)
        if sort.APorte(caraclanceur.posX, caraclanceur.posY,case_cible_x,case_cible_y, caraclanceur.PO):
            print caraclanceur.classe+" lance :"+sort.nom
            res,explication,coutPA = sort.estLancable(niveau, caraclanceur, joueurCible)
            if res == True:
                caraclanceur.PA -= coutPA
                sort.marquerLancer(joueurCible)
                print caraclanceur.classe+": -"+str(coutPA)+" PA (reste "+str(caraclanceur.PA)+"PA)"
                sestApplique = True
                for effet in sort.effets:
                    if sort.chaine == True:
                        if sestApplique == True:
                            sestApplique = False
                        else:
                            return None
                    sestApplique, cibles = niveau.lancerEffet(effet,caraclanceur.posX,caraclanceur.posY,sort.nom, case_cible_x, case_cible_y,caraclanceur)          
                    #Apres application d'un effet sur toutes les cibles:
            else:
                print explication
        else:
            print "Cible hors de porte"
        niveau.afficherSorts()

    def joue(self,event,niveau,mouse_xy,sortSelectionne):
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicGauche,clicMilieu,clicDroit = pygame.mouse.get_pressed()
            if clicGauche:
            #Click sort
                if mouse_xy[1] > y_sorts:
                    for sort in niveau.tourDe.sorts:
                        if sort.vue.isMouseOver(mouse_xy):
                            
                            coutPA = sort.coutPA
                            for etat in niveau.tourDe.etats:
                                if etat.actif():
                                    if etat.nom == "CoutPA" and sort.nom == etat.tabCarac[0]:
                                        coutPA+=etat.tabCarac[1]
                            if coutPA < 0:
                                coutPA = 0
                            if (coutPA <= niveau.tourDe.PA):
                                res, explication,coutPA = sort.estLancable(niveau,niveau.tourDe,None)
                                if res == True:
                                    sortSelectionne = sort
                                else:
                                    print explication

                            else:
                                print "PA insuffisant : coute "+str(coutPA)+ " mais "+str(niveau.tourDe.PA) + " restant."
                            break
                #Click map
                else:
                    #Un sort est selectionne
                    if sortSelectionne != None:
                        case_cible_x = mouse_xy[0]/taille_sprite
                        case_cible_y = mouse_xy[1]/taille_sprite
                        niveau.tourDe.lanceSort(sortSelectionne,niveau, case_cible_x,case_cible_y)
                        sortSelectionne = None
                    #Aucun sort n'est selectionne: on pm
                    else:
                        niveau.Deplacement(mouse_xy)
            elif clicDroit:
                if mouse_xy[1]<y_sorts:
                    case_x = mouse_xy[0]/taille_sprite
                    case_y = mouse_xy[1]/taille_sprite
                    joueurInfo = niveau.getJoueurSur(case_x, case_y)
                    if joueurInfo != None:
                        for etat in joueurInfo.etats:
                            print joueurInfo.classe+" est dans l'etat "+etat.nom+" ("+str(etat.duree)+")"
        elif event.type == pygame.KEYDOWN:
            if event.key == K_F1:
                niveau.finTour()
            #elif event.key == K_ESCAPE:
            #    continuer = 0 
            
        elif event.type==KEYDOWN and event.key == K_ESCAPE:
            sortSelectionne = None


        return sortSelectionne
class PersonnageMur(Personnage):
    def __init__(self, *args):
        super(PersonnageMur, self).__init__(*args)
    def deepcopy(self):
        cp = PersonnageMur(self.classe, self.vie, self.fo, self.agi, self.cha, self.int, self.pui,self.do,self.doFo,self.doAgi,self.doCha,self.doInt,self.doPou,self.PM,self.PA,self.PO,self.lvl,self.team,self.icone)
        cp.sorts = Personnage.ChargerSorts(cp.classe)
        return cp
    def joue(self,event,niveau,mouse_xy,sortSelectionne):
        print "Tour de "+str(niveau.tourDe.classe)
        niveau.finTour()

class PersonnageSansPM(Personnage):
    def __init__(self, *args):
        super(PersonnageSansPM, self).__init__(*args)
    def deepcopy(self):
        cp = PersonnageSansPM(self.classe, self.vie, self.fo, self.agi, self.cha, self.int, self.pui,self.do,self.doFo,self.doAgi,self.doCha,self.doInt,self.doPou,self.PM,self.PA,self.PO,self.lvl,self.team,self.icone)
        cp.sorts = Personnage.ChargerSorts(cp.classe)
        return cp
    def joue(self,event,niveau,mouse_xy,sortSelectionne):
        niveau.tourDe.lanceSort(self.sorts[0], niveau, self.posX, self.posY)
        niveau.finTour()
class Case:
    def __init__(self, typ, hitbox):
        self.type = typ
        self.hitbox = hitbox
        self.effetsSur = []
class Sort:
    def __init__(self,nom,coutPA,POMin,POMax, tableauEffets, nbLancerParTour, nbLancerParTourParJoueur, nbTourEntreDeux, POMod,typeLancer, **kwargs):
        self.nom = nom
        self.coutPA = coutPA
        self.POMin = POMin
        self.POMax = POMax
        self.effets = tableauEffets
        self.POMod = POMod
        self.typeLancer = typeLancer
        self.image = "sorts/"+normaliser(nom.lower())+".png"
        self.hitbox = None
        self.chaine = kwargs.get("chaine",True)
        self.nbLancerParTour = nbLancerParTour
        self.nbLancerParTourParJoueur = nbLancerParTourParJoueur
        self.nbTourEntreDeux = nbTourEntreDeux
        self.compteLancerParTour = 0
        self.compteLancerParTourParJoueur = {}
        self.compteTourEntreDeux = nbTourEntreDeux
        self.description = kwargs.get("description","")
        self.overlay = Overlay(self,ColoredText("nom",(210,105,30)),ColoredText("description",(224,238,238)),(56,56,56))

    def APorte(self, j1x,j1y,ciblex,cibley,PO):
        distanceX = abs(ciblex-j1x)
        distanceY = abs(cibley-j1y)
        distance = distanceX+distanceY
        sortPoMin = self.POMin
        sortPoMax = self.POMax+(self.POMod*PO)
        if self.typeLancer == "ligne":
            if distanceX > 0 and distanceY>0:
                return False
        elif self.typeLancer == "diagonale":
            if distanceY != distanceX:
                return False
            sortPoMin*=2
            sortPoMax*=2
        return (distance >= sortPoMin and distance <= sortPoMax)

    def getCoutPA(self,joueurLanceur):
        coutPA = self.coutPA
        for etat in joueurLanceur.etats:
            if etat.actif():
                coutPA = etat.triggerCoutPA(self,coutPA)

        if coutPA < 0:
            coutPA = 0
        return coutPA

    def estLancable(self, niveau, joueurLanceur,joueurCible):
        coutPA = self.getCoutPA(joueurLanceur)
        if self.compteTourEntreDeux >= self.nbTourEntreDeux:
            if self.compteLancerParTour < self.nbLancerParTour:
                if joueurCible != None:
                    if not joueurCible in self.compteLancerParTourParJoueur:
                        self.compteLancerParTourParJoueur[joueurCible] = 0
                    if self.compteLancerParTourParJoueur[joueurCible] < self.nbLancerParTourParJoueur:
                        return True,"",coutPA
                    else:
                        return False,"Ce sort ne peut plus etre utilise sur ce personnage ce tour.",0
                else:
                    return True,"",coutPA
            else:
                return False,"Ce sort ne peut plus etre utilise ce tour.",0
        else:
            return False,"Delai avant prochain lance:"+str(self.nbTourEntreDeux-self.compteTourEntreDeux),0

    def marquerLancer(self,joueurCible):
        self.compteLancerParTour+=1
        if joueurCible != None:
            self.compteLancerParTourParJoueur[joueurCible]+=1
        self.compteTourEntreDeux = 0

class Niveau:
    INVOCS = {
u"Cawotte" : PersonnageMur(u"Cawotte",800,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"cawotte.png"),
u"Synchro" : PersonnageMur(u"Synchro",1200,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"synchro.png"),
u"Cadran de Xélor" : PersonnageSansPM(u"Cadran de Xélor",1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"cadran_de_xelor.png"),
u"Complice" : PersonnageMur(u"Complice",650,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"complice.png"),
u"Balise de Rappel" : PersonnageSansPM(u"Balise de Rappel",1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"balise_de_rappel.png"),
u"Balise Tactique" : PersonnageMur(u"Balise Tactique",1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"balise_tactique.png"),
u"Stratège Top" : PersonnageMur(u"Stratège Top",1385,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"conquete.png")
}
    """Classe permettant de créer un niveau"""
    def __init__(self, fenetre, joueurs,font):
        self.structure = None
        
        self.taille = taille_carte
        self.departT1 = [[5,5]]
        self.departT2 = [[8,8]]
        self.joueurs = joueurs
        self.tourIndex = 0
        self.tourDe = self.joueurs[self.tourIndex]
        self.glyphes=[]
        self.fenetre = fenetre
        self.myfont = font
        self.generer()
        self.initJoueurs()


    def Deplacement(self, mouse_xy):
        case_x = mouse_xy[0]/taille_sprite
        case_y = mouse_xy[1]/taille_sprite
        joueur = self.tourDe
        cases = self.pathFinding(case_x,case_y,joueur)
        if cases != None:
            if len(cases)<=joueur.PM:
                joueur.PM -= len(cases)
                self.structure[joueur.posY][joueur.posX].type = "v"
                for case in cases:
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
        departX = case_x
        departY = case_y
        retour = []
        if distance == 0:
            return [[case_x,case_y]]
        delta = 0
        #Oblige de faire delta 0 a la main pour eviter l'ajour de +0 et -0
        if departX-delta >=0:
            if departY-distance+delta>=0:
                retour.append([departX-delta, departY-distance+delta])
            if departY+distance-delta<taille_carte:
                retour.append([departX-delta, departY+distance-delta])
        for delta in xrange(1,distance):
            if departX-delta >=0:
                if departY-distance+delta>=0:
                    retour.append([departX-delta, departY-distance+delta])
                if departY+distance-delta<taille_carte:
                    retour.append([departX-delta, departY+distance-delta])
            if departX+delta < taille_carte:
                if departY-distance+delta>=0:
                    retour.append([departX+delta, departY-distance+delta])
                if departY+distance-delta<taille_carte:
                    retour.append([departX+delta, departY+distance-delta])    
        delta=distance
        #Oblige de faire delta distance a la main pour eviter l'ajout de +0 et -0
        if departX-delta >=0:
            if departY-distance+delta>=0:
                retour.append([departX-delta, departY-distance+delta])
        if departX+delta >=0:
            if departY-distance+delta>=0:
                retour.append([departX+delta, departY-distance+delta])
        return retour

    def afficherSorts(self):
        pygame.draw.rect(self.fenetre, pygame.Color(0, 0, 0), pygame.Rect(x_sorts, y_sorts, width_sorts, height_sorts))
        surfaceGrise = pygame.Surface((30   ,30), pygame.SRCALPHA)   # per-pixel alpha
        surfaceGrise.fill((128,128,128,128))                         # notice the alpha value in the color
        x = x_sorts
        y = y_sorts
        for sort in self.tourDe.sorts:
            sort.vue = VueForOverlay(self.fenetre, x, y, 30, 30,sort)
            try:
                imageSort = pygame.image.load(sort.image).convert()
                self.fenetre.blit(imageSort, (x,y))
            except:
                pass
            res,explication,coutPA = sort.estLancable(self,self.tourDe,None)
            if res == False:
                self.fenetre.blit(surfaceGrise, (x,y))
                if "avant prochain lance" in explication:
                    delai = int(explication.split(":")[1])
                    delaiLabel = self.myfont.render(str(delai), 1, (0,0,0))
                    self.fenetre.blit(delaiLabel, (x, y))
            x+=30
            if(x+30>x_sorts+width_sorts):
                y+=30
                x=x_sorts
    
    def initJoueurs(self):
        placeT1 = 0
        placeT2 = 0
        for joueur in self.joueurs:
            if joueur.team == 1:
                joueur.posX = self.departT1[placeT1][0]
                joueur.posY = self.departT1[placeT1][1]
                placeT1+=1
                joueur.posDebTour = [joueur.posX, joueur.posY]
            else:
                joueur.posX = self.departT2[placeT2][0]
                joueur.posY = self.departT2[placeT2][1]
                placeT2+=1
                joueur.posDebTour = [joueur.posX, joueur.posY]
            self.structure[joueur.posY][joueur.posX].type="j"

    def rafraichirGlyphes(self, duJoueur):
        i=0
        longueurTab = len(self.glyphes)
        while i < longueurTab:
            if self.glyphes[i].lanceur == duJoueur:
                if self.glyphes[i].actif():
                    self.glyphes[i].duree -= 1
                    if(self.glyphes[i].duree <= 0):
                        del self.glyphes[i]
                        i-=1
            longueurTab = len(self.glyphes)
            i+=1
    
    def finTour(self):
        self.tourDe.finTour(self)
        self.tourIndex = (self.tourIndex + 1) % len(self.joueurs)
        self.tourDe = self.joueurs[self.tourIndex]
        self.tourDe.debutTour(self)
        
    def tue(self, perso):
        print perso.classe+" est mort!"
        i= 0 
        while i < xrange(len(self.joueurs)):
            if self.joueurs[i] == perso:
                self.structure[perso.posY][perso.posX].type="v"
                del self.joueurs[i]
                i-=1
                break
            i+=1

    def generer(self):
        """Méthode permettant de générer le niveau en fonction du fichier.
        On crée une liste générale, contenant une liste par ligne à afficher""" 
        #On ouvre le fichier
        structure_niveau=[]
        for i in xrange(self.taille):
            ligne_niveau = []
            #On parcourt les sprites (lettres) contenus dans le fichier
            for j in xrange(self.taille):
                x = j * taille_sprite
                y = i * taille_sprite
                ligne_niveau.append(Case("v", pygame.draw.rect(self.fenetre, (0,0,0), [x , y, taille_sprite, taille_sprite])))
            #On ajoute la ligne à la liste du niveau
            structure_niveau.append(ligne_niveau)
        #On sauvegarde cette structure
        self.structure = structure_niveau

    def getJoueurSur(self, case_x,case_y):
        for i,joueur in enumerate(self.joueurs):
            if joueur.posX == case_x and joueur.posY == case_y:
                return self.joueurs[i]
        return None

    def joueursAvecEtat(self,nomEtatCherche):
        retourListeJoueurs = []
        for joueur in self.joueurs:
            for etat in joueur.etats:
                if etat.nom == nomEtatCherche:
                    retourListeJoueurs.append(joueur)
        return retourListeJoueurs

    def invoque(self,invoc,case_x,case_y):
        print "Invocation "+invoc.classe
        self.structure[case_y][case_x].type = "j"
        invoc.posX = case_x
        invoc.posY = case_y
        for i in xrange(len(self.joueurs)):
            if self.joueurs[i] == self.tourDe:
                self.joueurs.insert(i+1, invoc)
                break

    def getZoneEffet(self, effet, case_x,case_y):
        tab_cases_zone = []
        x0 = case_x
        y0 = case_y
        for tailleCercle in xrange(64):
            casesAXDistance = Niveau.getCasesAXDistanceDe(case_x,case_y,tailleCercle)
            for case in casesAXDistance:
                if effet.APorteZone(case_x,case_y,case[0],case[1], self.tourDe.posX, self.tourDe.posY):
                    tab_cases_zone.append(case)
        return tab_cases_zone

    def getZonePorteSort(self, sort, x0, y0, poLanceur):
        tab_cases_zone = []
        for tailleCercle in xrange(sort.POMin,sort.POMax+1):
            casesAXDistance = Niveau.getCasesAXDistanceDe(x0,y0,tailleCercle)
            for case in casesAXDistance:
                if sort.APorte(x0,y0,case[0],case[1], poLanceur):
                    tab_cases_zone.append(case)
        return tab_cases_zone    

    def determinerSensPousser(self,joueurCible,depuisX,depuisY):
        if depuisY == joueurCible.posY and depuisX == joueurCible.posX:
            return None,None
        if depuisY == None:
            depuisY = self.tourDe.posY-1
        if depuisX == None:
            depuisX = self.tourDe.posX    
        horizontal = not (joueurCible.posX == depuisX)
        if horizontal and joueurCible.posX > depuisX:
            positif = True
        elif (not horizontal) and joueurCible.posY > depuisY:
            positif = 1
        else:
            positif = -1 
        return horizontal,positif
    def effectuerPousser(self,joueurCible,doDeg,posPouX,posPouY,D,pousseur):
        self.structure[joueurCible.posY][joueurCible.posX].type = "v"
        joueurCible.bouge(posPouX,posPouY)
        self.structure[joueurCible.posY][joueurCible.posX].type = "j"
        R = 6
        if doDeg:
            doPou = pousseur.doPou
            for etat in pousseur.etats:
                if etat.actif():
                    doPou = etat.triggerCalculPousser(doPou,self,pousseur,joueurCible)
            for etat in joueurCible.etats:
                if etat.actif():
                    doPou = etat.triggerCalculPousser(doPou,self,pousseur,joueurCible)
            total = (8+R*pousseur.lvl/50)*D+doPou
            if total > 0:
                print joueurCible.classe+" perd "+ str(total) + "PV (do pou)"
                joueurCible.subit(pousseur,self,total,"doPou")

    def pousser(self, nbCases, joueurCible,pousseur,doDeg=True,depuisX=None,depuisY=None):
        horizontal,positif = self.determinerSensPousser(joueurCible,depuisX,depuisY)
        if horizontal != None:
            posPouX,posPouY,D = self.calculerArrivePousser(joueurCible, nbCases, int(horizontal), positif)
            self.effectuerPousser(joueurCible,doDeg,posPouX,posPouY,D,pousseur)
        
    def calculerArrivePousser(self, joueurCible, nbCases, horizontal, positif):
        D = 0    
        _posPouX = joueurCible.posX
        _posPouY = joueurCible.posY
        for fait in xrange(nbCases):
            posPouX = _posPouX
            posPouY = _posPouY
            posPouX = posPouX + (1*positif*horizontal)
            posPouY = posPouY + (1*positif*((horizontal+1)%2))
            if posPouX >= self.taille or posPouX < 0 or posPouY >= self.taille or posPouY < 0:
                D+=1
                posPouY = _posPouY
                posPouX = _posPouX
            #Case separe de l'autre car les index sont nike et pas envie de try except pour un cas attendu
            elif self.structure[posPouY][posPouX].type != "v":
                D+=1
                posPouY = _posPouY
                posPouX = _posPouX
            else:
                _posPouX = posPouX
                _posPouY = posPouY
        return posPouX,posPouY,D

    def attire(self, nbCases, joueurCible, attireur):
        distanceX = abs(joueurCible.posX - attireur.posX)
        distanceY = abs(joueurCible.posY - attireur.posY)
        horizontal = distanceX > distanceY
        if horizontal:
            positif = joueurCible.posX > attireur.posX
        else:
            positif = joueurCible.posY > attireur.posY
        if horizontal and positif:
            self.pousser(nbCases,joueurCible,attireur,False,joueurCible.posX+1,joueurCible.posY)
        elif horizontal:
            self.pousser(nbCases,joueurCible,attireur,False,joueurCible.posX-1,joueurCible.posY)
        elif not horizontal and positif:
            self.pousser(nbCases,joueurCible,attireur,False,joueurCible.posX,joueurCible.posY+1)
        else:
            self.pousser(nbCases,joueurCible,attireur,False,joueurCible.posX,joueurCible.posY-1)

    def deplacementTFVersCaseVide(self,joueurBougeant, posAtteinte,AjouteHistorique):
        self.structure[posAtteinte[1]][posAtteinte[0]].type = "j"
        self.structure[joueurBougeant.posY][joueurBougeant.posX].type = "v"
        if AjouteHistorique:
            joueurBougeant.bouge(posAtteinte[0], posAtteinte[1])
        else:
            joueurBougeant.posX = posAtteinte[0]
            joueurBougeant.posY = posAtteinte[1]

    def boostSynchrosApresTF(self,nomSort,reelLanceur):
        synchros = self.getJoueurs("Synchro")
        for synchro in synchros:
            if not synchro.aEtat(nomSort) and nomSort != "Rembobinage" and not synchro.aEtat("DejaBoost"):
                synchro.appliquerEtat(Etat("Boost Synchro "+nomSort,0,-1, reelLanceur),reelLanceur)
                synchro.appliquerEtat(Etat("DejaBoost",0,1,[nomSort], reelLanceur),reelLanceur)

    def exploserSynchro(self,synchro,reelLanceur):
        nbTF = 0
        for etat in synchro.etats:
            if etat.nom.startswith("Boost Synchro"):
                nbTF+=1
        synchro.lanceSort(Sort("Fin_des_temps",0,0,0,[EffetDegats(int(reelLanceur.lvl*1.90)*(nbTF*2-1),int(reelLanceur.lvl*1.90)*(nbTF*2-1),"air",zone=TypeZoneCercle(3),cibles_possibles="Ennemis")], 99,99,0,0,"cercle"),self,synchro.posX,synchro.posY)
        self.tue(synchro)

    def glypheActiveTF(self,reelLanceur,nomSort):
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

    def deplacementTFVersCaseOccupee(self, joueurBougeant, posAtteinte, reelLanceur,nomSort, AjouteHistorique,genereTF):
        joueurSwap = self.effectuerTF(joueurBougeant,posAtteinte,reelLanceur,nomSort,AjouteHistorique,genereTF)
        #Si le xelor est pas deja boostPA par ce sort, rembo ne peut pas boost PA
        if genereTF:
            if not reelLanceur.aEtat(nomSort) and nomSort != "Rembobinage":
                reelLanceur.appliquerEtat(Etat("BoostPA",0,1,[2],reelLanceur),reelLanceur)
                reelLanceur.appliquerEtat(Etat(nomSort,0,1,["Telefrag"],reelLanceur),reelLanceur)
            self.boostSynchrosApresTF(nomSort,reelLanceur)
            if ("Synchro" == joueurBougeant.classe) and not reelLanceur.aEtat("Faille_temporelle"):
                self.exploserSynchro(joueurBougeant,reelLanceur)
            elif ("Synchro" == joueurSwap.classe) and not reelLanceur.aEtat("Faille_temporelle"):
                self.exploserSynchro(joueurSwap,reelLanceur)
            self.glypheActiveTF(reelLanceur,nomSort)
        return joueurSwap    

    def effectuerTF(self, joueurBougeant,posAtteinte,reelLanceur,nomSort,AjouteHistorique,genereTF):
        joueurASwap = self.getJoueurSur(posAtteinte[0],posAtteinte[1])
        joueurASwap.bouge(joueurBougeant.posX, joueurBougeant.posY)
        if AjouteHistorique:
            joueurBougeant.bouge(posAtteinte[0], posAtteinte[1])
        else:
            joueurBougeant.posX = posAtteinte[0]
            joueurBougeant.posY = posAtteinte[1]
        if genereTF:
            joueurBougeant.retirerEtats("Telefrag")
            joueurASwap.retirerEtats("Telefrag")
            joueurBougeant.appliquerEtat(Etat("Telefrag",0,2,[nomSort],reelLanceur),reelLanceur)
            joueurASwap.appliquerEtat(Etat("Telefrag",0,2,[nomSort],reelLanceur),reelLanceur)
        return joueurASwap

    def gereDeplacementTF(self, joueurBougeant, posAtteinte, lanceur, nomSort, AjouteHistorique=True, genereTF=True):
        if posAtteinte[1]<0 or posAtteinte[1]>=taille_carte or posAtteinte[0]<0 or posAtteinte[0]>=taille_carte:
            return None
        if self.structure[posAtteinte[1]][posAtteinte[0]].type == "v":
            self.deplacementTFVersCaseVide(joueurBougeant, posAtteinte,AjouteHistorique)
            return None
        elif self.structure[posAtteinte[1]][posAtteinte[0]].type == "j":
            if lanceur.invocateur != None:
                reelLanceur = lanceur.invocateur
            else:
                reelLanceur = lanceur
            joueurASwap = self.deplacementTFVersCaseOccupee(joueurBougeant, posAtteinte, reelLanceur,nomSort, AjouteHistorique,genereTF)
            return joueurASwap
        else:
            print "Deplacement pas implemente"
        return None

    def appliquerEffetSansBoucleSurZone(self,effet,joueurLanceur,case_cible_x,case_cible_y,nomSort,ciblesTraitees,prov_x,prov_y):
        if type(effet) == type(EffetGlyphe(None,None,None,None)):
            effet.appliquerEffet(self,None,joueurLanceur, case_cible_x=case_cible_x, case_cible_y=case_cible_y, nom_sort=nomSort, cibles_traitees=ciblesTraitees, prov_x=prov_x, prov_y=prov_y)
            return True
        return False

    def appliquerEffetSurZone(self,zoneEffet,effet,joueurLanceur,joueurCibleDirect,case_cible_x,case_cible_y,nomSort,ciblesTraitees,prov_x,prov_y):
        sestApplique = False
        for case_effet in zoneEffet:
            case_x = case_effet[0]
            case_y = case_effet[1]
            joueurCaseEffet = self.getJoueurSur(case_x, case_y)

            if joueurCaseEffet != None:
                if effet.cibleValide(joueurLanceur, joueurCaseEffet,joueurCibleDirect,ciblesTraitees):

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
        if lanceur == None:
            joueurLanceur = self.getJoueurSur(prov_x,prov_y)
        else:
            joueurLanceur = lanceur

        ciblesTraitees = []
        joueurCibleDirect = self.getJoueurSur(case_cible_x, case_cible_y)
        if type(effet) is EffetDegatsPosLanceur or type(effet) is EffetTeleportePosPrecLanceur:
            case_cible_x = joueurLanceur.posX
            case_cible_y = joueurLanceur.posY
        zoneEffet = self.getZoneEffet(effet, case_cible_x,case_cible_y)
        #Effet non boucles
        sestApplique = self.appliquerEffetSansBoucleSurZone(effet,joueurLanceur,case_cible_x,case_cible_y,nomSort,ciblesTraitees,prov_x,prov_y)
        if sestApplique == True:
            return sestApplique,ciblesTraitees
        return self.appliquerEffetSurZone(zoneEffet,effet,joueurLanceur,joueurCibleDirect,case_cible_x,case_cible_y,nomSort,ciblesTraitees,prov_x,prov_y)

    def getJoueurs(self, cibles):
        onCherche = cibles.split("|")
        retour = []
        #if (joueurCaseEffet.team == joueurLanceur.team and joueurCaseEffet != joueurLanceur and effet.faireAuxAllies) or (joueurCaseEffet.team == joueurLanceur.team and joueurCaseEffet == joueurLanceur and effet.faireAuLanceur) or (joueurCaseEffet.team != joueurLanceur.team and effet.faireAuxEnnemis):
        for joueur in self.joueurs:
            if joueur.classe in onCherche:
                retour.append(joueur)
        return retour

    def getJoueurslesPlusProches(self, case_x,case_y,lanceur,zone=TypeZoneCercle(99),etatRequisCibles=[],ciblesPossibles=[],ciblesExclues=[],ciblesTraitees=[]):
        joueurs_cases_zone = []
        x0 = case_x
        y0 = case_y
        for tailleCercle in xrange(64):
            casesAXDistance = self.getCasesAXDistanceDe(case_x,case_y,tailleCercle)
            for case in casesAXDistance:
                if zone.testCaseEstDedans([case_x,case_y],case,None):
                    joueur = self.getJoueurSur(case[0],case[1])
                    if joueur != None:
                        if (joueur.team == lanceur.team and joueur != lanceur and "Allies" in ciblesPossibles) or (joueur.team == lanceur.team and joueur == lanceur and "Lanceur" in ciblesPossibles) or (joueur.team != lanceur.team and "Ennemis" in ciblesPossibles) or (joueur.classe in ciblesPossibles):
                            if not(joueur.classe in ciblesExclues or (joueur.classe == lanceur.classe and "Lanceur" in ciblesExclues)):
                                #Test sur l'etat requis.
                                if joueur.aEtatsRequis(etatRequisCibles):
                                    #Test si le joueur cible a deja ete impacte, pour raulebque notamment
                                    if joueur not in ciblesTraitees:
                                        joueurs_cases_zone.append(joueur)
        return joueurs_cases_zone

    def afficher(self, fenetre, sortSelectionne, mouse_xy):
        """Méthode permettant d'afficher le niveau en fonction 
        de la liste de structure renvoyée par generer(), La fonction n'appelle pas de sous fonction car le test de performance etait catastrophique"""
        #Chargement des images (seule celle d'arrivée contient de la transparence)
        
        vide1 = pygame.image.load(image_vide_1).convert()
        vide2 = pygame.image.load(image_vide_2).convert()
        team1 = pygame.image.load(image_team_1).convert_alpha()
        team2 = pygame.image.load(image_team_2).convert_alpha()
        prevision = pygame.image.load(image_prevision).convert()
        zone = pygame.image.load(image_zone).convert()
        glyphe_ou_piege = pygame.image.load(image_team_1).convert()
        #On parcourt la liste du niveau
        num_ligne = 0
        tab_cases_previ = []
        
        for ligne in self.structure:
            #Onparcourt les listes de lignes
            num_case = 0
            for sprite in ligne:
                #On calcule la position réelle en pixels
                x = num_case * taille_sprite
                y = num_ligne * taille_sprite
                if sprite.type == 'v' or sprite.type == 'j':          #v = Vide, j = joueur
                    if (num_case+(num_ligne*len(ligne)))%2 == 0:
                        fenetre.blit(vide1, (x,y))
                    else:
                        fenetre.blit(vide2, (x,y))
                    #Afficher les cases glyphees
                    for glyphe in self.glyphes:
                        if glyphe.actif():
                            if glyphe.sortMono.APorte(glyphe.centre_x, glyphe.centre_y, num_case, num_ligne, 0):
                                pygame.draw.rect(fenetre, glyphe.couleur, Rect(num_case*taille_sprite+1, num_ligne*taille_sprite+1,taille_sprite-2,taille_sprite-2))

                    #Afficher previsualation portee du sort selectionne
                    if sortSelectionne != None:
                        #Previsu de la porte du sort, une case teste par tour de double boucle
                        if sortSelectionne.APorte(self.tourDe.posX, self.tourDe.posY, num_case,num_ligne, self.tourDe.PO):
                            fenetre.blit(prevision, (x,y))
                        if mouse_xy[1] < y_sorts:
                            case_x = mouse_xy[0]/taille_sprite
                            case_y = mouse_xy[1]/taille_sprite
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
                fenetre.blit(zone, (case[0]*taille_sprite,case[1]*taille_sprite))
        else:
            if mouse_xy[1] < y_sorts:
                case_x = mouse_xy[0]/taille_sprite
                case_y = mouse_xy[1]/taille_sprite
                tab_cases_previ = self.pathFinding(case_x,case_y,self.tourDe)
                if tab_cases_previ != None:
                    if len(tab_cases_previ) <= self.tourDe.PM:
                        for case in tab_cases_previ:
                            fenetre.blit(prevision, (case[0]*taille_sprite,case[1]*taille_sprite))


        #Afficher joueurs
        for joueur in self.joueurs:
            
            x = joueur.posX*taille_sprite
            y = joueur.posY*taille_sprite
            if joueur.team == 1:    
                fenetre.blit(team1, (x,y))
            else:
                fenetre.blit(team2, (x,y))
            joueur.vue = VueForOverlay(self.fenetre, x, y, 30, 30,joueur)
            fenetre.blit(pygame.image.load(joueur.icone).convert_alpha(), (x,y))

        #AfficherOverlays
        if mouse_xy[1] > y_sorts:
            for sort in self.tourDe.sorts:
                if sort.vue.isMouseOver(mouse_xy):
                    sort.overlay.afficher(sort.vue.x,y_sorts)
        else:
            for joueur in self.joueurs:
                if joueur.vue.isMouseOver(mouse_xy):
                    joueur.overlay.afficher(joueur.posX*taille_sprite,joueur.posY*taille_sprite)

    def poseGlyphe(self,glyphe):
        self.glyphes.append(glyphe)
        return len(self.glyphes)-1

    def ajoutTrie(self,liste,noeud):
        liste.append(noeud)
        liste.sort(cmp=compare2Noeuds)

    def getVoisins(self,x,y):
        voisins = []
        if x > 0:
            if self.structure[y][x-1].type == "v":
                voisins.append(Noeud(x-1,y))
        if x < taille_carte-1:
            if self.structure[y][x+1].type == "v":
                voisins.append(Noeud(x+1,y))
        if y > 0:
            if self.structure[y-1][x].type == "v":
                voisins.append(Noeud(x,y-1))
        if y < taille_carte-1:
            if self.structure[y+1][x].type == "v":
                voisins.append(Noeud(x,y+1))
        return voisins

    def pathFinding(self, case_cible_x, case_cible_y, joueur):
        listeFermee = []
        listeOuverte = []
        if self.structure[case_cible_y][case_cible_x].type != "v":
            return None
        depart = Noeud(joueur.posX, joueur.posY)
        self.ajoutTrie(listeOuverte,depart)
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
                    self.ajoutTrie(listeOuverte,v)
            listeFermee.append(u)
        print "Aucun chemin trouvee"
        return None
