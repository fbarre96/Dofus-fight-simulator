# -*- coding: utf-8 -*
import zones
import constantes
import pygame
from pygame.locals import *
import Overlays
import Etats
import Effets 

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
        self.posDebCombat = None
        self.invocateur = None
        self.team = int(team)
        if not(icone.startswith("images/")):
            self.icone = ("images/"+icone)
        else:
            self.icone = (icone)
        self.icone=constantes.normaliser(self.icone)
        self.overlay = Overlays.Overlay(self, Overlays.ColoredText("classe",(210,105,30)), Overlays.ColoredText("vie",(224,238,238)),(56,56,56))

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
        retourParadoxe = Sort(u"Retour Paradoxe",0,0,0,[Effets.EffetTpSymCentre(zone=zones.TypeZoneCercle(99),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis_cibles="ParadoxeTemporel",consomme_etat=True)],99,99,0,0,"cercle")
        activationInstabiliteTemporelle = Sort(u"Activation Instabilité Temporelle",0,0,3,[Effets.EffetTeleportePosPrec(1)], 99,99,0,0,"cercle")
        activationParadoxeTemporel = Sort(u"Paradoxe Temporel", 0,0,0,[Effets.EffetTpSymCentre(zone=zones.TypeZoneCercle(4),cibles_possibles="Allies|Ennemis",cibles_exclues=u"Lanceur|Xélor|Synchro"),Effets.EffetEtat(Etats.Etat("ParadoxeTemporel",0,2),zone=zones.TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur|Xelor|Synchro"), Effets.EffetEtatSelf(Etats.EtatActiveSort("RetourParadoxe",1,1,retourParadoxe),cibles_possibles="Lanceur")],99,99,0,0,"cercle")
        if(classe==u"Stratège Iop"):
            sorts.append(Sort("Strategie_iop",0,0,0,[Effets.EffetEtat(Etats.EtatRedistribuerPer("Stratégie Iop",0,-1, 50,"Ennemis|Allies",2))],99,99,0,0,"cercle"))
            return sorts
        elif(classe==u"Cadran de Xélor"):
            sorts.append(Sort("Synchronisation",0,0,0,[Effets.EffetDegats(100,130,"feu",zone=zones.TypeZoneCercleSansCentre(4), cibles_possibles="Ennemis|Lanceur",etat_requis_cibles="Telefrag"),Effets.EffetEtat(Etats.EtatBoostPA("Synchronisation",0,2,2),zone=zones.TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Lanceur",etat_requis_cibles="Telefrag")],99,99,0,0,"cercle"))
            return sorts
        elif(classe==u"Synchro"):
            sorts.append(Sort(u"Début des Temps",0,0,0,[Effets.EffetEtat(Etats.EtatBoostPA("Synchro",1,1,-1),zone=zones.TypeZoneCercle(99),cibles_possibles="Xelor")],99,99,0,0,"cercle"))
            return sorts
        elif(classe==u"Balise de Rappel"):
            sorts.append(Sort("Rappel",0,0,0,[Effets.EffetEchangePlace(zone=zones.TypeZoneCercle(99),cibles_possibles="Cra"), Effets.EffetTue(zone=zones.TypeZoneCercle(99),cibles_possibles="Lanceur")],99,99,0,0,"cercle"))
        elif classe == u"Poutch":
            return sorts
        elif(classe==u"Xélor"):
            sorts.append(Sort(u"Ralentissement",2,1,6,[Effets.EffetDegats(8,9,"eau"),Effets.EffetRetPA(1),Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag")],4,2,0,1,"cercle",description=u"Occasionne des dommages Eau et retire 1 PA à la cible. Retire 1 PA supplémentaire aux ennemis dans l'état Téléfrag. Le retrait de PA ne peut pas être désenvoûté."))
            sorts.append(Sort(u"Souvenir",4,1,6,[Effets.EffetDegats(26,30,"terre"),Effets.EffetTeleportePosPrec(1)], 3,2,0,1,"ligne",description=u"Occasionne des dommages Terre et téléporte la cible à sa position précédente."))
            sorts.append(Sort(u"Aiguille",3,1,8,[Effets.EffetDegats(22,26,"feu"),Effets.EffetRetPA(1),Effets.EffetRetPA(2,etat_requis_cibles="Telefrag",consomme_etat=True)], 3,2,0,1,"cercle", description=u"Occasionne des dommages Feu et retire 1 PA à la cible. Retire des PA supplémentaires aux ennemis dans l'état Téléfrag. Le retrait de PA ne peut pas être désenvoûté. Retire l'état Téléfrag."))
            sorts.append(Sort(u"Rouage",3,1,7,[Effets.EffetDegats(12,14,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostPA("Rouage",1,1,1))], 2,99,0,1,"cercle",chaine=True,description="Occasionne des dommages Eau. Le lanceur gagne 1 PA au tour suivant."))
            sorts.append(Sort(u"Téléportation",2,1,5,[Effets.EffetTpSym()], 1,1,3,0,"cercle",description=u"Téléporte le lanceur symétriquement par rapport à la cible. Le lanceur gagne 2 PA pour 1 tour à chaque fois qu’il génère un Téléfrag. Le temps de relance est supprimé quand un Téléfrag est généré ou consommé. Un Téléfrag est généré lorsqu'une entité prend la place d'une autre."))
            sorts.append(Sort(u"Retour Spontané",1,0,7,[Effets.EffetTeleportePosPrec(1)], 3,3,0,1,"cercle",description=u"La cible revient à sa position précédente."))
            sorts.append(Sort(u"Flétrissement",3,1,6,[Effets.EffetDegats(26,29,"air"),Effets.EffetDegats(10,10,"air",etat_requis_cibles="Telefrag")], 3,2,0,1,"ligne",description=u"Occasionne des dommages Air en ligne. Occasionne des dommages supplémentaires aux ennemis dans l'état Téléfrag."))
            sorts.append(Sort(u"Dessèchement",4,1,6,[Effets.EffetDegats(38,42,"air"),Effets.EffetEtat(Etats.EtatEffetDebutTour(u"Dessèchement", 1,1,Effets.EffetDegats(44,48,"air",cibles_possbiles="Ennemis",zone=zones.TypeZoneCercleSansCentre(2)),"Dessechement","lanceur"))], 3,2,0,0,"ligne",description=u"Occasionne des dommages Air. Au prochain tour du lanceur, la cible occasionne des dommages autour d'elle."))
            sorts.append(Sort(u"Rembobinage",2,0,6,[Effets.EffetEtat(Etats.EtatRetourCaseDepart("Bobine",0,1),cibles_possibles="Allies|Lanceur")], 1,1,3, 0, "ligne",description=u"À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour."))
            sorts.append(Sort(u"Renvoi",3,1,6,[Effets.EffetTeleporteDebutTour()], 1,1,2, 0, "ligne",description=u"Téléporte la cible ennemie à sa cellule de début de tour."))
            sorts.append(Sort(u"Rayon Obscur",5,1,6,[Effets.EffetDegats(37,41,"terre"),Effets.EffetDegats(37,41,"terre",cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag",consomme_etat=True)], 3,2,0,0,"ligne",description=u"Occasionne des dommages Terre en ligne. Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag. Retire l'état Téléfrag."))
            sorts.append(Sort(u"Rayon Ténebreux",3,1,5,[Effets.EffetDegats(19,23,"terre"),Effets.EffetDegats(19,23,"terre",zone=zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")], 3,2,0,1,"ligne",description=u"Occasionne des dommages Terre. Si la cible est dans l'état Téléfrag, occasionne des dommages Terre en zone autour d'elle."))
            sorts.append(Sort(u"Complice",2,1,5,[Effets.EffetInvoque("Complice",cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles=u"Cadran de Xélor|Complice",zone=zones.TypeZoneCercleSansCentre(99))], 1,1,0,0,"cercle",chaine=True,description=u"Invoque un Complice statique qui ne possède aucun sort. Il est tué si un autre Complice est invoqué."))
            sorts.append(Sort(u"Cadran de Xélor",3,1,5,[Effets.EffetInvoque(u"Cadran de Xélor",cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles=u"Cadran de Xélor|Complice",zone=zones.TypeZoneCercleSansCentre(99))], 1,1,4,0,"cercle",chaine=True,description=u"Invoque un Cadran qui occasionne des dommages Feu en zone et retire des PA aux ennemis dans l'état Téléfrag. Donne des PA aux alliés autour de lui et dans l'état Téléfrag."))
            sorts.append(Sort(u"Gelure",2,2,5,[Effets.EffetDegats(11,13,"air",cibles_possibles="Ennemis|Lanceur"), Effets.EffetTeleportePosPrec(1)], 3,2,0,1,"cercle",description=u"Occasionne des dommages Air aux ennemis. Téléporte la cible à sa position précédente."))
            sorts.append(Sort(u"Perturbation",2,1,4,[Effets.EffetDegats(9,11,"feu",cibles_possibles="Ennemis|Lanceur"), Effets.EffetTpSymSelf()], 3,2,0,0,"ligne", chaine=False,description=u"Occasionne des dommages Feu et téléporte la cible symétriquement par rapport au lanceur."))
            sorts.append(Sort(u"Sablier de Xélor",2,1,7,[Effets.EffetDegats(15,17,"feu"),Effets.EffetRetPA(2),Effets.EffetDegats(15,17,"feu",zone=zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")], 3,1,0,1,"ligne",description=u"Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue. Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone. Le retrait de PA ne peut pas être désenvoûté."))
            sorts.append(Sort(u"Distorsion Temporelle",4,0,0,[Effets.EffetDegats(26,30,"air",zone=zones.TypeZoneCarre(1),cibles_possibles="Ennemis"),Effets.EffetTeleportePosPrec(1,zone=zones.TypeZoneCarre(1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur")], 2,1,0,0,"cercle",description=u"Occasionne des dommages Air aux ennemis. Téléporte les cibles à leur position précédente."))
            sorts.append(Sort(u"Vol du Temps",4,1,5,[Effets.EffetDegats(30,34,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostPA("Vol du Temps",1,1,1))], 3,2,0,0,"cercle",chaine=True,description=u"Occasionne des dommages Eau à la cible. Le lanceur gagne 1 PA au début de son prochain tour."))
            sorts.append(Sort(u"Pétrification",5,1,7,[Effets.EffetDegats(34,38,"eau"),Effets.EffetEtatSelf(Etats.EtatCoutPA("Petrification",0,2,u"Petrification",-1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag")], 3,2,0,1,"ligne",description=u"Occasionne des dommages Eau et retire des PA. Si la cible est dans l'état Téléfrag, le coût en PA du sort est réduit pendant 2 tours."))
            sorts.append(Sort(u"Flou",2,1,3,[Effets.EffetEtat(Etats.EtatBoostPA("Flou",0,1,-2),zone=zones.TypeZoneCercle(3),faire_au_vide=True),Effets.EffetEtat(Etats.EtatBoostPA("Flou",1,1,2),zone=zones.TypeZoneCercle(3),faire_au_vide=True)], 1,1,3,0,"cercle",description=u"Retire des PA en zone le tour en cours. Augmente les PA en zone le tour suivant."))
            sorts.append(Sort(u"Conservation",2,0,5,[Effets.EffetEtat(Etats.EtatModDegPer("Conservation",0,1,130),zone=zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur"),Effets.EffetEtat(Etats.EtatModDegPer("Conservation",1,1,70),zone=zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur")], 1,1,2,0,"cercle",description=u"Augmente les dommages subis par l'allié ciblé ou le lanceur de 50%% pour le tour en cours. Au tour suivant, la cible réduit les dommages subis de 30%%."))
            sorts.append(Sort(u"Poussière Temporelle",4,0,6,[Effets.EffetDegats(34,37,"feu",cibles_possibles="Ennemis"), Effets.EffetDegats(34,37,"feu",zone=zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")], 2,2,0,1,"cercle",description=u"Occasionne des dommages Feu. Si la cible est dans l'état Téléfrag, les dommages sont occasionnés en zone et les entités à proximité sont téléportées symétriquement par rapport au centre de la zone d'effet."))
            sorts.append(Sort(u"Suspension Temporelle",3,1,4,[Effets.EffetDureeEtats(1,etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(25,29,"feu")], 3,2,0,0,"ligne",description=u"Occasionne des dommages Feu sur les ennemis. Réduit la durée des effets sur les cibles ennemies dans l'état Téléfrag et retire l'état."))
            sorts.append(Sort(u"Raulebaque",2,0,0,[Effets.EffetTeleportePosPrec(1,zone=zones.TypeZoneCercle(99))], 1,1,2, 0, "cercle",description=u"Replace tous les personnages à leurs positions précédentes."))
            sorts.append(Sort(u"Instabilité Temporelle",3,0,7,[Effets.EffetGlyphe(activationInstabiliteTemporelle,2,u"Instabilité Temporelle",(255,255,0),zone=zones.TypeZoneCercle(3),faire_au_vide=True)], 1,1,3,1,"cercle",description=u"Pose un glyphe qui renvoie les entités à leur position précédente. Les effets du glyphe sont également exécutés lorsque le lanceur génère un Téléfrag."))
            sorts.append(Sort(u"Démotivation",3,1,5,[Effets.EffetDegats(23,26,"terre",cibles_possibles="Ennemis"),Effets.EffetDureeEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True)], 3,2,0,0,"diagonale",description=u"Occasionne des dommages Terre aux ennemis en diagonale. Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état."))
            sorts.append(Sort(u"Pendule",5,1,5,[Effets.EffetTpSym(),Effets.EffetDegatsPosLanceur(48,52,"air",zone=zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis"), Effets.EffetTeleportePosPrecLanceur(1,cibles_possibles="Lanceur")], 2,1,0,0,"cercle",chaine=True,description=u"Le lanceur se téléporte symétriquement par rapport à la cible et occasionne des dommages Air en zone sur sa cellule de destination. Il revient ensuite à sa position précédente."))
            sorts.append(Sort(u"Paradoxe Temporel",3,0,0,[Effets.EffetEntiteLanceSort(u"Complice|Cadran de Xélor",activationParadoxeTemporel)], 1,1,2,0,"cercle",description=u"Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran). Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles. Fixe le temps de relance de Cadran de Xélor et de Complice à 1."))
            sorts.append(Sort(u"Faille Temporelle",3,0,0,[Effets.EffetEchangePlace(zone=zones.TypeZoneCercle(99),cibles_possibles=u"Cadran de Xélor|Complice",generer_TF=True),Effets.EffetEtat(Etats.EtatEffetFinTour("Retour faille temporelle", 1,1,Effets.EffetTeleportePosPrec(1),"Fin faille Temporelle","cible")), Effets.EffetEtat(Etats.Etat("Faille_temporelle",0,1),zone=zones.TypeZoneCercle(99),cibles_possibles="Xelor")], 1,1,3,0,"cercle",description=u"Le lanceur échange sa position avec celle du Complice (ou du Cadran). À la fin du tour, le Complice (ou le Cadran) revient à sa position précédente. La Synchro ne peut pas être déclenchée pendant la durée de Faille Temporelle."))
            sorts.append(Sort(u"Synchro",2,1,4,[Effets.EffetInvoque("Synchro",cibles_possibles="",faire_au_vide=True)], 1,1,3,0,"cercle",description=u"Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour. La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag. Elle n'est pas affectée par les effets de Rembobinage. À partir du tour suivant son lancer, son invocateur perd 1 PA."))
            sorts.append(Sort(u"Contre",2,0,6,[Effets.EffetEtat(Etats.EtatContre("Contre",0,2, 50,1),zone=zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur")], 1,1,5,0,"cercle", description=u"Renvoie une partie des dommages subis en mêlée à l'attaquant."))
            sorts.append(Sort(u"Bouclier Temporel",3,0,3,[Effets.EffetEtat(Etats.EtatEffetSiSubit("Bouclier temporel",0,1, Effets.EffetTeleportePosPrec(1),"Bouclier Temporel","lanceur",""))], 1,1,3,0,"cercle",description=u"Si la cible subit des dommages, son attaquant revient à sa position précédente."))
            sorts.append(Sort(u"Fuite",1,0,5,[Effets.EffetEtat(Etats.EtatEffetDebutTour("Fuite", 1,1,Effets.EffetTeleportePosPrec(1),"Fuite","cible"))], 4,2,0,0,"cercle",description=u"Téléporte la cible sur sa position précédente au début du prochain tour du lanceur."))
            sorts.append(Sort(u"Horloge",5,1,6,[Effets.EffetVolDeVie(36,39,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostPA("Horloge",1,1,1)),Effets.EffetRetPA(4,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)], 3,2,0,0,"ligne", chaine=True,description=u"Vole de vie dans l'élément Eau. Le lanceur gagne 1 PA au début de son prochain tour. Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état. Le retrait de PA ne peut pas être désenvoûté."))
            sorts.append(Sort(u"Clepsydre",4,1,3,[Effets.EffetDegats(30,34,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostPA("Clepsydre",1,1,2),etat_requis="Telefrag",consomme_etat=True)], 2,2,0,0,"cercle", chaine=True,description=u"Occasionne des dommages Eau. Si la cible est dans l'état Téléfrag, le lanceur gagne 2 PA au prochain tour. Retire l'état Téléfrag."))
            sorts.append(Sort(u"Frappe de Xélor",3,1,3,[Effets.EffetDegats(23,27,"terre",cibles_possibles="Ennemis"), Effets.EffetTpSymSelf()], 3,2,0,0,"cercle",chaine=False,description=u"Occasionne des dommages Terre aux ennemis. Téléporte la cible symétriquement par rapport au lanceur du sort."))
            sorts.append(Sort(u"Engrenage",3,1,5,[Effets.EffetDegats(31,35,"terre",zone=zones.TypeZoneLignePerpendiculaire(1),cibles_possibles="Ennemis"), Effets.EffetTpSymCentre(zone=zones.TypeZoneLignePerpendiculaire(1))], 2,2,0,0,"ligne",chaine=False,description=u"Occasionne des dommages Terre et téléporte les cibles symétriquement par rapport au centre de la zone d'effet."))
            sorts.append(Sort(u"Momification",2,0,0,[Effets.EffetEtat(Etats.EtatBoostPM("Momification",0,1,2)),Effets.EffetEtat(Etats.EtatTelefrag("Telefrag",0,2,"Momification"),zone=zones.TypeZoneCercle(99)),Effets.EffetEtat(Etats.EtatBoostDommage("Momie",0,1,-99999999))], 1,1,3,0,"cercle",description=u"Le lanceur ne peut plus occasionner de dommages avec ses sorts élémentaires et gagne 2 PM pendant 1 tour. Fixe l'état Téléfrag à tous les alliés et ennemis pendant 2 tours. Quand l'état Téléfrag est retiré, le lanceur gagne 100 Puissance pendant 2 tours."))
            sorts.append(Sort(u"Glas",15,0,3,[Effets.EffetTeleporteDebutCombat(),Effets.EffetEtat(Etats.EtatBoostPerDommageSorts("Glas",1,1,-50)),Effets.EffetRetireEtat("Glas",zone=zones.TypeZoneCercle(99),cibles_possibles="Lanceur")], 1,1,3,0,"ligne",description=u" Renvoie la cible à sa cellule de début de combat (en ignorant les états qui empêchent les déplacements) et divise ses dommages occasionnés par 2 pendant 1 tour. Le coût en PA est réduit en fonction du nombre de téléfrags générés depuis son dernier lancer."))
        elif(classe==u"Iop"):
            activationRassemblement= Sort(u"AttireAllies",0,0,0,[Effets.EffetAttire(2,zone=zones.TypeZoneCroix(3))],99,99,0,0,"cercle")
            activationFriction= Sort(u"Attire",0,0,0,[Effets.EffetAttire(1,zone=zones.TypeZoneCroix(99))],99,99,0,0,"cercle")
            sorts.append(Sort(u"Pression",3,1,3,[Effets.EffetDegats(21,25,"terre")], 99,3,0,0,"cercle",description=u"Occasionne des dommages Terre et applique un malus d'Érosion."))
            sorts.append(Sort(u"Tannée",4,1,7,[Effets.EffetDegats(30,34,"air",zone=zones.TypeZoneLignePerpendiculaire(1)),Effets.EffetRetPM(3,zone=zones.TypeZoneLignePerpendiculaire(1))], 2,2,0,0,"ligne",description=u"Occasionne des dommages Air en zone et retire des PM."))
            sorts.append(Sort(u"Bond",5,1,6,[Effets.EffetTp(cibles_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatModDegPer("Bond",0,1,115),zone=zones.TypeZoneCercle(1),cibles_possibles="Ennemis")], 1,1,2,0,"cercle",description=u"Téléporte sur la case ciblée. Augmente les dommages reçus par les ennemis situés sur les cases adjacentes."))
            sorts.append(Sort(u"Détermination",2,0,0,[Effets.EffetEtat(Etats.Etat("Indeplacable",0,1)),Effets.EffetEtat(Etats.EtatModDegPer("Determination",0,1,75))], 1,1,2,0,"cercle",description="Fixe l'état Indéplaçable et réduit 25%% des dommages subis pendant 1 tour. Ne peut pas être désenvoûté."))
            sorts.append(Sort(u"Intimidation",2,1,2,[Effets.EffetDegats(11,13,"terre"),Effets.EffetRepousser(4)], 3,2,0,0,"ligne",description=u"Occasionne des dommages Neutre sur les ennemis et repousse la cible."))
            sorts.append(Sort(u"Menace",3,0,3,[Effets.EffetDegats(26,28,"eau",cibles_exclues="Lanceur"),Effets.EffetAttire(2,cibles_exclues="Lanceur")], 3,2,0,0,"cercle",description=u"Occasionne des dommages Eau et attire la cible. Le lanceur gagne des points de bouclier."))
            sorts.append(Sort(u"Déferlement",3,0,5,[Effets.EffetDegats(28,32,"eau",cibles_exclues="Lanceur"),Effets.EffetAttireAttaquant(4,cibles_exclues="Lanceur")], 3,2,0,0,"ligne",description=u"Occasionne des dommages Eau aux ennemis et rapproche le lanceur de la cible. Le lanceur gagne des points de bouclier."))
            sorts.append(Sort(u"Conquête",3,1,6,[Effets.EffetInvoque("Stratège Iop",cible_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatRedistribuerPer("Strategie iop",0,-1, 50,"Ennemis|Allies",2))], 1,1,3,0,"ligne",description=u"Invoque un épouvantail qui redistribue à proximité (2 cases) 50%% des dommages qu'il subit."))
            sorts.append(Sort(u"Epée_Divine",3,0,0,[Effets.EffetDegats(21,23,"air",zone=zones.TypeZoneCroix(3),cibles_possibles="Ennemis"), Effets.EffetEtat(Etats.EtatBoostDommage("Epee Divine",0,4,20),zone=zones.TypeZoneCroix(3),cibles_possibles="Allies|Lanceur")], 2,2,0,0,"cercle",chaine=False,description=u"Occasionne des dommages Air et augmente les dommages des alliés ciblés."))
            sorts.append(Sort(u"Fendoir",5,0,4,[Effets.EffetDegats(47,53,"eau",zone=zones.TypeZoneCroix(1),cibles_exclues="Lanceur")], 2,2,0,0,"cercle",description=u"Occasionne des dommages Eau en zone. Applique des points de bouclier pour chaque ennemi touché."))
            sorts.append(Sort(u"Épée Destructrice",4,1,5,[Effets.EffetDegats(32,36,"feu",zone=zones.TypeZoneLignePerpendiculaire(1))], 2,2,0,0,"ligne",description=u"Occasionne des dommages Feu et réduit la probabilité que la cible occasionne des coups critiques."))
            sorts.append(Sort(u"Anneau Destructeur",3,0,2,[Effets.EffetDegats(26,30,"air",zone=zones.TypeZoneAnneau(3)), Effets.EffetAttire(1,zone=zones.TypeZoneAnneau(3))], 2,2,0,0,"cercle",description=u"Occasionne des dommages Air en anneau et attire les cibles."))
            sorts.append(Sort(u"Massacre",2,1,7,[Effets.EffetEtat(Etats.EtatRedistribuerPer("Massacre",0,2,50,"Ennemis",1))], 1,1,3,0,"cercle",description=u"Lorsque la cible ennemie reçoit des dommages de sorts, elle occasionne 50% de ces dommages aux entités au contact."))
            sorts.append(Sort(u"Rassemblement",2,1,6,[Effets.EffetAttire(2,zone=zones.TypeZoneCroix(3),cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatLanceSortSiSubit("Rassemblement",0,1,activationRassemblement),cible_possibles="Ennemis")], 1,1,2,0,"cercle",description=u"La cible attire ses alliés à proximité (2 cases) lorsqu'elle est attaquée."))
            sorts.append(Sort(u"Souffle",2,2,8,[Effets.EffetPousser(1,zone=zones.TypeZoneCroix(1),faire_au_vide=True)],1,1,2,0,"cercle",description=u"Repousse les alliés et les ennemis situés autour de la cellule ciblée."))
            sorts.append(Sort(u"Violence",2,0,0,[Effets.EffetAttire(1,zone=zones.TypeZoneCercle(2),cibles_possibles="Allies|Ennemis"),Effets.EffetEtat(Etats.EtatBoostDoPou("Violence",0,1,50))],1,1,0,0,"cercle",description=u"Attire les entités à proximité et augmente les dommages de poussée et le Tacle pour chaque ennemi dans la zone d'effet."))
            sorts.append(Sort(u"Concentration",2,1,1,[Effets.EffetDegats(20,24,"terre")],4,3,0,0,"ligne",description=u"Occasionne des dommages Terre. Les dommages sont augmentés contre les Invocations."))
            sorts.append(Sort(u"Accumulation",3,0,4,[Effets.EffetDegats(28,32,"terre",cibles_possibles="Ennemis"),Effets.EffetRetireEtat("Accumulation",zone=zones.TypeZoneCercle(99),cible_possibles="Iop"),Effets.EffetEtat(Etats.EtatBoostBaseDeg("Accumulation",0,3,"Accumulation",20),cibles_possibles="Lanceur")],2,2,0,0,"ligne",chaine=False,description=u"Occasionne des dommages Terre. Si le sort est lancé sur soi, le sort n'occasionne pas de dommages et ils sont augmentés pour les prochains lancers."))
            sorts.append(Sort(u"Couper",3,1,4,[Effets.EffetDegats(18,22,"feu",zone=zones.TypeZoneLigne(3)),Effets.EffetRetPM(3,zone=zones.TypeZoneLigne(3))],2,2,0,1,"ligne",description=u"Occasionne des dommages Feu et retire des PM."))
            sorts.append(Sort(u"Fracture",4,1,4,[Effets.EffetDegats(26,30,"air",zone=zones.TypeZoneLigneJusque(0))],2,2,0,0,"ligne",description=u"Occasionne des dommages Air jusqu'à la cellule ciblée. Applique un malus d'Érosion."))
            sorts.append(Sort(u"Friction",2,0,5,[Effets.EffetAttire(1,zone=zones.TypeZoneCroix(99)),Effets.EffetEtat(Etats.EtatLanceSortSiSubit("Friction",0,2,activationFriction))],1,1,3,0,"cercle",description=u"La cible se rapproche de l'attaquant si elle reçoit des dommages issus de sorts. Nécessite d'être aligné avec la cible."))
            sorts.append(Sort(u"Coup pour coup",2,1,3,[Effets.EffetRepousser(2),Effets.EffetEtat(Etats.EtatRepousserSiSubit("Coup_pour_coup",0,2,2))],1,1,3,0,"cercle",description=u"La cible est repoussée de 2 cases à chaque fois qu'elle attaque le lanceur."))
            sorts.append(Sort(u"Duel",3,1,1,[],1,1,4,0,"cercle",description=u"Retire leurs PM à la cible et au lanceur, leur applique l'état Pesanteur et les rend invulnérable aux dommages à distance. Ne fonctionne que si lancé sur un ennemi."))
            sorts.append(Sort(u"Emprise",3,1,1,[],1,1,4,0,"cercle",description=u"Retire tous les PM de l'ennemi ciblé mais le rend invulnérable."))
            sorts.append(Sort(u"Épée du Jugement",4,1,5,[Effets.EffetDegats(20,28,"air"),Effets.EffetVolDeVie(10,12,"feu")],3,2,0,0,"cercle",description=u"Occasionne des dommages Air et vole de la vie dans l'élément Feu sans ligne de vue."))
            sorts.append(Sort(u"Condamnation",3,1,6,[
                Effets.EffetDegats(33,37,"feu",zone=zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_2",consomme_etat=False),
                Effets.EffetDegats(33,37,"air",zone=zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_2",consomme_etat=True),
                Effets.EffetEtat(Etats.Etat("Condamnation_lancer_2",0,-1),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=True),
                Effets.EffetDegats(23,27,"feu",zone=zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=False),
                Effets.EffetDegats(23,27,"air",zone=zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=True),
                Effets.EffetEtat(Etats.Etat("Condamnation_lancer_1",0,-1),etat_requis_cibles="!Condamnation_lancer_2")
                ],3,2,0,0,"cercle",chaine=False,description=u"Occasionne des dommages Air et Feu. Les dommages sont appliqués lorsque le sort est lancé sur une autre cible. Peut se cumuler 2 fois sur une même cible."))
            sorts.append(Sort(u"Puissance",3,0,6,[Effets.EffetEtat(Etats.EtatBoostPuissance("Puissance",0,2,300))],1,1,3,0,"cercle",description=u"Augmente la Puissance de la cible."))
            sorts.append(Sort(u"Vertu",3,0,0,[Effets.EffetEtat(Etats.EtatBoostPuissance("Vertu",0,2,-150),zone=zones.TypeZoneCercle(1))],1,1,3,0,"cercle",description=u"Applique un bouclier zone mais réduit la Puissance du lanceur."))
            sorts.append(Sort(u"Précipitation",2,0,6,[Effets.EffetEtat(Etats.EtatBoostPA("Precipite",0,1,5)),Effets.EffetEtat(Etats.EtatBoostPA("Sortie de Precipitation",1,1,-3))],1,1,2,0,"cercle",description=u"Augmente les PA de la cible pour le tour en cours mais lui retire des PA le tour suivant. Interdit l'utilisation des armes et du sort Colère de Iop."))
            sorts.append(Sort(u"Agitation",2,0,5,[Effets.EffetEtat(Etats.EtatBoostPM("Agitation",0,1,2)),Effets.EffetEtat(Etats.Etat("Intaclable",1,1))],2,2,0,0,"cercle",description=u"Augmente les PM et la Fuite pour le tours en cours."))
            sorts.append(Sort(u"Tempête de Puissance",3,3,5,[Effets.EffetDegats(34,38,"feu")],3,2,0,0,"cercle",description=u"Occasionne des dommages Feu."))
            sorts.append(Sort(u"Tumulte",4,2,5,[Effets.EffetDegats(19,21,"feu",zone=zones.TypeZoneCroix(1))],1,1,1,0,"cercle",description=u"Occasionne des dommages Feu en zone. Plus le nombre de cibles est important, plus les dommages sont importants.*"))
            sorts.append(Sort(u"Épée Céleste",4,0,4,[Effets.EffetDegats(36,40,"air",zone=zones.TypeZoneCercle(2))],2,2,0,0,"ligne",description=u"Occasionne des dommages Air en zone."))
            sorts.append(Sort(u"Zénith",5,1,3,[Effets.EffetDegats(86,94,"air",zone=zones.TypeZoneLigne(4))],1,1,0,0,"ligne",description=u"Occasionne des dommages Air en zone. Les dommages sont augmentés pour chaque PM disponible lorsque le sort est lancé."))
            sorts.append(Sort(u"Vitalité",3,0,6,[Effets.EffetEtat(Etats.EtatBoostVita("Vitalite",0,4,20))],1,1,2,0,"cercle",description=u"Augmente temporairement les PV de la cible en pourcentage. Le bonus de PV est plus faible sur les alliés que sur le lanceur."))
            sorts.append(Sort(u"Endurance",4,0,1,[Effets.EffetDegats(34,38,"eau",cibles_exclues="Lanceur")],3,2,0,0,"cercle",description="Occasionne des dommages Eau. Applique des points de bouclier au lanceur."))
            sorts.append(Sort(u"Épée de Iop",4,1,6,[Effets.EffetDegats(37,41,"terre",zone=zones.TypeZoneCroix(3),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",faire_au_vide=True)],2,2,0,0,"ligne",description=u"Occasionne des dommages Terre en croix.")) 
            sorts.append(Sort(u"Pugilat",2,1,4,[Effets.EffetDegats(9,11,"terre",zone=zones.TypeZoneCercle(2),cibles_exclues="Lanceur"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Pugilat",0,1,"Pugilat",20))],4,1,0,0,"cercle",description=u"Occasionne des dommages Terre en zone. Les dommages sont augmentés pendant 1 tour après chaque lancer.")) 
            sorts.append(Sort(u"Épée du Destin",4,1,1,[Effets.EffetDegats(38,42,"feu"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Epee_du_destin", 2,1,u"Épée du Destin",30))], 1,1,2,0,"ligne",description=u"Occasionne des dommages Feu. Les dommages sont augmentés à partir du second lancer.")) 
            sorts.append(Sort(u"Sentence",2,1,6,[Effets.EffetDegats(13,16,"feu"),Effets.EffetEtat(Etats.EtatEffetFinTour("Sentence", 1,1,Effets.EffetDegats(13,16,"feu",zone=zones.TypeZoneCercle(2)),"Sentence","lanceur"))], 3,1,0,0,"ligne",description=u"Occasionne des dommages Feu. Occasionne des dommages Feu supplémentaires en zone à la fin du tour de la cible.")) 
            sorts.append(Sort(u"Colère de Iop",7,1,1,[Effets.EffetDegats(81,100,"terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Colere_de_Iop", 3,1,u"Colère de Iop",110))], 1,1,3,0,"ligne",description=u"Occasionne des dommages Terre. Augmente les dommages du sort au troisième tour après son lancer.")) 
            sorts.append(Sort(u"Fureur",3,1,1,[Effets.EffetDegats(28,32,"terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fureur", 1,2,"Fureur",40))], 1,1,0,0,"ligne",description=u"Occasionne des dommages Terre. Les dommages sont augmentés à chaque lancer du sort, mais ce bonus est perdu si le sort n'est pas relancé."))
        elif classe==u"Crâ":
            sorts.append(Sort(u"Flèche Magique",3,1,12,[Effets.EffetDegats(19,21,"air"),Effets.EffetEtat(Etats.EtatBoostPO("Fleche Magique",1,1,-2)),Effets.EffetEtatSelf(Etats.EtatBoostPO("Fleche Magique",0,1,2))],3,2,0,1,"cercle",description=u"Occasionne des dommages Air et vole la portée de la cible."))
            sorts.append(Sort(u"Flèche de Concentration",3,3,8,[Effets.EffetDegats(22,26,"air",zone=zones.TypeZoneCroix(3)),Effets.EffetAttireAttaquant(1,zone=zones.TypeZoneCroix(3))],2,1,0,1,"cercle",description=u"Occasionne des dommages Air et attire vers la cible."))
            sorts.append(Sort(u"Flèche de Recul",3,1,8,[Effets.EffetDegats(25,28,"air"),Effets.EffetRepousser(4)],2,1,0,0,"ligne",description=u"Occasionne des dommages Air aux ennemis et pousse la cible."))
            sorts.append(Sort(u"Flèche Érosive",3,1,3,[Effets.EffetDegats(25,29,"terre")],3,2,0,1,"ligne",description=u"Occasionne des dommages Terre et applique un malus d'Érosion."))
            sorts.append(Sort(u"Flèche de Dispersion",3,1,12,[Effets.EffetPousser(2,zone=zones.TypeZoneCroix(2),faire_au_vide=True)],1,1,2,1,"cercle",description=u"Pousse les ennemis et alliés, même s'ils sont bloqués par d'autres entités."))
            sorts.append(Sort(u"Représailles",4,2,5,[Effets.EffetEtat(Etats.EtatBoostPM("Immobilise",1,1,-100)),Effets.EffetEtat(Etats.Etat("Pesanteur",1,1))],1,1,5,0,"ligne",description=u"Immobilise la cible."))
            sorts.append(Sort(u"Flèche Glacée",3,3,6,[Effets.EffetDegats(17,19,"feu"),Effets.EffetRetPA(2)],99,2,0,1,"cercle",description=u"Occasionne des dommages Feu et retire des PA."))
            sorts.append(Sort(u"Flèche Paralysante",5,2,6,[Effets.EffetDegats(39,42,"feu",zone=zones.TypeZoneCroix(1)),Effets.EffetRetPA(4,zone=zones.TypeZoneCroix(1))],1,1,0,0,"cercle",description=u"Occasionne des dommages Feu et retire des PA."))
            sorts.append(Sort(u"Flèche Enflammée",4,1,8,[Effets.EffetDegats(33,35,"feu",zone=zones.TypeZoneLigne(5)),Effets.EffetPousser(1,zone=zones.TypeZoneLigne(5))],2,2,0,1,"ligne",description=u"Occasionne des dommages Feu et pousse les cibles présentes dans la zone d'effet du sort."))
            sorts.append(Sort(u"Flèche Repulsive",3,1,7,[Effets.EffetDegats(28,32,"feu",zone=zones.TypeZoneLignePerpendiculaire(1)),Effets.EffetPousser(1,zone=zones.TypeZoneLignePerpendiculaire(1))],2,2,0,0,"ligne",description=u"Occasionne des dommages Feu et repousse de 1 case."))
            sorts.append(Sort(u"Tir Éloigne",3,0,0,[Effets.EffetEtat(Etats.EtatBoostPO("Tir_eloigne",0,4,6),zone=zones.TypeZoneCercle(3))],1,1,5,0,"cercle",description=u"Augmente la portée des cibles présentes dans la zone d'effet."))
            sorts.append(Sort(u"Acuité Absolue",4,0,0,[Effets.EffetEtat(Etats.Etat("Desactive_ligne_de_vue",0,1))],1,1,3,0,"cercle",description=u"Tous les sorts du Crâ peuvent être lancés au travers des obstacles."))
            sorts.append(Sort(u"Flèche d'Expiation",4,6,10,[Effets.EffetDegats(35,37,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg(u"Fleche_d_expiation",0,-1,u"Flèche d'Expiation",36))],1,1,3,1,"cercle",description=u"Occasionne des dommages Eau, augmente les dommages du sort tous les 3 tours et empêche la cible d'utiliser des sorts de déplacement."))
            sorts.append(Sort(u"Flèche de Rédemption",3,6,8,[Effets.EffetDegats(19,22,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_de_redemption",1,1,u"Flèche de Rédemption",12))],3,2,0,1,"cercle",description=u"Occasionne des dommages Eau qui sont augmentés si le sort est relancé le tour suivant."))
            sorts.append(Sort(u"Oeil de Taupe",3,5,10,[Effets.EffetVolDeVie(16,18,"eau",zone=zones.TypeZoneCercle(3)),Effets.EffetEtat(Etats.EtatBoostPO("Oeil_de_taupe",1,3,-3),zone=zones.TypeZoneCercle(3)),Effets.EffetRetireEtat("Invisibilite",zone=zones.TypeZoneCercle(3))],1,1,4,1,"cercle",description=u"Réduit la portée des personnages ciblés, vole de la vie dans l'élément Eau et repère les objets invisibles dans sa zone d'effet."))
            sorts.append(Sort(u"Flèche Écrasante",3,5,7,[Effets.EffetDegats(34,38,"feu",zone=zones.TypeZoneCroixDiagonale(1)),Effets.EffetEtat(Etats.Etat("Pesanteur",1,1),zone=zones.TypeZoneCroixDiagonale(1))],1,1,3,1,"cercle",description=u"Occasionne des dommages Feu et applique l'état Pesanteur."))
            sorts.append(Sort(u"Tir Critique",2,0,6,[Effets.EffetEtat(Etats.Etat("Tir_critique",0,4))],1,1,5,1,"cercle",description=u"Augmente la probabilité de faire un coup critique."))
            sorts.append(Sort(u"Balise de Rappel",2,1,5,[Effets.EffetInvoque("Balise_de_rappel",cibles_possibles="",faire_au_vide=True)],1,1,2,0,"cercle",description=u"Invoque une balise qui échange sa position avec celle du lanceur (au début du prochain tour)."))
            sorts.append(Sort(u"Flèche d'Immobilisation",2,1,6,[Effets.EffetDegats(10,11,"eau"),Effets.EffetEtat(Etats.EtatBoostPM("Fleche_d_immobilisation",1,1,-1)),Effets.EffetEtatSelf(Etats.EtatBoostPM("Fleche_d_immobilisation",0,1,1))],4,2,0,1,"cercle",description=u"Occasionne des dommages Eau et vole des PM à la cible."))
            sorts.append(Sort(u"Flèche Assaillante",3,2,6,[Effets.EffetDegats(33,37,"eau",cibles_possibles="Ennemis"),Effets.EffetRepousser(1,cibles_possibles="Ennemis"),Effets.EffetAttireAttaquant(1,cibles_possibles="Allies")],3,2,0,1,"ligne",description=u"Occasionne des dommages Eau sur les ennemis et le lanceur recule de 1 case. Sur un allié : rapproche le lanceur de 1 case."))
            sorts.append(Sort(u"Flèche Punitive",4,6,8,[Effets.EffetDegats(29,31,"terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_punitive",0,-1,u"Flèche Punitive",30))],1,1,2,1,"cercle",description=u"Occasionne des dommages Terre et augmente les dommages du sort tous les 2 tours."))
            sorts.append(Sort(u"Flèche du Jugement",3,5,7,[Effets.EffetDegats(39,45,"terre")],3,2,0,1,"cercle",description=u"Occasionne des dommages Terre. Plus le pourcentage de PM du personnage au lancement du sort est important, plus les dommages occasionnés sont importants."))
            sorts.append(Sort(u"Tir Puissant",3,0,6,[Effets.EffetEtat(Etats.EtatBoostPuissance("Tir_puissant",0,3,250))],1,1,6,1,"cercle",description=u"Augmente les dommages des sorts."))
            sorts.append(Sort(u"Balise Tactique",1,1,10,[Effets.EffetInvoque("Balise_tactique",cibles_possibles="", faire_au_vide=True)],1,1,2,1,"cercle",description=u"Invoque une Balise qui peut servir d'obstacle et de cible. La Balise subit 2 fois moins de dommages des alliés."))
            sorts.append(Sort(u"Flèche Harcelante",3,1,7,[Effets.EffetDegats(13,15,"air")],1,1,2,1,"cercle",description=u"Occasionne des dommages Air sans ligne de vue."))
            sorts.append(Sort(u"Flèche Massacrante",4,4,8,[Effets.EffetDegats(34,38,"air"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_massacrante",1,1,u"Flèche Massacrante",10))],3,2,0,1,"ligne",description=u"Occasionne des dommages Air. Les dommages du sort sont augmentés au tour suivant."))
            sorts.append(Sort(u"Flèche Empoisonnée",3,1,10,[Effets.EffetRetPM(3),Effets.EffetEtat(Etats.EtatEffetDebutTour("Fleche_empoisonnee", 1,2,Effets.EffetDegats(17,18,"terre"),"Fleche_empoisonnee","lanceur"))],4,1,0,1,"cercle",description=u"Occasionne des dommages Neutre sur plusieurs tours et retire des PM."))
            sorts.append(Sort(u"Flèche Persecutrice",3,5,8,[Effets.EffetDegats(15,17,"feu"),Effets.EffetDegats(15,17,"air")],99,2,0,1,"ligne",description=u"Occasionne des dommages Air et Feu."))
            sorts.append(Sort(u"Flèche Tyrannique",4,2,7,[Effets.EffetEtat(Etats.EtatEffetSiPousse("Fleche_tyrannique_air",0,2, Effets.EffetDegats(12,12,"air"),"Fleche_tyrannique","lanceur")),Effets.EffetEtat(Etats.EtatEffetSiSubit("Fleche_tyrannique_feu",0,2, Effets.EffetDegats(12,12,"feu"),"Fleche_tyrannique","doPou","lanceur"))],99,1,0,1,"ligne",description=u"Occasionne des dommages Air si la cible est poussée. Occasionne des dommages Feu si la cible subit des dommages de poussée."))
            sorts.append(Sort(u"Flèche Destructrice",4,5,8,[Effets.EffetDegats(30,32,"terre"),Effets.EffetEtat(Etats.EtatBoostDommage(u"Flèche destructrice",1,1,-60))],99,2,0,1,"cercle",description=u"Occasionne des dommages Terre et réduit les dommages occasionnés par la cible."))
            sorts.append(Sort(u"Tir de Barrage",4,4,8,[Effets.EffetDegats(29,33,"terre"),Effets.EffetRepousser(2)],3,2,0,1,"cercle",description=u"Occasionne des dommages Terre et repousse la cible."))
            sorts.append(Sort(u"Flèche Absorbante",4,6,8,[Effets.EffetVolDeVie(29,31,"air")],3,2,0,1,"cercle",description=u"Vole de la vie dans l'élément Air."))
            sorts.append(Sort(u"Flèche Dévorante",3,1,6,[
                Effets.EffetDegats(70,74,"air",zone=zones.TypeZoneCercle(99),etat_requis_cibles="Fleche_devorante_lancer_3",consomme_etat=True),
                Effets.EffetEtat(Etats.Etat("Fleche_devorante_lancer_3",0,-1),etat_requis_cibles="Fleche_devorante_lancer_2",consomme_etat=True),
                Effets.EffetDegats(52,56,"air",zone=zones.TypeZoneCercle(99),etat_requis_cibles="Fleche_devorante_lancer_2",consomme_etat=True),
                Effets.EffetEtat(Etats.Etat("Fleche_devorante_lancer_2",0,-1),etat_requis_cibles="Fleche_devorante_lancer_1",consomme_etat=True),
                Effets.EffetDegats(34,38,"air",zone=zones.TypeZoneCercle(99),etat_requis_cibles="Fleche_devorante_lancer_1",consomme_etat=True),
                Effets.EffetEtat(Etats.Etat("Fleche_devorante_lancer_1",0,-1),etat_requis_cibles="!Fleche_devorante_lancer_2|!Fleche_devorante_lancer_3")
                ],2,1,0,1,"cercle",chaine=False,description=u"Occasionne des dommages Air. Les dommages sont appliqués lorsque le sort est lancé sur une autre cible. Peut se cumuler 3 fois sur une même cible."))
            sorts.append(Sort(u"Flèche cinglante",2,1,9,[Effets.EffetRepousser(2)],4,2,0,1,"ligne",description=u"Applique de l'Érosion aux ennemis et repousse de 2 cases."))
            sorts.append(Sort(u"Flèche de repli",1,2,7,[Effets.EffetPousser(1,zone=zones.TypeZoneCercleSansCentre(5),cible_possibles="Lanceur")],4,2,0,1,"ligne",description=u"Le lanceur du sort recule de 2 cases."))
            sorts.append(Sort(u"Flèche ralentissante",4,1,8,[Effets.EffetRetPA(3,zone=zones.TypeZoneCercle(2)),Effets.EffetDegats(36,38,"eau",zone=zones.TypeZoneCercle(2))],2,1,0,1,"ligne",description=u"Occasionne des dommages Eau et retire des PA en zone."))
            sorts.append(Sort(u"Flèche percutante",2,1,6,[Effets.EffetDegats(6,10,"eau"),Effets.EffetEtat(Etats.EtatEffetFinTour("Fleche_percutante_retardement", 1,1,Effets.EffetDegats(6,10,"eau",zone=zones.TypeZoneCercleSansCentre(2)),"Fleche_percutante_retardement","lanceur")),Effets.EffetEtat(Etats.EtatEffetFinTour("Fleche_percutante_retardementPA", 1,1,Effets.EffetRetPA(2,zone=zones.TypeZoneCercleSansCentre(2)),"Fleche_percutante_retardementPA","lanceur"))],2,1,0,1,"cercle",description=u"Occasionne des dommages Eau. À la fin de son tour, la cible occasionne des dommages Eau et retire des PA en cercle de taille 2 autour d'elle."))
            sorts.append(Sort(u"Flèche explosive",4,1,8,[Effets.EffetDegats(30,34,"feu",zone=zones.TypeZoneCercle(3))],2,1,0,1,"cercle",description=u"Occasionne des dommages Feu en zone."))
            fleche_fulminante=Sort(u"Flèche Fulminante",4,1,8,[Effets.EffetDegats(34,38,"feu",cibles_possibles="Ennemis|Balise_tactique"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_Fulminante_boost",0,1,u"Flèche Fulminante Rebond",10))],1,1,0,1,"cercle",description=u"Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
            fleche_fulminante_rebond=Sort(u"Flèche Fulminante Rebond",0,0,99,[Effets.EffetDegats(34,38,"feu",cibles_possibles="Ennemis|Balise_tactique"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_Fulminante_boost",0,1,u"Flèche Fulminante Rebond",10))],9,1,0,0,"cercle",description=u"Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
            fleche_fulminante.effets.append(EffetPropage(fleche_fulminante_rebond,TypeZoneCercle(2),cibles_possibles="Ennemis|Balise_tactique"))
            fleche_fulminante_rebond.effets.append(EffetPropage(fleche_fulminante_rebond,TypeZoneCercle(2),cibles_possibles="Ennemis|Balise_tactique"))
            sorts.append(fleche_fulminante)
            sorts.append(Sort(u"Maîtrise de l'arc",2,0,6,[Effets.EffetEtat(Etats.EtatBoostDommage("Maitrise de l'arc",0,3,60))],1,1,5,1,"cercle",description=u"Augmente les dommages."))
            sorts.append(Sort(u"Sentinelle",2,0,0,[Effets.EffetEtatSelf(Etats.EtatBoostPerDommageSorts("Sentinelle",1,1,30)),Effets.EffetEtatSelf(Etats.EtatBoostPM("Sentinelle",1,1,-100))],1,1,3,0,"cercle",description=u"Au tour suivant, le lanceur perd tous ses PM mais gagne un bonus de dommages."))
        sorts.append(Sort(u"Cawotte",4,1,6,[Effets.EffetInvoque("Cawotte",cibles_possibles="", faire_au_vide=True)], 1,1,6,0,"cercle",description=u"Invoque une Cawotte")) 
        
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
                if mouse_xy[1] > constantes.y_sorts:
                    for sort in niveau.tourDe.sorts:
                        if sort.vue.isMouseOver(mouse_xy):
                            
                            coutPA = sort.getCoutPA(self)
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
                        case_cible_x = mouse_xy[0]/constantes.taille_sprite
                        case_cible_y = mouse_xy[1]/constantes.taille_sprite
                        niveau.tourDe.lanceSort(sortSelectionne,niveau, case_cible_x,case_cible_y)
                        sortSelectionne = None
                    #Aucun sort n'est selectionne: on pm
                    else:
                        niveau.Deplacement(mouse_xy)
            elif clicDroit:
                if mouse_xy[1]<constantes.y_sorts:
                    case_x = mouse_xy[0]/constantes.taille_sprite
                    case_y = mouse_xy[1]/constantes.taille_sprite
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
        
        self.taille = constantes.taille_carte
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
        case_x = mouse_xy[0]/constantes.taille_sprite
        case_y = mouse_xy[1]/constantes.taille_sprite
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
            if departY+distance-delta<constantes.taille_carte:
                retour.append([departX-delta, departY+distance-delta])
        for delta in xrange(1,distance):
            if departX-delta >=0:
                if departY-distance+delta>=0:
                    retour.append([departX-delta, departY-distance+delta])
                if departY+distance-delta<constantes.taille_carte:
                    retour.append([departX-delta, departY+distance-delta])
            if departX+delta < constantes.taille_carte:
                if departY-distance+delta>=0:
                    retour.append([departX+delta, departY-distance+delta])
                if departY+distance-delta<constantes.taille_carte:
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
        pygame.draw.rect(self.fenetre, pygame.Color(0, 0, 0), pygame.Rect(constantes.x_sorts, constantes.y_sorts, constantes.width_sorts, constantes.height_sorts))
        surfaceGrise = pygame.Surface((30   ,30), pygame.SRCALPHA)   # per-pixel alpha
        surfaceGrise.fill((128,128,128,128))                         # notice the alpha value in the color
        x = constantes.x_sorts
        y = constantes.y_sorts
        for sort in self.tourDe.sorts:
            sort.vue = Overlays.VueForOverlay(self.fenetre, x, y, 30, 30,sort)
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
            if(x+30>constantes.x_sorts+constantes.width_sorts):
                y+=30
                x=constantes.x_sorts
    
    def initJoueurs(self):
        placeT1 = 0
        placeT2 = 0
        for joueur in self.joueurs:
            if joueur.team == 1:
                joueur.posX = self.departT1[placeT1][0]
                joueur.posY = self.departT1[placeT1][1]
                placeT1+=1
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
                x = j * constantes.taille_sprite
                y = i * constantes.taille_sprite
                ligne_niveau.append(Case("v", pygame.draw.rect(self.fenetre, (0,0,0), [x , y, constantes.taille_sprite, constantes.taille_sprite])))
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

    def boostApresTF(self,nomSort,reelLanceur):
        #BoostSynchro
        synchros = self.getJoueurs("Synchro")
        for synchro in synchros:
            if not synchro.aEtat(nomSort) and nomSort != "Rembobinage" and not synchro.aEtat("DejaBoost"):
                synchro.appliquerEtat(Etats.Etat("Boost Synchro "+nomSort,0,-1, reelLanceur),reelLanceur)
                synchro.appliquerEtat(Etats.Etat("DejaBoost",0,1,[nomSort], reelLanceur),reelLanceur)
        #BoostGlas
        reelLanceur.appliquerEtat(Etats.EtatCoutPA("Glas",0,-1,u"Glas",-1),reelLanceur)

    def exploserSynchro(self,synchro,reelLanceur):
        nbTF = 0
        for etat in synchro.etats:
            if etat.nom.startswith("Boost Synchro"):
                nbTF+=1
        synchro.lanceSort(Sort("Fin_des_temps",0,0,0,[Effets.EffetDegats(int(reelLanceur.lvl*1.90)*(nbTF*2-1),int(reelLanceur.lvl*1.90)*(nbTF*2-1),"air",zone=zones.TypeZoneCercle(3),cibles_possibles="Ennemis")], 99,99,0,0,"cercle"),self,synchro.posX,synchro.posY)
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

    def deplacementTFVersCaseOccupee(self, joueurASwap,joueurBougeant, posAtteinte, reelLanceur,nomSort, AjouteHistorique,genereTF):
        self.effectuerTF(joueurASwap,joueurBougeant,posAtteinte,reelLanceur,nomSort,AjouteHistorique,genereTF)
        #Si le xelor est pas deja boostPA par ce sort, rembo ne peut pas boost PA
        if genereTF:
            if not reelLanceur.aEtat(nomSort) and nomSort != "Rembobinage":
                reelLanceur.appliquerEtat(Etats.Etat("BoostPA",0,1,[2],reelLanceur),reelLanceur)
                reelLanceur.appliquerEtat(Etats.Etat(nomSort,0,1,["Telefrag"],reelLanceur),reelLanceur)
            self.boostApresTF(nomSort,reelLanceur)
            if ("Synchro" == joueurBougeant.classe) and not reelLanceur.aEtat("Faille_temporelle"):
                self.exploserSynchro(joueurBougeant,reelLanceur)
            elif ("Synchro" == joueurASwap.classe) and not reelLanceur.aEtat("Faille_temporelle"):
                self.exploserSynchro(joueurASwap,reelLanceur)
            self.glypheActiveTF(reelLanceur,nomSort)
 

    def effectuerTF(self, joueurASwap,joueurBougeant,posAtteinte,reelLanceur,nomSort,AjouteHistorique,genereTF):
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
        if posAtteinte[1]<0 or posAtteinte[1]>=constantes.taille_carte or posAtteinte[0]<0 or posAtteinte[0]>=constantes.taille_carte:
            return None
        if self.structure[posAtteinte[1]][posAtteinte[0]].type == "v":
            self.deplacementTFVersCaseVide(joueurBougeant, posAtteinte,AjouteHistorique)
            return None
        elif self.structure[posAtteinte[1]][posAtteinte[0]].type == "j":
            if lanceur.invocateur != None:
                reelLanceur = lanceur.invocateur
            else:
                reelLanceur = lanceur
            joueurSwap = joueurASwap = self.getJoueurSur(posAtteinte[0],posAtteinte[1])
            if joueurASwap != joueurBougeant:
                self.deplacementTFVersCaseOccupee(joueurASwap,joueurBougeant, posAtteinte, reelLanceur,nomSort, AjouteHistorique,genereTF)
                return joueurASwap
        else:
            print "Deplacement pas implemente"
        return None

    def appliquerEffetSansBoucleSurZone(self,effet,joueurLanceur,case_cible_x,case_cible_y,nomSort,ciblesTraitees,prov_x,prov_y):
        if type(effet) == type(Effets.EffetGlyphe(None,None,None,None)):
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
        if type(effet) is Effets.EffetDegatsPosLanceur or type(effet) is Effets.EffetTeleportePosPrecLanceur:
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

    def getJoueurslesPlusProches(self, case_x,case_y,lanceur,zone=zones.TypeZoneCercle(99),etatRequisCibles=[],ciblesPossibles=[],ciblesExclues=[],ciblesTraitees=[]):
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
            if mouse_xy[1] < constantes.y_sorts:
                case_x = mouse_xy[0]/constantes.taille_sprite
                case_y = mouse_xy[1]/constantes.taille_sprite
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
