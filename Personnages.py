# -*- coding: utf-8 -*
import Sort as Sort
import Effets as Effets
import Zones as Zones
import Etats as Etats
import constantes
import Overlays
import pygame
from pygame.locals import *
import json
class Personnage(object):
    """@summary: Classe décrivant un personnage joueur de dofus."""
    def __init__(self, classe, lvl,team,caracsPrimaires, caracsSecondaires,dommages, resistances,icone=""):
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
        self.PA = int(caracsPrimaires.get("PA",0))
        self.PM = int(caracsPrimaires.get("PM",0))
        self.PO = int(caracsPrimaires.get("PO",0))
        self.vie = int(caracsPrimaires.get("Vitalite",1))
        self.agi = int(caracsPrimaires.get("Agilite",0))
        self.cha = int(caracsPrimaires.get("Chance",0))
        self.fo = int(caracsPrimaires.get("Force",0))
        self.int = int(caracsPrimaires.get("Intelligence",0))
        self.pui = int(caracsPrimaires.get("Puissance",0))
        self.cc = int(caracsPrimaires.get("Coups critiques",0)) #TODO
        self.sagesse = int(caracsPrimaires.get("Sagesse",0))    # Aucune utilité dans le simulateur de combat
        self.caracsPrimaires = caracsPrimaires

        self.retPA = int(caracsSecondaires.get("Retrait PA",0))
        self.esqPA = int(caracsSecondaires.get("Esquive PA",0))
        self.retPM = int(caracsSecondaires.get("Retrait PM",0))
        self.esqPM = int(caracsSecondaires.get("Esquive PM",0))
        self.soins = int(caracsSecondaires.get("Soins",0))      #TODO
        self.tacle = int(caracsSecondaires.get("Tacle",0))      #TODO
        self.fuite = int(caracsSecondaires.get("Fuite",0))      #TODO
        self.ini = int(caracsSecondaires.get("Initiative",0))    
        self.invocationLimite = int(caracsSecondaires.get("Invocation",1))    
        self.prospection = int(caracsSecondaires.get("Prospection",0))  # Aucune utilité dans le simulateur de combat
        self.caracsSecondaires = caracsSecondaires

        self.do = int(dommages.get("Dommages",0))
        self.doCri = int(dommages.get("Dommages critiques",0))          #TODO
        self.doNeutre = int(dommages.get("Neutre",0))                   
        self.doTerre = int(dommages.get("Terre",0))
        self.doFeu = int(dommages.get("Feu",0))
        self.doEau = int(dommages.get("Eau",0))
        self.doAir= int(dommages.get("Air",0))
        self.doRenvoi= int(dommages.get("Renvoi",0))                    
        self.doMaitriseArme= int(dommages.get("Maitrise d'arme",0))     #TODO
        self.doPieges= int(dommages.get("Pieges",0))                    
        self.doPiegesPui= int(dommages.get("Pieges Puissance",0))       
        self.doPou =  int(dommages.get("Poussee",0))
        self.doSorts =  int(dommages.get("Sorts",0))                    
        self.doArmes =  int(dommages.get("Armes",0))                    
        self.doDist =  int(dommages.get("Distance",0))                  
        self.doMelee =  int(dommages.get("Melee",0))                    
        self.dommages = dommages
        
        self.reNeutre = int(resistances.get("Neutre",0))                
        self.rePerNeutre = int(resistances.get("Neutre%",0))            
        self.reTerre = int(resistances.get("Terre",0))                  
        self.rePerTerre= int(resistances.get("Terre%",0))               
        self.reFeu = int(resistances.get("Feu",0))                      
        self.rePerFeu = int(resistances.get("Feu%",0))                  
        self.reEau = int(resistances.get("Eau",0))                      
        self.rePerEau = int(resistances.get("Eau%",0))                  
        self.reAir = int(resistances.get("Air",0))                      
        self.rePerAir = int(resistances.get("Air%",0))                  
        self.reCc = int(resistances.get("Coups critiques",0))           #TODO
        self.rePou = int(resistances.get("Poussee",0))                  
        self.reDist = int(resistances.get("Distance",0))                
        self.reMelee = int(resistances.get("Melee",0))                  
        self.resistances = resistances

        self._vie = self.vie
        self._PM = int(self.PM)
        self._PA = int(self.PA)

        self.erosion = 10 # Erosion de base
        self.lvl = int(lvl)
        self.classe = classe

        self.sorts = Personnage.ChargerSorts(self.classe,self.lvl) # la liste des sorts du personnage
        
        self.posX = 0                                     # Sa position X sur la carte
        self.posY = 0                                     # Sa position Y sur la carte
        self.etats = []                                   # La liste des états affectant le personange
        self.historiqueDeplacement = []                   # Les déplacements effectués par le personnage dans ses 2 derniers tours
        self.posDebTour = None
        self.posDebCombat = None
        self.invocateur = None
        self.invocations = []
        self.overlayTexte = ""
        self.team = int(team)
        
        if not(icone.startswith("images/")):
            self.icone = ("images/"+icone)
        else:
            self.icone = (icone)
        self.icone=constantes.normaliser(self.icone)
        # Overlay affichange le nom de classe et sa vie restante
        self.overlay = Overlays.Overlay(self, Overlays.ColoredText("classe",(210,105,30)), Overlays.ColoredText("overlayTexte",(224,238,238)),(56,56,56))
    def setOverlayText(self):
        self.overlayTexte = str(self.vie) +" PV"
        boubou = self.getBoucliers()
        if boubou > 0:
            self.overlayTexte += " "+str(boubou)+" PB"

    def aEtatsRequis(self,etatsRequis):
        """@summary: Indique si le personnage possède les états donnés en paramètres.
        @etatsRequis: la liste des états à tester. si un ! se situe au début de la chaîne, il faut que l'état soit absent.
        @type: tableau de strings (noms d'états préfixé éventuellement par "!")


        @return: booléen valant True si tous les états requis sont sur le personnage, False sinon."""
        for checkEtat in etatsRequis:
            if checkEtat.strip() != "":
                #calcul du nom de l'état requis
                if checkEtat.startswith("!"):
                    etatRequis = checkEtat[1:]
                else:
                    etatRequis = checkEtat
                #Est-ce que le personnage possede l'état requis
                aEtat = self.aEtat(etatRequis)
                #Si test l'absence qu'on l'a ou si on test la présence et qu'on ne l'a pas
                if (checkEtat.startswith("!") and aEtat) or (not checkEtat.startswith("!") and not aEtat):
                    #print "DEBUG : la cibleDirect n'a pas ou a l'etat requis :"+str(checkEtat)
                    return False
        return True
        
    @staticmethod
    def getSortRightLvl(lvl,tab_sorts):
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
    def ChargerSorts(classe,lvl):
        """@summary: Méthode statique qui initialise les sorts du personnage selon sa classe.
        @classe: le nom de classe dont on souhaite récupérer les sorts
        @type: string

        @return: tableau de Sort"""
        sorts = []
        if(classe=="Stratege Iop"):
            sorts.append(Sort.Sort("Strategie_iop",0,0,0,0,[Effets.EffetEtat(Etats.EtatRedistribuerPer("Stratégie Iop",0,-1, 50,"Ennemis|Allies",2))],[],0,99,99,0,0,"cercle",False))
            return sorts
        elif(classe=="Cadran de Xelor"):
            sorts.append(Sort.Sort("Synchronisation",0,0,0,0,[Effets.EffetDegats(100,130,"feu",zone=Zones.TypeZoneCercleSansCentre(4), cibles_possibles="Ennemis|Lanceur",etat_requis_cibles="Telefrag"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Synchronisation",0,2,"_PA",2),zone=Zones.TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Lanceur",etat_requis_cibles="Telefrag")],[],0,99,99,0,0,"cercle",False))
            return sorts
        elif(classe=="Balise de Rappel"):
            sorts.append(Sort.Sort("Rappel",0,0,0,0,[Effets.EffetEchangePlace(zone=Zones.TypeZoneCercle(99),cibles_possibles="Cra"), Effets.EffetTue(zone=Zones.TypeZoneCercle(99),cibles_possibles="Lanceur")],[],0,99,99,0,0,"cercle",False))
        elif classe == "Poutch":
            return sorts
        elif(classe=="Xelor"):
            retourParadoxe = Sort.Sort("Retour Paradoxe",0,0,0,0,[Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercle(99),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis_cibles="ParadoxeTemporel",consomme_etat=True)],[],0,99,99,0,0,"cercle",False)
            activationInstabiliteTemporelle = Sort.Sort("Activation Instabilité Temporelle",0,0,0,3,[Effets.EffetTeleportePosPrec(1)],[],0, 99,99,0,0,"cercle",False)
            activationParadoxeTemporel = Sort.Sort("Paradoxe Temporel", 0,0,0,0,[Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercle(4),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur|Xélor|Synchro"),Effets.EffetEtat(Etats.Etat("ParadoxeTemporel",0,2),zone=Zones.TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur|Xelor|Synchro"), Effets.EffetEtatSelf(Etats.EtatActiveSort("RetourParadoxe",1,1,retourParadoxe),cibles_possibles="Lanceur")],[],0,99,99,0,0,"cercle",False)
            activationDesynchro = [Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3))]
            activationRune = [Effets.EffetTp(generer_TF=True, faire_au_vide=True)]
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Ralentissement",1,2,1,4,[Effets.EffetDegats(4,5,"Eau"), Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis"),Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag")],[Effets.EffetDegats(7,8,"Eau"), Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis"),Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag")],5,4,2,0,1,"cercle",True,description="""Occasionne des dommages Eau et retire 1 PA à la cible.
            Retire 1 PA supplémentaire aux ennemis dans l'état Téléfrag.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),
                Sort.Sort("Ralentissement",25,2,1,5,[Effets.EffetDegats(6,7,"Eau"), Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis"),Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag")],[Effets.EffetDegats(9,10,"Eau"), Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis"),Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag")],5,4,2,0,1,"cercle",True,description="""Occasionne des dommages Eau et retire 1 PA à la cible.
            Retire 1 PA supplémentaire aux ennemis dans l'état Téléfrag.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),
                Sort.Sort("Ralentissement",52,2,1,6,[Effets.EffetDegats(8,9,"Eau"), Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis"),Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag")],[Effets.EffetDegats(11,12,"Eau"), Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis"),Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag")],5,4,2,0,1,"cercle",True,description="""Occasionne des dommages Eau et retire 1 PA à la cible.
            Retire 1 PA supplémentaire aux ennemis dans l'état Téléfrag.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Souvenir",105,4,1,6,[Effets.EffetDegats(26,30,"Terre"),Effets.EffetTeleportePosPrec(1)],[Effets.EffetDegats(30,34,"Terre"),Effets.EffetTeleportePosPrec(1)],15,3,2,0,1,"ligne",True,description="""Occasionne des dommages Terre et téléporte la cible à sa position précédente.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Aiguille",1,3,1,4,[Effets.EffetDegats(14,18,"Feu"),Effets.EffetRetPA(1),Effets.EffetRetPA(2,etat_requis_cibles="Telefrag",consomme_etat=True)],[Effets.EffetDegats(20,20,"Feu"),Effets.EffetRetPA(1),Effets.EffetRetPA(2,etat_requis_cibles="Telefrag",consomme_etat=True)],15,3,2,0,1,"cercle",True,description="""Occasionne des dommages Feu et retire 1 PA à la cible.
            Retire des PA supplémentaires aux ennemis dans l'état Téléfrag.
            Le retrait de PA ne peut pas être désenvoûté.
            Retire l'état Téléfrag.""", chaine=True),
                Sort.Sort("Aiguille",30,3,1,6,[Effets.EffetDegats(18,22,"Feu"),Effets.EffetRetPA(1),Effets.EffetRetPA(2,etat_requis_cibles="Telefrag",consomme_etat=True)],[Effets.EffetDegats(24,24,"Feu"),Effets.EffetRetPA(1),Effets.EffetRetPA(2,etat_requis_cibles="Telefrag",consomme_etat=True)],15,3,2,0,1,"cercle",True,description="""Occasionne des dommages Feu et retire 1 PA à la cible.
            Retire des PA supplémentaires aux ennemis dans l'état Téléfrag.
            Le retrait de PA ne peut pas être désenvoûté.
            Retire l'état Téléfrag.""", chaine=True),
                Sort.Sort("Aiguille",60,3,1,8,[Effets.EffetDegats(22,26,"Feu"),Effets.EffetRetPA(1),Effets.EffetRetPA(2,etat_requis_cibles="Telefrag",consomme_etat=True)],[Effets.EffetDegats(28,28,"Feu"),Effets.EffetRetPA(1),Effets.EffetRetPA(2,etat_requis_cibles="Telefrag",consomme_etat=True)],15,3,2,0,1,"cercle",True,description="""Occasionne des dommages Feu et retire 1 PA à la cible.
            Retire des PA supplémentaires aux ennemis dans l'état Téléfrag.
            Le retrait de PA ne peut pas être désenvoûté.
            Retire l'état Téléfrag.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Rouage",110,3,1,7,[Effets.EffetDegats(12,14,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Rouage",0,1,"_PA",1))],[Effets.EffetDegats(15,17,"Eau"), Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Rouage",0,1,"_PA",1))],5,2,99,0,1,"cercle",True,description="""Occasionne des dommages Eau.
            Le lanceur gagne 1 PA au tour suivant.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Téléportation",1,2,1,3,[Effets.EffetTpSym()],[],0,1,1,5,0,"cercle",False,description="""Téléporte le lanceur symétriquement par rapport à la cible.
            Le lanceur gagne 2 PA pour 1 tour à chaque fois qu’il génère un Téléfrag.
            Le temps de relance est supprimé quand un Téléfrag est généré ou consommé.
            Un Téléfrag est généré lorsqu'une entité prend la place d'une autre.""", chaine=True),
                Sort.Sort("Téléportation",20,2,1,4,[Effets.EffetTpSym()],[],0,1,1,4,0,"cercle",False,description="""Téléporte le lanceur symétriquement par rapport à la cible.
            Le lanceur gagne 2 PA pour 1 tour à chaque fois qu’il génère un Téléfrag.
            Le temps de relance est supprimé quand un Téléfrag est généré ou consommé.
            Un Téléfrag est généré lorsqu'une entité prend la place d'une autre.""", chaine=True),
                Sort.Sort("Téléportation",40,2,1,5,[Effets.EffetTpSym()],[],0,1,1,3,0,"cercle",False,description="""Téléporte le lanceur symétriquement par rapport à la cible.
            Le lanceur gagne 2 PA pour 1 tour à chaque fois qu’il génère un Téléfrag.
            Le temps de relance est supprimé quand un Téléfrag est généré ou consommé.
            Un Téléfrag est généré lorsqu'une entité prend la place d'une autre.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Retour Spontané",101,1,7,7,[Effets.EffetTeleportePosPrec(1)],[],0,3,99,0,1,"cercle",False,description="""La cible revient à sa position précédente.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flétrissement",3,3,1,4,[Effets.EffetDegats(16,19,"Air"),Effets.EffetDegats(8,8,"air",etat_requis_cibles="Telefrag")],[Effets.EffetDegats(21,24,"Air"),Effets.EffetDegats(8,8,"air",etat_requis_cibles="Telefrag")],15,3,2,0,1,"ligne",True,description="""Occasionne des dommages Air en ligne.
            Occasionne des dommages supplémentaires aux ennemis dans l'état Téléfrag.""", chaine=True),
                Sort.Sort("Flétrissement",35,3,1,5,[Effets.EffetDegats(21,24,"Air"),Effets.EffetDegats(9,9,"air",etat_requis_cibles="Telefrag")],[Effets.EffetDegats(26,29,"Air"),Effets.EffetDegats(9,9,"air",etat_requis_cibles="Telefrag")],15,3,2,0,1,"ligne",True,description="""Occasionne des dommages Air en ligne.
            Occasionne des dommages supplémentaires aux ennemis dans l'état Téléfrag.""", chaine=True),
                Sort.Sort("Flétrissement",67,3,1,6,[Effets.EffetDegats(26,29,"Air"),Effets.EffetDegats(10,10,"air",etat_requis_cibles="Telefrag")],[Effets.EffetDegats(31,34,"Air"),Effets.EffetDegats(10,10,"air",etat_requis_cibles="Telefrag")],15,3,2,0,1,"ligne",True,description="""Occasionne des dommages Air en ligne.
            Occasionne des dommages supplémentaires aux ennemis dans l'état Téléfrag.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Dessèchement",115,4,1,6,[Effets.EffetDegats(38,42,"Air"),Effets.EffetEtat(Etats.EtatEffetDebutTour("Dessèchement", 1,1,Effets.EffetDegats(44,48,"air",cibles_possbiles="Ennemis",zone=Zones.TypeZoneCercleSansCentre(2)),"Dessechement","lanceur"))],[Effets.EffetDegats(44,48,"Air"),Effets.EffetEtat(Etats.EtatEffetDebutTour("Dessèchement", 1,1,Effets.EffetDegats(44,48,"air",cibles_possbiles="Ennemis",zone=Zones.TypeZoneCercleSansCentre(2)),"Dessechement","lanceur"))],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Air.
            Occasionne des dommages Air supplémentaires aux ennemis autour de la cible au début du prochain tour du lanceur.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Rembobinage",6,2,2,2,[Effets.EffetEtat(Etats.EtatRetourCaseDepart("Bobine",0,1),cibles_possibles="Allies|Lanceur")],[],0,1,1,3,0,"ligne",True,description="""À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour.""", chaine=True),
                Sort.Sort("Rembobinage",42,2,4,4,[Effets.EffetEtat(Etats.EtatRetourCaseDepart("Bobine",0,1),cibles_possibles="Allies|Lanceur")],[],0,1,1,3,0,"ligne",True,description="""À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour.""", chaine=True),
                Sort.Sort("Rembobinage",74,2,6,6,[Effets.EffetEtat(Etats.EtatRetourCaseDepart("Bobine",0,1),cibles_possibles="Allies|Lanceur")],[],0,1,1,3,0,"ligne",True,description="""À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Renvoi",120,3,1,6,[Effets.EffetTeleporteDebutTour()],[],0,1,1,2,0,"ligne",True,description="""Téléporte la cible ennemie à sa cellule de début de tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Frappe de Xélor",9,3,1,3,[Effets.EffetTpSymSelf(),Effets.EffetDegats(15,19,"Terre",cibles_possibles="Ennemis")],[Effets.EffetTpSymSelf(),Effets.EffetDegats(21,25,"Terre",cibles_possibles="Ennemis")],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Terre aux ennemis.
            Téléporte la cible symétriquement par rapport au lanceur du sort.""", chaine=False),

                Sort.Sort("Frappe de Xélor",47,3,1,3,[Effets.EffetTpSymSelf(),Effets.EffetDegats(19,23,"Terre",cibles_possibles="Ennemis")],[Effets.EffetTpSymSelf(),Effets.EffetDegats(25,29,"Terre",cibles_possibles="Ennemis")],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Terre aux ennemis.
            Téléporte la cible symétriquement par rapport au lanceur du sort.""", chaine=False),

                Sort.Sort("Frappe de Xélor",87,3,1,3,[Effets.EffetTpSymSelf(),Effets.EffetDegats(23,27,"Terre",cibles_possibles="Ennemis")],[Effets.EffetTpSymSelf(),Effets.EffetDegats(29,33,"Terre",cibles_possibles="Ennemis")],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Terre aux ennemis.
            Téléporte la cible symétriquement par rapport au lanceur du sort.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Engrenage",125,3,1,5,[Effets.EffetTpSymCentre(zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True),Effets.EffetDegats(31,35,"Terre",cibles_possibles="Ennemis",zone=Zones.TypeZoneLignePerpendiculaire(1))],[Effets.EffetTpSymCentre(zone=Zones.TypeZoneLignePerpendiculaire(1)),Effets.EffetDegats(34,38,"Terre",cibles_possibles="Ennemis",zone=Zones.TypeZoneLignePerpendiculaire(1))],25,2,99,0,0,"ligne",True,description="""Occasionne des dommages Terre et téléporte les cibles symétriquement par rapport au centre de la zone d'effet.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Complice",13,2,1,3,[Effets.EffetInvoque("Complice",False,cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles="Cadran de Xélor|Complice",zone=Zones.TypeZoneCercleSansCentre(99))],[],0,1,99,0,0,"cercle",True,description="""Invoque un Complice statique qui ne possède aucun sort.
            Il est tué si un autre Complice est invoqué.""", chaine=True),

                Sort.Sort("Complice",54,2,1,4,[Effets.EffetInvoque("Complice",False,cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles="Cadran de Xélor|Complice",zone=Zones.TypeZoneCercleSansCentre(99))],[],0,1,99,0,0,"cercle",True,description="""Invoque un Complice statique qui ne possède aucun sort.
            Il est tué si un autre Complice est invoqué.""", chaine=True),

                Sort.Sort("Complice",94,2,1,5,[Effets.EffetInvoque("Complice",False,cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles="Cadran de Xélor|Complice",zone=Zones.TypeZoneCercleSansCentre(99))],[],0,1,99,0,0,"cercle",True,description="""Invoque un Complice statique qui ne possède aucun sort.
            Il est tué si un autre Complice est invoqué.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Cadran de Xélor",130,3,1,5,[Effets.EffetInvoque("Cadran de Xélor",False,cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles="Cadran de Xélor|Complice",zone=Zones.TypeZoneCercleSansCentre(99))],[],0,1,1,3,0,"cercle",True,description="""Invoque un Cadran qui occasionne des dommages Feu en zone et retire des PA aux ennemis dans l'état Téléfrag.
            Donne des PA aux alliés autour de lui et dans l'état Téléfrag.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Gelure",17,2,2,4,[Effets.EffetDegats(5,7,"Air",cibles_possibles="Ennemis|Lanceur"),Effets.EffetTeleportePosPrec(1)],[Effets.EffetDegats(11,11,"Air",cibles_possibles="Ennemis|Lanceur"),Effets.EffetTeleportePosPrec(1)],5,3,2,0,1,"cercle",True,description="""Occasionne des dommages Air aux ennemis.
            Téléporte la cible à sa position précédente.""", chaine=False),

                Sort.Sort("Gelure",58,2,2,4,[Effets.EffetDegats(8,10,"Air",cibles_possibles="Ennemis|Lanceur"),Effets.EffetTeleportePosPrec(1)],[Effets.EffetDegats(14,14,"Air",cibles_possibles="Ennemis|Lanceur"),Effets.EffetTeleportePosPrec(1)],5,3,2,0,1,"cercle",True,description="""Occasionne des dommages Air aux ennemis.
            Téléporte la cible à sa position précédente.""", chaine=False),

                Sort.Sort("Gelure",102,2,2,5,[Effets.EffetDegats(11,13,"Air",cibles_possibles="Ennemis|Lanceur"),Effets.EffetTeleportePosPrec(1)],[Effets.EffetDegats(17,17,"Air",cibles_possibles="Ennemis|Lanceur"),Effets.EffetTeleportePosPrec(1)],5,3,2,0,1,"cercle",True,description="""Occasionne des dommages Air aux ennemis.
            Téléporte la cible à sa position précédente.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Perturbation",135,2,1,4,[Effets.EffetDegats(9,11,"Feu",cibles_possibles="Ennemis|Lanceur"),Effets.EffetTpSymSelf()],[Effets.EffetDegats(11,13,"Feu",cibles_possibles="Ennemis|Lanceur"),Effets.EffetTpSymSelf()],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Feu et téléporte la cible symétriquement par rapport au lanceur.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Sablier de Xélor",22,2,1,6,[Effets.EffetDegats(9,11,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(9,11,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],[Effets.EffetDegats(13,15,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(13,15,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],5,3,1,0,1,"ligne",False,description="""Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue.
            Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

                Sort.Sort("Sablier de Xélor",65,2,1,6,[Effets.EffetDegats(12,14,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(12,14,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],[Effets.EffetDegats(16,18,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(16,15,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],5,3,1,0,1,"ligne",False,description="""Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue.
            Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

                Sort.Sort("Sablier de Xélor",108,2,1,7,[Effets.EffetDegats(15,17,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(15,17,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],[Effets.EffetDegats(19,21,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(19,21,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],5,3,1,0,1,"ligne",False,description="""Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue.
            Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True)
            ]))

            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Distorsion Temporelle",140,4,0,0,[Effets.EffetDegats(34,38,"Air",zone=Zones.TypeZoneCarre(1),cibles_possibles="Ennemis"),Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneCarre(1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur")],[Effets.EffetDegats(38,42,"Air",cibles_possibles="Ennemis", zone=Zones.TypeZoneCarre(1)),Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneCarre(1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur")],15,2,99,0,0,"cercle",False,description="""Occasionne des dommages Air aux ennemis.
            Téléporte les cibles à leur position précédente.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Vol du Temps",27,4,1,5,[Effets.EffetDegats(20,24,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",0,1,"_PA",1))],[Effets.EffetDegats(25,29,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",0,1,"_PA",1))],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Eau à la cible.
            Le lanceur gagne 1 PA au début de son prochain tour.""", chaine=True),

                Sort.Sort("Vol du Temps",72,4,1,5,[Effets.EffetDegats(25,29,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",0,1,"_PA",1))],[Effets.EffetDegats(30,34,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",0,1,"_PA",1))],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Eau à la cible.
            Le lanceur gagne 1 PA au début de son prochain tour.""", chaine=True),

                Sort.Sort("Vol du Temps",118,4,1,5,[Effets.EffetDegats(30,34,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",0,1,"_PA",1))],[Effets.EffetDegats(35,39,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",0,1,"_PA",1))],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Eau à la cible.
            Le lanceur gagne 1 PA au début de son prochain tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Pétrification",145,5,1,7,[Effets.EffetDegats(34,38,"Eau"),Effets.EffetEtatSelf(Etats.EtatCoutPA("Pétrification",0,2,"Pétrification",-1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag"), Effets.EffetRetPA(2)],[Effets.EffetDegats(38,42,"Eau"), Effets.EffetEtatSelf(Etats.EtatCoutPA("Pétrification",0,2,"Pétrification",-1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag"), Effets.EffetRetPA(2)],25,3,2,0,1,"ligne",True,description="""Occasionne des dommages Eau et retire des PA.
            Si la cible est dans l'état Téléfrag, le coût en PA du sort est réduit pendant 2 tours.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flou",32,2,1,1,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",0,1,"PA",-2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",0,1,"_PA",2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)],[],0,1,1,5,0,"cercle",False,description="""Retire des PA en zone le tour en cours.
            Augmente les PA en zone le tour suivant.""", chaine=True),

                Sort.Sort("Flou",81,2,1,2,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",0,1,"PA",-2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",0,1,"_PA",2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)],[],0,1,1,4,0,"cercle",True,description="""Retire des PA en zone le tour en cours.
            Augmente les PA en zone le tour suivant.""", chaine=True),

                Sort.Sort("Flou",124,2,1,3,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",0,1,"PA",-2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",0,1,"_PA",2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)],[],0,1,1,3,0,"cercle",True,description="""Retire des PA en zone le tour en cours.
            Augmente les PA en zone le tour suivant.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Conservation",150,2,5,5,[Effets.EffetEtat(Etats.EtatModDegPer("Conservation",0,1,130),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur"),Effets.EffetEtat(Etats.EtatModDegPer("Conservation",1,1,70),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur")],[],0,1,1,2,0,"cercle",True,description="""Augmente les dommages subis par les alliés en zone de 30% pour le tour en cours.
            Au tour suivant, les cibles réduisent les dommages subis de 30%.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Poussière Temporelle",38,4,4,4,[Effets.EffetDegats(22,25,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(22,25,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],[Effets.EffetDegats(26,29,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(26,29,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],25,2,99,0,1,"cercle",True,description="""Occasionne des dommages Feu.
            Les entités dans l'état Téléfrag dans la zone d'effet subissent également des dommages Feu et sont téléportées symétriquement par rapport à la cellule ciblée.""", chaine=True),

                Sort.Sort("Poussière Temporelle",90,4,5,5,[Effets.EffetDegats(28,31,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(28,31,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],[Effets.EffetDegats(32,35,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(32,35,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],25,2,99,0,1,"cercle",True,description="""Occasionne des dommages Feu.
            Les entités dans l'état Téléfrag dans la zone d'effet subissent également des dommages Feu et sont téléportées symétriquement par rapport à la cellule ciblée.""", chaine=True),

                Sort.Sort("Poussière Temporelle",132,4,6,6,[Effets.EffetDegats(34,37,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(34,37,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],[Effets.EffetDegats(38,41,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(38,41,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],25,2,99,0,1,"cercle",True,description="""Occasionne des dommages Feu.
            Les entités dans l'état Téléfrag dans la zone d'effet subissent également des dommages Feu et sont téléportées symétriquement par rapport à la cellule ciblée.""", chaine=True)
            ]))

            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Suspension Temporelle",155,3,1,6,[Effets.EffetDureeEtats(1,etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(25,29,"Feu")],[Effets.EffetDureeEtats(1,etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(29,33,"Feu")],15,3,2,0,1,"ligne",True,description="""Occasionne des dommages Feu sur les ennemis.
            Réduit la durée des effets sur les cibles ennemies dans l'état Téléfrag et retire l'état.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Raulebaque",44,2,0,0,[Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneCercle(99))],[],0,1,1,4,0,"cercle",False,description="""Replace tous les personnages à leurs positions précédentes.""", chaine=True),

                Sort.Sort("Raulebaque",97,2,0,0,[Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneCercle(99))],[],0,1,1,3,0,"cercle",False,description="""Replace tous les personnages à leurs positions précédentes.""", chaine=True),

                Sort.Sort("Raulebaque",137,2,0,0,[Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneCercle(99))],[],0,1,1,2,0,"cercle",False,description="""Replace tous les personnages à leurs positions précédentes.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Instabilité Temporelle",160,3,7,7,[Effets.EffetGlyphe(activationInstabiliteTemporelle,2,"Instabilité Temporelle",(255,255,0),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)],[],0,1,1,3,1,"cercle",False,description="""Pose un glyphe qui renvoie les entités à leur position précédente.
            Les entités dans le glyphe sont dans l'état Intaclable.
            Les effets du glyphe sont également exécutés lorsque le lanceur génère un Téléfrag.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Démotivation",50,3,1,3,[Effets.EffetDureeEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(17,20,"Terre",cibles_possibles="Ennemis")],[Effets.EffetDureeEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(22,25,"Terre",cibles_possibles="Ennemis")],25,3,2,0,0,"diagonale",True,description="""Occasionne des dommages Terre aux ennemis en diagonale.
            Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état.""", chaine=True),

                Sort.Sort("Démotivation",103,3,1,4,[Effets.EffetDureeEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(20,23,"Terre",cibles_possibles="Ennemis")],[Effets.EffetDureeEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(25,28,"Terre",cibles_possibles="Ennemis")],25,3,2,0,0,"diagonale",True,description="""Occasionne des dommages Terre aux ennemis en diagonale.
            Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état.""", chaine=True),

                Sort.Sort("Démotivation",143,3,1,5,[Effets.EffetDureeEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(23,26,"Terre",cibles_possibles="Ennemis")],[Effets.EffetDureeEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(28,31,"Terre",cibles_possibles="Ennemis")],25,3,2,0,0,"diagonale",True,description="""Occasionne des dommages Terre aux ennemis en diagonale.
            Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Pendule",165,4,1,5,[Effets.EffetTpSym(),Effets.EffetDegats(38,42,"Air",zone=Zones.TypeZoneCercle(2),cibles_possibles="Ennemis"),Effets.EffetTeleportePosPrecLanceur(1,cibles_possibles="Lanceur")],[Effets.EffetTpSym(),Effets.EffetDegats(46,50,"Air",zone=Zones.TypeZoneCercle(2),cibles_possibles="Ennemis"),Effets.EffetTeleportePosPrecLanceur(1,cibles_possibles="Lanceur")],5,2,1,0,0,"cercle",True,description="""Le lanceur se téléporte symétriquement par rapport à la cible et occasionne des dommages Air en zone sur sa cellule de destination.
            Il revient ensuite à sa position précédente.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Paradoxe Temporel",56,3,0,0,[Effets.EffetEntiteLanceSort("Complice|Cadran de Xélor",activationParadoxeTemporel)],[],0,1,1,4,0,"cercle",False,description="""Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran).
            Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles.
            Fixe le temps de relance de Cadran de Xélor et de Complice à 1.""", chaine=True),

                Sort.Sort("Paradoxe Temporel",112,3,0,0,[Effets.EffetEntiteLanceSort("Complice|Cadran de Xélor",activationParadoxeTemporel)],[],0,1,1,3,0,"cercle",False,description="""Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran).
            Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles.
            Fixe le temps de relance de Cadran de Xélor et de Complice à 1.""", chaine=True),

                Sort.Sort("Paradoxe Temporel",147,3,0,0,[Effets.EffetEntiteLanceSort("Complice|Cadran de Xélor",activationParadoxeTemporel)],[],0,1,1,2,0,"cercle",False,description="""Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran).
            Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles.
            Fixe le temps de relance de Cadran de Xélor et de Complice à 1.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Faille Temporelle",170,3,0,0,[Effets.EffetEchangePlace(zone=Zones.TypeZoneCercle(99),cibles_possibles="Cadran de Xélor|Complice",generer_TF=True),Effets.EffetEtat(Etats.EtatEffetFinTour("Retour faille temporelle", 1,1,Effets.EffetTeleportePosPrec(1),"Fin faille Temporelle","cible")), Effets.EffetEtat(Etats.Etat("Faille_temporelle",0,1),zone=Zones.TypeZoneCercle(99),cibles_possibles="Xelor")],[],0,1,1,2,0,"cercle",False,description="""Le lanceur échange sa position avec celle du Complice (ou du Cadran).
            À la fin du tour, le Complice (ou le Cadran) revient à sa position précédente.
            La Synchro ne peut pas être déclenchée pendant la durée de Faille Temporelle.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Synchro",62,2,1,2,[Effets.EffetInvoque("Synchro",False,cibles_possibles="",faire_au_vide=True),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Synchro",0,-1,"_PA",-1))],[],0,1,1,3,0,"cercle",False,description="""Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour.
            La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag.
            Elle n'est pas affectée par les effets de Rembobinage.
            À partir du tour suivant son lancer, son invocateur perd 1 PA.""", chaine=True),

                Sort.Sort("Synchro",116,2,1,3,[Effets.EffetInvoque("Synchro",False,cibles_possibles="",faire_au_vide=True),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Synchro",0,-1,"_PA",-1))],[],0,1,1,3,0,"cercle",False,description="""Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour.
            La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag.
            Elle n'est pas affectée par les effets de Rembobinage.
            À partir du tour suivant son lancer, son invocateur perd 1 PA.""", chaine=True),

                Sort.Sort("Synchro",153,2,1,4,[Effets.EffetInvoque("Synchro",False,cibles_possibles="",faire_au_vide=True),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Synchro",0,-1,"_PA",-1))],[],0,1,1,3,0,"cercle",False,description="""Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour.
            La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag.
            Elle n'est pas affectée par les effets de Rembobinage.
            À partir du tour suivant son lancer, son invocateur perd 1 PA.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Désynchronisation",175,2,1,6,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationDesynchro,"Désynchronisation",(255,0,255),faire_au_vide=True)],[],0,2,99,0,1,"cercle",False,description="""Pose un piège qui téléporte symétriquement les entités proches.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Contre",69,2,2,2,[Effets.EffetEtat(Etats.EtatContre("Contre",0,2, 30,1),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur", faire_au_vide=True)],[],0,1,1,5,0,"cercle",True,description="""Renvoie une partie des dommages subis en mêlée à l'attaquant.""", chaine=True),
                Sort.Sort("Contre",122,2,4,4,[Effets.EffetEtat(Etats.EtatContre("Contre",0,2, 40,1),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur", faire_au_vide=True)],[],0,1,1,5,0,"cercle",True,description="""Renvoie une partie des dommages subis en mêlée à l'attaquant.""", chaine=True),
                Sort.Sort("Contre",162,2,6,6,[Effets.EffetEtat(Etats.EtatContre("Contre",0,2, 50,1),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur", faire_au_vide=True)],[],0,1,1,5,0,"cercle",True,description="""Renvoie une partie des dommages subis en mêlée à l'attaquant.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Bouclier Temporel",180,3,3,3,[Effets.EffetEtat(Etats.EtatEffetSiSubit("Bouclier temporel",0,1, Effets.EffetTeleportePosPrec(1),"Bouclier Temporel","lanceur",""))],[],0,1,1,3,0,"cercle",True,description="""Si la cible subit des dommages, son attaquant et elle reviennent à leur position précédente.""", chaine=True)
            ]))

            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Fuite",77,1,0,1,[Effets.EffetEtat(Etats.EtatEffetDebutTour("Fuite", 1,1,Effets.EffetTeleportePosPrec(1),"Fuite","cible"))],[],0,2,1,0,0,"cercle",False,description="""Téléporte la cible sur sa position précédente au début du prochain tour du lanceur.""", chaine=True),

                Sort.Sort("Fuite",128,1,0,3,[Effets.EffetEtat(Etats.EtatEffetDebutTour("Fuite", 1,1,Effets.EffetTeleportePosPrec(1),"Fuite","cible"))],[],0,3,1,0,0,"cercle",False,description="""Téléporte la cible sur sa position précédente au début du prochain tour du lanceur.""", chaine=True),

                Sort.Sort("Fuite",172,1,0,5,[Effets.EffetEtat(Etats.EtatEffetDebutTour("Fuite", 1,1,Effets.EffetTeleportePosPrec(1),"Fuite","cible"))],[],0,4,2,0,0,"cercle",False,description="""Téléporte la cible sur sa position précédente au début du prochain tour du lanceur.""", chaine=True)
            ]))

            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Prémonition",185,2,1,5,[Effets.EffetRune(1, activationRune,"Prémonition",(164,78,163),faire_au_vide=True)],[],0,1,1,1,0,"cercle",False,description="""Au prochain tour, le lanceur se téléporte sur la cellule ciblée.""", chaine=True)
            ]))

            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Horloge",84,5,1,4,[Effets.EffetVolDeVie(28,31,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",0,1,"_PA",1)),Effets.EffetRetPA(2,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetVolDeVie(32,35,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",0,1,"_PA",1)),Effets.EffetRetPA(2,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],25,3,2,0,0,"ligne",True,description="""Vole de vie dans l'élément Eau.
            Le lanceur gagne 1 PA au début de son prochain tour.
            Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

                Sort.Sort("Horloge",134,5,1,5,[Effets.EffetVolDeVie(32,35,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",0,1,"_PA",1)),Effets.EffetRetPA(3,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetVolDeVie(36,39,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",0,1,"_PA",1)),Effets.EffetRetPA(3,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],25,3,2,0,0,"ligne",True,description="""Vole de vie dans l'élément Eau.
            Le lanceur gagne 1 PA au début de son prochain tour.
            Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

                Sort.Sort("Horloge",178,5,1,6,[Effets.EffetVolDeVie(36,39,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",0,1,"_PA",1)),Effets.EffetRetPA(4,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetVolDeVie(40,43,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",0,1,"_PA",1)),Effets.EffetRetPA(4,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],25,3,2,0,0,"ligne",True,description="""Vole de vie dans l'élément Eau.
            Le lanceur gagne 1 PA au début de son prochain tour.
            Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Clepsydre",190,4,1,3,[Effets.EffetDegats(30,34,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Clepsydre",0,1,"_PA",2),etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetDegats(36,40,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Clepsydre",0,1,"_PA",2),etat_requis="Telefrag",consomme_etat=True)],15,2,99,0,0,"cercle",True,description="""Occasionne des dommages Eau.
            Si la cible est dans l'état Téléfrag, le lanceur gagne 2 PA au prochain tour.
            Retire l'état Téléfrag.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Rayon Obscur",92,5,1,4,[Effets.EffetDegats(54,62,"Terre",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(27,31,"Terre",etat_requis="!Telefrag")],[Effets.EffetDegats(68,76,"Terre",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(34,38,"Terre",etat_requis="!Telefrag")],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Terre en ligne.
            Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag.
            Retire l'état Téléfrag.""", chaine=True),

                Sort.Sort("Rayon Obscur",141,5,1,5,[Effets.EffetDegats(60,68,"Terre",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(30,34,"Terre",etat_requis="!Telefrag")],[Effets.EffetDegats(74,82,"Terre",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(37,41,"Terre",etat_requis="!Telefrag")],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Terre en ligne.
            Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag.
            Retire l'état Téléfrag.""", chaine=True),

                Sort.Sort("Rayon Obscur",187,5,1,6,[Effets.EffetDegats(66,74,"Terre",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(33,37,"Terre",etat_requis="!Telefrag")],[Effets.EffetDegats(80,88,"Terre",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(40,44,"Terre",etat_requis="!Telefrag")],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Terre en ligne.
            Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag.
            Retire l'état Téléfrag.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Rayon Ténébreux",195,3,1,5,[Effets.EffetDegats(19,23,"Terre"),Effets.EffetDegats(19,23,"terre",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],[Effets.EffetDegats(23,27,"Terre"),Effets.EffetDegats(23,37,"terre",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],5,3,2,0,1,"cercle",True,description="""Occasionne des dommages Terre.
            Si la cible est dans l'état Téléfrag, occasionne des dommages Terre en zone aux ennemis autour d'elle.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Momification",100,2,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Momification",0,1,"PM",2)),Effets.EffetEtat(Etats.EtatTelefrag("Telefrag",0,1,"Momification"),zone=Zones.TypeZoneCercle(99))],[],0,1,1,5,0,"cercle",False,description="""Gagne 2 PM et fixe l'état Téléfrag à tous les alliés et ennemis.""", chaine=True),

                Sort.Sort("Momification",147,2,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Momification",0,1,"PM",2)),Effets.EffetEtat(Etats.EtatTelefrag("Telefrag",0,1,"Momification"),zone=Zones.TypeZoneCercle(99))],[],0,1,1,4,0,"cercle",False,description="""Gagne 2 PM et fixe l'état Téléfrag à tous les alliés et ennemis.""", chaine=True),

                Sort.Sort("Momification",197,2,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Momification",0,1,"PM",2)),Effets.EffetEtat(Etats.EtatTelefrag("Telefrag",0,1,"Momification"),zone=Zones.TypeZoneCercle(99))],[],0,1,1,3,0,"cercle",False,description="""Gagne 2 PM et fixe l'état Téléfrag à tous les alliés et ennemis.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Glas",200,3,0,3,[Effets.EffetDegats(4,4,"Air",zone=Zones.TypeZoneCarre(1)),Effets.EffetDegats(4,4,"Eau",zone=Zones.TypeZoneCarre(1)),Effets.EffetDegats(4,4,"Terre",zone=Zones.TypeZoneCarre(1)),Effets.EffetDegats(4,4,"Feu",zone=Zones.TypeZoneCarre(1)),Effets.EffetRetireEtat("Glas",zone=Zones.TypeZoneCercle(99),cibles_possibles="Lanceur")],[],0,1,1,2,0,"ligne",True,description="""Occasionne des dommages Air, Eau, Terre, Feu.
            Les dommages sont augmentés pour chaque Téléfrag généré depuis son dernier lancer.
            N'occasionne pas de dommages si aucun Téléfrag n'a été généré depuis son dernier lancer.""", chaine=True)
            ]))
        elif(classe=="Iop"):
            activationRassemblement = Sort.Sort("Déclenche Rassemblement",0,0,0,0,[Effets.EffetAttire(2,zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies")],[],0,99,99,0,0,"cercle",False)
            activationFriction = Sort.Sort("Frikt",0,0,0,0,[Effets.EffetAttire(1,"Lanceur","JoueurCaseEffet", zone=Zones.TypeZoneCroix(99), etat_requis_cibles="Frikt")],[],0,99,99,0,0,"cercle",False)
            activationCoupPourCoup = Sort.Sort("Déclenche Coup pour Coup",0,0,0,0,[Effets.EffetPousser(2, zone=Zones.TypeZoneCroix(99), etat_requis_cibles="Coup pour coup")],[],0,99,99,0,0,"cercle",False)
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Pression",1,3,1,3,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Pression",0,2,"erosion",10),cibles_possibles="Ennemis"),Effets.EffetDegats(14,18,"Terre")],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Pression",0,2,"erosion",10),cibles_possibles="Ennemis"),Effets.EffetDegats(19,23,"Terre")],5,99,2,0,0,"cercle",True,description="""Occasionne des dommages Terre et applique un malus d'érosion.""", chaine=True),
                Sort.Sort("Pression",30,3,1,3,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Pression",0,2,"erosion",10),cibles_possibles="Ennemis"),Effets.EffetDegats(19,23,"Terre")],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Pression",0,2,"erosion",10),cibles_possibles="Ennemis"),Effets.EffetDegats(24,28,"Terre")],5,99,2,0,0,"cercle",True,description="""Occasionne des dommages Terre et applique un malus d'érosion.""", chaine=True),
                Sort.Sort("Pression",60,3,1,3,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Pression",0,2,"erosion",10),cibles_possibles="Ennemis"),Effets.EffetDegats(24,28,"Terre")],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Pression",0,2,"erosion",10),cibles_possibles="Ennemis"),Effets.EffetDegats(29,33,"Terre")],5,99,3,0,0,"cercle",True,description="""Occasionne des dommages Terre et applique un malus d'érosion.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Tannée",110,4,1,7,[Effets.EffetDegats(30,34,"Air",zone=Zones.TypeZoneLignePerpendiculaire(1)),Effets.EffetRetPM(3,zone=Zones.TypeZoneLignePerpendiculaire(1))],[Effets.EffetDegats(36,40,"Air",zone=Zones.TypeZoneLignePerpendiculaire(1)),Effets.EffetRetPM(3,zone=Zones.TypeZoneLignePerpendiculaire(1))],5,2,99,0,0,"ligne",True,description="""Occasionne des dommages Air en zone et retire des PM.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Bond",1,5,1,5,[Effets.EffetTp(cibles_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatModDegPer("Bond",0,1,115),zone=Zones.TypeZoneCercle(1),cibles_possibles="Ennemis")],[Effets.EffetTp(cibles_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatModDegPer("Bond",0,1,118),zone=Zones.TypeZoneCercle(1),cibles_possibles="Ennemis")],15,1,1,2,0,"cercle",False,description="""Téléporte sur la case ciblée.
            Augmente les dommages reçus par les ennemis situés sur les cases adjacentes.""", chaine=True),

                Sort.Sort("Bond",20,5,1,5,[Effets.EffetTp(cibles_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatModDegPer("Bond",0,1,115),zone=Zones.TypeZoneCercle(1),cibles_possibles="Ennemis")],[Effets.EffetTp(cibles_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatModDegPer("Bond",0,1,118),zone=Zones.TypeZoneCercle(1),cibles_possibles="Ennemis")],15,1,1,1,0,"cercle",False,description="""Téléporte sur la case ciblée.
            Augmente les dommages reçus par les ennemis situés sur les cases adjacentes.""", chaine=True),

                Sort.Sort("Bond",40,5,1,6,[Effets.EffetTp(cibles_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatModDegPer("Bond",0,1,115),zone=Zones.TypeZoneCercle(1),cibles_possibles="Ennemis")],[Effets.EffetTp(cibles_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatModDegPer("Bond",0,1,118),zone=Zones.TypeZoneCercle(1),cibles_possibles="Ennemis")],15,1,99,0,0,"cercle",False,description="""Téléporte sur la case ciblée.
            Augmente les dommages reçus par les ennemis situés sur les cases adjacentes.""", chaine=True)
            ]))
            
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Détermination",101,2,0,0,[Effets.EffetEtat(Etats.Etat("Indeplacable",0,1)),Effets.EffetEtat(Etats.EtatModDegPer("Determination",0,1,75))],[],0,1,1,2,0,"cercle",False,description="""Fixe l'êtat Indéplaçable et réduit 25% des dommages subis pendant 1 tour.
            Ne peut pas être désenvoûté.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Intimidation",1,2,1,2,[Effets.EffetDegats(7,9,"Neutre"),Effets.EffetPousser(2)],[Effets.EffetDegats(9,11,"Neutre"),Effets.EffetPousser(2)],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Neutre sur les ennemis et repousse la cible.""", chaine=True),

                Sort.Sort("Intimidation",25,2,1,2,[Effets.EffetDegats(9,11,"Neutre"),Effets.EffetPousser(3)],[Effets.EffetDegats(11,13,"Neutre"),Effets.EffetPousser(3)],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Neutre sur les ennemis et repousse la cible.""", chaine=True),

                Sort.Sort("Intimidation",52,2,1,2,[Effets.EffetDegats(11,13,"Neutre"),Effets.EffetPousser(3)],[Effets.EffetDegats(13,15,"Neutre"),Effets.EffetPousser(3)],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Neutre sur les ennemis et repousse la cible.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Conquête",105,3,1,6,[Effets.EffetInvoque("Stratège Iop",True,cible_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatRedistribuerPer("Strategie iop",0,-1, 50,"Ennemis|Allies",2))],[],0,1,1,3,0,"cercle",True,description="""Invoque un épouvantail qui redistribue à proximité (2 cases) 50% des dommages de sort qu'il subit.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Déferlement",3,4,0,5,[Effets.EffetAttire(4,"JoueurCaseEffet","Lanceur",cibles_exclues="Lanceur"),Effets.EffetDegats(24,28,"Eau",cibles_exclues="Lanceur"),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Déferlement",0,1,100))],[Effets.EffetAttire(4,"JoueurCaseEffet","Lanceur",cibles_exclues="Lanceur"),Effets.EffetDegats(32,36,"Eau",cibles_exclues="Lanceur"), Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Déferlement",0,1,100))],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Eau aux ennemis et rapproche le lanceur de la cible.
            Le lanceur gagne des points de bouclier.""", chaine=True),

                Sort.Sort("Déferlement",35,4,0,5,[Effets.EffetAttire(4,"JoueurCaseEffet","Lanceur",cibles_exclues="Lanceur"),Effets.EffetDegats(31,35,"Eau",cibles_exclues="Lanceur"),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Déferlement",0,1,100))],[Effets.EffetAttire(4,"JoueurCaseEffet","Lanceur",cibles_exclues="Lanceur"),Effets.EffetDegats(39,43,"Eau",cibles_exclues="Lanceur"),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Déferlement",0,1,100))],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Eau aux ennemis et rapproche le lanceur de la cible.
            Le lanceur gagne des points de bouclier.""", chaine=True),

                Sort.Sort("Déferlement",67,4,0,5,[Effets.EffetAttire(4,"JoueurCaseEffet","Lanceur",cibles_exclues="Lanceur"),Effets.EffetDegats(38,42,"Eau",cibles_exclues="Lanceur"),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Déferlement",0,1,100))],[Effets.EffetAttire(4,"JoueurCaseEffet","Lanceur",cibles_exclues="Lanceur"),Effets.EffetDegats(46,50,"Eau",cibles_exclues="Lanceur"),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Déferlement",0,1,100))],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Eau aux ennemis et rapproche le lanceur de la cible.
            Le lanceur gagne des points de bouclier.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Menace",115,3,0,3,[Effets.EffetDegats(26,28,"Eau"),Effets.EffetAttire(2),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Menace",0,1,100))],[Effets.EffetDegats(31,33,"Eau"),Effets.EffetAttire(2),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Menace",0,1,100))],5,3,2,0,0,"cercle",True,description="""Occasionne des dommages Eau et attire la cible.
            Le lanceur gagne des points de bouclier.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Epée Divine",6,3,0,0,[Effets.EffetDegats(15,17,"Air",zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Epée Divine",0,4,"do",10),zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")],[Effets.EffetDegats(24,24,"Air",zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Epée Divine",0,4,"do",13),zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")],5,2,99,0,0,"cercle",False,description="""Occasionne des dommages Air et augmente les dommages des alliés ciblés.""", chaine=False),

                Sort.Sort("Epée Divine",42,3,0,0,[Effets.EffetDegats(18,20,"Air",zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Epée Divine",0,4,"do",15),zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")],[Effets.EffetDegats(27,27,"Air",zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Epée Divine",0,4,"do",18),zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")],5,2,99,0,0,"cercle",False,description="""Occasionne des dommages Air et augmente les dommages des alliés ciblés.""", chaine=False),

                Sort.Sort("Epée Divine",74,3,0,0,[Effets.EffetDegats(21,23,"Air",zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Epée Divine",0,4,"do",20),zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")],[Effets.EffetDegats(30,30,"Air",zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Epée Divine",0,4,"do",23),zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")],5,2,99,0,0,"cercle",False,description="""Occasionne des dommages Air et augmente les dommages des alliés ciblés.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Fendoir",120,5,0,4,[Effets.EffetDegats(47,53,"Eau",zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis"),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Fendoir",0,1,100),zone=Zones.TypeZoneCroix(1))],[Effets.EffetDegats(52,58,"Eau",zone=Zones.TypeZoneCroix(1),cibles_possibles="Ennemis"),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Fendoir",0,1,100),zone=Zones.TypeZoneCroix(1))],25,2,99,0,0,"cercle",True,description="""Occasionne des dommages Eau en zone.
            Applique des points de bouclier pour chaque ennemi touché.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Epée Destructrice",9,4,1,5,[Effets.EffetDegats(24,28,"Feu",zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True),Effets.EffetAttire(2,zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True)],[Effets.EffetDegats(30,34,"Feu",zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True),Effets.EffetAttire(2,zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True)],15,2,99,0,0,"ligne",True,description="""Occasionne des dommages Feu aux ennemis et attire les cibles vers le lanceur.""", chaine=False),

                Sort.Sort("Epée Destructrice",47,4,1,5,[Effets.EffetDegats(28,32,"Feu",zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True),Effets.EffetAttire(2,zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True)],[Effets.EffetDegats(34,38,"Feu",zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True),Effets.EffetAttire(2,zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True)],15,2,99,0,0,"ligne",True,description="""Occasionne des dommages Feu aux ennemis et attire les cibles vers le lanceur.""", chaine=False),

                Sort.Sort("Epée Destructrice",87,4,1,5,[Effets.EffetDegats(32,36,"Feu",zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True),Effets.EffetAttire(2,zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True)],[Effets.EffetDegats(38,42,"Feu",zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True),Effets.EffetAttire(2,zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True)],15,2,99,0,0,"ligne",True,description="""Occasionne des dommages Feu aux ennemis et attire les cibles vers le lanceur.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Anneau Destructeur",125,3,0,2,[Effets.EffetDegats(26,30,"Air",zone=Zones.TypeZoneAnneau(3),cibles_possibles="Ennemis",faire_au_vide=True),Effets.EffetAttire(1,"CaseCible",zone=Zones.TypeZoneAnneau(3),faire_au_vide=True)],[Effets.EffetDegats(30,34,"Air",zone=Zones.TypeZoneAnneau(3), cibles_possibles="Ennemis",faire_au_vide=True),Effets.EffetAttire(1,"CaseCible", zone=Zones.TypeZoneAnneau(3),faire_au_vide=True)],15,2,99,0,0,"cercle",True,description="""Occasionne des dommages Air en anneau et attire les cibles.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Massacre",13,2,1,3,[Effets.EffetEtat(Etats.EtatRedistribuerPer("Massacre",0,2,50,"Allies",1))],[],0,1,1,3,0,"cercle",True,description="""Lorsque la cible ennemie reçoit des dommages de sorts, elle occasionne 50% de ces dommages aux ennemis au contact.""", chaine=True),

                Sort.Sort("Massacre",54,2,1,5,[Effets.EffetEtat(Etats.EtatRedistribuerPer("Massacre",0,2,50,"Allies",1))],[],0,1,1,3,0,"cercle",True,description="""Lorsque la cible ennemie reçoit des dommages de sorts, elle occasionne 50% de ces dommages aux ennemis au contact.""", chaine=True),

                Sort.Sort("Massacre",94,2,1,7,[Effets.EffetEtat(Etats.EtatRedistribuerPer("Massacre",0,2,50,"Allies",1))],[],0,1,1,3,0,"cercle",True,description="""Lorsque la cible ennemie reçoit des dommages de sorts, elle occasionne 50% de ces dommages aux ennemis au contact.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Rassemblement",130,2,1,6,[Effets.EffetAttire(2, source="CaseCible", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatLanceSortSiSubit("Rassemblement",0,1,activationRassemblement, "Porteur"),cible_possibles="Ennemis")],[],0,1,1,2,0,"cercle",True,description="""Rapproche les ennemis de la cible.
            Si la cible est un ennemi, elle attire ensuite ses alliés quand elle est attaquée pendant 1 tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Souffle",17,2,2,4,[Effets.EffetPousser(1,"CaseCible",zone=Zones.TypeZoneCroix(1),faire_au_vide=True)],[],0,1,1,2,0,"cercle",False,description="""Repousse les alliés et les ennemis situés autour de la cellule ciblée.""", chaine=True),

                Sort.Sort("Souffle",58,2,2,6,[Effets.EffetPousser(1,"CaseCible",zone=Zones.TypeZoneCroix(1),faire_au_vide=True)],[],0,1,1,2,0,"cercle",False,description="""Repousse les alliés et les ennemis situés autour de la cellule ciblée.""", chaine=True),

                Sort.Sort("Souffle",102,2,2,8,[Effets.EffetPousser(1,"CaseCible",zone=Zones.TypeZoneCroix(1),faire_au_vide=True)],[],0,1,1,2,0,"cercle",False,description="""Repousse les alliés et les ennemis situés autour de la cellule ciblée.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Violence",135,2,0,0,[Effets.EffetAttire(1,zone=Zones.TypeZoneCercle(2)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Violence tacle",0,1,"tacle",25),zone=Zones.TypeZoneCercle(2), cibles_possibles="Ennemis"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Violence dopou",0,1,"doPou",50),zone=Zones.TypeZoneCercle(2), cibles_possibles="Ennemis")],[],0,1,99,0,0,"cercle",False,description="""Attire les entités é proximité et augmente les dommages de poussée et le Tacle pour chaque ennemi dans la zone d'effet.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Concentration",22,2,1,1,[Effets.EffetDegats(20,24,"Terre",cibles_possibles="Invoc"),Effets.EffetDegats(12,16,"Terre",cibles_exclues="Invoc")],[Effets.EffetDegats(25,29,"Terre",cibles_possibles="Invoc"),Effets.EffetDegats(17,21,"Terre",cibles_exclues="Invoc")],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Terre.
            Les dommages sont augmentés contre les Invocations.""", chaine=False),

                Sort.Sort("Concentration",65,2,1,1,[Effets.EffetDegats(24,28,"Terre",cibles_possibles="Invoc"),Effets.EffetDegats(16,20,"Terre",cibles_exclues="Invoc")],[Effets.EffetDegats(29,33,"Terre",cibles_possibles="Invoc"),Effets.EffetDegats(21,25,"Terre",cibles_exclues="Invoc")],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Terre.
            Les dommages sont augmentés contre les Invocations.""", chaine=False),

                Sort.Sort("Concentration",108,2,1,1,[Effets.EffetDegats(30,34,"Terre",cibles_possibles="Invoc"),Effets.EffetDegats(20,24,"Terre",cibles_exclues="Invoc")],[Effets.EffetDegats(36,40,"Terre",cibles_possibles="Invoc"),Effets.EffetDegats(26,30,"Terre",cibles_exclues="Invoc")],5,4,3,0,0,"ligne",True,description="""Occasionne des dommages Terre.
            Les dommages sont augmentés contre les Invocations.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Accumulation",140,3,0,4,[Effets.EffetDegats(22,26,"Terre",cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatBoostBaseDeg("Accumulation",0,3,"Accumulation",20),cibles_possibles="Lanceur")],[Effets.EffetDegats(27,31,"Terre",cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatBoostBaseDeg("Accumulation",0,3,"Accumulation",24),cibles_possibles="Lanceur")],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Terre.
            Si le sort est lancé sur soi, le sort n'occasionne pas de dommages et ils sont augmentés pour les prochains lancers.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Couper",27,3,1,3,[Effets.EffetDegats(12,16,"Feu",zone=Zones.TypeZoneLigne(3), faire_au_vide=True),Effets.EffetRetPM(2,zone=Zones.TypeZoneLigne(3), faire_au_vide=True)],[Effets.EffetDegats(19,19,"Feu",zone=Zones.TypeZoneLigne(3), faire_au_vide=True),Effets.EffetRetPM(2,zone=Zones.TypeZoneLigne(3), faire_au_vide=True)],5,2,99,0,1,"ligne",True,description="""Occasionne des dommages Feu et retire des PM.""", chaine=True),

                Sort.Sort("Couper",72,3,1,3,[Effets.EffetDegats(15,19,"Feu",zone=Zones.TypeZoneLigne(3), faire_au_vide=True),Effets.EffetRetPM(2,zone=Zones.TypeZoneLigne(3), faire_au_vide=True)],[Effets.EffetDegats(22,22,"Feu",zone=Zones.TypeZoneLigne(3), faire_au_vide=True),Effets.EffetRetPM(2,zone=Zones.TypeZoneLigne(3), faire_au_vide=True)],5,2,99,0,1,"ligne",True,description="""Occasionne des dommages Feu et retire des PM.""", chaine=True),

                Sort.Sort("Couper",118,3,1,4,[Effets.EffetDegats(18,22,"Feu",zone=Zones.TypeZoneLigne(3), faire_au_vide=True),Effets.EffetRetPM(3,zone=Zones.TypeZoneLigne(3), faire_au_vide=True)],[Effets.EffetDegats(25,25,"Feu",zone=Zones.TypeZoneLigne(3), faire_au_vide=True),Effets.EffetRetPM(3,zone=Zones.TypeZoneLigne(3), faire_au_vide=True)],5,2,99,0,1,"ligne",True,description="""Occasionne des dommages Feu et retire des PM.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Fracture",145,4,1,4,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fracture",0,2,"erosion",13), zone=Zones.TypeZoneLigneJusque(0), faire_au_vide=True),Effets.EffetDegats(34,38,"Air", zone=Zones.TypeZoneLigneJusque(0), faire_au_vide=True)],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fracture",0,2,"erosion",13), zone=Zones.TypeZoneLigneJusque(0), faire_au_vide=True),Effets.EffetDegats(39,43,"Air", zone=Zones.TypeZoneLigneJusque(0), faire_au_vide=True)],15,2,99,0,0,"ligne",False,description="""Occasionne des dommages Air jusqu'é la cellule ciblée.
            Applique un malus d'érosion.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Friction",32,2,0,4,[Effets.EffetEtat(Etats.EtatLanceSortSiSubit("Frikt",0,2,activationFriction,"Attaquant")),Effets.EffetAttire(1)],[],0,1,1,5,0,"cercle",False,description="""Attire la cible d'une case.
            La cible se rapproche ensuite de l'attaquant si elle reçoit des dommages issus de sorts pendant 2 tours.
            Nécessite d'être aligné avec la cible.""", chaine=True),

                Sort.Sort("Friction",81,2,0,4,[Effets.EffetEtat(Etats.EtatLanceSortSiSubit("Frikt",0,2,activationFriction,"Attaquant")),Effets.EffetAttire(1)],[],0,1,1,4,0,"cercle",False,description="""Attire la cible d'une case.
            La cible se rapproche ensuite de l'attaquant si elle reçoit des dommages issus de sorts pendant 2 tours.
            Nécessite d'être aligné avec la cible.""", chaine=True),

                Sort.Sort("Friction",124,2,0,5,[Effets.EffetEtat(Etats.EtatLanceSortSiSubit("Frikt",0,2,activationFriction,"Attaquant")),Effets.EffetAttire(1)],[],0,1,1,3,0,"cercle",False,description="""Attire la cible d'une case.
            La cible se rapproche ensuite de l'attaquant si elle reçoit des dommages issus de sorts pendant 2 tours.
            Nécessite d'être aligné avec la cible.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Coup pour coup",150,2,1,3,[Effets.EffetEtatSelf(Etats.EtatLanceSortSiSubit("Rend coup pour coup",0,2,activationCoupPourCoup,"Porteur")),Effets.EffetEtat(Etats.Etat("Coup pour coup",0,2)),Effets.EffetPousser(2)],[],0,1,1,3,0,"cercle",True,description="""Repousse un ennemi.
            La cible est ensuite repoussée de 2 cases à chaque fois qu'elle attaque le lanceur pendant 2 tours.""", chaine=True)
            ]))
            # sorts.append(Sort.Sort("Duel",3,1,1,[],1,1,4,0,"cercle",description="Retire leurs PM à la cible et au lanceur, leur applique l'état Pesanteur et les rend invulnérable aux dommages à distance. Ne fonctionne que si lancé sur un ennemi."))
            # sorts.append(Sort.Sort("Emprise",3,1,1,[],1,1,4,0,"cercle",description="Retire tous les PM de l'ennemi ciblé mais le rend invulnérable."))
            # sorts.append(Sort.Sort("Épée du Jugement",4,1,5,[Effets.EffetDegats(20,28,"air"),Effets.EffetVolDeVie(10,12,"feu")],3,2,0,0,"cercle",description="Occasionne des dommages Air et vole de la vie dans l'élément Feu sans ligne de vue."))
            # sorts.append(Sort.Sort("Condamnation",3,1,6,[
            #     Effets.EffetDegats(33,37,"feu",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_2",consomme_etat=False),
            #     Effets.EffetDegats(33,37,"air",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_2",consomme_etat=True),
            #     Effets.EffetEtat(Etats.Etat("Condamnation_lancer_2",0,-1),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=True),
            #     Effets.EffetDegats(23,27,"feu",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=False),
            #     Effets.EffetDegats(23,27,"air",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=True),
            #     Effets.EffetEtat(Etats.Etat("Condamnation_lancer_1",0,-1),etat_requis_cibles="!Condamnation_lancer_2")
            #     ],3,2,0,0,"cercle",chaine=False,description="Occasionne des dommages Air et Feu. Les dommages sont appliqués lorsque le sort est lancé sur une autre cible. Peut se cumuler 2 fois sur une même cible."))
            # sorts.append(Sort.Sort("Puissance",3,0,6,[Effets.EffetEtat(Etats.EtatBoostPuissance("Puissance",0,2,300))],1,1,3,0,"cercle",description="Augmente la Puissance de la cible."))
            # sorts.append(Sort.Sort("Vertu",3,0,0,[Effets.EffetEtat(Etats.EtatBoostPuissance("Vertu",0,2,-150),zone=Zones.TypeZoneCercle(1))],1,1,3,0,"cercle",description="Applique un bouclier zone mais réduit la Puissance du lanceur."))
            # sorts.append(Sort.Sort("Précipitation",2,0,6,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Precipite",0,1,"_PA",5)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Sortie de Precipitation",1,1,"_PA",-3))],1,1,2,0,"cercle",description="Augmente les PA de la cible pour le tour en cours mais lui retire des PA le tour suivant. Interdit l'utilisation des armes et du sort Colère de Iop."))
            # sorts.append(Sort.Sort("Agitation",2,0,5,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Agitation",0,1,"_PM",2)),Effets.EffetEtat(Etats.Etat("Intaclable",1,1))],2,2,0,0,"cercle",description="Augmente les PM et la Fuite pour le tours en cours."))
            # sorts.append(Sort.Sort("Tempête de Puissance",3,3,5,[Effets.EffetDegats(34,38,"feu")],3,2,0,0,"cercle",description="Occasionne des dommages Feu."))
            # sorts.append(Sort.Sort("Tumulte",4,2,5,[Effets.EffetDegats(19,21,"feu",zone=Zones.TypeZoneCroix(1))],1,1,1,0,"cercle",description="Occasionne des dommages Feu en zone. Plus le nombre de cibles est important, plus les dommages sont importants.*"))
            # sorts.append(Sort.Sort("Épée Céleste",4,0,4,[Effets.EffetDegats(36,40,"air",zone=Zones.TypeZoneCercle(2))],2,2,0,0,"ligne",description="Occasionne des dommages Air en zone."))
            # sorts.append(Sort.Sort("Zénith",5,1,3,[Effets.EffetDegats(86,94,"air",zone=Zones.TypeZoneLigne(4))],1,1,0,0,"ligne",description="Occasionne des dommages Air en zone. Les dommages sont augmentés pour chaque PM disponible lorsque le sort est lancé."))
            # sorts.append(Sort.Sort("Vitalité",3,0,6,[Effets.EffetEtat(Etats.EtatBoostVita("Vitalite",0,4,20))],1,1,2,0,"cercle",description="Augmente temporairement les PV de la cible en pourcentage. Le bonus de PV est plus faible sur les alliés que sur le lanceur."))
            # sorts.append(Sort.Sort("Endurance",4,0,1,[Effets.EffetDegats(34,38,"eau",cibles_exclues="Lanceur")],3,2,0,0,"cercle",description="Occasionne des dommages Eau. Applique des points de bouclier au lanceur."))
            # sorts.append(Sort.Sort("Épée de Iop",4,1,6,[Effets.EffetDegats(37,41,"terre",zone=Zones.TypeZoneCroix(3),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",faire_au_vide=True)],2,2,0,0,"ligne",description="Occasionne des dommages Terre en croix.")) 
            # sorts.append(Sort.Sort("Pugilat",2,1,4,[Effets.EffetDegats(9,11,"terre",zone=Zones.TypeZoneCercle(2),cibles_exclues="Lanceur"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Pugilat",0,1,"Pugilat",20))],4,1,0,0,"cercle",description="Occasionne des dommages Terre en zone. Les dommages sont augmentés pendant 1 tour après chaque lancer.")) 
            # sorts.append(Sort.Sort("Épée du Destin",4,1,1,[Effets.EffetDegats(38,42,"feu"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Epee_du_destin", 2,1,"Épée du Destin",30))], 1,1,2,0,"ligne",description="Occasionne des dommages Feu. Les dommages sont augmentés à partir du second lancer.")) 
            # sorts.append(Sort.Sort("Sentence",2,1,6,[Effets.EffetDegats(13,16,"feu"),Effets.EffetEtat(Etats.EtatEffetFinTour("Sentence", 1,1,Effets.EffetDegats(13,16,"feu",zone=Zones.TypeZoneCercle(2)),"Sentence","lanceur"))], 3,1,0,0,"ligne",description="Occasionne des dommages Feu. Occasionne des dommages Feu supplémentaires en zone à la fin du tour de la cible.")) 
            # sorts.append(Sort.Sort("Colère de Iop",7,1,1,[Effets.EffetDegats(81,100,"terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Colere_de_Iop", 3,1,"Colère de Iop",110))], 1,1,3,0,"ligne",description="Occasionne des dommages Terre. Augmente les dommages du sort au troisième tour après son lancer.")) 
            # sorts.append(Sort.Sort("Fureur",3,1,1,[Effets.EffetDegats(28,32,"terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fureur", 1,2,"Fureur",40))], 1,1,0,0,"ligne",description="Occasionne des dommages Terre. Les dommages sont augmentés à chaque lancer du sort, mais ce bonus est perdu si le sort n'est pas relancé."))
        elif classe=="Cra":
            sorts.append(Sort.Sort("Flèche Magique",3,1,12,[Effets.EffetDegats(19,21,"air"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche Magique",1,1,"PO",-2)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",2))],3,2,0,1,"cercle",description="Occasionne des dommages Air et vole la portée de la cible."))
            sorts.append(Sort.Sort("Flèche de Concentration",3,3,8,[Effets.EffetDegats(22,26,"air",zone=Zones.TypeZoneCroix(3),cibles_possibles="Ennemis" ),Effets.EffetAttireVersCible(2,zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis")],2,1,0,1,"cercle",description="Occasionne des dommages Air et attire vers la cible."))
            sorts.append(Sort.Sort("Flèche de Recul",3,1,8,[Effets.EffetDegats(25,28,"air"),Effets.EffetRepousser(4)],2,1,0,0,"ligne",description="Occasionne des dommages Air aux ennemis et pousse la cible."))
            sorts.append(Sort.Sort("Flèche Érosive",3,1,3,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche Erosive",0,2,"erosion",10)), Effets.EffetDegats(25,29,"terre")],3,2,0,1,"ligne",description="Occasionne des dommages Terre et applique un malus d'Érosion."))
            sorts.append(Sort.Sort("Flèche de Dispersion",3,1,12,[Effets.EffetPousser(2,zone=Zones.TypeZoneCroix(2),faire_au_vide=True)],1,1,2,1,"cercle",description="Pousse les ennemis et alliés, même s'ils sont bloqués par d'autres entités."))
            sorts.append(Sort.Sort("Représailles",4,2,5,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Immobilise",0,1,"_PM",-100)),Effets.EffetEtat(Etats.Etat("Pesanteur",1,1))],1,1,5,0,"ligne",description="Immobilise la cible."))
            sorts.append(Sort.Sort("Flèche Glacée",3,3,6,[Effets.EffetDegats(17,19,"feu"),Effets.EffetRetPA(2)],99,2,0,1,"cercle",description="Occasionne des dommages Feu et retire des PA."))
            sorts.append(Sort.Sort("Flèche Paralysante",5,2,6,[Effets.EffetDegats(39,42,"feu",zone=Zones.TypeZoneCroix(1)),Effets.EffetRetPA(4,zone=Zones.TypeZoneCroix(1))],1,1,0,0,"cercle",description="Occasionne des dommages Feu et retire des PA."))
            sorts.append(Sort.Sort("Flèche Enflammée",4,1,8,[Effets.EffetDegats(33,35,"feu",zone=Zones.TypeZoneLigne(5) ,faire_au_vide=True),Effets.EffetRepousser(1,zone=Zones.TypeZoneLigne(5),faire_au_vide=True)],2,2,0,1,"ligne",description="Occasionne des dommages Feu et pousse les cibles présentes dans la zone d'effet du sort."))
            sorts.append(Sort.Sort("Flèche Repulsive",3,1,7,[Effets.EffetDegats(28,32,"feu",zone=Zones.TypeZoneLignePerpendiculaire(1),faire_au_vide=True),Effets.EffetPousser(1,zone=Zones.TypeZoneLignePerpendiculaire(1),faire_au_vide=True)],2,2,0,0,"ligne",description="Occasionne des dommages Feu et repousse de 1 case."))
            sorts.append(Sort.Sort("Tir Éloigne",3,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir_eloigne",0,4,"PO",6),zone=Zones.TypeZoneCercle(3))],1,1,5,0,"cercle",description="Augmente la portée des cibles présentes dans la zone d'effet."))
            sorts.append(Sort.Sort("Acuité Absolue",4,0,0,[Effets.EffetEtat(Etats.Etat("Desactive_ligne_de_vue",0,1))],1,1,3,0,"cercle",description="Tous les sorts du Crâ peuvent être lancés au travers des obstacles."))
            sorts.append(Sort.Sort("Flèche d'Expiation",4,6,10,[Effets.EffetDegats(35,37,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_d_expiation",0,-1,"Flèche d'Expiation",36))],1,1,3,1,"cercle",description="Occasionne des dommages Eau, augmente les dommages du sort tous les 3 tours et empêche la cible d'utiliser des sorts de déplacement."))
            sorts.append(Sort.Sort("Flèche de Rédemption",3,6,8,[Effets.EffetDegats(19,22,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_de_redemption",1,1,"Flèche de Rédemption",12))],3,2,0,1,"cercle",description="Occasionne des dommages Eau qui sont augmentés si le sort est relancé le tour suivant."))
            sorts.append(Sort.Sort("Oeil de Taupe",3,5,10,[Effets.EffetVolDeVie(16,18,"eau",zone=Zones.TypeZoneCercle(3), faire_au_vide=True),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Oeil_de_taupe",1,3,"PO",-3),zone=Zones.TypeZoneCercle(3)),Effets.EffetRetireEtat("Invisible",zone=Zones.TypeZoneCercle(3), faire_au_vide=True),Effets.EffetDevoilePiege(zone=Zones.TypeZoneCercle(3), faire_au_vide=True)],1,1,4,1,"cercle",chaine=False,description="Réduit la portée des personnages ciblés, vole de la vie dans l'élément Eau et repère les objets invisibles dans sa zone d'effet."))
            sorts.append(Sort.Sort("Flèche Écrasante",3,5,7,[Effets.EffetDegats(34,38,"feu",zone=Zones.TypeZoneCroixDiagonale(1)),Effets.EffetEtat(Etats.Etat("Pesanteur",1,1),zone=Zones.TypeZoneCroixDiagonale(1))],1,1,3,1,"cercle",description="Occasionne des dommages Feu et applique l'état Pesanteur."))
            sorts.append(Sort.Sort("Tir Critique",2,0,6,[Effets.EffetEtat(Etats.Etat("Tir_critique",0,4))],1,1,5,1,"cercle",description="Augmente la probabilité de faire un coup critique."))
            sorts.append(Sort.Sort("Balise de Rappel",2,1,5,[Effets.EffetInvoque("Balise de rappel",True,cibles_possibles="",faire_au_vide=True)],1,1,2,0,"cercle",description="Invoque une balise qui échange sa position avec celle du lanceur (au début du prochain tour)."))
            sorts.append(Sort.Sort("Flèche d'Immobilisation",2,1,6,[Effets.EffetDegats(10,11,"eau"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche_d_immobilisation",1,1,"_PM",-1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fleche_d_immobilisation",0,1,"_PM",1))],4,2,0,1,"cercle",description="Occasionne des dommages Eau et vole des PM à la cible."))
            sorts.append(Sort.Sort("Flèche Assaillante",3,2,6,[Effets.EffetDegats(33,37,"eau",cibles_possibles="Ennemis"),Effets.EffetPousser(1,cibles_possibles="Ennemis"),Effets.EffetAttireAttaquant(1,cibles_possibles="Allies")],3,2,0,1,"ligne",description="Occasionne des dommages Eau sur les ennemis et le lanceur recule de 1 case. Sur un allié : rapproche le lanceur de 1 case."))
            sorts.append(Sort.Sort("Flèche Punitive",4,6,8,[Effets.EffetDegats(29,31,"terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_punitive",0,-1,"Flèche Punitive",30))],1,1,2,1,"cercle",description="Occasionne des dommages Terre et augmente les dommages du sort tous les 2 tours."))
            sorts.append(Sort.Sort("Flèche du Jugement",3,5,7,[Effets.EffetDegats(39,45,"terre")],3,2,0,1,"cercle",description="Occasionne des dommages Terre. Plus le pourcentage de PM du personnage au lancement du sort est important, plus les dommages occasionnés sont importants."))
            sorts.append(Sort.Sort("Tir Puissant",3,0,6,[Effets.EffetEtat(Etats.EtatBoostPuissance("Tir_puissant",0,3,250))],1,1,6,1,"cercle",description="Augmente les dommages des sorts."))
            sorts.append(Sort.Sort("Balise Tactique",1,1,10,[Effets.EffetInvoque("Balise Tactique",True, cibles_possibles="", faire_au_vide=True)],1,1,2,1,"cercle",description="Invoque une Balise qui peut servir d'obstacle et de cible. La Balise subit 2 fois moins de dommages des alliés."))
            sorts.append(Sort.Sort("Flèche Harcelante",3,1,7,[Effets.EffetDegats(13,15,"air")],1,1,2,1,"cercle",description="Occasionne des dommages Air sans ligne de vue."))
            sorts.append(Sort.Sort("Flèche Massacrante",4,4,8,[Effets.EffetDegats(34,38,"air"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_massacrante",1,1,"Flèche Massacrante",10))],3,2,0,1,"ligne",description="Occasionne des dommages Air. Les dommages du sort sont augmentés au tour suivant."))
            sorts.append(Sort.Sort("Flèche Empoisonnée",3,1,10,[Effets.EffetRetPM(3),Effets.EffetEtat(Etats.EtatEffetDebutTour("Fleche_empoisonnee", 1,2,Effets.EffetDegats(17,18,"neutre"),"Fleche_empoisonnee","lanceur"))],4,1,0,1,"cercle",description="Occasionne des dommages Neutre sur plusieurs tours et retire des PM."))
            sorts.append(Sort.Sort("Flèche Persecutrice",3,5,8,[Effets.EffetDegats(15,17,"feu"),Effets.EffetDegats(15,17,"air")],99,2,0,1,"ligne",description="Occasionne des dommages Air et Feu."))
            sorts.append(Sort.Sort("Flèche Tyrannique",4,2,7,[Effets.EffetEtat(Etats.EtatEffetSiPousse("Fleche_tyrannique_air",0,2, Effets.EffetDegats(12,12,"air"),"Fleche_tyrannique","lanceur")),Effets.EffetEtat(Etats.EtatEffetSiSubit("Fleche_tyrannique_feu",0,2, Effets.EffetDegats(12,12,"feu"),"Fleche_tyrannique","doPou","lanceur"))],99,1,0,1,"ligne",description="Occasionne des dommages Air si la cible est poussée. Occasionne des dommages Feu si la cible subit des dommages de poussée."))
            sorts.append(Sort.Sort("Flèche Destructrice",4,5,8,[Effets.EffetDegats(30,32,"terre"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche destructrice",1,1,"do",-60))],99,2,0,1,"cercle",description="Occasionne des dommages Terre et réduit les dommages occasionnés par la cible."))
            sorts.append(Sort.Sort("Tir de Barrage",4,4,8,[Effets.EffetDegats(29,33,"terre"),Effets.EffetPousser(2)],3,2,0,1,"cercle",description="Occasionne des dommages Terre et repousse la cible."))
            sorts.append(Sort.Sort("Flèche Absorbante",4,6,8,[Effets.EffetVolDeVie(29,31,"air")],3,2,0,1,"cercle",description="Vole de la vie dans l'élément Air."))
            sorts.append(Sort.Sort("Flèche Dévorante",3,1,6,[
                Effets.EffetDegats(70,74,"air",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Fleche_devorante_lancer_3",consomme_etat=True),
                Effets.EffetEtat(Etats.Etat("Fleche_devorante_lancer_3",0,-1),etat_requis_cibles="Fleche_devorante_lancer_2",consomme_etat=True),
                Effets.EffetDegats(52,56,"air",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Fleche_devorante_lancer_2",consomme_etat=True),
                Effets.EffetEtat(Etats.Etat("Fleche_devorante_lancer_2",0,-1),etat_requis_cibles="Fleche_devorante_lancer_1",consomme_etat=True),
                Effets.EffetDegats(34,38,"air",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Fleche_devorante_lancer_1",consomme_etat=True),
                Effets.EffetEtat(Etats.Etat("Fleche_devorante_lancer_1",0,-1),etat_requis_cibles="!Fleche_devorante_lancer_2|!Fleche_devorante_lancer_3")
                ],2,1,0,1,"cercle",chaine=False,description="Occasionne des dommages Air. Les dommages sont appliqués lorsque le sort est lancé sur une autre cible. Peut se cumuler 3 fois sur une même cible."))
            sorts.append(Sort.Sort("Flèche cinglante",2,1,9,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche cinglante",0,2,"erosion",10)), Effets.EffetPousser(2)],4,2,0,1,"ligne",description="Applique de l'Érosion aux ennemis et repousse de 2 cases."))
            sorts.append(Sort.Sort("Flèche de repli",1,2,7,[Effets.EffetPousser(1,zone=Zones.TypeZoneCercleSansCentre(5),cible_possibles="Lanceur")],4,2,0,1,"ligne",description="Le lanceur du sort recule de 2 cases."))
            sorts.append(Sort.Sort("Flèche ralentissante",4,1,8,[Effets.EffetRetPA(3,zone=Zones.TypeZoneCercle(2)),Effets.EffetDegats(36,38,"eau",zone=Zones.TypeZoneCercle(2))],2,1,0,1,"ligne",description="Occasionne des dommages Eau et retire des PA en zone."))
            sorts.append(Sort.Sort("Flèche percutante",2,1,6,[Effets.EffetDegats(6,10,"eau"),Effets.EffetEtat(Etats.EtatEffetFinTour("Fleche_percutante_retardement", 1,1,Effets.EffetDegats(6,10,"eau",zone=Zones.TypeZoneCercleSansCentre(2)),"Fleche_percutante_retardement","lanceur")),Effets.EffetEtat(Etats.EtatEffetFinTour("Fleche_percutante_retardementPA", 1,1,Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2)),"Fleche_percutante_retardementPA","lanceur"))],2,1,0,1,"cercle",description="Occasionne des dommages Eau. À la fin de son tour, la cible occasionne des dommages Eau et retire des PA en cercle de taille 2 autour d'elle."))
            sorts.append(Sort.Sort("Flèche explosive",4,1,8,[Effets.EffetDegats(30,34,"feu",zone=Zones.TypeZoneCercle(3))],2,1,0,1,"cercle",description="Occasionne des dommages Feu en zone."))
            fleche_fulminante=Sort.Sort("Flèche Fulminante",4,1,8,[Effets.EffetDegats(34,38,"feu",cibles_possibles="Ennemis|Balise Tactique"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_Fulminante_boost",0,1,"Flèche Fulminante Rebond",10))],1,1,0,1,"cercle",description="Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
            fleche_fulminante_rebond=Sort.Sort("Flèche Fulminante Rebond",0,0,99,[Effets.EffetDegats(34,38,"feu",cibles_possibles="Ennemis|Balise Tactique"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_Fulminante_boost",0,1,"Flèche Fulminante Rebond",10))],9,1,0,0,"cercle",description="Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
            fleche_fulminante.effets.append(Effets.EffetPropage(fleche_fulminante_rebond,Zones.TypeZoneCercle(2),cibles_possibles="Ennemis|Balise Tactique"))
            fleche_fulminante_rebond.effets.append(Effets.EffetPropage(fleche_fulminante_rebond,Zones.TypeZoneCercle(2),cibles_possibles="Ennemis|Balise Tactique"))
            sorts.append(fleche_fulminante)
            sorts.append(Sort.Sort("Maîtrise de l'arc",2,0,6,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Maitrise de l'arc",0,3,"do",60))],1,1,5,1,"cercle",description="Augmente les dommages."))
            sorts.append(Sort.Sort("Sentinelle",2,0,0,[Effets.EffetEtatSelf(Etats.EtatBoostPerDommageSorts("Sentinelle",1,1,30)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Sentinelle",1,1,"_PM",-100))],1,1,3,0,"cercle",description="Au tour suivant, le lanceur perd tous ses PM mais gagne un bonus de dommages."))
        elif classe=="Sram":
            activationPiegeSournois = [Effets.EffetDegats(10,12,"feu",zone=Zones.TypeZoneCercle(1), faire_au_vide=True,piege=True),Effets.EffetAttire(1,zone=Zones.TypeZoneCercle(1), faire_au_vide=True)]
            activationPiegeRepulsif =[Effets.EffetDegats(10,12,"air",zone=Zones.TypeZoneCercle(1), faire_au_vide=True,piege=True),Effets.EffetPousser(2,zone=Zones.TypeZoneCercle(1), faire_au_vide=True)]
            #sorts.append(Sort.Sort(u"Sournoiserie",3,1,5,[Effets.EffetDegats(20,22,"terre")],99,3,0,1, "cercle", description=u"Occasionne des dommages Terre."))
            #TODO: ajout invisibilité et test avec oeil de taupe.
            sorts.append(Sort.Sort("Invisibilité",2,0,0,[Effets.EffetEtat(Etats.Etat("Invisible",0,3)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Invibilité_PM",0,4,"_PM",1))],1,1,6,0, "cercle", description=u"Rend invisible."))
            sorts.append(Sort.Sort("Piège sournois",3,1,8,[Effets.EffetPiege(Zones.TypeZoneCroix(1),activationPiegeSournois,"Piège sournois",(255,0,0),faire_au_vide=True)],1,1,0,1, "cercle", description="Occasionne des dommages Feu et attire."))
            sorts.append(Sort.Sort("Piège répulsif",3,1,7,[Effets.EffetPiege(Zones.TypeZoneCercle(1),activationPiegeRepulsif,"Piège répulsif",(255,0,255),faire_au_vide=True)],1,1,1,1, "cercle", description="Occasionne des dommages Feu et attire."))
        sorts.append(Sort.Sort("Cawotte",0,4,1,6,[Effets.EffetInvoque("Cawotte",False,cibles_possibles="", faire_au_vide=True)],[],0, 1,1,6,0,"cercle",True,description="Invoque une Cawotte")) 
        total_nb_sorts = len(sorts)
        i = 0
        while i < total_nb_sorts:
            if sorts[i] is None:
                sorts.remove(sorts[i])
                total_nb_sorts-=1
                i-=1
            i+=1
        return sorts

    def bouge(self, niveau, x,y, ajouteHistorique=True,canSwap=False):
        """@summary: téléporte le joueur sur la carte et stock le déplacement dans l'historique de déplacement.
        @x: la position d'arrivée en x.
        @type: int
        @x: la position d'arrivée en y.
        @type: int"""
        # test si la case d'arrivé est hors-map (compte comme un obstacle)
        if x >= niveau.taille or x < 0 or y >= niveau.taille or y < 0:
            return False,False
        elif niveau.structure[y][x].type != "v":
            return False,False
        if ajouteHistorique:
            self.historiqueDeplacement.append([self.posX,self.posY,2])
        niveau.structure[self.posY][self.posX].type = "v"
        niveau.structure[y][x].type = "j"
        self.posX = x
        self.posY = y
        
        nbPieges = len(niveau.pieges)
        i=0
        piegeDeclenche = False
        #Priorité au nouveau piège:
        sauvegardeFile = niveau.fileEffets[:]
        niveau.fileEffets = []
        while i < nbPieges:
            piege = niveau.pieges[i]
            if piege.aPorteDeclenchement(x,y):
                piegeDeclenche = True
                for effet in piege.effets: 
                    sestApplique, cibles = niveau.lancerEffet(effet,piege.centre_x,piege.centre_y,piege.nomSort, piege.centre_x,piege.centre_y,piege.lanceur)          
                i-=1
                niveau.pieges.remove(piege)
            i+=1
            nbPieges = len(niveau.pieges)
        niveau.fileEffets = niveau.fileEffets + sauvegardeFile
        niveau.depileEffets()
        return True,piegeDeclenche

    def echangePosition(self, niveau, joueurCible, ajouteHistorique=True):
        """@summary: téléporte le joueur sur la carte et stock le déplacement dans l'historique de déplacement.
        @x: la position d'arrivée en x.
        @type: int
        @x: la position d'arrivée en y.
        @type: int"""
        # test si la case d'arrivé est hors-map (compte comme un obstacle)
        if niveau.structure[joueurCible.posY][joueurCible.posX].type != "j":
            print("DEBUG : THIS SHOULD NOT BE POSSIBLE")
            return False,False
        if ajouteHistorique:
            self.historiqueDeplacement.append([self.posX,self.posY,2])
        joueurCible.historiqueDeplacement.append([joueurCible.posX,joueurCible.posY,2])
        x = self.posX
        y = self.posY
        self.posX = joueurCible.posX
        self.posY = joueurCible.posY
        joueurCible.posX = x
        joueurCible.posY = y
        nbPieges = len(niveau.pieges)
        i=0
        piegeDeclenche = False
        #Priorité au nouveau piège:
        sauvegardeFile = niveau.fileEffets[:]
        niveau.fileEffets = []
        while i < nbPieges:
            piege = niveau.pieges[i]
            if piege.aPorteDeclenchement(x,y):
                piegeDeclenche = True
                for effet in piege.effets:
                    niveau.pieges.remove(piege)
                    i-=1
                    sestApplique, cibles = niveau.lancerEffet(effet,piege.centre_x,piege.centre_y,piege.nomSort, piege.centre_x,piege.centre_y,piege.lanceur)          
            i+=1
            nbPieges = len(niveau.pieges)
        niveau.fileEffets = niveau.fileEffets + sauvegardeFile
        niveau.depileEffets()
        return True,piegeDeclenche

    def rafraichirHistoriqueDeplacement(self):
        """@summary: supprime les déplacements plus vieux que 2 tours"""
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
            if(len(self.historiqueDeplacement)>0):
                pos = self.historiqueDeplacement[-1]
                del self.historiqueDeplacement[-1]
                niveau.gereDeplacementTF(self,pos,lanceur,nomSort,AjouteHistorique=False)


    def rafraichirEtats(self,niveau,debutTour=True):
        """@summary: met à jour les états du personnage. (diminution de durée restante),  
                active le trigger triggerRafraichissement si un état débute et active triggerAvantRetrait si un état termine
        @niveau: la grille de jeu
        @type: Niveau
        @debutTour: Indique si le rafraichissement est dû au début de tour ou à un effet autre.
        @type: booléen."""
        i = 0
        nbEtats = len(self.etats)
        while i < nbEtats:
            #Baisse de la durée de vie si l'état était actif
            if self.etats[i].actif():
                  self.etats[i].duree -= 1
            #Si c'est un début de tour, le temps avant de début de l'état est diminué
            if debutTour:
                self.etats[i].debuteDans -= 1
            #Si c'est finalement le tour de début de l'état et si l'état est actif, on active le trigger d'état de rafraichissement
            if self.etats[i].debuteDans == 0: 
                if self.etats[i].actif():
                    self.etats[i].triggerRafraichissement(self,niveau)
            #Si c'est le tour de sortie de l'état on active le trigger d'état d'avant retrait
            if self.etats[i].duree == 0:
                #Appliquer les fin de bonus et malus des do, pm, pa, po, pui et carac ici
                print(self.classe+" sort de l'etat "+self.etats[i].nom)
                self.etats[i].triggerAvantRetrait(self)
                del self.etats[i]
                i-=1
                nbEtats = len(self.etats)
            i+=1

    def aEtat(self,nomEtatCherche):
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
                #Appliquer les fin de bonus et malus des do, pm, pa, po, pui et carac ici
                print(self.classe+" sort de l'etat "+self.etats[i].nom)
                self.etats[i].triggerAvantRetrait(self)
                del self.etats[i]
                i-=1
                nbEtats = len(self.etats)
            i+=1

    def getBoucliers(self):
        pb_restants = 0
        for etat in self.etats:
            if etat.actif():
                if isinstance(etat, Etats.EtatBouclierPerLvl):
                    pb_restants += etat.boostBouclier

        return pb_restants

    def subit(self,attaquant, niveau, degats,typeDegats):
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
                etat.triggerAvantSubirDegats(self,niveau,totalPerdu,typeDegats,attaquant)
        
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
        if erosion > 50: # L'érosion est capé à 50% dans le jeu
            erosion = 50
        elif erosion < 10: # L'érosion est capé mini à 10% dans le jeu
            erosion = 10
        self._vie -= int(totalPerdu * (erosion/100))
        if self._vie < 0:
            self._vie = 0
        if self.vie > self._vie:
            self.vie = self._vie
        toprint = ""
        toprint = self.classe+" a "+str(self.vie) +"/"+str(self._vie)+" PV"
        if pb_restants > 0:
            toprint+= " et "+str(pb_restants)+" PB"
        print("-"+str(totalPerdu)+" PV")
        print(toprint)
        if self.vie <= 0:
            niveau.tue(self)
        for etat in self.etats:
            if etat.actif():
                etat.triggerApresSubirDegats(self,niveau,attaquant,totalPerdu)

    def finTour(self,niveau):
        """@summary: Termine le tour du personnage, récupération des PA et PM, sorts utilisés, activation du trigger d'état triggerFinTour
        @niveau: La grille de jeu
        @type: Niveau"""
        self.PM = self._PM
        self.PA = self._PA
        for sort in self.sorts:
            sort.compteLancerParTour = 0
            sort.compteTourEntreDeux+=1
            sort.compteLancerParTourParJoueur = {}
        for etat in self.etats:
            if etat.actif():
                etat.triggerFinTour(self,niveau)
        

    def debutTour(self,niveau):
        """@summary: Débute le tour du personnage, déclenche glyphe, rafraîchit les états, les glyphes et l'historique de déplacement.
        @niveau: La grille de jeu
        @type: Niveau"""
        for glyphe in niveau.glyphes:
            if glyphe.actif():
                if glyphe.sortMono.APorte(glyphe.centre_x, glyphe.centre_y,self.posX,self.posY, 0):
                    for effet in glyphe.sortMono.effets:
                        niveau.lancerEffet(effet,glyphe.centre_x,glyphe.centre_y,glyphe.nomSort, self.posX, self.posY, glyphe.lanceur)
        niveau.depileEffets()
        self.rafraichirEtats(niveau)
        niveau.rafraichirGlyphes(self)
        niveau.rafraichirRunes(self)
        self.rafraichirHistoriqueDeplacement()
        for etat in self.etats:
            if etat.actif():
                etat.triggerDebutTour(self,niveau)

        self.posDebTour = [self.posX, self.posY]

        niveau.afficherSorts()
        print("Debut de tour.")
        print("PA : "+str(self.PA))
        print("PM : "+str(self.PM))
        print("PV : "+str(self.vie))


    def appliquerEtat(self,etat,lanceur, niveau=None):
        """@summary: Applique un nouvel état sur le Personnage. Active le trigger d'état triggerInstantane
        @etat: l'état qui va être appliqué
        @type: Etat
        @lanceur: le lanceur de l'état
        @type: Personnage
        @niveau: La grille de jeu (optionnel)
        @type: Niveau"""
        print(self.classe+"  etat "+etat.nom+" ("+str(etat.duree)+" tours)")
        etat.lanceur = lanceur
        self.etats.append(etat)
        if self.etats[-1].actif():
            self.etats[-1].triggerInstantane(lanceur=lanceur,niveau=niveau,joueurCaseEffet=self)

    def changeDureeEffets(self, n, niveau):
        """@summary: Réduit la durée des états sur le personnage
        @n: le nombre de tours d'état réduit
        @type: int
        @niveau: La grille de jeu
        @type: Niveau"""
        for i in range(abs(n)):
            self.rafraichirEtats(niveau,False)

    def selectionSort(self,sort,niveau):
        sortSelectionne = None
        coutPA = sort.getCoutPA(self)
        if coutPA < 0:
            coutPA = 0
        if (coutPA <= niveau.tourDe.PA):
            res, explication,coutPA = sort.estLancable(niveau,niveau.tourDe,None)
            if res == True:
                sortSelectionne = sort
            else:
                print(explication)

        else:
            print("PA insuffisant : coute "+str(coutPA)+ " mais "+str(niveau.tourDe.PA) + " restant.")
        return sortSelectionne

    def joue(self,event,niveau,mouse_xy,sortSelectionne):
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

        #Clic souris
        if event.type == pygame.KEYDOWN:
            if event.key == K_F1: # touche F1 = fin du tour
                sortSelectionne = None
                niveau.finTour()
            if event.key == K_ESCAPE: # touche échap = déselection de sort.
                sortSelectionne = None
            if event.key >= K_1 and event.key <= K_9:
                aLance = niveau.tourDe.sorts[event.key - K_1]
                sortSelectionne = self.selectionSort(aLance,niveau)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicGauche,clicMilieu,clicDroit = pygame.mouse.get_pressed()
            # Clic gauche
            if clicGauche:
                # Clic gauche sort = tentative de sélection de sort
                if mouse_xy[1] > constantes.y_sorts:
                    for sort in niveau.tourDe.sorts:
                        if sort.vue.isMouseOver(mouse_xy):
                            sortSelectionne = self.selectionSort(sort,niveau)
                            break
                #Clic gauche grille de jeu = tentative de lancé un sort si un sort est selectionné ou tentative de déplacement sinon
                else:
                    #Un sort est selectionne
                    if sortSelectionne != None:
                        case_cible_x = int(mouse_xy[0]/constantes.taille_sprite)
                        case_cible_y = int(mouse_xy[1]/constantes.taille_sprite)
                        sortSelectionne.lance(niveau.tourDe.posX,niveau.tourDe.posY,niveau, case_cible_x,case_cible_y)
                        sortSelectionne = None
                    #Aucun sort n'est selectionne: on pm
                    else:
                        niveau.Deplacement(mouse_xy)
            #Clic droit
            elif clicDroit:
                # Clic droit grille de jeu = affichage détaillé de l'état d'un personnage.
                if mouse_xy[1]<constantes.y_sorts:
                    case_x = int(mouse_xy[0]/constantes.taille_sprite)
                    case_y = int(mouse_xy[1]/constantes.taille_sprite)
                    joueurInfo = niveau.getJoueurSur(case_x, case_y)
                    if joueurInfo != None:
                        for etat in joueurInfo.etats:
                            print(joueurInfo.classe+" est dans l'etat "+etat.nom+" ("+str(etat.duree)+")")
                    if sortSelectionne != None:
                        sortSelectionne = None
        return sortSelectionne

class PersonnageMur(Personnage):
    """@summary: Classe décrivant un montre de type MUR immobile (cawotte, cadran de xélor...). hérite de Personnage"""
    def __init__(self, *args):
        """@summary: Initialise un personnage Mur, même initialisation que Personange
        @args: les arguments donnés, doivent être les mêmes que Personnage
        @type:*args"""
        super(PersonnageMur, self).__init__(*args)
    def deepcopy(self):
        """@summary: Clone le personnageMur
        @return: le clone"""
        cp = PersonnageMur(self.classe, self.lvl, self.team, self.caracsPrimaires, self.caracsSecondaires, self.dommages, self.resistances ,self.icone)
        cp.sorts = Personnage.ChargerSorts(cp.classe, cp.lvl)
        return cp
    def joue(self,event,niveau,mouse_xy,sortSelectionne):
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
        print("Tour de "+(niveau.tourDe.classe))
        niveau.finTour()

class PersonnageSansPM(Personnage):
    """@summary: Classe décrivant un personange pouvant faire des actions mais sans chercher à se déplacer (Stratège iop). hérite de Personnage"""
    def __init__(self, *args):
        """@summary: Initialise un personnage sans PM, même initialisation que Personange
        @args: les arguments donnés, doivent être les mêmes que Personnage
        @type:*args"""
        super(PersonnageSansPM, self).__init__(*args)
    def deepcopy(self):
        """@summary: Clone le PersonnageSansPM
        @return: le clone"""
        cp = PersonnageSansPM(self.classe, self.lvl, self.team, self.caracsPrimaires, self.caracsSecondaires, self.dommages, self.resistances ,self.icone)
        cp.sorts = Personnage.ChargerSorts(cp.classe, cp.lvl)
        return cp
    def joue(self,event,niveau,mouse_xy,sortSelectionne):
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
        self.sorts[0].lance(niveau.tourDe.posX,niveau.tourDe.posY, niveau, self.posX, self.posY)
        niveau.finTour()
# La liste des invocations disponibles.
INVOCS = {
"Cadran de Xélor" : PersonnageSansPM("Cadran de Xelor",100,1,{"Vitalite":1000},{},{},{},"cadran_de_xelor.png"),
"Cawotte" : PersonnageMur("Cawotte",0,1,{"Vitalite":800},{},{},{},"cawotte.png"),
"Synchro" : PersonnageMur("Synchro",0,1,{"Vitalite":1200},{},{},{},"synchro.png"),
"Complice" : PersonnageMur("Complice",0,1,{"Vitalite":650},{},{},{},"complice.png"),
"Balise de Rappel" : PersonnageSansPM("Balise de Rappel",0,1,{"Vitalite":1000},{},{},{},"balise_de_rappel.png"),
"Balise Tactique" : PersonnageMur("Balise Tactique",0,1,{"Vitalite":1000},{},{},{},"balise_tactique.png"),
"Stratège Iop" : PersonnageMur("Stratege Iop",0,1,{"Vitalite":1385},{},{},{},"conquete.png")
}
