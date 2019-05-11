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

    def lance(self, origine_x,origine_y,niveau, case_cible_x, case_cible_y, caraclanceur=None):
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
        case_cible_x = int(case_cible_x)
        case_cible_y = int(case_cible_y)
        caraclanceur = caraclanceur if caraclanceur != None else niveau.getJoueurSur(origine_x,origine_y)
        #Get toutes les cases dans la zone d'effet
        joueurCible=niveau.getJoueurSur(case_cible_x,case_cible_y)
        #Test si la case est bien dans la portée du sort
        if self.APorte(origine_x, origine_y,case_cible_x,case_cible_y, caraclanceur.PO):
            print(caraclanceur.classe+" lance :"+self.nom)
            #Test si le sort est lançable (cout PA suffisant, délai et nombre d'utilisations par tour et par cible)
            res,explication,coutPA = self.estLancable(niveau, caraclanceur, joueurCible)
            if res == True:
                #Lancer du sort
                caraclanceur.PA -= coutPA
                self.marquerLancer(joueurCible)
                print(caraclanceur.classe+": -"+str(coutPA)+" PA (reste "+str(caraclanceur.PA)+"PA)")
                sestApplique = True
                # Application des effets
                for effet in self.effets:
                    # Test si les effets sont dépendants les uns à la suite des autres
                    if self.chaine == True:
                        if sestApplique == True: # Si l'effet a été appliqué, on continue
                            sestApplique = False
                        else:                    # Sinon la chaîne d'effet est interrompue net.
                            return None     
                    sestApplique, cibles = niveau.lancerEffet(effet,origine_x,origine_y,self.nom, case_cible_x, case_cible_y,caraclanceur)          
                    #Apres application d'un effet sur toutes les cibles:
            else:
                print(explication)
        else:
            print("Cible hors de porte")
        niveau.depileEffets()
        niveau.afficherSorts() # réaffiche les sorts pour marquer les sorts qui ne sont plus utilisables
