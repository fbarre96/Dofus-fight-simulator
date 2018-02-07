# -*- coding: utf-8 -*
import constantes
import Overlays
class Sort:
    def __init__(self,nom,coutPA,POMin,POMax, tableauEffets, nbLancerParTour, nbLancerParTourParJoueur, nbTourEntreDeux, POMod,typeLancer, **kwargs):
        self.nom = nom
        self.coutPA = coutPA
        self.POMin = POMin
        self.POMax = POMax
        self.effets = tableauEffets
        self.POMod = POMod
        self.typeLancer = typeLancer
        self.image = "sorts/"+constantes.normaliser(nom.lower())+".png"
        self.hitbox = None
        self.chaine = kwargs.get("chaine",True)
        self.nbLancerParTour = nbLancerParTour
        self.nbLancerParTourParJoueur = nbLancerParTourParJoueur
        self.nbTourEntreDeux = nbTourEntreDeux
        self.compteLancerParTour = 0
        self.compteLancerParTourParJoueur = {}
        self.compteTourEntreDeux = nbTourEntreDeux
        self.description = kwargs.get("description","")
        self.overlay = Overlays.Overlay(self, Overlays.ColoredText("nom",(210,105,30)), Overlays.ColoredText("description",(224,238,238)),(56,56,56))

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
