# -*- coding: utf-8 -*
import constantes
import Overlays
import random
import Niveau
from copy import deepcopy
class Sort:
    def __init__(self,nom,lvl,coutPA,POMin,POMax, tableauEffets, tableauEffetsCC, probaCC, nbLancerParTour, nbLancerParTourParJoueur, nbTourEntreDeux, POMod,typeLancer,ldv, **kwargs):
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
        res,msg,coutPA = self.sortEstLancable(niveau, joueurLanceur,joueurCible)
        if res == False:
            return res,msg,coutPA
        for effet in self.effets:
            res, msg =effet.estLancable(joueurLanceur,joueurCible)
            if res == False:
                return res, msg, coutPA
        return True, msg, coutPA

    def sortEstLancable(self, niveau, joueurLanceur,joueurCible):
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

    def lance(self, origine_x,origine_y,niveau, case_cible_x, case_cible_y, caraclanceur=None , isPrevisu=False):
        """@summary: Lance un sort
        @origine_x: la pos x d'où est lancé le sort
        @type: int
        @origine_y: la pos y d'où est lancé le sort
        @type: int
        @niveau: La grille de jeu
        @type: Niveau
        @case_cible_x: La coordonnée x de la case cible du sort
        @type: int
        @case_cible_y: La coordonnée y de la case cible du sort
        @type: int
        @caraclanceur: le personnage dont les caractéristiques doivent être prise pour infliger les dégâts de sort. Optionnel : self est pris à la place
        @type: Personnage (ou None pour prendre le lanceur)"""
        if isPrevisu:
            save = Niveau.SaveStateNiveau(niveau)
        case_cible_x = int(case_cible_x)
        case_cible_y = int(case_cible_y)
        caraclanceur = caraclanceur if caraclanceur != None else niveau.getJoueurSur(origine_x,origine_y)
        #Get toutes les cases dans la zone d'effet
        joueurCible=niveau.getJoueurSur(case_cible_x,case_cible_y)
        #Test si la case est bien dans la portée du sort
        if self.APorte(origine_x, origine_y,case_cible_x,case_cible_y, caraclanceur.PO):
            if not isPrevisu:
                print(caraclanceur.classe+" lance :"+self.nom)
            #Test si le sort est lançable (cout PA suffisant, délai et nombre d'utilisations par tour et par cible)
            res,explication,coutPA = self.estLancable(niveau, caraclanceur, joueurCible)
            if res == True:
                #Lancer du sort
                if not isPrevisu:
                    caraclanceur.PA -= coutPA
                    self.marquerLancer(joueurCible)
                    print(caraclanceur.classe+": -"+str(coutPA)+" PA (reste "+str(caraclanceur.PA)+"PA)")
                chanceCC = caraclanceur.cc + self.probaCC
                randomVal = round(random.random(),2)
                if self.probaCC == 0:
                    isCC = False
                else:
                    isCC = (randomVal*100 <= chanceCC)
                
                if isCC and not isPrevisu: # TOFIX : PREVISUALISATION IMPOSSIBLE POUR CC
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
                    if self.chaine == True:
                        if sestApplique == True: # Si l'effet a été appliqué, on continue
                            sestApplique, cibles = niveau.lancerEffet(effet,origine_x,origine_y,self.nom, case_cible_x, case_cible_y,caraclanceur) 
                    else:
                        sestApplique, cibles = niveau.lancerEffet(effet,origine_x,origine_y,self.nom, case_cible_x, case_cible_y,caraclanceur) 
                    #Apres application d'un effet sur toutes les cibles:
            else:
                if not isPrevisu:
                    print(explication)
        else:
            if not isPrevisu:
                print("Cible hors de porte")
        niveau.depileEffets()
        niveau.afficherSorts() # réaffiche les sorts pour marquer les sorts qui ne sont plus utilisables
        if isPrevisu:
            toReturn = deepcopy(niveau.joueurs)
            save.restore(niveau)
            print("Restored !")
            return toReturn
