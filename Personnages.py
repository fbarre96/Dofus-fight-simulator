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
from copy import deepcopy
import copy 
import uuid
class Personnage(object):
    """@summary: Classe décrivant un personnage joueur de dofus."""
    def __init__(self, nomPerso, classe, lvl,team,caracsPrimaires, caracsSecondaires,dommages, resistances,icone=""):
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
        self.cc = int(caracsPrimaires.get("Coups Critiques",0))
        self.sagesse = int(caracsPrimaires.get("Sagesse",0))    # Aucune utilité dans le simulateur de combat
        self.caracsPrimaires = caracsPrimaires

        self.retPA = int(caracsSecondaires.get("Retrait PA",0))
        self.esqPA = int(caracsSecondaires.get("Esquive PA",0))
        self.retPM = int(caracsSecondaires.get("Retrait PM",0))
        self.esqPM = int(caracsSecondaires.get("Esquive PM",0))
        self.soins = int(caracsSecondaires.get("Soins",0))      #TODO
        self.tacle = int(caracsSecondaires.get("Tacle",0))      
        self.fuite = int(caracsSecondaires.get("Fuite",0))      
        self.ini = int(caracsSecondaires.get("Initiative",0))    
        self.invocationLimite = int(caracsSecondaires.get("Invocation",1))    
        self.prospection = int(caracsSecondaires.get("Prospection",0))  # Aucune utilité dans le simulateur de combat
        self.caracsSecondaires = caracsSecondaires

        self.do = int(dommages.get("Dommages",0))
        self.doCri = int(dommages.get("Dommages critiques",0))
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
        self.reCc = int(resistances.get("Coups critiques",0)) 
        self.rePou = int(resistances.get("Poussee",0))                  
        self.reDist = int(resistances.get("Distance",0))                
        self.reMelee = int(resistances.get("Melee",0))                  
        self.resistances = resistances

        self._vie = self.vie
        self._PM = int(self.PM)
        self._PA = int(self.PA)
        self.nomPerso = nomPerso
        self.erosion = 10 # Erosion de base
        self.lvl = int(lvl)
        self.classe = classe
        self.uid = uuid.uuid4()
        self.sortsDebutCombat = []
        self.sorts, self.sortsDebutCombat = Personnage.ChargerSorts(self.classe,self.lvl) # la liste des sorts du personnage
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

        self.msgsPrevisu = []
        
        if not(icone.startswith("images/")):
            self.icone = ("images/"+icone)
        else:
            self.icone = (icone)
        self.icone=constantes.normaliser(self.icone)
        # Overlay affichange le nom de classe et sa vie restante
        self.overlay = Overlays.Overlay(self, Overlays.ColoredText("nomPerso",(210,105,30)), Overlays.ColoredText("overlayTexte",(224,238,238)),(56,56,56))
    
    def __deepcopy__(self,memo):
        toReturn = Personnage(self.nomPerso, self.classe,self.lvl,self.team,
                    {"PA":self.PA,"PM":self.PM,"PO":self.PO,"Vitalite":self.vie,"Agilite":self.agi,"Chance":self.cha,"Force":self.fo,"Intelligence":self.int,"Puissance":self.pui,"Coups Critiques":self.cc,"Sagesse":self.sagesse},
                    {"Retrait PA":self.retPA,"Esquive PA":self.esqPA, "Retrait PM":self.retPM,"Esquive PM":self.esqPM,"Soins":self.soins,"Tacle":self.tacle,"Fuite":self.fuite,"Initiative":self.ini,"Invocation":self.invocationLimite,"Prospection":self.prospection},
                    {"Dommages":self.do,"Dommages critiques":self.doCri,"Neutre":self.doNeutre,"Terre":self.doTerre,"Feu":self.doFeu,"Eau":self.doEau,"Air":self.doAir,"Renvoi":self.doRenvoi,"Maitrise d'arme":self.doMaitriseArme,"Pieges":self.doPieges,"Pieges Puissance":self.doPiegesPui,"Poussee":self.doPou,"Sorts":self.doSorts,"Armes":self.doArmes,"Distance":self.doDist,"Melee":self.doMelee},
                    {"Neutre":self.reNeutre,"Neutre%":self.rePerNeutre,"Terre":self.reTerre,"Terre%":self.rePerTerre,"Feu":self.reFeu,"Feu%":self.rePerFeu,"Eau":self.reEau,"Eau%":self.rePerEau,"Air":self.reAir,"Air%":self.rePerAir,"Coups critiques":self.reCc,"Poussee":self.rePou,"Distance":self.reDist,"Melee":self.reMelee},
                        self.icone)
        toReturn.sortsDebutCombat = self.sortsDebutCombat
        toReturn.posX = self.posX
        toReturn.posY = self.posY
        toReturn._PA = self._PA
        toReturn._PM = self._PM
        toReturn._vie = self._vie
        toReturn.uid = self.uid
        toReturn.sorts = deepcopy(self.sorts)
        toReturn.sortsDebutCombat = deepcopy(self.sortsDebutCombat)
        toReturn.etats = deepcopy(self.etats)
        toReturn.historiqueDeplacement = deepcopy(self.historiqueDeplacement)
        toReturn.posDebTour = self.posDebTour
        toReturn.posDebCombat = self.posDebCombat
        toReturn.invocateur = self.invocateur
        toReturn.invocations = deepcopy(self.invocations)
        toReturn.invocationLimite = self.invocationLimite
        toReturn.msgsPrevisu = deepcopy(self.msgsPrevisu)
        return toReturn

    def setOverlayText(self):
        self.overlayTexte = str(self.vie) +" PV"
        boubou = self.getBoucliers()
        if boubou > 0:
            self.overlayTexte += " "+str(boubou)+" PB"
    
    def setOverlayTextGenerique(self, text):
        self.overlayTexte = text


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
        sortsDebutCombat = []
        if(classe=="Stratege Iop"):
            sorts.append(Sort.Sort("Strategie_iop",0,0,0,0,[Effets.EffetEtat(Etats.EtatRedistribuerPer("Stratégie Iop",0,-1, 50,"Ennemis|Allies",2))],[],0,99,99,0,0,"cercle",False))
            return sorts,sortsDebutCombat
        elif(classe=="Cadran de Xelor"):
            sorts.append(Sort.Sort("Synchronisation",0,0,0,0,[Effets.EffetDegats(100,130,"feu",zone=Zones.TypeZoneCercleSansCentre(4), cibles_possibles="Ennemis|Lanceur",etat_requis_cibles="Telefrag"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Synchronisation",0,1,"PA",2),zone=Zones.TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Lanceur",etat_requis_cibles="Telefrag")],[],0,99,99,0,0,"cercle",False,chaine=False))
            return sorts,sortsDebutCombat
        elif(classe=="Balise de Rappel"):
            sorts.append(Sort.Sort("Rappel",0,0,0,0,[Effets.EffetEchangePlace(zone=Zones.TypeZoneInfini(),cibles_possibles="Cra"), Effets.EffetTue(zone=Zones.TypeZoneInfini(),cibles_possibles="Lanceur")],[],0,99,99,0,0,"cercle",False))
            return sorts,sortsDebutCombat
        elif classe == "Poutch":
            return sorts,sortsDebutCombat
        elif classe == "Synchro":
            # TODO FIX : La limite par tour se met meme si l'état TF était déjà fait et donc aucun nouveau boost a été rajouté
            activationFinDesTemps = Sort.Sort("Fin des temps",0,0,0,0,[Effets.EffetDegats(0,0,"air",zone=Zones.TypeZoneCercle(3),cibles_possibles="Ennemis"), Effets.EffetTue(cibles_possibles="Lanceur")],[],0, 99,99,0,0,"cercle",False, chaine=False)
            sortsDebutCombat.append(
                Sort.Sort("Synchronisation",0,0,0,0,[
                    Effets.EffetEtatSelf(Etats.EtatEffetSiTFGenere("Synchronisation",0,-1,[Effets.EffetEtatSelfTF(Etats.EtatBoostBaseDegLvlBased("toReplace",0,-1,"Fin des temps",190), "Rembobinage", cumulMax=1, etat_requis="!DejaBoost"),Effets.EffetEtatSelfTF(Etats.Etat("DejaBoost",0,1), "Rembobinage", remplaceNom=False, cumulMax=1)],"Téléfrageur","porteur","porteur")), 
                    Effets.EffetEtatSelf(Etats.EtatEffetSiTFGenere("Attente de la fin des temps",0,-1,Effets.EffetEntiteLanceSort("Synchro",activationFinDesTemps),"Téléfrageur","porteur","porteur",True,"Rembobinage"))],[],0,99,99,0,0,"cercle",False,description="""""", chaine=False)
            )
            return sorts,sortsDebutCombat
        elif(classe=="Xelor"):
            sortsDebutCombat.append(
                Sort.Sort("Téléfrageur",0,0,0,0,[Effets.EffetEtatSelf(Etats.EtatEffetSiTFGenere("Téléfrageur",0,-1,Effets.EffetEtatSelfTF(Etats.EtatBoostCaracFixe("toReplace",0,-1,"PA",2), "Rembobinage", cumulMax=1),"Téléfrageur","reelLanceur","reelLanceur"))],[],0,99,99,0,0,"cercle",False,description="""""", chaine=False),
            )
            sortsDebutCombat.append(
                Sort.Sort("Glas Boost",0,0,0,0,[Effets.EffetEtatSelf(Etats.EtatEffetSiTFGenere("Glas Boost",0,-1,Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Glas",0,-1,"Glas",4), cumulMax=10),"Glas","porteur","porteur"))],[],0,99,99,0,0,"cercle",False,description="""""", chaine=False),
            )
            sortsDebutCombat.append(
                Sort.Sort("Instabilité Temporelle Réactivation",0,0,0,0,[Effets.EffetEtatSelf(Etats.EtatEffetSiTFGenere("Instabilité Temporelle Réactivation",0,-1,Effets.EffetActiveGlyphe("Instabilité Temporelle"),"Instabilité Temporelle","reelLanceur","reelLanceur",False,"Activation Instabilité Temporelle"))],[],0,99,99,0,0,"cercle",False,description="""""", chaine=False),
            )


            retourParadoxe = Sort.Sort("Retour Paradoxe",0,0,0,0,[Effets.EffetTpSymCentre(zone=Zones.TypeZoneInfini(),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis_cibles="ParadoxeTemporel",consomme_etat=True)],[],0,99,99,0,0,"cercle",False)
            activationInstabiliteTemporelle = Sort.Sort("Activation Instabilité Temporelle",0,0,0,3,[Effets.EffetTeleportePosPrec(1)],[],0, 99,99,0,0,"cercle",False)
            sortieInstabiliteTemporelle = Sort.Sort("Instabilité Temporelle: Sortie",0,0,0,99,[Effets.EffetRetireEtat("Intaclable")],[],0, 99,99,0,0,"cercle",False)
            deplacementInstabiliteTemporelle = Sort.Sort("Instabilité Temporelle: Intaclabe",0,0,0,3,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Intaclable",0,1,"fuite",999999), etat_requis_cibles="!Intaclable")],[],0, 99,99,0,0,"cercle",False)
            activationParadoxeTemporel = Sort.Sort("Paradoxe Temporel", 0,0,0,0,[Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercle(4),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur|Xelor|Synchro"),Effets.EffetEtat(Etats.Etat("ParadoxeTemporel",0,2),zone=Zones.TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur|Xelor|Synchro"), Effets.EffetEtatSelf(Etats.EtatActiveSort("RetourParadoxe",1,1,retourParadoxe),cibles_possibles="Lanceur")],[],0,99,99,0,0,"cercle",False)
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
                Sort.Sort("Rouage",110,3,1,7,[Effets.EffetDegats(12,14,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Rouage",1,1,"PA",1))],[Effets.EffetDegats(15,17,"Eau"), Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Rouage",1,1,"PA",1))],5,2,99,0,1,"cercle",True,description="""Occasionne des dommages Eau.
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
                Sort.Sort("Retour Spontané",101,1,0,7,[Effets.EffetTeleportePosPrec(1)],[],0,3,99,0,1,"cercle",False,description="""La cible revient à sa position précédente.""", chaine=True)
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
                Sort.Sort("Rembobinage",6,2,0,2,[Effets.EffetEtat(Etats.EtatRetourCaseDepart("Bobine",0,1,"Rembobinage"),cibles_possibles="Allies|Lanceur")],[],0,1,1,3,0,"ligne",True,description="""À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour.""", chaine=True),
                Sort.Sort("Rembobinage",42,2,0,4,[Effets.EffetEtat(Etats.EtatRetourCaseDepart("Bobine",0,1,"Rembobinage"),cibles_possibles="Allies|Lanceur")],[],0,1,1,3,0,"ligne",True,description="""À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour.""", chaine=True),
                Sort.Sort("Rembobinage",74,2,0,6,[Effets.EffetEtat(Etats.EtatRetourCaseDepart("Bobine",0,1,"Rembobinage"),cibles_possibles="Allies|Lanceur")],[],0,1,1,3,0,"ligne",True,description="""À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Renvoi",120,3,1,6,[Effets.EffetTeleporteDebutTour()],[],0,1,1,2,0,"ligne",True,description="""Téléporte la cible ennemie à sa cellule de début de tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Frappe de Xelor",9,3,1,3,[Effets.EffetTpSymSelf(),Effets.EffetDegats(15,19,"Terre",cibles_possibles="Ennemis")],[Effets.EffetTpSymSelf(),Effets.EffetDegats(21,25,"Terre",cibles_possibles="Ennemis")],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Terre aux ennemis.
            Téléporte la cible symétriquement par rapport au lanceur du sort.""", chaine=False),

                Sort.Sort("Frappe de Xelor",47,3,1,3,[Effets.EffetTpSymSelf(),Effets.EffetDegats(19,23,"Terre",cibles_possibles="Ennemis")],[Effets.EffetTpSymSelf(),Effets.EffetDegats(25,29,"Terre",cibles_possibles="Ennemis")],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Terre aux ennemis.
            Téléporte la cible symétriquement par rapport au lanceur du sort.""", chaine=False),

                Sort.Sort("Frappe de Xelor",87,3,1,3,[Effets.EffetTpSymSelf(),Effets.EffetDegats(23,27,"Terre",cibles_possibles="Ennemis")],[Effets.EffetTpSymSelf(),Effets.EffetDegats(29,33,"Terre",cibles_possibles="Ennemis")],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Terre aux ennemis.
            Téléporte la cible symétriquement par rapport au lanceur du sort.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Engrenage",125,3,1,5,[Effets.EffetTpSymCentre(zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True),Effets.EffetDegats(31,35,"Terre",cibles_possibles="Ennemis",zone=Zones.TypeZoneLignePerpendiculaire(1),  faire_au_vide=True)],[Effets.EffetTpSymCentre(zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True),Effets.EffetDegats(34,38,"Terre",cibles_possibles="Ennemis",zone=Zones.TypeZoneLignePerpendiculaire(1), faire_au_vide=True)],25,2,99,0,0,"ligne",True,description="""Occasionne des dommages Terre et téléporte les cibles symétriquement par rapport au centre de la zone d'effet.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Complice",13,2,1,3,[Effets.EffetInvoque("Complice",False,cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles="Cadran de Xelor|Complice",zone=Zones.TypeZoneCercleSansCentre(99))],[],0,1,99,0,0,"cercle",True,description="""Invoque un Complice statique qui ne possède aucun sort.
            Il est tué si un autre Complice est invoqué.""", chaine=True),

                Sort.Sort("Complice",54,2,1,4,[Effets.EffetInvoque("Complice",False,cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles="Cadran de Xelor|Complice",zone=Zones.TypeZoneCercleSansCentre(99))],[],0,1,99,0,0,"cercle",True,description="""Invoque un Complice statique qui ne possède aucun sort.
            Il est tué si un autre Complice est invoqué.""", chaine=True),

                Sort.Sort("Complice",94,2,1,5,[Effets.EffetInvoque("Complice",False,cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles="Cadran de Xelor|Complice",zone=Zones.TypeZoneCercleSansCentre(99))],[],0,1,99,0,0,"cercle",True,description="""Invoque un Complice statique qui ne possède aucun sort.
            Il est tué si un autre Complice est invoqué.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Cadran de Xelor",130,3,1,5,[Effets.EffetInvoque("Cadran de Xelor",False,cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles="Cadran de Xelor|Complice",zone=Zones.TypeZoneCercleSansCentre(99))],[],0,1,1,3,0,"cercle",True,description="""Invoque un Cadran qui occasionne des dommages Feu en zone et retire des PA aux ennemis dans l'état Téléfrag.
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
                Sort.Sort("Sablier de Xelor",22,2,1,6,[Effets.EffetDegats(9,11,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(9,11,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],[Effets.EffetDegats(13,15,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(13,15,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],5,3,1,0,1,"ligne",False,description="""Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue.
            Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

                Sort.Sort("Sablier de Xelor",65,2,1,6,[Effets.EffetDegats(12,14,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(12,14,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],[Effets.EffetDegats(16,18,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(16,15,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],5,3,1,0,1,"ligne",False,description="""Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue.
            Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

                Sort.Sort("Sablier de Xelor",108,2,1,7,[Effets.EffetDegats(15,17,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(15,17,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],[Effets.EffetDegats(19,21,"Feu"),Effets.EffetRetPA(2),Effets.EffetDegats(19,21,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],5,3,1,0,1,"ligne",False,description="""Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue.
            Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True)
            ]))

            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Distorsion Temporelle",140,4,0,0,[Effets.EffetDegats(34,38,"Air",zone=Zones.TypeZoneCarre(1),cibles_possibles="Ennemis"),Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneCarre(1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur")],[Effets.EffetDegats(38,42,"Air",cibles_possibles="Ennemis", zone=Zones.TypeZoneCarre(1)),Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneCarre(1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur")],15,2,99,0,0,"cercle",False,description="""Occasionne des dommages Air aux ennemis.
            Téléporte les cibles à leur position précédente.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Vol du Temps",27,4,1,5,[Effets.EffetDegats(20,24,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",1,1,"PA",1))],[Effets.EffetDegats(25,29,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",1,1,"PA",1))],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Eau à la cible.
            Le lanceur gagne 1 PA au début de son prochain tour.""", chaine=True),

                Sort.Sort("Vol du Temps",72,4,1,5,[Effets.EffetDegats(25,29,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",1,1,"PA",1))],[Effets.EffetDegats(30,34,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",1,1,"PA",1))],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Eau à la cible.
            Le lanceur gagne 1 PA au début de son prochain tour.""", chaine=True),

                Sort.Sort("Vol du Temps",118,4,1,5,[Effets.EffetDegats(30,34,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",1,1,"PA",1))],[Effets.EffetDegats(35,39,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Vol du Temps",1,1,"PA",1))],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Eau à la cible.
            Le lanceur gagne 1 PA au début de son prochain tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Pétrification",145,5,1,7,[Effets.EffetDegats(34,38,"Eau"),Effets.EffetEtatSelf(Etats.EtatCoutPA("Pétrification",0,2,"Pétrification",-1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag"), Effets.EffetRetPA(2)],[Effets.EffetDegats(38,42,"Eau"), Effets.EffetEtatSelf(Etats.EtatCoutPA("Pétrification",0,2,"Pétrification",-1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag"), Effets.EffetRetPA(2)],25,3,2,0,1,"ligne",True,description="""Occasionne des dommages Eau et retire des PA.
            Si la cible est dans l'état Téléfrag, le coût en PA du sort est réduit pendant 2 tours.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flou",32,2,1,1,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",0,1,"PA",-2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True,cibles_exclues="Lanceur"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",1,1,"PA",2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)],[],0,1,1,5,0,"cercle",False,description="""Retire des PA en zone le tour en cours.
            Augmente les PA en zone le tour suivant.""", chaine=True),

                Sort.Sort("Flou",81,2,1,2,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",0,1,"PA",-2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True,cibles_exclues="Lanceur"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",1,1,"PA",2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)],[],0,1,1,4,0,"cercle",True,description="""Retire des PA en zone le tour en cours.
            Augmente les PA en zone le tour suivant.""", chaine=True),

                Sort.Sort("Flou",124,2,1,3,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",0,1,"PA",-2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True,cibles_exclues="Lanceur"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flou",1,1,"PA",2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)],[],0,1,1,3,0,"cercle",True,description="""Retire des PA en zone le tour en cours.
            Augmente les PA en zone le tour suivant.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Conservation",150,2,0,5,[Effets.EffetEtat(Etats.EtatModDegPer("Conservation",0,1,130),zone=Zones.TypeZoneCercle(2),faire_au_vide=True,cibles_possibles="Allies|Lanceur"),Effets.EffetEtat(Etats.EtatModDegPer("Conservation",1,1,70),zone=Zones.TypeZoneCercle(2),faire_au_vide=True,cibles_possibles="Allies|Lanceur")],[],0,1,1,2,0,"cercle",True,description="""Augmente les dommages subis par les alliés en zone de 30% pour le tour en cours.
            Au tour suivant, les cibles réduisent les dommages subis de 30%.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Poussière Temporelle",38,4,0,4,[Effets.EffetDegats(22,25,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(22,25,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],[Effets.EffetDegats(26,29,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(26,29,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],25,2,99,0,1,"cercle",True,description="""Occasionne des dommages Feu.
            Les entités dans l'état Téléfrag dans la zone d'effet subissent également des dommages Feu et sont téléportées symétriquement par rapport à la cellule ciblée.""", chaine=True),

                Sort.Sort("Poussière Temporelle",90,4,0,5,[Effets.EffetDegats(28,31,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(28,31,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],[Effets.EffetDegats(32,35,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(32,35,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],25,2,99,0,1,"cercle",True,description="""Occasionne des dommages Feu.
            Les entités dans l'état Téléfrag dans la zone d'effet subissent également des dommages Feu et sont téléportées symétriquement par rapport à la cellule ciblée.""", chaine=True),

                Sort.Sort("Poussière Temporelle",132,4,0,6,[Effets.EffetDegats(34,37,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(34,37,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],[Effets.EffetDegats(38,41,"Feu",cibles_possibles="Ennemis",zone=Zones.TypeZoneCercle(3)),Effets.EffetDegats(38,41,"Feu",zone=Zones.TypeZoneCercle(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")],25,2,99,0,1,"cercle",True,description="""Occasionne des dommages Feu.
            Les entités dans l'état Téléfrag dans la zone d'effet subissent également des dommages Feu et sont téléportées symétriquement par rapport à la cellule ciblée.""", chaine=True)
            ]))

            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Suspension Temporelle",155,3,1,6,[Effets.EffetRafraichirEtats(1,etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(25,29,"Feu")],[Effets.EffetRafraichirEtats(1,etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(29,33,"Feu")],15,3,2,0,1,"ligne",True,description="""Occasionne des dommages Feu sur les ennemis.
            Réduit la durée des effets sur les cibles ennemies dans l'état Téléfrag et retire l'état.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Raulebaque",44,2,0,0,[Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneInfini())],[],0,1,1,4,0,"cercle",False,description="""Replace tous les personnages à leurs positions précédentes.""", chaine=True),

                Sort.Sort("Raulebaque",97,2,0,0,[Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneInfini())],[],0,1,1,3,0,"cercle",False,description="""Replace tous les personnages à leurs positions précédentes.""", chaine=True),

                Sort.Sort("Raulebaque",137,2,0,0,[Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneInfini())],[],0,1,1,2,0,"cercle",False,description="""Replace tous les personnages à leurs positions précédentes.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Instabilité Temporelle",160,3,0,7,[Effets.EffetGlyphe(activationInstabiliteTemporelle,deplacementInstabiliteTemporelle,sortieInstabiliteTemporelle, 2,"Instabilité Temporelle",(255,255,0),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)],[],0,1,1,3,1,"cercle",False,description="""Pose un glyphe qui renvoie les entités à leur position précédente.
            Les entités dans le glyphe sont dans l'état Intaclable.
            Les effets du glyphe sont également exécutés lorsque le lanceur génère un Téléfrag.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Démotivation",50,3,1,3,[Effets.EffetRafraichirEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(17,20,"Terre",cibles_possibles="Ennemis")],[Effets.EffetRafraichirEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(22,25,"Terre",cibles_possibles="Ennemis")],25,3,2,0,0,"diagonale",True,description="""Occasionne des dommages Terre aux ennemis en diagonale.
            Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état.""", chaine=True),

                Sort.Sort("Démotivation",103,3,1,4,[Effets.EffetRafraichirEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(20,23,"Terre",cibles_possibles="Ennemis")],[Effets.EffetRafraichirEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(25,28,"Terre",cibles_possibles="Ennemis")],25,3,2,0,0,"diagonale",True,description="""Occasionne des dommages Terre aux ennemis en diagonale.
            Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état.""", chaine=True),

                Sort.Sort("Démotivation",143,3,1,5,[Effets.EffetRafraichirEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(23,26,"Terre",cibles_possibles="Ennemis")],[Effets.EffetRafraichirEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(28,31,"Terre",cibles_possibles="Ennemis")],25,3,2,0,0,"diagonale",True,description="""Occasionne des dommages Terre aux ennemis en diagonale.
            Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Pendule",165,4,1,5,[Effets.EffetTpSym(),Effets.EffetDegats(38,42,"Air",zone=Zones.TypeZoneCercle(2),cibles_possibles="Ennemis"),Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneInfini(),cibles_possibles="Lanceur")],[Effets.EffetTpSym(),Effets.EffetDegats(46,50,"Air",zone=Zones.TypeZoneCercle(2),cibles_possibles="Ennemis"),Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneInfini(),cibles_possibles="Lanceur")],5,2,1,0,0,"cercle",True,description="""Le lanceur se téléporte symétriquement par rapport à la cible et occasionne des dommages Air en zone sur sa cellule de destination.
            Il revient ensuite à sa position précédente.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Paradoxe Temporel",56,3,0,0,[Effets.EffetEntiteLanceSort("Complice|Cadran de Xelor",activationParadoxeTemporel)],[],0,1,1,4,0,"cercle",False,description="""Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran).
            Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles.
            Fixe le temps de relance de Cadran de Xelor et de Complice à 1.""", chaine=True),

                Sort.Sort("Paradoxe Temporel",112,3,0,0,[Effets.EffetEntiteLanceSort("Complice|Cadran de Xelor",activationParadoxeTemporel)],[],0,1,1,3,0,"cercle",False,description="""Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran).
            Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles.
            Fixe le temps de relance de Cadran de Xelor et de Complice à 1.""", chaine=True),

                Sort.Sort("Paradoxe Temporel",147,3,0,0,[Effets.EffetEntiteLanceSort("Complice|Cadran de Xelor",activationParadoxeTemporel)],[],0,1,1,2,0,"cercle",False,description="""Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran).
            Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles.
            Fixe le temps de relance de Cadran de Xelor et de Complice à 1.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Faille Temporelle",170,3,0,0,[Effets.EffetEchangePlace(zone=Zones.TypeZoneInfini(),cibles_possibles="Cadran de Xelor|Complice",generer_TF=True),Effets.EffetEtat(Etats.EtatEffetFinTour("Retour faille temporelle", 0,1,Effets.EffetTeleportePosPrec(1),"Fin faille Temporelle","cible")), Effets.EffetEtat(Etats.Etat("Faille_temporelle",0,1),zone=Zones.TypeZoneInfini(),cibles_possibles="Xelor")],[],0,1,1,2,0,"cercle",False,description="""Le lanceur échange sa position avec celle du Complice (ou du Cadran).
            À la fin du tour, le Complice (ou le Cadran) revient à sa position précédente.
            La Synchro ne peut pas être déclenchée pendant la durée de Faille Temporelle.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Synchro",62,2,1,2,[Effets.EffetTue(zone=Zones.TypeZoneInfini(),cibles_possibles="Synchro"),Effets.EffetInvoque("Synchro",False,cibles_possibles="",faire_au_vide=True),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Synchro",1,-1,"PA",-1))],[],0,1,1,3,0,"cercle",False,description="""Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour.
            La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag.
            Elle n'est pas affectée par les effets de Rembobinage.
            À partir du tour suivant son lancer, son invocateur perd 1 PA.""", chaine=False),

                Sort.Sort("Synchro",116,2,1,3,[Effets.EffetTue(zone=Zones.TypeZoneInfini(),cibles_possibles="Synchro"),Effets.EffetInvoque("Synchro",False,cibles_possibles="",faire_au_vide=True),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Synchro",1,-1,"PA",-1))],[],0,1,1,3,0,"cercle",False,description="""Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour.
            La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag.
            Elle n'est pas affectée par les effets de Rembobinage.
            À partir du tour suivant son lancer, son invocateur perd 1 PA.""", chaine=False),

                Sort.Sort("Synchro",153,2,1,4,[Effets.EffetTue(zone=Zones.TypeZoneInfini(),cibles_possibles="Synchro"),Effets.EffetInvoque("Synchro",False,cibles_possibles="",faire_au_vide=True),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Synchro",1,-1,"PA",-1))],[],0,1,1,3,0,"cercle",False,description="""Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour.
            La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag.
            Elle n'est pas affectée par les effets de Rembobinage.
            À partir du tour suivant son lancer, son invocateur perd 1 PA.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Désynchronisation",175,2,1,6,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationDesynchro,"Désynchronisation",(255,0,255),faire_au_vide=True)],[],0,2,99,0,1,"cercle",False,description="""Pose un piège qui téléporte symétriquement les entités proches.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Contre",69,2,0,2,[Effets.EffetEtat(Etats.EtatContre("Contre",0,2, 30,1),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur", faire_au_vide=True)],[],0,1,1,5,0,"cercle",True,description="""Renvoie une partie des dommages subis en mêlée à l'attaquant.""", chaine=True),
                Sort.Sort("Contre",122,2,0,4,[Effets.EffetEtat(Etats.EtatContre("Contre",0,2, 40,1),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur", faire_au_vide=True)],[],0,1,1,5,0,"cercle",True,description="""Renvoie une partie des dommages subis en mêlée à l'attaquant.""", chaine=True),
                Sort.Sort("Contre",162,2,0,6,[Effets.EffetEtat(Etats.EtatContre("Contre",0,2, 50,1),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur", faire_au_vide=True)],[],0,1,1,5,0,"cercle",True,description="""Renvoie une partie des dommages subis en mêlée à l'attaquant.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Bouclier Temporel",180,3,0,3,[Effets.EffetEtat(Etats.EtatEffetSiSubit("Bouclier temporel",0,1, Effets.EffetTeleportePosPrec(1),"Bouclier Temporel","lanceur","attaquant",""))],[],0,1,1,3,0,"cercle",True,description="""Si la cible subit des dommages, son attaquant et elle reviennent à leur position précédente.""", chaine=True)
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
                Sort.Sort("Horloge",84,5,1,4,[Effets.EffetVolDeVie(28,31,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",1,1,"PA",1)),Effets.EffetRetPA(2,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetVolDeVie(32,35,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",1,1,"PA",1)),Effets.EffetRetPA(2,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],25,3,2,0,0,"ligne",True,description="""Vole de vie dans l'élément Eau.
            Le lanceur gagne 1 PA au début de son prochain tour.
            Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

                Sort.Sort("Horloge",134,5,1,5,[Effets.EffetVolDeVie(32,35,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",1,1,"PA",1)),Effets.EffetRetPA(3,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetVolDeVie(36,39,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",1,1,"PA",1)),Effets.EffetRetPA(3,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],25,3,2,0,0,"ligne",True,description="""Vole de vie dans l'élément Eau.
            Le lanceur gagne 1 PA au début de son prochain tour.
            Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

                Sort.Sort("Horloge",178,5,1,6,[Effets.EffetVolDeVie(36,39,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",1,1,"PA",1)),Effets.EffetRetPA(4,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetVolDeVie(40,43,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Horloge",1,1,"PA",1)),Effets.EffetRetPA(4,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)],25,3,2,0,0,"ligne",True,description="""Vole de vie dans l'élément Eau.
            Le lanceur gagne 1 PA au début de son prochain tour.
            Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état.
            Le retrait de PA ne peut pas être désenvoûté.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Clepsydre",190,4,1,3,[Effets.EffetDegats(30,34,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Clepsydre",1,1,"PA",2),etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetDegats(36,40,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Clepsydre",1,1,"PA",2),etat_requis="Telefrag",consomme_etat=True)],15,2,99,0,0,"cercle",True,description="""Occasionne des dommages Eau.
            Si la cible est dans l'état Téléfrag, le lanceur gagne 2 PA au prochain tour.
            Retire l'état Téléfrag.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Rayon Obscur",92,5,1,4,[Effets.EffetDegats(27,31,"Terre",etat_requis="!Telefrag"), Effets.EffetDegats(54,62,"Terre",etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetDegats(34,38,"Terre",etat_requis="!Telefrag"),Effets.EffetDegats(68,76,"Terre",etat_requis="Telefrag",consomme_etat=True)],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Terre en ligne.
            Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag.
            Retire l'état Téléfrag.""", chaine=False),

                Sort.Sort("Rayon Obscur",141,5,1,5,[Effets.EffetDegats(30,34,"Terre",etat_requis="!Telefrag"), Effets.EffetDegats(60,68,"Terre",etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetDegats(37,41,"Terre",etat_requis="!Telefrag"),Effets.EffetDegats(74,82,"Terre",etat_requis="Telefrag",consomme_etat=True)],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Terre en ligne.
            Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag.
            Retire l'état Téléfrag.""", chaine=False),

                Sort.Sort("Rayon Obscur",187,5,1,6,[Effets.EffetDegats(33,37,"Terre",etat_requis="!Telefrag"), Effets.EffetDegats(66,74,"Terre",etat_requis="Telefrag",consomme_etat=True)],[Effets.EffetDegats(40,44,"Terre",etat_requis="!Telefrag"),Effets.EffetDegats(80,88,"Terre",etat_requis="Telefrag",consomme_etat=True)],5,3,2,0,0,"ligne",True,description="""Occasionne des dommages Terre en ligne.
            Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag.
            Retire l'état Téléfrag.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Rayon Ténébreux",195,3,1,5,[Effets.EffetDegats(19,23,"Terre"),Effets.EffetDegats(19,23,"terre",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],[Effets.EffetDegats(23,27,"Terre"),Effets.EffetDegats(23,37,"terre",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")],5,3,2,0,1,"cercle",True,description="""Occasionne des dommages Terre.
            Si la cible est dans l'état Téléfrag, occasionne des dommages Terre en zone aux ennemis autour d'elle.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Momification",100,2,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Momification",0,1,"PM",2)),Effets.EffetEtat(Etats.EtatTelefrag("Telefrag",0,1,"Momification"),zone=Zones.TypeZoneInfini())],[],0,1,1,5,0,"cercle",False,description="""Gagne 2 PM et fixe l'état Téléfrag à tous les alliés et ennemis.""", chaine=True),

                Sort.Sort("Momification",147,2,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Momification",0,1,"PM",2)),Effets.EffetEtat(Etats.EtatTelefrag("Telefrag",0,1,"Momification"),zone=Zones.TypeZoneInfini())],[],0,1,1,4,0,"cercle",False,description="""Gagne 2 PM et fixe l'état Téléfrag à tous les alliés et ennemis.""", chaine=True),

                Sort.Sort("Momification",197,2,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Momification",0,1,"PM",2)),Effets.EffetEtat(Etats.EtatTelefrag("Telefrag",0,1,"Momification"),zone=Zones.TypeZoneInfini())],[],0,1,1,3,0,"cercle",False,description="""Gagne 2 PM et fixe l'état Téléfrag à tous les alliés et ennemis.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Glas",200,3,0,3,[Effets.EffetDegats(4,4,"Air",zone=Zones.TypeZoneCarre(1)),Effets.EffetDegats(4,4,"Eau",zone=Zones.TypeZoneCarre(1)),Effets.EffetDegats(4,4,"Terre",zone=Zones.TypeZoneCarre(1)),Effets.EffetDegats(4,4,"Feu",zone=Zones.TypeZoneCarre(1)),Effets.EffetRetireEtat("Glas",zone=Zones.TypeZoneInfini(),cibles_possibles="Lanceur")],[],0,1,1,2,0,"ligne",True,description="""Occasionne des dommages Air, Eau, Terre, Feu.
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
                Sort.Sort("Conquête",105,3,1,6,[Effets.EffetInvoque("Stratege Iop",True,cible_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatRedistribuerPer("Strategie iop",0,-1, 50,"Ennemis|Allies",2))],[],0,1,1,3,0,"cercle",True,description="""Invoque un épouvantail qui redistribue à proximité (2 cases) 50% des dommages de sort qu'il subit.""", chaine=True)
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
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Duel",38,3,1,1,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Duel: Invulnérabilité à distance",0,1,"reDist",999999), cible_possible="Ennemis"), Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Duel: Invulnérabilité à distance",0,1,"reDist",999999), cible_possible="Ennemis"), Effets.EffetEtat(Etats.Etat("Pesanteur",0,1), cible_possible="Ennemis"), Effets.EffetEtatSelf(Etats.Etat("Pesanteur",0,2), cible_possible="Ennemis"), Effets.EffetEtat(Etats.EtatBoostCaracFixe("Duel: Immobilisation",0,1,"PM",-100), cible_possible="Ennemis"), Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Duel: Immobilisation",0,2,"PM",-100), cible_possible="Ennemis")],[],0,1,1,6,0,"cercle",False,description="""Retire leurs PM à la cible et au lanceur, leur applique l'état Pesanteur et les rend invuln�rable aux dommages � distance.
            Ne fonctionne que si lancé sur un ennemi.""", chaine=True),

                Sort.Sort("Duel",90,3,1,1,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Duel: Invulnérabilité à distance",0,1,"reDist",999999), cible_possible="Ennemis"), Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Duel: Invulnérabilité à distance",0,1,"reDist",999999), cible_possible="Ennemis"), Effets.EffetEtat(Etats.Etat("Pesanteur",0,1), cible_possible="Ennemis"), Effets.EffetEtatSelf(Etats.Etat("Pesanteur",0,2), cible_possible="Ennemis"), Effets.EffetEtat(Etats.EtatBoostCaracFixe("Duel: Immobilisation",0,1,"PM",-100), cible_possible="Ennemis"), Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Duel: Immobilisation",0,2,"PM",-100), cible_possible="Ennemis")],[],0,1,1,5,0,"cercle",False,description="""Retire leurs PM à la cible et au lanceur, leur applique l'état Pesanteur et les rend invuln�rable aux dommages � distance.
            Ne fonctionne que si lancé sur un ennemi.""", chaine=True),

                Sort.Sort("Duel",132,3,1,1,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Duel: Invulnérabilité à distance",0,1,"reDist",999999), cible_possible="Ennemis"), Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Duel: Invulnérabilité à distance",0,1,"reDist",999999), cible_possible="Ennemis"), Effets.EffetEtat(Etats.Etat("Pesanteur",0,1), cible_possible="Ennemis"), Effets.EffetEtatSelf(Etats.Etat("Pesanteur",0,2), cible_possible="Ennemis"), Effets.EffetEtat(Etats.EtatBoostCaracFixe("Duel: Immobilisation",0,1,"PM",-100), cible_possible="Ennemis"), Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Duel: Immobilisation",0,2,"PM",-100), cible_possible="Ennemis")],[],0,1,1,4,0,"cercle",False,description="""Retire leurs PM à la cible et au lanceur, leur applique l'état Pesanteur et les rend invuln�rable aux dommages � distance.
            Ne fonctionne que si lancé sur un ennemi.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Emprise",155,3,1,1,[Effets.EffetEtat(Etats.EtatModDegPer("Emprise: Invulnérable",0,1, 0)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Emprise",0,1,"PM",-100))],[],0,1,1,4,0,"cercle",False,description="""Retire tous les PM de l'ennemi cible mais le rend invulnérable.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Épée du Jugement",44,4,1,4,[Effets.EffetDegats(13,15,"Air"),Effets.EffetDegats(13,15,"Feu")],[Effets.EffetDegats(17,19,"Air"),Effets.EffetDegats(17,19,"Feu")],5,2,1,0,0,"cercle",False,description="""Occasionne des dommages Air et Feu sans ligne de vue.""", chaine=True),

                Sort.Sort("Épée du Jugement",97,4,1,4,[Effets.EffetDegats(16,18,"Air"),Effets.EffetDegats(16,18,"Feu")],[Effets.EffetDegats(20,22,"Air"),Effets.EffetDegats(20,22,"Feu")],5,2,1,0,0,"cercle",False,description="""Occasionne des dommages Air et Feu sans ligne de vue.""", chaine=True),

                Sort.Sort("Épée du Jugement",137,4,1,5,[Effets.EffetDegats(19,21,"Air"),Effets.EffetDegats(19,21,"Feu")],[Effets.EffetDegats(23,25,"Air"),Effets.EffetDegats(23,25,"Feu")],5,3,2,0,0,"cercle",False,description="""Occasionne des dommages Air et Feu sans ligne de vue.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Condamnation",160,3,1,6,[
                    Effets.EffetDegats(41,45,"feu",zone=Zones.TypeZoneCercleSansCentre(99),etat_requis_cibles="Condamnation 2",consomme_etat=True),
                    Effets.EffetEtat(Etats.Etat("Condamnation 2",0,-1),etat_requis_cibles="Condamnation 1",consomme_etat=True),
                    Effets.EffetDegats(25,29,"feu",zone=Zones.TypeZoneCercleSansCentre(99),etat_requis_cibles="Condamnation 1",consomme_etat=True),
                    Effets.EffetEtat(Etats.Etat("Condamnation 1",0,-1),etat_requis_cibles="!Condamnation 2"),
                    Effets.EffetDegats(25,29,"air")
            ],[],0,3,2,0,0,"cercle",True,description="""Occasionne des dommages Air.
            Occasionne des dommages Feu sur la cible initiale lorsque le sort est lanc� sur une autre cible.
            Les dommages Feu sont augment�s si le sort est utilis� une deuxi�me fois sur la cible initiale.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Puissance",50,3,0,2,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Puissance",0,2,"pui",100))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Puissance",0,2,"pui",120))],15,1,1,3,0,"cercle",True,description="""Augmente la Puissance de la cible.""", chaine=True),

                Sort.Sort("Puissance",103,3,0,4,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Puissance",0,2,"pui",200))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Puissance",0,2,"pui",240))],15,1,1,3,0,"cercle",True,description="""Augmente la Puissance de la cible.""", chaine=True),

                Sort.Sort("Puissance",143,3,0,6,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Puissance",0,2,"pui",300))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Puissance",0,2,"pui",350))],15,1,1,3,0,"cercle",True,description="""Augmente la Puissance de la cible.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Vertu",165,3,0,0,[Effets.EffetEtat(Etats.EtatBouclierPerLvl("Vertu : bouclier",0,2,500),zone=Zones.TypeZoneCroix(1)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Vertu: malus puissance",0,2,"pui",-150))],[],0,1,1,3,0,"cercle",False,description="""Applique un bouclier zone mais réduit la Puissance du lanceur.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Précipitation",56,2,0,2,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Précipité",0,1,"PA",5)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Sortie de précipitation",1,1,"PA",-3))],[],0,1,1,4,0,"cercle",True,description="""Augmente les PA de la cible pour le tour en cours mais lui retire des PA le tour suivant.
            Interdit l'utilisation des armes et du sort Colère de Iop.""", chaine=True),

                Sort.Sort("Précipitation",112,2,0,4,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Précipité",0,1,"PA",5)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Sortie de précipitation",1,1,"PA",-3))],[],0,1,1,3,0,"cercle",True,description="""Augmente les PA de la cible pour le tour en cours mais lui retire des PA le tour suivant.
            Interdit l'utilisation des armes et du sort Colère de Iop.""", chaine=True),

                Sort.Sort("Précipitation",147,2,0,6,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Précipité",0,1,"PA",5)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Sortie de précipitation",1,1,"PA",-3))],[],0,1,1,2,0,"cercle",True,description="""Augmente les PA de la cible pour le tour en cours mais lui retire des PA le tour suivant.
            Interdit l'utilisation des armes et du sort Colère de Iop.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Agitation",170,2,0,5,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Agitation",0,1,"PM",2)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Intaclable",0,1,"fuite",999999))],[],0,1,1,2,0,"cercle",True,description="""Augmente les PM et rend Intaclable pour le tour en cours.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Tempête de Puissance",62,3,3,4,[Effets.EffetDegats(24,28,"Feu")],[Effets.EffetDegats(29,33,"Feu")],5,3,2,0,0,"cercle",True,description="""Occasionne des dommages Feu.""", chaine=True),

                Sort.Sort("Tempête de Puissance",116,3,3,4,[Effets.EffetDegats(29,33,"Feu")],[Effets.EffetDegats(34,38,"Feu")],5,3,2,0,0,"cercle",True,description="""Occasionne des dommages Feu.""", chaine=True),

                Sort.Sort("Tempête de Puissance",153,3,3,5,[Effets.EffetDegats(34,38,"Feu")],[Effets.EffetDegats(41,45,"Feu")],5,3,2,0,0,"cercle",True,description="""Occasionne des dommages Feu.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Tumulte",175,4,2,5,[Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Tumulte",0,1,"Tumulte",30), zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis"),Effets.EffetDegats(19,21,"Feu",zone=Zones.TypeZoneCroix(1))],[Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Tumulte",0,1,"Tumulte",30), zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis"),Effets.EffetDegats(23,25,"Feu",zone=Zones.TypeZoneCroix(1))],5,1,1,1,0,"cercle",True,description="""Occasionne des dommages Feu en zone.
                Plus le nombre de cibles ennemies est important, plus les dommages sont importants.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
	            Sort.Sort("Épée Céleste",69,4,0,3,[Effets.EffetDegats(28,32,"Air",zone=Zones.TypeZoneCercle(2))],[Effets.EffetDegats(34,38,"Air",zone=Zones.TypeZoneCercle(2))],15,2,99,0,0,"ligne",True,description="""Occasionne des dommages Air en zone.""", chaine=True),

                Sort.Sort("Épée Céleste",122,4,0,3,[Effets.EffetDegats(32,36,"Air",zone=Zones.TypeZoneCercle(2))],[Effets.EffetDegats(38,42,"Air",zone=Zones.TypeZoneCercle(2))],15,2,99,0,0,"ligne",True,description="""Occasionne des dommages Air en zone.""", chaine=True),

                Sort.Sort("Épée Céleste",162,4,0,4,[Effets.EffetDegats(36,40,"Air",zone=Zones.TypeZoneCercle(2))],[Effets.EffetDegats(42,46,"Air",zone=Zones.TypeZoneCercle(2))],15,2,99,0,0,"ligne",True,description="""Occasionne des dommages Air en zone.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Zénith",180,5,1,3,[Effets.EffetDegatsSelonPMUtilises(86,94,"Air",zone=Zones.TypeZoneLigne(4), faire_au_vide=True)],[Effets.EffetDegatsSelonPMUtilises(104,112,"Air",zone=Zones.TypeZoneLigne(4), faire_au_vide=True)],5,1,99,0,0,"ligne",True,description="""Occasionne des dommages Air en zone.
            Moins le lanceur a utilisé de PM pendant son tour de jeu, plus les dommages occasionnés sont importants.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Vitalité",77,3,0,2,[Effets.EffetEtat(Etats.EtatBoostCaracPer("Vitalite",0,4,"vie",16))],[Effets.EffetEtat(Etats.EtatBoostCaracPer("Vitalite",0,4,"vie",18))],25,1,1,2,0,"cercle",True,description="""Augmente temporairement la Vitalité de la cible en pourcentage.
            Le bonus de Vitalité est divisé par 2 sur les cibles autres que le lanceur.""", chaine=True),

                Sort.Sort("Vitalité",128,3,0,4,[Effets.EffetEtat(Etats.EtatBoostCaracPer("Vitalite",0,4,"vie",18))],[Effets.EffetEtat(Etats.EtatBoostCaracPer("Vitalite",0,4,"vie",20))],25,1,1,2,0,"cercle",True,description="""Augmente temporairement la Vitalité de la cible en pourcentage.
            Le bonus de Vitalité est divisé par 2 sur les cibles autres que le lanceur.""", chaine=True),

                Sort.Sort("Vitalité",172,3,0,6,[Effets.EffetEtat(Etats.EtatBoostCaracPer("Vitalite",0,4,"vie",20))],[Effets.EffetEtat(Etats.EtatBoostCaracPer("Vitalite",0,4,"vie",22))],25,1,1,2,0,"cercle",True,description="""Augmente temporairement la Vitalité de la cible en pourcentage.
            Le bonus de Vitalité est divisé par 2 sur les cibles autres que le lanceur.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Endurance",185,3,1,1,[Effets.EffetDegats(34,38,"Eau"),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Endurance",0,1,150))],[Effets.EffetDegats(39,43,"Eau"),Effets.EffetEtatSelf(Etats.EtatBouclierPerLvl("Endurance",0,1,150))],15,3,2,0,0,"cercle",False,description="""Occasionne des dommages Eau.
            Applique des points de bouclier au lanceur.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Épée de Iop",84,4,1,5,[Effets.EffetDegats(27,31,"Terre",zone=Zones.TypeZoneCroix(3),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",faire_au_vide=True)],[Effets.EffetDegats(32,36,"Terre",zone=Zones.TypeZoneCroix(3),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",faire_au_vide=True)],15,2,99,0,0,"ligne",True,description="""Occasionne des dommages Terre en croix.""", chaine=True),

                Sort.Sort("Épée de Iop",134,4,1,5,[Effets.EffetDegats(32,36,"Terre",zone=Zones.TypeZoneCroix(3),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",faire_au_vide=True)],[Effets.EffetDegats(37,41,"Terre",zone=Zones.TypeZoneCroix(3),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",faire_au_vide=True)],15,2,99,0,0,"ligne",True,description="""Occasionne des dommages Terre en croix.""", chaine=True),

                Sort.Sort("Épée de Iop",178,4,1,6,[Effets.EffetDegats(37,41,"Terre",zone=Zones.TypeZoneCroix(3),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",faire_au_vide=True)],[Effets.EffetDegats(42,46,"Terre",zone=Zones.TypeZoneCroix(3),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",faire_au_vide=True)],15,2,99,0,0,"ligne",True,description="""Occasionne des dommages Terre en croix.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Pugilat",190,2,1,6,[Effets.EffetDegats(9,11,"Terre",zone=Zones.TypeZoneCercle(2),cibles_exclues="Lanceur"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Pugilat",0,1,"Pugilat",15))],[Effets.EffetDegats(11,13,"Terre",cibles_exclues="Lanceur",zone=Zones.TypeZoneCercle(2)), Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Pugilat",0,1,"Pugilat",18))],5,4,1,0,0,"cercle",True,description="""Occasionne des dommages Terre en zone.
            Les dommages sont augmentés pendant 1 tour après chaque lancer.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Épée du destin",92,4,1,1,[Effets.EffetDegats(28,32,"Feu"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Épée du destin", 2,1,"Épée du destin",30))],[Effets.EffetDegats(33,37,"Feu"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Épée du destin", 2,1,"Épée du destin",35))],25,1,1,2,0,"ligne",True,description="""Occasionne des dommages Feu.
            Les dommages sont augmentés à partir du second lancer.""", chaine=True),

                Sort.Sort("Épée du destin",141,4,1,1,[Effets.EffetDegats(33,37,"Feu"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Épée du destin", 2,1,"Épée du destin",35))],[Effets.EffetDegats(38,42,"Feu"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Épée du destin", 2,1,"Épée du destin",40))],25,1,1,2,0,"ligne",True,description="""Occasionne des dommages Feu.
            Les dommages sont augmentés à partir du second lancer.""", chaine=True),

                Sort.Sort("Épée du destin",187,4,1,1,[Effets.EffetDegats(38,42,"Feu"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Épée du destin", 2,1,"Épée du destin",40))],[Effets.EffetDegats(43,47,"Feu"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Épée du destin", 2,1,"Épée du destin",45))],25,1,1,2,0,"ligne",True,description="""Occasionne des dommages Feu.
            Les dommages sont augmentés à partir du second lancer.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Sentence",195,2,1,6,[Effets.EffetDegats(13,16,"Feu"),Effets.EffetEtat(Etats.EtatEffetFinTour("Sentence", 0,1,Effets.EffetDegats(13,16,"feu",zone=Zones.TypeZoneCercle(2), cibles_possibles="Ennemis"),"Sentence","lanceur"))],[Effets.EffetDegats(15,18,"Feu"),Effets.EffetEtat(Etats.EtatEffetFinTour("Sentence", 1,1,Effets.EffetDegats(15,18,"feu",zone=Zones.TypeZoneCercle(2)),"Sentence","lanceur"))],25,3,1,0,1,"cercle",True,description="""Occasionne des dommages Feu.
            Occasionne des dommages Feu supplémentaires aux ennemis à proximité de la cible (2 cases ou moins) à la fin de son tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Colère de Iop",100,7,1,1,[Effets.EffetDegats(61,80,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Colère de Iop", 3,1,"Colère de Iop",90))],[Effets.EffetDegats(71,90,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Colère de Iop", 3,1,"Colère de Iop",100))],25,1,1,3,0,"cercle",True,description="""Occasionne des dommages Terre.
            Augmente les dommages du sort au troisième tour après son lancer.""", chaine=True),

                Sort.Sort("Colère de Iop",149,7,1,1,[Effets.EffetDegats(71,90,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Colère de Iop", 3,1,"Colère de Iop",100))],[Effets.EffetDegats(81,100,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Colère de Iop", 3,1,"Colère de Iop",110))],25,1,1,3,0,"cercle",True,description="""Occasionne des dommages Terre.
            Augmente les dommages du sort au troisième tour après son lancer.""", chaine=True),

                Sort.Sort("Colère de Iop",197,7,1,1,[Effets.EffetDegats(81,100,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Colère de Iop", 3,1,"Colère de Iop",110))],[Effets.EffetDegats(91,110,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Colère de Iop", 3,1,"Colère de Iop",120))],25,1,1,3,0,"cercle",True,description="""Occasionne des dommages Terre.
            Augmente les dommages du sort au troisième tour après son lancer.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Fureur",200,3,1,1,[Effets.EffetDegats(28,32,"Terre"), Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fureur", 0,2,"Fureur",30))],[Effets.EffetDegats(34,38,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fureur", 0,2,"Fureur",36))],5,1,99,0,0,"cercle",False,description="""Occasionne des dommages Terre.
            Les dommages sont augmentés à chaque lancer du sort, mais ce bonus est perdu si le sort n'est pas relancé.""", chaine=True)
            ]))
        elif classe=="Cra":
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Magique",1,3,1,8,[Effets.EffetDegats(13,15,"Air"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",-2)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",2))],[Effets.EffetDegats(16,18,"Air"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",-2)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",2))],15,3,2,0,1,"cercle",True,description="""Occasionne des dommages Air et vole la port�e de la cible.""", chaine=True),

                Sort.Sort("Flèche Magique",20,3,1,10,[Effets.EffetDegats(16,18,"Air"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",-2)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",2))],[Effets.EffetDegats(19,21,"Air"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",-2)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",2))],15,3,2,0,1,"cercle",True,description="""Occasionne des dommages Air et vole la port�e de la cible.""", chaine=True),

                Sort.Sort("Flèche Magique",40,3,1,12,[Effets.EffetDegats(19,21,"Air"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",-2)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",2))],[Effets.EffetDegats(22,24,"Air"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",-2)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fleche Magique",0,1,"PO",2))],15,3,2,0,1,"cercle",True,description="""Occasionne des dommages Air et vole la port�e de la cible.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche de Concentration",101,3,3,8,[Effets.EffetDegats(22,26,"Air",zone=Zones.TypeZoneCroix(3), cibles_exclues="Lanceur"),Effets.EffetAttire(2,"CaseCible", zone=Zones.TypeZoneCroix(3), cibles_exclues="Lanceur")],[Effets.EffetDegats(25,29,"Air",zone=Zones.TypeZoneCroix(3), cibles_exclues="Lanceur"),Effets.EffetAttire(2,"CaseCible", zone=Zones.TypeZoneCroix(3), cibles_exclues="Lanceur")],15,2,1,0,1,"cercle",True,description="""Occasionne des dommages Air et attire vers la cible.
            N'affecte pas le lanceur.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche de Recul",1,3,1,4,[Effets.EffetDegats(17,20,"Air"),Effets.EffetPousser(2)],[Effets.EffetDegats(21,24,"Air"),Effets.EffetPousser(2)],25,2,1,0,0,"ligne",True,description="""Occasionne des dommages Air aux ennemis et pousse la cible.""", chaine=True),

                Sort.Sort("Flèche de Recul",25,3,1,6,[Effets.EffetDegats(21,24,"Air"),Effets.EffetPousser(3)],[Effets.EffetDegats(25,28,"Air"),Effets.EffetPousser(3)],25,2,1,0,0,"ligne",True,description="""Occasionne des dommages Air aux ennemis et pousse la cible.""", chaine=True),

                Sort.Sort("Flèche de Recul",52,3,1,8,[Effets.EffetDegats(25,28,"Air"),Effets.EffetPousser(4)],[Effets.EffetDegats(29,32,"Air"),Effets.EffetPousser(4)],25,2,1,0,0,"ligne",True,description="""Occasionne des dommages Air aux ennemis et pousse la cible.""", chaine=True)
            ]))    
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche érosive",105,3,1,3,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche Erosive",0,2,"erosion",10)),Effets.EffetDegats(25,29,"Terre")],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche Erosive",0,2,"erosion",10)),Effets.EffetDegats(29,33,"Terre")],15,3,2,0,1,"ligne",True,description="""Occasionne des dommages Terre et applique un malus d'�rosion.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche de dispersion",1,3,1,6,[Effets.EffetPousser(2,"CaseCible",reversedTreatmentOrder=True,zone=Zones.TypeZoneCroix(2),faire_au_vide=True)],[],0,1,1,2,1,"cercle",True,description="""Pousse les ennemis et alliés, même s'ils sont bloqués par d'autres entités.""", chaine=True),

                Sort.Sort("Flèche de dispersion",30,3,1,9,[Effets.EffetPousser(2,"CaseCible",reversedTreatmentOrder=True,zone=Zones.TypeZoneCroix(2),faire_au_vide=True)],[],0,1,1,2,1,"cercle",True,description="""Pousse les ennemis et alliés, même s'ils sont bloqués par d'autres entités.""", chaine=True),

                Sort.Sort("Flèche de dispersion",60,3,1,12,[Effets.EffetPousser(2,"CaseCible",reversedTreatmentOrder=True,zone=Zones.TypeZoneCroix(2),faire_au_vide=True)],[],0,1,1,2,1,"cercle",True,description="""Pousse les ennemis et alliés, même s'ils sont bloqués par d'autres entités.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Represailles",110,4,2,5,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Represailles",0,1,"PM",-100)),Effets.EffetEtat(Etats.Etat("Pesanteur",0,1))],[],0,1,1,5,0,"ligne",True,description="""Immobilise la cible et applique l'état Pesanteur.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
	            Sort.Sort("Flèche Glacée",3,3,3,6,[Effets.EffetDegats(9,11,"Feu"),Effets.EffetRetPA(2)],[Effets.EffetDegats(12,14,"Feu"),Effets.EffetRetPA(2)],5,99,2,0,1,"cercle",True,description="""Occasionne des dommages Feu et retire des PA.""", chaine=True),

                Sort.Sort("Flèche Glacée",35,3,3,8,[Effets.EffetDegats(13,15,"Feu"),Effets.EffetRetPA(2)],[Effets.EffetDegats(16,18,"Feu"),Effets.EffetRetPA(2)],5,99,2,0,1,"cercle",True,description="""Occasionne des dommages Feu et retire des PA.""", chaine=True),

                Sort.Sort("Flèche Glacée",67,3,3,10,[Effets.EffetDegats(17,19,"Feu"),Effets.EffetRetPA(2)],[Effets.EffetDegats(20,22,"Feu"),Effets.EffetRetPA(2)],5,99,2,0,1,"cercle",True,description="""Occasionne des dommages Feu et retire des PA.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Paralysante",115,5,2,6,[Effets.EffetDegats(39,42,"Feu",faire_au_vide=True,zone=Zones.TypeZoneCroix(1)),Effets.EffetRetPA(4,zone=Zones.TypeZoneCroix(1),faire_au_vide=True)],[Effets.EffetDegats(43,46,"Feu",zone=Zones.TypeZoneCroix(1),faire_au_vide=True),Effets.EffetRetPA(4,zone=Zones.TypeZoneCroix(1),faire_au_vide=True)],25,1,99,0,0,"cercle",True,description="""Occasionne des dommages Feu et retire des PA.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Enflammée",6,4,1,4,[Effets.EffetDegats(23,25,"Feu",faire_au_vide=True,zone=Zones.TypeZoneLigne(5)),Effets.EffetPousser(1,zone=Zones.TypeZoneLigne(5),faire_au_vide=True,reversedTreatmentOrder=True)],[Effets.EffetDegats(26,28,"Feu",zone=Zones.TypeZoneLigne(5),faire_au_vide=True),Effets.EffetPousser(1,zone=Zones.TypeZoneLigne(5),faire_au_vide=True,reversedTreatmentOrder=True)],25,2,99,0,1,"ligne",True,description="""Occasionne des dommages Feu et pousse les cibles présentes dans la zone d'effet du sort.""", chaine=True),

                Sort.Sort("Flèche Enflammée",42,4,1,6,[Effets.EffetDegats(27,29,"Feu",faire_au_vide=True,zone=Zones.TypeZoneLigne(5)),Effets.EffetPousser(1,zone=Zones.TypeZoneLigne(5),faire_au_vide=True,reversedTreatmentOrder=True)],[Effets.EffetDegats(30,32,"Feu",zone=Zones.TypeZoneLigne(5),faire_au_vide=True),Effets.EffetPousser(1,zone=Zones.TypeZoneLigne(5),faire_au_vide=True,reversedTreatmentOrder=True)],25,2,99,0,1,"ligne",True,description="""Occasionne des dommages Feu et pousse les cibles présentes dans la zone d'effet du sort.""", chaine=True),

                Sort.Sort("Flèche Enflammée",74,4,1,8,[Effets.EffetDegats(33,35,"Feu",faire_au_vide=True,zone=Zones.TypeZoneLigne(5)),Effets.EffetPousser(1,zone=Zones.TypeZoneLigne(5),faire_au_vide=True,reversedTreatmentOrder=True)],[Effets.EffetDegats(39,41,"Feu",zone=Zones.TypeZoneLigne(5),faire_au_vide=True),Effets.EffetPousser(1,zone=Zones.TypeZoneLigne(5),faire_au_vide=True,reversedTreatmentOrder=True)],25,2,99,0,1,"ligne",True,description="""Occasionne des dommages Feu et pousse les cibles présentes dans la zone d'effet du sort.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Répulsive",120,3,1,7,[Effets.EffetDegats(28,32,"Feu",faire_au_vide=True,zone=Zones.TypeZoneLignePerpendiculaire(1)),Effets.EffetPousser(1,"CaseCible",faire_au_vide=True,zone=Zones.TypeZoneLignePerpendiculaire(1))],[Effets.EffetDegats(34,38,"Feu",zone=Zones.TypeZoneLignePerpendiculaire(1),faire_au_vide=True),Effets.EffetPousser(1,"CibleDirect",faire_au_vide=True,zone=Zones.TypeZoneLignePerpendiculaire(1))],5,2,99,0,0,"ligne",True,description="""Occasionne des dommages Feu et repousse de 1 case.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Tir éloigné",9,3,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir_eloigne",0,4,"PO",2),zone=Zones.TypeZoneCercle(2))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir_eloigne",0,4,"PO",3),zone=Zones.TypeZoneCercle(2))],25,1,1,5,0,"cercle",False,description="""Augmente la port�e des cibles pr�sentes dans la zone d'effet.""", chaine=True),

                Sort.Sort("Tir éloigné",47,3,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir_eloigne",0,4,"PO",4),zone=Zones.TypeZoneCercle(2))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir_eloigne",0,4,"PO",5),zone=Zones.TypeZoneCercle(2))],25,1,1,5,0,"cercle",False,description="""Augmente la port�e des cibles pr�sentes dans la zone d'effet.""", chaine=True),

                Sort.Sort("Tir éloigné",87,3,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir_eloigne",0,4,"PO",6),zone=Zones.TypeZoneCercle(3))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir_eloigne",0,4,"PO",7),zone=Zones.TypeZoneCercle(3))],25,1,1,5,0,"cercle",False,description="""Augmente la port�e des cibles pr�sentes dans la zone d'effet.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Acuité Absolue",125,4,0,0,[Effets.EffetEtat(Etats.Etat("Desactive_ligne_de_vue",0,1))],[],0,1,1,3,0,"cercle",False,description="""Tous les sorts du Cr� peuvent �tre lanc�s au travers des obstacles pendant 1 tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche d'Expiation",13,4,6,10,[Effets.EffetDegats(19,21,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche d'Expiation",0,-1,"Flèche d'Expiation",22))],[Effets.EffetDegats(25,27,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche d'Expiation",0,-1,"Flèche d'Expiation",28))],25,1,1,3,1,"cercle",True,description="""Occasionne des dommages Eau, augmente les dommages du sort tous les 3 tours.""", chaine=False),

                Sort.Sort("Flèche d'Expiation",54,4,6,10,[Effets.EffetDegats(27,29,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche d'Expiation",0,-1,"Flèche d'Expiation",30))],[Effets.EffetDegats(33,35,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche d'Expiation",0,-1,"Flèche d'Expiation",36))],25,1,1,3,1,"cercle",True,description="""Occasionne des dommages Eau, augmente les dommages du sort tous les 3 tours.""", chaine=False),

                Sort.Sort("Flèche d'Expiation",94,4,6,10,[Effets.EffetDegats(35,37,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche d'Expiation",0,-1,"Flèche d'Expiation",36))],[Effets.EffetDegats(41,43,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche d'Expiation",0,-1,"Flèche d'Expiation",42))],25,1,1,3,1,"cercle",True,description="""Occasionne des dommages Eau, augmente les dommages du sort tous les 3 tours.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche de Rédemption",130,3,6,8,[Effets.EffetDegats(19,22,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche de rédemption",1,1,"Flèche de Rédemption",12))],[Effets.EffetDegats(23,26,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche de rédemption",1,1,"Flèche de Rédemption",12))],25,3,2,0,1,"cercle",True,description="""Occasionne des dommages Eau qui sont augment�s si le sort est relanc� le tour suivant.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Oeil de Taupe",17,3,5,6,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Oeil de taupe",0,3,"PO",-2),zone=Zones.TypeZoneCercle(2), faire_au_vide=True),Effets.EffetVolDeVie(8,10,"Eau",zone=Zones.TypeZoneCercle(2), faire_au_vide=True),Effets.EffetDevoilePiege(zone=Zones.TypeZoneCercle(2), faire_au_vide=True)],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Oeil de taupe",0,3,"PO",-2), faire_au_vide=True,zone=Zones.TypeZoneCercle(2)),Effets.EffetVolDeVie(11,13,"Eau", faire_au_vide=True,zone=Zones.TypeZoneCercle(2)),Effets.EffetDevoilePiege(zone=Zones.TypeZoneCercle(2), faire_au_vide=True)],25,1,1,4,1,"cercle",True,description="""R�duit la port�e des personnages cibl�s, vole de la vie dans l'�l�ment Eau et rep�re les objets invisibles dans sa zone d'effet.""", chaine=True),

                Sort.Sort("Oeil de Taupe",58,3,5,8,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Oeil de taupe",0,3,"PO",-4),zone=Zones.TypeZoneCercle(2), faire_au_vide=True),Effets.EffetVolDeVie(12,14,"Eau",zone=Zones.TypeZoneCercle(2), faire_au_vide=True),Effets.EffetDevoilePiege(zone=Zones.TypeZoneCercle(2), faire_au_vide=True)],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Oeil de taupe",0,3,"PO",-4), faire_au_vide=True,zone=Zones.TypeZoneCercle(2)),Effets.EffetVolDeVie(15,17,"Eau", faire_au_vide=True,zone=Zones.TypeZoneCercle(2)),Effets.EffetDevoilePiege(zone=Zones.TypeZoneCercle(2), faire_au_vide=True)],25,1,1,4,1,"cercle",True,description="""R�duit la port�e des personnages cibl�s, vole de la vie dans l'�l�ment Eau et rep�re les objets invisibles dans sa zone d'effet.""", chaine=True),

                Sort.Sort("Oeil de Taupe",102,3,5,10,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Oeil de taupe",1,3,"PO",-6),zone=Zones.TypeZoneCercle(3), faire_au_vide=True),Effets.EffetVolDeVie(16,18,"Eau",zone=Zones.TypeZoneCercle(3), faire_au_vide=True),Effets.EffetDevoilePiege(zone=Zones.TypeZoneCercle(3), faire_au_vide=True)],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Oeil de taupe",0,3,"PO",-6), faire_au_vide=True,zone=Zones.TypeZoneCercle(3)),Effets.EffetVolDeVie(19,21,"Eau", faire_au_vide=True,zone=Zones.TypeZoneCercle(3)),Effets.EffetDevoilePiege(zone=Zones.TypeZoneCercle(3), faire_au_vide=True)],25,1,1,4,1,"cercle",True,description="""R�duit la port�e des personnages cibl�s, vole de la vie dans l'�l�ment Eau et rep�re les objets invisibles dans sa zone d'effet.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche écrasante",135,3,5,7,[Effets.EffetEtat(Etats.Etat("Pesanteur",0,1),faire_au_vide=True,zone=Zones.TypeZoneCroixDiagonale(1)),Effets.EffetDegats(34,38,"Feu",faire_au_vide=True,zone=Zones.TypeZoneCroixDiagonale(1))],[Effets.EffetEtat(Etats.Etat("Pesanteur",1,1),faire_au_vide=True,zone=Zones.TypeZoneCroixDiagonale(1)),Effets.EffetDegats(37,41,"Feu",faire_au_vide=True,zone=Zones.TypeZoneCroixDiagonale(1))],25,1,1,3,1,"cercle",True,description="""Occasionne des dommages Feu et applique l'�tat Pesanteur.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Tir Critique",22,2,0,2,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Critique",0,4,"cc", 10))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Critique",0,4,"cc", 10)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Critique Critique",0,4,"pui", 10))],25,1,1,5,1,"cercle",True,description="""Augmente la probabilit� de faire un coup critique.""", chaine=True),

                Sort.Sort("Tir Critique",65,2,0,4,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Critique",0,4,"cc", 12))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Critique",0,4,"cc", 12)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Critique Critique",0,4,"pui", 30))],25,1,1,5,1,"cercle",True,description="""Augmente la probabilit� de faire un coup critique.""", chaine=True),

                Sort.Sort("Tir Critique",108,2,0,6,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Critique",0,4,"cc", 14))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Critique",0,4,"cc", 14)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Critique Critique",0,4,"pui", 50))],25,1,1,5,1,"cercle",True,description="""Augmente la probabilit� de faire un coup critique.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Balise de Rappel",140,2,1,5,[Effets.EffetInvoque("Balise de Rappel",True,cibles_possibles="",faire_au_vide=True)],[],0,1,1,2,0,"cercle",True,description="""Invoque une balise qui échange sa position avec celle du lanceur (au début du prochain tour).""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche d'Immobilisation",27,2,1,6,[Effets.EffetDegats(6,7,"Eau"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",-1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",1))],[Effets.EffetDegats(7,8,"Eau"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",-1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",1))],5,4,2,0,1,"cercle",True,description="""Occasionne des dommages Eau et vole des PM � la cible.""", chaine=True),

                Sort.Sort("Flèche d'Immobilisation",72,2,1,8,[Effets.EffetDegats(8,9,"Eau"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",-1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",1))],[Effets.EffetDegats(9,10,"Eau"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",-1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",1))],5,4,2,0,1,"cercle",True,description="""Occasionne des dommages Eau et vole des PM � la cible.""", chaine=True),

                Sort.Sort("Flèche d'Immobilisation",118,2,1,10,[Effets.EffetDegats(10,11,"Eau"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",-1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",1))],[Effets.EffetDegats(12,13,"Eau"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",-1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Flèche d'Immobilisation",0,1,"PM",1))],5,4,2,0,1,"cercle",True,description="""Occasionne des dommages Eau et vole des PM � la cible.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Assaillante",145,4,2,6,[Effets.EffetDegats(33,37,"Eau",zone=Zones.TypeZoneCroix(1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Assaillante",0,1,"pui",100),zone=Zones.TypeZoneCroix(1))],[Effets.EffetDegats(36,40,"Eau",zone=Zones.TypeZoneCroix(1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Assaillante",0,1,"pui",100),zone=Zones.TypeZoneCroix(1))],15,3,2,0,1,"cercle",True,description="""Occasionne des dommages Eau en zone.
            Pour chaque entité comprise dans la zone d'effet, le lanceur gagne 100 Puissance pendant 1 tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Punitive",32,4,6,8,[Effets.EffetDegats(19,21,"Terre"), Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche Punitive",0,-1,"Flèche Punitive",20))],[Effets.EffetDegats(23,25,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche Punitive",0,-1,"Flèche Punitive",24))],25,1,1,2,1,"cercle",True,description="""Occasionne des dommages Terre et augmente les dommages du sort tous les 2 tours.""", chaine=True),

                Sort.Sort("Flèche Punitive",81,4,6,8,[Effets.EffetDegats(24,26,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche Punitive",0,-1,"Flèche Punitive",25))],[Effets.EffetDegats(28,30,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche Punitive",0,-1,"Flèche Punitive",29))],25,1,1,2,1,"cercle",True,description="""Occasionne des dommages Terre et augmente les dommages du sort tous les 2 tours.""", chaine=True),

                Sort.Sort("Flèche Punitive",124,4,6,8,[Effets.EffetDegats(29,31,"Terre"), Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche Punitive",0,-1,"Flèche Punitive",30))],[Effets.EffetDegats(35,37,"Terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche Punitive",0,-1,"Flèche Punitive",36))],25,1,1,2,1,"cercle",True,description="""Occasionne des dommages Terre et augmente les dommages du sort tous les 2 tours.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche du Jugement",150,3,5,9,[Effets.EffetDegatsSelonPMUtilises(39,45,"Terre")],[Effets.EffetDegatsSelonPMUtilises(47,53,"Terre")],5,3,2,0,1,"cercle",True,description="""Occasionne des dommages Terre.
            Moins le lanceur a utilisé de PM pendant son tour de jeu, plus les dommages occasionnés sont importants.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Tir Puissant",38,3,0,2,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Puissant",0,3,"pui",150))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Puissant",0,3,"pui",170))],25,1,1,6,1,"cercle",True,description="""Augmente les dommages des sorts.""", chaine=True),

                Sort.Sort("Tir Puissant",90,3,0,4,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Puissant",0,3,"pui",200))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Puissant",0,3,"pui",230))],25,1,1,6,1,"cercle",True,description="""Augmente les dommages des sorts.""", chaine=True),

                Sort.Sort("Tir Puissant",132,3,0,6,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Puissant",0,3,"pui",250))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Tir Puissant",0,3,"pui",290))],25,1,1,6,1,"cercle",True,description="""Augmente les dommages des sorts.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Balise Tactique",155,1,1,10,[Effets.EffetTue(cibles_possibles="Balise Tactique",zone=Zones.TypeZoneInfini()),Effets.EffetInvoque("Balise Tactique",True, cibles_possibles="", faire_au_vide=True), Effets.EffetEtat(Etats.EtatModDegPer("Balise Tactique",0,-1,50,"Allies"))],[],0,1,1,2,1,"cercle",True,description="""Invoque une Balise qui peut servir d'obstacle et de cible.
            La Balise subit 2 fois moins de dommages des alliés.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Harcelante",44,3,1,5,[Effets.EffetDegats(9,11,"Air")],[Effets.EffetDegats(11,13,"Air")],5,4,2,0,1,"cercle",False,description="""Occasionne des dommages Air sans ligne de vue.""", chaine=True),

                Sort.Sort("Flèche Harcelante",97,3,1,6,[Effets.EffetDegats(11,13,"Air")],[Effets.EffetDegats(13,15,"Air")],5,4,2,0,1,"cercle",False,description="""Occasionne des dommages Air sans ligne de vue.""", chaine=True),

                Sort.Sort("Flèche Harcelante",137,3,1,7,[Effets.EffetDegats(13,15,"Air")],[Effets.EffetDegats(16,18,"Air")],5,4,2,0,1,"cercle",False,description="""Occasionne des dommages Air sans ligne de vue.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Massacrante",160,4,4,8,[Effets.EffetDegats(34,38,"Air"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche massacrante",1,1,"Flèche Massacrante",18))],[Effets.EffetDegats(41,45,"Air"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_massacrante",1,1,"Flèche Massacrante",21))],5,3,2,0,1,"ligne",True,description="""Occasionne des dommages Air.
            Les dommages du sort sont augmentés au tour suivant.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Empoisonnée",50,3,1,6,[Effets.EffetRetPM(2),Effets.EffetEtat(Etats.EtatEffetDebutTour("Flèche Empoisonnée",0,2,Effets.EffetDegats(11,12,"Neutre"),"Flèche Empoisonnée","lanceur"))],[Effets.EffetRetPM(2),Effets.EffetEtat(Etats.EtatEffetDebutTour("Flèche Empoisonnée",0,2,Effets.EffetDegats(14,15,"Neutre"),"Flèche Empoisonnée","lanceur"))],5,4,1,0,1,"cercle",True,description="""Occasionne des dommages Neutre sur plusieurs tours et retire des PM.""", chaine=True),

                Sort.Sort("Flèche Empoisonnée",103,3,1,8,[Effets.EffetRetPM(2),Effets.EffetEtat(Etats.EtatEffetDebutTour("Flèche Empoisonnée",0,2,Effets.EffetDegats(14,15,"Neutre"),"Flèche Empoisonnée","lanceur"))],[Effets.EffetRetPM(2),Effets.EffetEtat(Etats.EtatEffetDebutTour("Flèche Empoisonnée",0,2,Effets.EffetDegats(17,18,"Neutre"),"Flèche Empoisonnée","lanceur"))],5,4,1,0,1,"cercle",True,description="""Occasionne des dommages Neutre sur plusieurs tours et retire des PM.""", chaine=True),

                Sort.Sort("Flèche Empoisonnée",143,3,1,10,[Effets.EffetRetPM(3),Effets.EffetEtat(Etats.EtatEffetDebutTour("Flèche Empoisonnée",0,2,Effets.EffetDegats(17,18,"Neutre"),"Flèche Empoisonnée","lanceur"))],[Effets.EffetRetPM(3),Effets.EffetEtat(Etats.EtatEffetDebutTour("Flèche Empoisonnée",0,2,Effets.EffetDegats(21,22,"Neutre"),"Flèche Empoisonnée","lanceur"))],5,4,1,0,1,"cercle",True,description="""Occasionne des dommages Neutre sur plusieurs tours et retire des PM.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Curative",165,3,3,6,[Effets.EffetSoinPerPVMax(10),Effets.EffetEtat(Etats.EtatModSoinPer("Flèche Curative",1,1,130))],[Effets.EffetSoinPerPVMax(12),Effets.EffetEtat(Etats.EtatModSoinPer("Flèche Curative",1,1,130))],15,3,1,0,1,"ligne",True,description="""Soigne et augmente les soins re�us par la cible.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Persécutrice",56,3,5,8,[Effets.EffetDegats(7,9,"Feu"),Effets.EffetDegats(7,9,"Air")],[Effets.EffetDegats(10,12,"Feu"),Effets.EffetDegats(10,12,"Air")],5,99,2,0,1,"ligne",True,description="""Occasionne des dommages Air et Feu.""", chaine=True),

                Sort.Sort("Flèche Persécutrice",112,3,5,8,[Effets.EffetDegats(9,11,"Feu"),Effets.EffetDegats(9,11,"Air")],[Effets.EffetDegats(12,14,"Feu"),Effets.EffetDegats(12,14,"Air")],5,99,2,0,1,"ligne",True,description="""Occasionne des dommages Air et Feu.""", chaine=True),

                Sort.Sort("Flèche Persécutrice",147,3,5,8,[Effets.EffetDegats(11,13,"Feu"),Effets.EffetDegats(11,13,"Air")],[Effets.EffetDegats(13,15,"Feu"),Effets.EffetDegats(13,15,"Air")],5,99,2,0,1,"ligne",True,description="""Occasionne des dommages Air et Feu.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Tyrannique",170,4,2,7,[Effets.EffetEtat(Etats.EtatEffetSiPousse("Flèche tyrannique air",0,2, Effets.EffetDegats(15,15,"Air"),"Flèche tyrannique","lanceur")), Effets.EffetEtat(Etats.EtatEffetSiSubit("Flèche tyrannique feu",0,2, Effets.EffetDegats(15,15,"Feu"),"Flèche tyrannique","lanceur","cible","doPou"))],[],0,3,1,0,1,"ligne",True,description="""Occasionne des dommages Air si la cible est pouss�e.
            Occasionne des dommages Feu si la cible subit des dommages de poussée.
            Les dommages de chaque élément peuvent être déclenchés 3 fois par tour.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Destructrice",62,4,5,8,[Effets.EffetDegats(20,22,"Terre"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche Destructrice",0,1,"do",-20))],[Effets.EffetDegats(24,26,"Terre"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche Destructrice",0,1,"do",-22))],15,99,2,0,1,"cercle",True,description="""Occasionne des dommages Terre et réduit les dommages occasionnés par la cible.""", chaine=True),

                Sort.Sort("Flèche Destructrice",116,4,5,8,[Effets.EffetDegats(25,27,"Terre"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche Destructrice",0,1,"do",-40))],[Effets.EffetDegats(29,31,"Terre"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche Destructrice",0,1,"do",-44))],15,99,2,0,1,"cercle",True,description="""Occasionne des dommages Terre et réduit les dommages occasionnés par la cible.""", chaine=True),

                Sort.Sort("Flèche Destructrice",153,4,5,8,[Effets.EffetDegats(30,32,"Terre"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche Destructrice",0,1,"do",-60))],[Effets.EffetDegats(34,36,"Terre"),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Flèche Destructrice",0,1,"do",-66))],15,99,2,0,1,"cercle",True,description="""Occasionne des dommages Terre et réduit les dommages occasionnés par la cible.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Tir de Barrage",175,4,4,8,[Effets.EffetDegats(29,33,"Terre"),Effets.EffetPousser(2)],[Effets.EffetDegats(35,39,"Terre"),Effets.EffetPousser(2)],25,3,2,0,1,"cercle",True,description="""Occasionne des dommages Terre et repousse la cible.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Absorbante",69,4,6,8,[Effets.EffetVolDeVie(19,21,"Air")],[Effets.EffetVolDeVie(23,25,"Air")],15,3,2,0,1,"cercle",True,description="""Vole de la vie dans l'élément Air.""", chaine=True),

                Sort.Sort("Flèche Absorbante",122,4,6,8,[Effets.EffetVolDeVie(24,26,"Air")],[Effets.EffetVolDeVie(28,30,"Air")],15,3,2,0,1,"cercle",True,description="""Vole de la vie dans l'élément Air.""", chaine=True),

                Sort.Sort("Flèche Absorbante",162,4,6,8,[Effets.EffetVolDeVie(29,31,"Air")],[Effets.EffetVolDeVie(33,35,"Air")],15,3,2,0,1,"cercle",True,description="""Vole de la vie dans l'élément Air.""", chaine=True)
            ]))

            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Dévorante",180,3,1,6,[
                    Effets.EffetDegats(70,74,"Air",zone=Zones.TypeZoneInfini(),etat_requis_cibles="Flèche dévorante lancer 3",consomme_etat=True),
                    Effets.EffetEtat(Etats.Etat("Flèche dévorante lancer 3",0,-1),etat_requis_cibles="Flèche dévorante lancer 2",consomme_etat=True),
                    Effets.EffetDegats(52,56,"Air",zone=Zones.TypeZoneInfini(),etat_requis_cibles="Flèche dévorante lancer 2",consomme_etat=True),
                    Effets.EffetEtat(Etats.Etat("Flèche dévorante lancer 2",0,-1),etat_requis_cibles="Flèche dévorante lancer 1",consomme_etat=True),
                    Effets.EffetDegats(34,38,"Air",zone=Zones.TypeZoneInfini(),etat_requis_cibles="Flèche dévorante lancer 1",consomme_etat=True),
                    Effets.EffetEtat(Etats.Etat("Flèche dévorante lancer 1",0,-1),etat_requis_cibles="!Flèche dévorante lancer 2|!Flèche dévorante lancer 3")
                    ],
                    [
                    Effets.EffetDegats(81,85,"Air",zone=Zones.TypeZoneInfini(),etat_requis_cibles="Flèche dévorante lancer 3",consomme_etat=True),
                    Effets.EffetEtat(Etats.Etat("Flèche dévorante lancer 3",0,-1),etat_requis_cibles="Flèche dévorante lancer 2",consomme_etat=True),
                    Effets.EffetDegats(60,64,"Air",zone=Zones.TypeZoneInfini(),etat_requis_cibles="Flèche dévorante lancer 2",consomme_etat=True),
                    Effets.EffetEtat(Etats.Etat("Flèche dévorante lancer 2",0,-1),etat_requis_cibles="Flèche dévorante lancer 2",consomme_etat=True),
                    Effets.EffetDegats(39,43,"Air",zone=Zones.TypeZoneInfini(),etat_requis_cibles="Flèche dévorante lancer 1",consomme_etat=True),
                    Effets.EffetEtat(Etats.Etat("Flèche dévorante lancer 1",0,-1),etat_requis_cibles="!Flèche dévorante lancer 2|!Flèche dévorante lancer 3")
                    ]
                    ,15,2,1,0,1,"cercle",True,description="""Occasionne des dommages Air.
            Les dommages sont appliqués lorsque le sort est lancé sur une autre cible.
            Peut se cumuler 3 fois sur une même cible.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Cinglante",77,2,1,5,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche cinglante",0,2,"erosion",10)), Effets.EffetPousser(2)],[],0,4,2,0,1,"ligne",True,description="""Applique de l'�rosion aux ennemis et repousse de 2 cases.""", chaine=True),

                Sort.Sort("Flèche Cinglante",128,2,1,7,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche cinglante",0,2,"erosion",10)), Effets.EffetPousser(2)],[],0,4,2,0,1,"ligne",True,description="""Applique de l'�rosion aux ennemis et repousse de 2 cases.""", chaine=True),

                Sort.Sort("Flèche Cinglante",172,2,1,9,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fleche cinglante",0,2,"erosion",10)), Effets.EffetPousser(2)],[],0,4,2,0,1,"ligne",True,description="""Applique de l'�rosion aux ennemis et repousse de 2 cases.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche de Repli",185,1,2,7,[Effets.EffetPousser(2,source="CaseCible",cible="Lanceur")],[],0,3,2,0,1,"ligne",True,description="""Le lanceur du sort recule de 2 cases.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Fèche Ralentissante",84,4,1,8,[Effets.EffetRetPA(2,zone=Zones.TypeZoneCercle(2)),Effets.EffetDegats(26,28,"Eau",zone=Zones.TypeZoneCercle(2))],[Effets.EffetRetPA(2,zone=Zones.TypeZoneCercle(2)),Effets.EffetDegats(32,34,"Eau",zone=Zones.TypeZoneCercle(2))],15,2,1,0,1,"ligne",True,description="""Occasionne des dommages Eau et retire des PA en zone.""", chaine=True),

                Sort.Sort("Flèche Ralentissante",134,4,1,8,[Effets.EffetRetPA(2,zone=Zones.TypeZoneCercle(2)),Effets.EffetDegats(31,33,"Eau",zone=Zones.TypeZoneCercle(2))],[Effets.EffetRetPA(2,zone=Zones.TypeZoneCercle(2)),Effets.EffetDegats(37,39,"Eau",zone=Zones.TypeZoneCercle(2))],15,2,1,0,1,"ligne",True,description="""Occasionne des dommages Eau et retire des PA en zone.""", chaine=True),

                Sort.Sort("Flèche Ralentissante",178,4,1,8,[Effets.EffetRetPA(3,zone=Zones.TypeZoneCercle(2)),Effets.EffetDegats(36,38,"Eau",zone=Zones.TypeZoneCercle(2))],[Effets.EffetRetPA(3,zone=Zones.TypeZoneCercle(2)),Effets.EffetDegats(42,44,"Eau",zone=Zones.TypeZoneCercle(2))],15,2,1,0,1,"ligne",True,description="""Occasionne des dommages Eau et retire des PA en zone.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Percutante",190,2,1,6,[Effets.EffetDegats(6,10,"Eau"),Effets.EffetEtat(Etats.EtatEffetFinTour("Flèche percutante à retardement",0,1,Effets.EffetDegats(6,10,"eau",zone=Zones.TypeZoneCercleSansCentre(2)),"Flèche percutante à retardement","lanceur")),Effets.EffetEtat(Etats.EtatEffetFinTour("Flèche percutante à retardement PA", 0,1,Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2)),"Flèche percutante à retardement PA","lanceur"))],[Effets.EffetDegats(9,13,"Eau"),Effets.EffetEtat(Etats.EtatEffetFinTour("Flèche percutante à retardement",0,1,Effets.EffetDegats(9,13,"eau",zone=Zones.TypeZoneCercleSansCentre(2)),"Flèche percutante à retardement","lanceur")),Effets.EffetEtat(Etats.EtatEffetFinTour("Flèche percutante à retardement PA", 0,1,Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2)),"Flèche percutante à retardement PA","lanceur"))],5,4,2,0,1,"cercle",True,description="""Occasionne des dommages Eau.
            à la fin de son tour, la cible occasionne des dommages Eau et retire des PA en cercle de taille 2 autour d'elle.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Flèche Explosive",92,4,1,8,[Effets.EffetDegats(22,26,"Feu",zone=Zones.TypeZoneCercle(2))],[Effets.EffetDegats(27,31,"Feu",zone=Zones.TypeZoneCercle(2))],25,2,1,0,1,"cercle",True,description="""Occasionne des dommages Feu en zone.""", chaine=True),

                Sort.Sort("Flèche Explosive",141,4,1,8,[Effets.EffetDegats(26,30,"Feu",zone=Zones.TypeZoneCercle(2))],[Effets.EffetDegats(31,35,"Feu",zone=Zones.TypeZoneCercle(2))],25,2,1,0,1,"cercle",True,description="""Occasionne des dommages Feu en zone.""", chaine=True),

                Sort.Sort("Flèche Explosive",187,4,1,8,[Effets.EffetDegats(30,34,"Feu",zone=Zones.TypeZoneCercle(3))],[Effets.EffetDegats(35,39,"Feu",zone=Zones.TypeZoneCercle(3))],25,2,1,0,1,"cercle",True,description="""Occasionne des dommages Feu en zone.""", chaine=True)
            ]))
            fleche_fulminante=Sort.Sort("Flèche Fulminante",195,4,1,8,[Effets.EffetDegats(38,42,"Feu",cibles_possibles="Ennemis|Balise Tactique"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche Fulminante boost",0,1,"Flèche Fulminante Rebond",10))],[],0,1,1,0,1,"cercle",True,description="Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
            fleche_fulminante_rebond=Sort.Sort("Flèche Fulminante Rebond",195,0,0,99,[Effets.EffetDegats(38,42,"Feu",cibles_possibles="Ennemis|Balise Tactique"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Flèche Fulminante boost",0,1,"Flèche Fulminante Rebond",10))],[],0,9,1,0,0,"cercle",True,description="Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
            fleche_fulminante.effets.append(Effets.EffetPropage(fleche_fulminante_rebond,Zones.TypeZoneCercle(2),cibles_possibles="Ennemis|Balise Tactique"))
            fleche_fulminante_rebond.effets.append(Effets.EffetPropage(fleche_fulminante_rebond,Zones.TypeZoneCercle(2),cibles_possibles="Ennemis|Balise Tactique"))
            sorts.append(Personnage.getSortRightLvl(lvl,[fleche_fulminante]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Maîtrise de l'Arc",100,2,0,2,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Maitrise de l'arc",0,3,"do",40))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Maitrise de l'arc",0,3,"do",50))],25,1,1,5,1,"cercle",False,description="""Augmente les dommages.""", chaine=True),

                Sort.Sort("Maîtrise de l'Arc",149,2,0,4,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Maitrise de l'arc",0,3,"do",50))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Maitrise de l'arc",0,3,"do",60))],25,1,1,5,1,"cercle",False,description="""Augmente les dommages.""", chaine=True),

                Sort.Sort("Maîtrise de l'Arc",197,2,0,6,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Maitrise de l'arc",0,3,"do",60))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Maitrise de l'arc",0,3,"do",70))],25,1,1,5,1,"cercle",False,description="""Augmente les dommages.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Sentinelle",200,3,0,0,[Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Sentinelle",1,1,"PM",-100)),Effets.EffetEtatSelf(Etats.EtatBoostSortsPer("Sentinelle",1,1,30))],[],0,1,1,3,0,"cercle",False,description="""Le lanceur perd tous ses PM mais gagne un bonus de dommages pour le tour en cours.""", chaine=True)
            ]))
        elif classe=="Sram":
            sortsDebutCombat.append(
                Sort.Sort("Chausse-Trappe Boost",0,0,0,0,[Effets.EffetEtatSelf(Etats.EtatEffetSiPiegeDeclenche("Chausse-Trappe Boost",0,-1,Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Chausse-Trappe",0,-1,"Chausse-Trappe",8), cumulMax=4),"Chausse-Trappe Boost","porteur","porteur"))],[],0,99,99,0,0,"cercle",False,description="""""", chaine=False),
            )
            sortsDebutCombat.append(
                Sort.Sort("Traquenard Boost",0,0,0,0,[Effets.EffetEtatSelf(Etats.EtatEffetSiPiegeDeclenche("Traquenard Boost",0,-1,Effets.EffetEtatSelf(Etats.EtatBoostSortCarac("Traquenard",0,-1,"Traquenard","POMax",1), cumulMax=4),"Traquenard Boost","porteur","porteur"))],[],0,99,99,0,0,"cercle",False,description="""""", chaine=False),
            )
            sortsDebutCombat.append(
                Sort.Sort("Injection Toxique Boost",0,0,0,0,[Effets.EffetEtatSelf(Etats.EtatEffetSiPiegeDeclenche("Injection Toxique Boost",0,-1,Effets.EffetEtatSelf(Etats.EtatBoostSortCarac("Injection Toxique",0,-1,"Injection Toxique","nbTourEntreDeux",-1), cumulMax=4),"Injection Toxique Boost","porteur","porteur"))],[],0,99,99,0,0,"cercle",False,description="""""", chaine=False),
            )
            activationPiegeSournois = [Effets.EffetDegats(26,28,"feu",zone=Zones.TypeZoneCercle(1), faire_au_vide=True,piege=True),Effets.EffetAttire(1,"CaseCible",zone=Zones.TypeZoneCercle(1), faire_au_vide=True)]
            activationPiegePerfide = [Effets.EffetAttire(3,"CaseCible",zone=Zones.TypeZoneCroix(3), faire_au_vide=True,piege=True)]
            activationPiegeFangeux = [Effets.EffetEtat(Etats.EtatEffetSiSubit('Etat temporaire',0,1,Effets.EffetSoinSelonSubit(50,zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies"),"Piège Fangeux","lanceur","cible")),Effets.EffetDegats(33,37,"Eau",piege=True,faire_au_vide=True),Effets.EffetRetireEtat('Etat temporaire')]
            activationPiegeDeMasse = [Effets.EffetDegats(34,38,"Terre",zone=Zones.TypeZoneCercle(2), faire_au_vide=True,piege=True)]
            activationPiegeEmpoisonne = [Effets.EffetEtat(Etats.EtatEffetDebutTour("Piège Empoisonné",0,3,Effets.EffetDegats(10,10,"Air"),"Piège Empoisonné","lanceur"),zone=Zones.TypeZoneCroix(1), faire_au_vide=True,piege=True)]
            activationPiegeAFragmentation = [Effets.EffetDegats(18,22,"feu",zone=Zones.TypeZoneCercle(0), faire_au_vide=True,piege=True),Effets.EffetDegats(33,37,"feu",zone=Zones.TypeZoneAnneau(1), faire_au_vide=True,piege=True),Effets.EffetDegats(43,47,"feu",zone=Zones.TypeZoneAnneau(2), faire_au_vide=True,piege=True),Effets.EffetDegats(58,62,"feu",zone=Zones.TypeZoneAnneau(3), faire_au_vide=True,piege=True)]
            activationPiegeDimmobilisation = [Effets.EffetRetPM(4,zone=Zones.TypeZoneCercle(3), faire_au_vide=True,piege=True)]
            activationPiegeDeDerive = [Effets.EffetPousser(2,"CaseCible",zone=Zones.TypeZoneCroixDiagonale(1), faire_au_vide=True,piege=True)]
            activationGlypheInsidieuse = Sort.Sort("Piège insidieux : poison fin de tour",0,0,0,3,[Effets.EffetEtat(Etats.EtatEffetFinTour("Piège insidieux : poison fin de tour",0,1,Effets.EffetDegats(34,38,"Air"), "Piège insidieux : poison fin de tour", "lanceur"), cumulMax=1, cibles_possibles="Ennemis")],[],0, 99,99,0,0,"cercle",False)
            sortieGlypheInsidieuse = Sort.Sort("Piège insidieux: Sortie",0,0,0,99,[Effets.EffetRetireEtat("Piège insidieux : poison fin de tour",cibles_possibles="Ennemis", faire_au_vide=True)],[],0, 99,99,0,0,"cercle",False)
            activationPiegeInsidieux = [Effets.EffetGlyphe(activationGlypheInsidieuse,activationGlypheInsidieuse,sortieGlypheInsidieuse,1,"Piège insidieux",(0,200,0),zone=Zones.TypeZoneCercle(2), faire_au_vide=True, piege=True)]
            activationPiegeRepulsif = [Effets.EffetDegats(12,12,"air",zone=Zones.TypeZoneCercle(1), faire_au_vide=True,piege=True),Effets.EffetPousser(2,"CaseCible",zone=Zones.TypeZoneCercle(1), faire_au_vide=True)]
            activationPiegeRepoussant = [Effets.EffetPousser(2,"CaseCible",zone=Zones.TypeZoneCercle(2), faire_au_vide=True,piege=True)]
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Sournoiserie",1,3,1,4,[Effets.EffetDegats(14,16,"Terre")],[Effets.EffetDegats(18,20,"Terre")],5,99,3,0,1,"cercle",True,description="""Occasionne des dommages Terre.""", chaine=True),

                Sort.Sort("Sournoiserie",25,3,1,4,[Effets.EffetDegats(17,19,"Terre")],[Effets.EffetDegats(21,23,"Terre")],5,99,3,0,1,"cercle",True,description="""Occasionne des dommages Terre.""", chaine=True),

                Sort.Sort("Sournoiserie",52,3,1,5,[Effets.EffetDegats(20,22,"Terre")],[Effets.EffetDegats(24,26,"Terre")],5,99,3,0,1,"cercle",True,description="""Occasionne des dommages Terre.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Chausse-Trappe",110,4,1,4,[Effets.EffetDegats(30,34,"Terre"),Effets.EffetRetireEtat("Chausse-Trappe",zone=Zones.TypeZoneInfini(),cibles_possibles="Lanceur")],[Effets.EffetDegats(34,38,"Terre"),Effets.EffetRetireEtat("Chausse-Trappe",zone=Zones.TypeZoneInfini(),cibles_possibles="Lanceur")],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Terre. Chaque piège déclenché augmente les dommages de Chausse-Trape.
            Le bonus de dommages disparaît quand le sort est lancé.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Piège Sournois",1,3,1,4,[Effets.EffetPiege(Zones.TypeZoneCroix(1),activationPiegeSournois,"Piège sournois",(255,0,0),faire_au_vide=True)],[],0,1,99,0,1,"cercle",False,description="""Occasionne des dommages Feu et attire.""", chaine=True),

                Sort.Sort("Piège Sournois",30,3,1,6,[Effets.EffetPiege(Zones.TypeZoneCroix(1),activationPiegeSournois,"Piège sournois",(255,0,0),faire_au_vide=True)],[],0,1,99,0,1,"cercle",False,description="""Occasionne des dommages Feu et attire.""", chaine=True),

                Sort.Sort("Piège Sournois",60,3,1,8,[Effets.EffetPiege(Zones.TypeZoneCroix(1),activationPiegeSournois,"Piège sournois",(255,0,0),faire_au_vide=True)],[],0,1,99,0,1,"cercle",False,description="""Occasionne des dommages Feu et attire.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Piège Perfide",105,2,1,7,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegePerfide,"Piège Perfide",(240,0,0),faire_au_vide=True)],[],0,1,99,0,1,"cercle",False,description="""Pose un piège mono-cellule qui attire en zone.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Invisibilité",1,2,0,0,[Effets.EffetEtat(Etats.Etat("Invisible",0,3)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Invibilité_PM",0,4,"PM",1))],[],0,1,1,7,0,"cercle",False,description="""Rend invisible.""", chaine=True),

                Sort.Sort("Invisibilité",20,2,0,0,[Effets.EffetEtat(Etats.Etat("Invisible",0,3)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Invibilité_PM",0,4,"PM",1))],[],0,1,1,6,0,"cercle",False,description="""Rend invisible.""", chaine=True),

                Sort.Sort("Invisibilité",40,2,0,0,[Effets.EffetEtat(Etats.Etat("Invisible",0,3)),Effets.EffetEtat(Etats.EtatBoostCaracFixe("Invibilité_PM",0,4,"PM",2))],[],0,1,1,6,0,"cercle",False,description="""Rend invisible.""", chaine=True)
            ]))
            activationBrume = Sort.Sort("Activation Brume",0,0,0,3,[Effets.EffetEtat(Etats.Etat("Invisible",0,2),cibles_possibles="Allies|Lanceur")],[],0, 99,99,0,0,"cercle",False)
            sortieBrume = Sort.Sort("Brume: Sortie",0,0,0,99,[Effets.EffetRetireEtat("Invisible",cibles_possibles="Allies|Lanceur")],[],0, 99,99,0,0,"cercle",False)
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Brume",101,3,1,3,[Effets.EffetGlyphe(activationBrume,activationBrume,sortieBrume, 2,"Brume",(255,0,255),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)],[],0,1,1,4,0,"cercle",True,description="""Pose un glyphe-aura qui rend invisible les alliés présents dans la zone.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Poison insidieux",3,3,1,4,[Effets.EffetEtat(Etats.EtatEffetDebutTour("Poison insidieux",0,2,Effets.EffetDegats(6,7,"Air"),"Poison insidieux","lanceur"))],[Effets.EffetEtat(Etats.EtatEffetDebutTour("Poison insidieux",0,2,Effets.EffetDegats(8,9,"Air"),"Poison insidieux","lanceur"))],15,99,1,0,1,"ligne",False,description="""Empoisonne la cible pendant 2 tours en occasionnant des dommages Air.""", chaine=True),

                Sort.Sort("Poison insidieux",35,3,1,4,[Effets.EffetEtat(Etats.EtatEffetDebutTour("Poison insidieux",0,2,Effets.EffetDegats(8,9,"Air"),"Poison insidieux","lanceur"))],[Effets.EffetEtat(Etats.EtatEffetDebutTour("Poison insidieux",0,2,Effets.EffetDegats(10,11,"Air"),"Poison insidieux","lanceur"))],15,99,1,0,1,"ligne",False,description="""Empoisonne la cible pendant 2 tours en occasionnant des dommages Air.""", chaine=True),

                Sort.Sort("Poison insidieux",67,3,1,4,[Effets.EffetEtat(Etats.EtatEffetDebutTour("Poison insidieux",0,2,Effets.EffetDegats(10,11,"Air"),"Poison insidieux","lanceur"))],[Effets.EffetEtat(Etats.EtatEffetDebutTour("Poison insidieux",0,2,Effets.EffetDegats(12,13,"Air"),"Poison insidieux","lanceur"))],15,99,1,0,1,"ligne",False,description="""Empoisonne la cible pendant 2 tours en occasionnant des dommages Air.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Toxines",115,3,1,7,[
                    Effets.EffetRetireEtat("Toxines", zone=Zones.TypeZoneInfini()),
                    Effets.EffetEtat(Etats.EtatEffetDebutTour("Toxines",0,2,Effets.EffetDegats(10,11,"Air"),"Toxines","lanceur")),
                    Effets.EffetEtatSelf(Etats.EtatEffetSiPiegeDeclenche("Toxines",0,2,Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Toxines",0,-1,"Toxines",10)),"Toxines","lanceur","lanceur"), etat_requis_cibles="Toxines"),
                    Effets.EffetEtatSelf(Etats.EtatEffetSiPiegeDeclenche("Toxines",0,2,Effets.EffetSetDureeEtat("Toxines",0,2,zone=Zones.TypeZoneInfini()),"Toxines","lanceur","declencheur"), etat_requis_cibles="Toxines")
                ],[],0,1,1,2,1,"cercle",True,description="""L'ennemi ciblé subit un poison Air pendant 2 tours.
            Si la cible subit un piège alors qu'elle est sous les effets de Toxines, les dommages du poison sont augmentés et sa durée est réinitialisée.
            Il ne peut y avoir qu'un seul ennemi sous l'effet de Toxines.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
	            Sort.Sort("Fourvoiement",6,4,0,0,[
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"erosion",10),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",-30),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",30)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",-30),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",30)),
                    Effets.EffetDegats(11,14,"Air",cibles_exclues="Lanceur",zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetDegats(11,14,"Terre",cibles_exclues="Lanceur",zone=Zones.TypeZoneCroix(1))
                    ],
                    [
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"erosion",10),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",-40),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",40)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",-40),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",40)),
                    Effets.EffetDegats(15,18,"Air",cibles_exclues="Lanceur",zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetDegats(15,18,"Terre",cibles_exclues="Lanceur",zone=Zones.TypeZoneCroix(1))
                    ],5,2,99,0,0,"cercle",False,description="""Occasionne des dommages Air et Terre.
            Vole de l'Agilité et de la Force.
            Applique de l'érosion.""", chaine=True),

                Sort.Sort("Fourvoiement",42,4,0,0,[
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"erosion",10),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",-40),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",40)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",-40),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",40)),
                    Effets.EffetDegats(14,17,"Air",zone=Zones.TypeZoneCroix(1),cibles_exclues="Lanceur"),
                    Effets.EffetDegats(14,17,"Terre",zone=Zones.TypeZoneCroix(1),cibles_exclues="Lanceur")
                    ],
                    [
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"erosion",10),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",-50),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",50)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",-50),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",50)),
                    Effets.EffetDegats(18,21,"Air",zone=Zones.TypeZoneCroix(1),cibles_exclues="Lanceur"),
                    Effets.EffetDegats(18,21,"Terre",zone=Zones.TypeZoneCroix(1),cibles_exclues="Lanceur")
                    ],5,2,99,0,0,"cercle",False,description="""Occasionne des dommages Air et Terre.
            Vole de l'Agilité et de la Force.
            Applique de l'érosion.""", chaine=True),

                Sort.Sort("Fourvoiement",74,4,0,0,[
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"erosion",10),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",-50),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",50)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",-50),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",50)),
                    Effets.EffetDegats(17,20,"Air",zone=Zones.TypeZoneCroix(1),cibles_exclues="Lanceur"),
                    Effets.EffetDegats(17,20,"Terre",zone=Zones.TypeZoneCroix(1),cibles_exclues="Lanceur")
                    ],
                    [
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"erosion",10),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",-60),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"agi",60)),
                    Effets.EffetEtat(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",-60),cibles_exclues="Lanceur", zone=Zones.TypeZoneCroix(1)),
                    Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Fourvoiement",0,3,"fo",60)),
                    Effets.EffetDegats(21,24,"Air",zone=Zones.TypeZoneCroix(1),cibles_exclues="Lanceur"),
                    Effets.EffetDegats(21,24,"Terre",zone=Zones.TypeZoneCroix(1),cibles_exclues="Lanceur")
                    ],5,2,99,0,0,"cercle",False,description="""Occasionne des dommages Air et Terre.
            Vole de l'Agilité et de la Force.
            Applique de l'érosion.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
	            Sort.Sort("Pillage",120,3,1,1,[Effets.EffetEtat(Etats.EtatEffetSiSubit('Etat temporaire',0,1,Effets.EffetSoinSelonSubit(50,zone=Zones.TypeZoneCercle(3),cibles_possibles="Allies"),"Pillage","lanceur","cible")),Effets.EffetDegats(34,38,"Eau"),Effets.EffetRetireEtat('Etat temporaire')],[Effets.EffetEtat(Etats.EtatEffetSiSubit('Etat temporaire',0,1,Effets.EffetSoinSelonSubit(50,zone=Zones.TypeZoneCercle(3)),"Pillage","lanceur","cible")),Effets.EffetDegats(40,44,"Eau"),Effets.EffetRetireEtat('Etat temporaire')],15,3,2,0,0,"cercle",False,description="""Occasionne des dommages Eau.
                50% des dommages sont distribués sous forme de soin aux alliés à 3 cellules ou moins de la cible.
                N'affecte pas le lanceur.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Coup Sournois",9,3,1,3,[Effets.EffetDegats(18,21,"Feu"),Effets.EffetPousser(2)],[Effets.EffetDegats(22,25,"Feu"),Effets.EffetPousser(2)],15,3,2,0,0,"ligne",True,description="""Occasionne des dommages Feu sur les ennemis.
            Pousse la cible.""", chaine=True),

                Sort.Sort("Coup Sournois",47,3,1,3,[Effets.EffetDegats(22,25,"Feu"),Effets.EffetPousser(2)],[Effets.EffetDegats(26,29,"Feu"),Effets.EffetPousser(2)],15,3,2,0,0,"ligne",True,description="""Occasionne des dommages Feu sur les ennemis.
            Pousse la cible.""", chaine=True),

                Sort.Sort("Coup Sournois",87,3,1,4,[Effets.EffetDegats(26,29,"Feu"),Effets.EffetPousser(3)],[Effets.EffetDegats(31,34,"Feu"),Effets.EffetPousser(3)],15,3,2,0,0,"ligne",True,description="""Occasionne des dommages Feu sur les ennemis.
            Pousse la cible.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Coupe-gorge",125,4,1,7,[Effets.EffetDegats(34,38,"Feu"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Coupe-gorge",0,2,"doPiegesPui",250))],[Effets.EffetDegats(40,44,"Feu"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Coupe-gorge",0,2,"doPiegesPui",250))],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Feu et augmente la puissance des pièges.""", chaine=True)
            ]))
            activationDoubleComplot2 = Sort.Sort("Complot",0,0,0,99,[Effets.EffetEchangePlace(zone=Zones.TypeZoneInfini(),cibles_possibles="Invocateur"),Effets.EffetTue(zone=Zones.TypeZoneInfini(),cibles_possibles="Lanceur")],[],0,1,1,0,0,"cercle",False,description="Echange de place avec son invocateur, tue l'invocation")
            activationDoubleComplot = Sort.Sort("Complot",0,0,0,99,[Effets.EffetEtatSelf(Etats.EtatEffetFinTour("Explosion Double",0,2,Effets.EffetEntiteLanceSort("Double",activationDoubleComplot2),"Explosion Double","lanceur"))],[],0,1,1,0,0,"cercle",False,description="Echange de place avec son invocateur, tue l'invocation")
            activationComploteurComplot2 = Sort.Sort("Complot",0,0,0,99,[Effets.EffetDegats(39,41,"Neutre",zone=Zones.TypeZoneCercleSansCentre(1)),Effets.EffetTue(zone=Zones.TypeZoneInfini(),cibles_possibles="Lanceur")],[],0,1,1,0,0,"cercle",False,description="Echange de place avec son invocateur, tue l'invocation", chaine=False)
            activationComploteurComplot = Sort.Sort("Complot",0,0,0,99,[Effets.EffetEtatSelf(Etats.EtatEffetFinTour("Explosion Comploteur",0,2,Effets.EffetEntiteLanceSort("Comploteur",activationComploteurComplot2),"Explosion Comploteur","lanceur"))],[],0,1,1,0,0,"cercle",False,description="Echange de place avec son invocateur, tue l'invocation")
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Double",13,3,1,2,[Effets.EffetInvoque("Double",True,cibles_possibles="", faire_au_vide=True),Effets.EffetDouble()],[],0,1,1,6,0,"ligne",True,description="""Invoque un double contrôlable qui possède les mêmes caractéristiques que l'invocateur.
            N'attaque pas et meurt au bout de 2 tours en échangeant de place avec son invocateur.""", chaine=True),

                Sort.Sort("Double",54,3,1,2,[Effets.EffetInvoque("Double",True,cibles_possibles="", faire_au_vide=True),Effets.EffetDouble()],[],0,1,1,5,0,"ligne",True,description="""Invoque un double contrôlable qui possède les mêmes caractéristiques que l'invocateur.
            N'attaque pas et meurt au bout de 2 tours en échangeant de place avec son invocateur.""", chaine=True),

                Sort.Sort("Double",94,3,1,2,[Effets.EffetInvoque("Double",True,cibles_possibles="", faire_au_vide=True),Effets.EffetDouble(),Effets.EffetEtat(Etats.EtatActiveSort("Complot",2,1,activationDoubleComplot))],[],0,1,1,4,0,"ligne",True,description="""Invoque un double contrôlable qui possède les mêmes caractéristiques que l'invocateur.
            N'attaque pas et meurt au bout de 2 tours en échangeant de place avec son invocateur.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Comploteur",130,3,1,2,[Effets.EffetInvoque("Comploteur",True,cibles_possibles="", faire_au_vide=True),Effets.EffetDouble(),Effets.EffetEtat(Etats.EtatActiveSort("Complot",2,1,activationComploteurComplot)),Effets.EffetEtat(Etats.EtatEffetSiPiegeDeclenche("Comploteur",0,-1,Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("ComplotBoost",0,-1,"Complot",14),cumulMax=4),"Complot","porteur","porteur"))],[],0,1,1,4,0,"cercle",True,description="""Invoque un Double contrôlable.
            Chaque piège déclenché augmente la Puissance du Double.
            Il meurt après 2 tours.
            Il occasionne des dommages Neutre en zone autour de lui lorsqu'il meurt.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Piège Fangeux",17,3,1,4,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeFangeux,"Piège Fangeux",(0,0,255),faire_au_vide=True)],[],0,1,99,0,1,"cercle",True,description="""Pose un piège qui occasionne des dommages Eau.
            Les alliés à proximité de la cible sont soignés à hauteur de 50% des dommages occasionnés.""", chaine=True),

                Sort.Sort("Piège Fangeux",58,3,1,6,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeFangeux,"Piège Fangeux",(0,0,255),faire_au_vide=True)],[],0,1,99,0,1,"cercle",True,description="""Pose un piège qui occasionne des dommages Eau.
            Les alliés à proximité de la cible sont soignés à hauteur de 50% des dommages occasionnés.""", chaine=True),

                Sort.Sort("Piège Fangeux",102,3,1,8,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeFangeux,"Piège Fangeux",(0,0,255),faire_au_vide=True)],[],0,2,99,0,1,"cercle",True,description="""Pose un piège qui occasionne des dommages Eau.
            Les alliés à proximité de la cible sont soignés à hauteur de 50% des dommages occasionnés.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Larcin",135,4,0,0,[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Larcin",0,2,"cha",-80),cibles_exclues="Lanceur",zone=Zones.TypeZoneCroixDiagonale(1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Larcin",0,2,"cha",80),cibles_exclues="Lanceur",zone=Zones.TypeZoneCroixDiagonale(1)),Effets.EffetDegats(40,44,"Eau",cibles_exclues="Lanceur",zone=Zones.TypeZoneCroixDiagonale(1))],[Effets.EffetEtat(Etats.EtatBoostCaracFixe("Larcin",0,2,"cha",-100),cibles_exclues="Lanceur",zone=Zones.TypeZoneCroixDiagonale(1)),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Larcin",0,2,"cha",100),cibles_exclues="Lanceur",zone=Zones.TypeZoneCroixDiagonale(1)),Effets.EffetDegats(44,48,"Eau",cibles_exclues="Lanceur",zone=Zones.TypeZoneCroixDiagonale(1))],25,2,99,0,0,"cercle",False,description="""Occasionne des dommages Eau et vole de la Chance.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
	            Sort.Sort("Piège de Masse",22,4,1,3,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeDeMasse,"Piège de Masse",(50,50,30),faire_au_vide=True)],[],0,2,99,0,1,"cercle",False,description="""Pose un piège mono-cellule qui occasionne des dommages Terre en zone.""", chaine=True),

                Sort.Sort("Piège de Masse",65,4,1,4,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeDeMasse,"Piège de Masse",(50,50,30),faire_au_vide=True)],[],0,2,99,0,1,"cercle",False,description="""Pose un piège mono-cellule qui occasionne des dommages Terre en zone.""", chaine=True),

                Sort.Sort("Piège de Masse",108,4,1,5,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeDeMasse,"Piège de Masse",(50,50,30),faire_au_vide=True)],[],0,2,99,0,1,"cercle",False,description="""Pose un piège mono-cellule qui occasionne des dommages Terre en zone.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Traquenard",140,3,1,1,[Effets.EffetDegats(30,34,"Terre"),Effets.EffetRetireEtat("Traquenard")],[Effets.EffetDegats(33,37,"Terre"),Effets.EffetRetireEtat("Traquenard")],5,3,2,0,0,"ligne",False,description="""Occasionne des dommages Terre. Chaque piège déclenché augmente la portée de Traquenard.
            Le bonus de portée disparaît quand le sort est lancé.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Cruauté",27,3,1,5,[Effets.EffetDegats(12,14,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Cruauté",0,1,"PM",1))],[Effets.EffetDegats(16,18,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Cruauté",0,1,"PM",1))],5,2,99,0,1,"cercle",True,description="""Occasionne des dommages Eau et augmente les PM du lanceur.""", chaine=True),

                Sort.Sort("Cruauté",72,3,1,6,[Effets.EffetDegats(15,17,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Cruauté",0,1,"PM",1))],[Effets.EffetDegats(19,21,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Cruauté",0,1,"PM",1))],5,2,99,0,1,"cercle",True,description="""Occasionne des dommages Eau et augmente les PM du lanceur.""", chaine=True),

                Sort.Sort("Cruauté",118,3,1,7,[Effets.EffetDegats(18,20,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Cruauté",0,1,"PM",1))],[Effets.EffetDegats(22,24,"Eau"),Effets.EffetEtatSelf(Etats.EtatBoostCaracFixe("Cruauté",0,1,"PM",1))],5,2,99,0,1,"cercle",True,description="""Occasionne des dommages Eau et augmente les PM du lanceur.""", chaine=True)
            ]))
            activationGuetApens = Sort.Sort("Activation Guet-apens",145,0,0,99,[Effets.EffetAttire(2,"Lanceur","JoueurCaseEffet",zone=Zones.TypeZoneInfini(),etat_requis_cibles="Guet-Apens",consomme_etat=True)],[],0,99,99,0,0,"cercle",False,description="""Occasionne des dommages Feu et attire la cible vers le Double.""", chaine=True)
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Guet-apens",145,3,1,5,[Effets.EffetDegats(30,34,"Feu"),Effets.EffetEtat(Etats.Etat("Guet-Apens",0,-1)),Effets.EffetEntiteLanceSort("Double|Comploteur",activationGuetApens)],[Effets.EffetDegats(34,38,"Feu"),Effets.EffetAttire(2,"JoueurCaseEffet","Lanceur",zone=Zones.TypeZoneInfini(),cibles_possibles="Double|Comploteur")],15,3,2,0,0,"cercle",True,description="""Occasionne des dommages Feu et attire la cible vers le Double.""", chaine=True)
            ]))
            
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Piège Empoisonné",32,3,1,3,[Effets.EffetPiege(Zones.TypeZoneCroix(1),activationPiegeEmpoisonne,"Piège Empoisonné",(120,120,120),faire_au_vide=True)],[],0,1,1,3,1,"cercle",False,description="""Empoisonne la cible en occasionnant des dommages Air pendant 3 tours.""", chaine=True),

                Sort.Sort("Piège Empoisonné",81,3,1,3,[Effets.EffetPiege(Zones.TypeZoneCroix(1),activationPiegeEmpoisonne,"Piège Empoisonné",(120,120,120),faire_au_vide=True)],[],0,1,1,3,1,"cercle",False,description="""Empoisonne la cible en occasionnant des dommages Air pendant 3 tours.""", chaine=True),

                Sort.Sort("Piège Empoisonné",124,3,1,4,[Effets.EffetPiege(Zones.TypeZoneCroix(1),activationPiegeEmpoisonne,"Piège Empoisonné",(120,120,120),faire_au_vide=True)],[],0,1,1,2,1,"cercle",False,description="""Empoisonne la cible en occasionnant des dommages Air pendant 3 tours.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Injection Toxique",150,5,1,5,[
                    Effets.EffetRetireEtat("Injection Toxique",zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur"),Effets.EffetEtat(Etats.EtatEffetDebutTour("Injection Toxique",0,3,Effets.EffetDegats(28,32,"Air"),"Injection Toxique","lanceur"))],
                    [ Effets.EffetRetireEtat("Injection Toxique",zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur"),Effets.EffetEtat(Etats.EtatEffetDebutTour("Injection Toxique",0,3,Effets.EffetDegats(34,38,"Air"),"Injection Toxique","lanceur"))],5,1,1,5,0,"cercle",True,description="""Applique un poison Air sur la cible. Chaque piège déclenché réduit le temps de relance d'Injection Toxique.
            La réduction du temps de relance disparaît quand le sort est lancé.""", chaine=False)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Concentration de Chakra",38,2,1,4,[Effets.EffetEtat(Etats.EtatEffetSiPiegeDeclenche('Concentration de Chakra',0,1,Effets.EffetVolDeVie(15,15,"Feu"),"Concentration de Chakra","lanceur","porteur"))],[],0,1,1,4,0,"ligne",True,description="""Vole de la vie dans l'élément Feu lorsque la cible déclenche un piège.""", chaine=True),

                Sort.Sort("Concentration de Chakra",90,2,1,5,[Effets.EffetEtat(Etats.EtatEffetSiPiegeDeclenche('Concentration de Chakra',0,1,Effets.EffetVolDeVie(15,15,"Feu"),"Concentration de Chakra","lanceur","porteur"))],[],0,1,1,3,0,"ligne",True,description="""Vole de la vie dans l'élément Feu lorsque la cible déclenche un piège.""", chaine=True),

                Sort.Sort("Concentration de Chakra",132,2,1,6,[Effets.EffetEtat(Etats.EtatEffetSiPiegeDeclenche('Concentration de Chakra',0,1,Effets.EffetVolDeVie(15,15,"Feu"),"Concentration de Chakra","lanceur","porteur"))],[],0,1,1,2,0,"ligne",True,description="""Vole de la vie dans l'élément Feu lorsque la cible déclenche un piège.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Piège à Fragmentation",155,4,1,8,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeAFragmentation,"Piège à Fragmentation",(120,0,0),faire_au_vide=True)],[],0,1,99,0,1,"cercle",True,description="""Pose un piège mono-cellule qui inflige des dommages Feu.
            Les dommages augmentent en fonction de la distance avec le centre de la zone d'effet.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Piège d'Immobilisation",44,4,1,4,[Effets.EffetPiege(Zones.TypeZoneCercle(2),activationPiegeDimmobilisation,"Piège d'Immobilisation",(120,0,120),faire_au_vide=True)],[],0,1,1,7,1,"ligne",False,description="""Retire des PM.""", chaine=True),

                Sort.Sort("Piège d'Immobilisation",97,4,1,4,[Effets.EffetPiege(Zones.TypeZoneCercle(3),activationPiegeDimmobilisation,"Piège d'Immobilisation",(120,0,120),faire_au_vide=True)],[],0,1,1,6,1,"ligne",False,description="""Retire des PM.""", chaine=True),

                Sort.Sort("Piège d'Immobilisation",137,4,1,5,[Effets.EffetPiege(Zones.TypeZoneCercle(3),activationPiegeDimmobilisation,"Piège d'Immobilisation",(120,0,120),faire_au_vide=True)],[],0,1,1,5,1,"ligne",False,description="""Retire des PM.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Piège de Dérive",160,2,1,6,[Effets.EffetPiege(Zones.TypeZoneCroixDiagonale(1),activationPiegeDeDerive,"Piège de Dérive",(0,0,120),faire_au_vide=True)],[],0,1,1,2,1,"cercle",False,description="""Pose un piège qui pousse de 2 cases.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Piège Insidieux",50,3,1,4,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeInsidieux,"Piège Insidieux",(0,200,0),faire_au_vide=True)],[],0,2,99,0,1,"cercle",False,description="""Pose un piège. Une fois déclenché, les ennemis qui terminent leur tour dans sa zone d'effet subissent des dommages Air.""", chaine=True),

                Sort.Sort("Piège Insidieux",103,3,1,5,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeInsidieux,"Piège Insidieux",(0,200,0),faire_au_vide=True)],[],0,2,99,0,1,"cercle",False,description="""Pose un piège. Une fois déclenché, les ennemis qui terminent leur tour dans sa zone d'effet subissent des dommages Air.""", chaine=True),

                Sort.Sort("Piège Insidieux",143,3,1,6,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeInsidieux,"Piège Insidieux",(0,200,0),faire_au_vide=True)],[],0,2,99,0,1,"cercle",False,description="""Pose un piège. Une fois déclenché, les ennemis qui terminent leur tour dans sa zone d'effet subissent des dommages Air.""", chaine=True)
            ]))
            effetPoisonEpidemie = Effets.EffetEtat(Etats.EtatEffetFinTour("Poison Épidémie",0,1,Effets.EffetDegats(38,42,"Air"),"Poison Épidémie","lanceur"), cibles_possibles="Ennemis")
            etatPropageEpidemie = Etats.EtatEffetFinTour("Propagation Épidémie",0,1,Effets.EffetEtat(Etats.EtatEffetFinTour("Propagation Poison Épidémie",0,1,Effets.EffetDegats(38,42,"Air"),"Propagation Poison Épidémie","lanceur"), cibles_possibles="Ennemis",zone=Zones.TypeZoneCercleSansCentre(2)),"Propagation Épidémie","lanceur")
            effetPropagationEpidemie = Effets.EffetEtat(etatPropageEpidemie, cibles_possibles="Ennemis")
            effetPropagationPropagationEpidemie = Effets.EffetEtat(Etats.EtatEffetFinTour("Continue Épidémie",0,1,Effets.EffetEtat(etatPropageEpidemie,zone=Zones.TypeZoneCercleSansCentre(2)),"Continue Épidémie","lanceur"), cibles_possibles="Ennemis")
           
            effetPoisonEpidemieCC = Effets.EffetEtat(Etats.EtatEffetFinTour("Poison Épidémie",0,1,Effets.EffetDegats(46,50,"Air"),"Poison Épidémie","lanceur"), cibles_possibles="Ennemis")
            etatPropageEpidemieCC = Etats.EtatEffetFinTour("Propagation Épidémie",0,1,Effets.EffetEtat(Etats.EtatEffetFinTour("Propagation Poison Épidémie",0,1,Effets.EffetDegats(46,50,"Air"),"Propagation Poison Épidémie","lanceur"), cibles_possibles="Ennemis",zone=Zones.TypeZoneCercleSansCentre(2)),"Propagation Épidémie","lanceur")
            effetPropagationEpidemieCC = Effets.EffetEtat(etatPropageEpidemieCC, cibles_possibles="Ennemis")
            effetPropagationPropagationEpidemieCC = Effets.EffetEtat(Etats.EtatEffetFinTour("Continue Épidémie",0,1,Effets.EffetEtat(etatPropageEpidemieCC,zone=Zones.TypeZoneCercleSansCentre(2)),"Continue Épidémie","lanceur"), cibles_possibles="Ennemis")
            
            epidemie=Sort.Sort("Épidémie",165,4,1,5,[effetPropagationEpidemie,effetPropagationPropagationEpidemie,effetPoisonEpidemie],[
                effetPropagationEpidemieCC,effetPropagationPropagationEpidemieCC,effetPoisonEpidemieCC
                ],5,2,1,0,0,"ligne",True, description="""Applique un poison Air de fin de tour sur les ennemis.
            La cible propage le poison en zone autour d'elle.""", chaine=True)
            sorts.append(Personnage.getSortRightLvl(lvl,[epidemie]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Piège répulsif",56,3,1,3,[Effets.EffetPiege(Zones.TypeZoneCercle(1),activationPiegeRepulsif,"Piège répulsif",(255,0,255),faire_au_vide=True)],[],0,1,1,1,1,"cercle",False,description="""Repousse les alliés et les ennemis.
            Occasionne des dommages Air aux ennemis.""", chaine=True),

                Sort.Sort("Piège répulsif",112,3,1,5,[Effets.EffetPiege(Zones.TypeZoneCercle(1),activationPiegeRepulsif,"Piège répulsif",(255,0,255),faire_au_vide=True)],[],0,1,1,1,1,"cercle",False,description="""Repousse les alliés et les ennemis.
            Occasionne des dommages Air aux ennemis.""", chaine=True),

                Sort.Sort("Piège répulsif",147,3,1,7,[Effets.EffetPiege(Zones.TypeZoneCercle(1),activationPiegeRepulsif,"Piège répulsif",(255,0,255),faire_au_vide=True)],[],0,1,1,1,1,"cercle",False,description="""Repousse les alliés et les ennemis.
            Occasionne des dommages Air aux ennemis.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Piège Repoussant",170,2,1,6,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationPiegeRepoussant,"Piège Repoussant",(0,100,20),faire_au_vide=True)],[],0,2,99,0,1,"cercle",False,description="""Piège mono-cellule qui repousse de 2 cases en zone.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
                Sort.Sort("Peur",62,2,2,3,[Effets.EffetPousserJusque(faire_au_vide=True)],[],0,99,99,0,0,"ligne",False,description="""Pousse un allié ou un ennemi sur la cellule ciblée.""", chaine=True),

                Sort.Sort("Peur",116,2,2,5,[Effets.EffetPousserJusque(faire_au_vide=True)],[],0,99,99,0,0,"ligne",False,description="""Pousse un allié ou un ennemi sur la cellule ciblée.""", chaine=True),

                Sort.Sort("Peur",153,2,2,7,[Effets.EffetPousserJusque(faire_au_vide=True)],[],0,99,99,0,0,"ligne",False,description="""Pousse un allié ou un ennemi sur la cellule ciblée.""", chaine=True)
            ]))
            sorts.append(Personnage.getSortRightLvl(lvl,[
            Sort.Sort("Méprise",175,3,1,4,[Effets.EffetEchangePlace("cible",zone=Zones.TypeZoneInfini(),cibles_possibles="Double|Comploteur"), Effets.EffetRetireEtat("Invisible",zone=Zones.TypeZoneInfini(),cibles_possibles="Lanceur")],[],0,1,99,0,0,"ligne",True,description="""La cible échange de place avec le Double.
                Dissipe l'invisibilité du lanceur.""", chaine=True)
            ]))
                        
        sorts.append(Sort.Sort("Cawotte",0,4,1,6,[Effets.EffetInvoque("Cawotte",False,cibles_possibles="", faire_au_vide=True)],[],0, 1,1,6,0,"cercle",True,description="Invoque une Cawotte")) 
        total_nb_sorts = len(sorts)
        i = 0
        while i < total_nb_sorts:
            if sorts[i] is None:
                sorts.remove(sorts[i])
                total_nb_sorts-=1
                i-=1
            i+=1
        return sorts, sortsDebutCombat

    def LancerSortsDebutCombat(self, niveau):
        for sort in self.sortsDebutCombat:
            sort.lance(self.posX,self.posY,niveau, self.posX, self.posY)

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
                for joueur in niveau.joueurs:
                    for etat in joueur.etats:
                        if etat.actif():
                            etat.triggerAvantPiegeDeclenche(niveau,piege, self, joueur)
                
                for effet in piege.effets: 
                    sestApplique, cibles = niveau.lancerEffet(effet,piege.centre_x,piege.centre_y,piege.nomSort, piege.centre_x,piege.centre_y,piege.lanceur)          
                i-=1
                niveau.pieges.remove(piege)
            i+=1
            nbPieges = len(niveau.pieges)
        # Verifie les entrées et sorties de glyphes:
        for glyphe in niveau.glyphes:
            if glyphe.actif():
                # Test Entre dans la glyphe
                if glyphe.sortDeplacement.APorte(glyphe.centre_x, glyphe.centre_y,self.posX,self.posY, 0):
                    for effet in glyphe.sortDeplacement.effets:
                        niveau.lancerEffet(effet,glyphe.centre_x,glyphe.centre_y,glyphe.nomSort, self.posX, self.posY, glyphe.lanceur)
                else: # n'est pas dans la glyphe
                    dernierePos = self.historiqueDeplacement[-1]
                    # Test s'il était dans la glyphe avant
                    
                    if glyphe.sortDeplacement.APorte(glyphe.centre_x, glyphe.centre_y,dernierePos[0],dernierePos[1], 0):
                        for effet in glyphe.sortSortie.effets:
                            niveau.lancerEffet(effet,glyphe.centre_x,glyphe.centre_y,glyphe.nomSort, self.posX, self.posY, glyphe.lanceur)
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
                print(self.nomPerso+" sort de l'etat "+self.etats[i].nom)
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

    def soigne(self, soigneur, niveau, soins, shouldprint=True):
        """@summary: subit des dégâts de combats. Active les triggers d'états triggerAvantSubirDegats et triggerApresSubirDegats
        @soigneur: Le joueur soignant
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau
        @soins: Le nombre de points de soins calculés
        @type: int
        """
        self.vie += soins
        if shouldprint:
            print("+"+str(soins)+" PV")

    def subit(self,attaquant, niveau, degats,typeDegats, shouldprint=True):
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
        toprint = self.nomPerso+" a "+str(self.vie) +"/"+str(self._vie)+" PV"
        if pb_restants > 0:
            toprint+= " et "+str(pb_restants)+" PB"
        if shouldprint:
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
        niveau.rafraichirEtats(self)
        niveau.rafraichirGlyphes(self)
        niveau.rafraichirRunes(self)
        self.rafraichirHistoriqueDeplacement()
        for etat in self.etats:
            if etat.actif():
                etat.triggerDebutTour(self,niveau)

        self.posDebTour = [self.posX, self.posY]
        niveau.depileEffets()
        niveau.afficherSorts()
        print("Debut de tour de "+str(self.nomPerso)+".")
        print("PA : "+str(self.PA))
        print("PM : "+str(self.PM))
        print("PV : "+str(self.vie))


    def appliquerEtat(self,etat,lanceur, cumulMax=-1, niveau=None):
        """@summary: Applique un nouvel état sur le Personnage. Active le trigger d'état triggerInstantane
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
        print(self.nomPerso+"  etat "+etat.nom+" ("+str(etat.duree)+" tours)")
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
            niveau.rafraichirEtats(self,False)

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
                            print("Sort selectionne "+str(sortSelectionne))
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
                            if etat.actif():
                                print(joueurInfo.nomPerso+" est dans l'etat "+etat.nom+" ("+str(etat.duree)+")")
                            elif etat.debuteDans > 0:
                                print(joueurInfo.nomPerso+" sera dans l'etat "+etat.nom+" dans "+str(etat.debuteDans)+" tour(s)")    
                    if sortSelectionne != None:
                        sortSelectionne = None
        return sortSelectionne

class PersonnageMur(Personnage):
    """@summary: Classe décrivant un montre de type MUR immobile (cawotte, cadran de Xelor...). hérite de Personnage"""
    def __init__(self, *args):
        """@summary: Initialise un personnage Mur, même initialisation que Personange
        @args: les arguments donnés, doivent être les mêmes que Personnage
        @type:*args"""
        super(PersonnageMur, self).__init__(*args)
    def deepcopy(self):
        """@summary: Clone le personnageMur
        @return: le clone"""
        cp = PersonnageMur(self.nomPerso, self.classe, self.lvl, self.team, self.caracsPrimaires, self.caracsSecondaires, self.dommages, self.resistances ,self.icone)
        cp.sorts, cp.sortsDebutCombat = Personnage.ChargerSorts(cp.classe, cp.lvl)
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
        print("Tour de "+(niveau.tourDe.nomPerso))
        niveau.finTour()

class PersonnageSansPM(Personnage):
    """@summary: Classe décrivant un personange pouvant faire des actions mais sans chercher à se déplacer (Stratege iop). hérite de Personnage"""
    def __init__(self, *args):
        """@summary: Initialise un personnage sans PM, même initialisation que Personange
        @args: les arguments donnés, doivent être les mêmes que Personnage
        @type:*args"""
        super(PersonnageSansPM, self).__init__(*args)
    def deepcopy(self):
        """@summary: Clone le PersonnageSansPM
        @return: le clone"""
        cp = PersonnageSansPM(self.nomPerso,self.classe, self.lvl, self.team, self.caracsPrimaires, self.caracsSecondaires, self.dommages, self.resistances ,self.icone)
        cp.sorts, cp.sortsDebutCombat = Personnage.ChargerSorts(cp.classe, cp.lvl)
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
"Cadran de Xelor" : PersonnageSansPM("Cadran de Xelor","Cadran de Xelor",100,1,{"Vitalite":1000},{},{},{},"cadran_de_xelor.png"),
"Cawotte" : PersonnageMur("Cawotte","Cawotte",0,1,{"Vitalite":800},{},{},{},"cawotte.png"),
"Synchro" : PersonnageMur("Synchro","Synchro",0,1,{"Vitalite":1200},{},{},{},"synchro.png"),
"Complice" : PersonnageMur("Complice","Complice",0,1,{"Vitalite":650},{},{},{},"complice.png"),
"Balise de Rappel" : PersonnageSansPM("Balise de Rappel","Balise de Rappel",0,1,{"Vitalite":1000},{},{},{},"balise_de_rappel.png"),
"Balise Tactique" : PersonnageMur("Balise Tactique","Balise Tactique",0,1,{"Vitalite":1000},{},{},{},"balise_tactique.png"),
"Stratege Iop" : PersonnageMur("Stratege Iop","Stratège Iop",0,1,{"Vitalite":1385},{},{},{},"conquete.png"),
"Double" : Personnage("Double","Double",0,1,{"Vitalite":1},{},{},{},"sram.png"),
"Comploteur" : Personnage("Comploteur","Comploteur",0,1,{"Vitalite":1},{},{},{},"sram.png"),
}
