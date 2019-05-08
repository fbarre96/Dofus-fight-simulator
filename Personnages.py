# -*- coding: utf-8 -*
import Sort
import Effets
import Zones
import Etats
import constantes
import Overlays
import pygame
from pygame.locals import *

class Personnage(object):
    """@summary: Classe décrivant un personnage joueur de dofus."""
    def __init__(self, classe, v,f,a,c,i,p,d,df,da,dc,di,dp,retPA,retPM,esqPA,esqPM,pm,pa,po,lvl,team=1,icone=""):
        """@summary: Initialise un personnage.
        @classe: la classe du personnage (les 18 classes de Dofus). Pour l'instant sert d'identifiant étant donné que 1v1 vs Poutch.
        @type: string
        @v: la vie du personnage
        @type: int
        @f: la force du personnage
        @type: int
        @a: l'agilité du personnage
        @type: int
        @c: la chance du personnage
        @type: int
        @i: l'intelligence du personnage
        @type: int
        @p: la puissance du personnage
        @type: int
        @d: les dommages du personnage
        @type: int
        @df: les dommages terre du personnage
        @type: int
        @da: les dommages air du personnage
        @type: int
        @dc: les dommages eau du personnage
        @type: int
        @di: les dommages feu du personnage
        @type: int
        @dp: les dommages de poussé du personnage
        @type: int
        @pm: les points de mouvements du personnage
        @type: int
        @pa: les points d'action du personnage
        @type: int
        @po: les points de portée du personnage
        @type: int
        @lvl: le niveau (level) du personnage
        @type: int
        @team: le numéro d'équipe du personnage
        @type: int
        @icone: le chemin de l'image pour afficher l'icône du personnage
        @type: string (nom de l'image. L'image doit faire moins de 30x30 pixels, se situer dans /image et porté le même nom que la classe une fois normalisé)
        """
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
        self.retPA = int(retPA)
        self.retPM = int(retPM)
        self.esqPA = int(esqPA)
        self.esqPM = int(esqPM)
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
        self._esqPA = int(esqPA)
        self._esqPM = int(esqPM)
        self._retPA = int(retPA)
        self._retPM = int(retPM)
        self.erosion = 0
        self.lvl = int(lvl)
        self.classe = classe
        self.sorts = Personnage.ChargerSorts(self.classe) # la liste des sorts du personnage
        self.posX = 0                                     # Sa position X sur la carte
        self.posY = 0                                     # Sa position Y sur la carte
        self.etats = []                                   # La liste des états affectant le personange
        self.historiqueDeplacement = []                   # Les déplacements effectués par le personnage dans ses 2 derniers tours
        self.posDebTour = None
        self.posDebCombat = None
        self.invocateur = None
        self.team = int(team)
        if not(icone.startswith("images/")):
            self.icone = ("images/"+icone)
        else:
            self.icone = (icone)
        self.icone=constantes.normaliser(self.icone)
        # Overlay affichange le nom de classe et sa vie restante
        self.overlay = Overlays.Overlay(self, Overlays.ColoredText("classe",(210,105,30)), Overlays.ColoredText("vie",(224,238,238)),(56,56,56))

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
    def ChargerSorts(classe):
        """@summary: Méthode statique qui initialise les sorts du personnage selon sa classe.
        @classe: le nom de classe dont on souhaite récupérer les sorts
        @type: string

        @return: tableau de Sort"""
        sorts = []
        if(classe=="Stratège Iop"):
            sorts.append(Sort.Sort("Strategie_iop",0,0,0,[Effets.EffetEtat(Etats.EtatRedistribuerPer("Stratégie Iop",0,-1, 50,"Ennemis|Allies",2))],99,99,0,0,"cercle"))
            return sorts
        elif(classe=="Cadran de Xélor"):
            sorts.append(Sort.Sort("Synchronisation",0,0,0,[Effets.EffetDegats(100,130,"feu",zone=Zones.TypeZoneCercleSansCentre(4), cibles_possibles="Ennemis|Lanceur",etat_requis_cibles="Telefrag"),Effets.EffetEtat(Etats.EtatBoostPA("Synchronisation",0,2,2),zone=Zones.TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Lanceur",etat_requis_cibles="Telefrag")],99,99,0,0,"cercle"))
            return sorts
        elif(classe=="Synchro"):
            sorts.append(Sort.Sort("Début des Temps",0,0,0,[Effets.EffetEtat(Etats.EtatBoostPA("Synchro",1,1,-1),zone=Zones.TypeZoneCercle(99),cibles_possibles="Xelor")],99,99,0,0,"cercle"))
            return sorts
        elif(classe=="Balise de Rappel"):
            sorts.append(Sort.Sort("Rappel",0,0,0,[Effets.EffetEchangePlace(zone=Zones.TypeZoneCercle(99),cibles_possibles="Cra"), Effets.EffetTue(zone=Zones.TypeZoneCercle(99),cibles_possibles="Lanceur")],99,99,0,0,"cercle"))
        elif classe == "Poutch":
            return sorts
        elif(classe=="Xélor"):
            retourParadoxe = Sort.Sort("Retour Paradoxe",0,0,0,[Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercle(99),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis_cibles="ParadoxeTemporel",consomme_etat=True)],99,99,0,0,"cercle")
            activationInstabiliteTemporelle = Sort.Sort("Activation Instabilité Temporelle",0,0,3,[Effets.EffetTeleportePosPrec(1)], 99,99,0,0,"cercle")
            activationParadoxeTemporel = Sort.Sort("Paradoxe Temporel", 0,0,0,[Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercle(4),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur|Xélor|Synchro"),Effets.EffetEtat(Etats.Etat("ParadoxeTemporel",0,2),zone=Zones.TypeZoneCercleSansCentre(4),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur|Xelor|Synchro"), Effets.EffetEtatSelf(Etats.EtatActiveSort("RetourParadoxe",1,1,retourParadoxe),cibles_possibles="Lanceur")],99,99,0,0,"cercle")
            activationDesynchro = [Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3))]
            sorts.append(Sort.Sort("Ralentissement",2,1,6,[Effets.EffetDegats(8,9,"eau"),Effets.EffetRetPA(1),Effets.EffetRetPA(1,cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag")],4,2,0,1,"cercle",description="Occasionne des dommages Eau et retire 1 PA à la cible. Retire 1 PA supplémentaire aux ennemis dans l'état Téléfrag. Le retrait de PA ne peut pas être désenvoûté."))
            sorts.append(Sort.Sort("Souvenir",4,1,6,[Effets.EffetDegats(26,30,"terre"),Effets.EffetTeleportePosPrec(1)], 3,2,0,1,"ligne",description="Occasionne des dommages Terre et téléporte la cible à sa position précédente."))
            sorts.append(Sort.Sort("Aiguille",3,1,8,[Effets.EffetDegats(22,26,"feu"),Effets.EffetRetPA(1),Effets.EffetRetPA(2,etat_requis_cibles="Telefrag",consomme_etat=True)], 3,2,0,1,"cercle", description="Occasionne des dommages Feu et retire 1 PA à la cible. Retire des PA supplémentaires aux ennemis dans l'état Téléfrag. Le retrait de PA ne peut pas être désenvoûté. Retire l'état Téléfrag."))
            sorts.append(Sort.Sort("Rouage",3,1,7,[Effets.EffetDegats(12,14,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostPA("Rouage",1,1,1))], 2,99,0,1,"cercle",chaine=True,description="Occasionne des dommages Eau. Le lanceur gagne 1 PA au tour suivant."))
            sorts.append(Sort.Sort("Téléportation",2,1,5,[Effets.EffetTpSym()], 1,1,3,0,"cercle",description="Téléporte le lanceur symétriquement par rapport à la cible. Le lanceur gagne 2 PA pour 1 tour à chaque fois qu’il génère un Téléfrag. Le temps de relance est supprimé quand un Téléfrag est généré ou consommé. Un Téléfrag est généré lorsqu'une entité prend la place d'une autre."))
            sorts.append(Sort.Sort("Retour Spontané",1,0,7,[Effets.EffetTeleportePosPrec(1)], 3,3,0,1,"cercle",description="La cible revient à sa position précédente."))
            sorts.append(Sort.Sort("Flétrissement",3,1,6,[Effets.EffetDegats(26,29,"air"),Effets.EffetDegats(10,10,"air",etat_requis_cibles="Telefrag")], 3,2,0,1,"ligne",description="Occasionne des dommages Air en ligne. Occasionne des dommages supplémentaires aux ennemis dans l'état Téléfrag."))
            sorts.append(Sort.Sort("Dessèchement",4,1,6,[Effets.EffetDegats(38,42,"air"),Effets.EffetEtat(Etats.EtatEffetDebutTour("Dessèchement", 1,1,Effets.EffetDegats(44,48,"air",cibles_possbiles="Ennemis",zone=Zones.TypeZoneCercleSansCentre(2)),"Dessechement","lanceur"))], 3,2,0,0,"ligne",description="Occasionne des dommages Air. Au prochain tour du lanceur, la cible occasionne des dommages autour d'elle."))
            sorts.append(Sort.Sort("Rembobinage",2,0,6,[Effets.EffetEtat(Etats.EtatRetourCaseDepart("Bobine",0,1),cibles_possibles="Allies|Lanceur")], 1,1,3, 0, "ligne",description="À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour."))
            sorts.append(Sort.Sort("Renvoi",3,1,6,[Effets.EffetTeleporteDebutTour()], 1,1,2, 0, "ligne",description="Téléporte la cible ennemie à sa cellule de début de tour."))
            sorts.append(Sort.Sort("Rayon Obscur",5,1,6,[Effets.EffetDegats(37,41,"terre"),Effets.EffetDegats(37,41,"terre",cibles_possibles="Allies|Ennemis",etat_requis_cibles="Telefrag",consomme_etat=True)], 3,2,0,0,"ligne",description="Occasionne des dommages Terre en ligne. Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag. Retire l'état Téléfrag."))
            sorts.append(Sort.Sort("Rayon Ténebreux",3,1,5,[Effets.EffetDegats(19,23,"terre"),Effets.EffetDegats(19,23,"terre",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")], 3,2,0,1,"ligne",description="Occasionne des dommages Terre. Si la cible est dans l'état Téléfrag, occasionne des dommages Terre en zone autour d'elle."))
            sorts.append(Sort.Sort("Complice",2,1,5,[Effets.EffetInvoque("Complice",cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles="Cadran de Xélor|Complice",zone=Zones.TypeZoneCercleSansCentre(99))], 1,1,0,0,"cercle",chaine=True,description="Invoque un Complice statique qui ne possède aucun sort. Il est tué si un autre Complice est invoqué."))
            sorts.append(Sort.Sort("Cadran de Xélor",3,1,5,[Effets.EffetInvoque("Cadran de Xélor",cibles_possibles="",faire_au_vide=True),Effets.EffetTue(cibles_possibles="Cadran de Xélor|Complice",zone=Zones.TypeZoneCercleSansCentre(99))], 1,1,4,0,"cercle",chaine=True,description="Invoque un Cadran qui occasionne des dommages Feu en zone et retire des PA aux ennemis dans l'état Téléfrag. Donne des PA aux alliés autour de lui et dans l'état Téléfrag."))
            sorts.append(Sort.Sort("Gelure",2,2,5,[Effets.EffetDegats(11,13,"air",cibles_possibles="Ennemis|Lanceur"), Effets.EffetTeleportePosPrec(1)], 3,2,0,1,"cercle",description="Occasionne des dommages Air aux ennemis. Téléporte la cible à sa position précédente."))
            sorts.append(Sort.Sort("Perturbation",2,1,4,[Effets.EffetDegats(9,11,"feu",cibles_possibles="Ennemis|Lanceur"), Effets.EffetTpSymSelf()], 3,2,0,0,"ligne", chaine=False,description="Occasionne des dommages Feu et téléporte la cible symétriquement par rapport au lanceur."))
            sorts.append(Sort.Sort("Sablier de Xélor",2,1,7,[Effets.EffetDegats(15,17,"feu"),Effets.EffetRetPA(2),Effets.EffetDegats(15,17,"feu",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag"),Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis",etat_requis="Telefrag")], 3,1,0,1,"ligne",description="Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue. Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone. Le retrait de PA ne peut pas être désenvoûté."))
            sorts.append(Sort.Sort("Distorsion Temporelle",4,0,0,[Effets.EffetDegats(26,30,"air",zone=Zones.TypeZoneCarre(1),cibles_possibles="Ennemis"),Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneCarre(1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur")], 2,1,0,0,"cercle",description="Occasionne des dommages Air aux ennemis. Téléporte les cibles à leur position précédente."))
            sorts.append(Sort.Sort("Vol du Temps",4,1,5,[Effets.EffetDegats(30,34,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostPA("Vol du Temps",1,1,1))], 3,2,0,0,"cercle",chaine=True,description="Occasionne des dommages Eau à la cible. Le lanceur gagne 1 PA au début de son prochain tour."))
            sorts.append(Sort.Sort("Pétrification",5,1,7,[Effets.EffetDegats(34,38,"eau"),Effets.EffetEtatSelf(Etats.EtatCoutPA("Pétrification",0,2,"Pétrification",-1),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag"), Effets.EffetRetPA(2)], 3,2,0,1,"ligne",description="Occasionne des dommages Eau et retire des PA. Si la cible est dans l'état Téléfrag, le coût en PA du sort est réduit pendant 2 tours."))
            sorts.append(Sort.Sort("Flou",2,1,3,[Effets.EffetEtat(Etats.EtatBoostPA("Flou",0,1,-2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True),Effets.EffetEtat(Etats.EtatBoostPA("Flou",1,1,2),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)], 1,1,3,0,"cercle",description="Retire des PA en zone le tour en cours. Augmente les PA en zone le tour suivant."))
            sorts.append(Sort.Sort("Conservation",2,0,5,[Effets.EffetEtat(Etats.EtatModDegPer("Conservation",0,1,130),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur"),Effets.EffetEtat(Etats.EtatModDegPer("Conservation",1,1,70),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur")], 1,1,2,0,"cercle",description="Augmente les dommages subis par l'allié ciblé ou le lanceur de 50%% pour le tour en cours. Au tour suivant, la cible réduit les dommages subis de 30%%."))
            sorts.append(Sort.Sort("Poussière Temporelle",4,0,6,[Effets.EffetDegats(34,37,"feu",cibles_possibles="Ennemis"), Effets.EffetDegats(34,37,"feu",zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag"),Effets.EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3),etat_requis_cibles="Telefrag")], 2,2,0,1,"cercle",description="Occasionne des dommages Feu. Si la cible est dans l'état Téléfrag, les dommages sont occasionnés en zone et les entités à proximité sont téléportées symétriquement par rapport au centre de la zone d'effet."))
            sorts.append(Sort.Sort("Suspension Temporelle",3,1,4,[Effets.EffetDureeEtats(1,etat_requis="Telefrag",consomme_etat=True),Effets.EffetDegats(25,29,"feu")], 3,2,0,0,"ligne",description="Occasionne des dommages Feu sur les ennemis. Réduit la durée des effets sur les cibles ennemies dans l'état Téléfrag et retire l'état."))
            sorts.append(Sort.Sort("Raulebaque",2,0,0,[Effets.EffetTeleportePosPrec(1,zone=Zones.TypeZoneCercle(99))], 1,1,2, 0, "cercle",description="Replace tous les personnages à leurs positions précédentes."))
            sorts.append(Sort.Sort("Instabilité Temporelle",3,0,7,[Effets.EffetGlyphe(activationInstabiliteTemporelle,2,"Instabilité Temporelle",(255,255,0),zone=Zones.TypeZoneCercle(3),faire_au_vide=True)], 1,1,3,1,"cercle",description="Pose un glyphe qui renvoie les entités à leur position précédente. Les effets du glyphe sont également exécutés lorsque le lanceur génère un Téléfrag."))
            sorts.append(Sort.Sort("Démotivation",3,1,5,[Effets.EffetDegats(23,26,"terre",cibles_possibles="Ennemis"),Effets.EffetDureeEtats(1,cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",etat_requis="Telefrag",consomme_etat=True)], 3,2,0,0,"diagonale",description="Occasionne des dommages Terre aux ennemis en diagonale. Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état."))
            sorts.append(Sort.Sort("Pendule",5,1,5,[Effets.EffetTpSym(),Effets.EffetDegatsPosLanceur(48,52,"air",zone=Zones.TypeZoneCercleSansCentre(2),cibles_possibles="Ennemis"), Effets.EffetTeleportePosPrecLanceur(1,cibles_possibles="Lanceur")], 2,1,0,0,"cercle",chaine=True,description="Le lanceur se téléporte symétriquement par rapport à la cible et occasionne des dommages Air en zone sur sa cellule de destination. Il revient ensuite à sa position précédente."))
            sorts.append(Sort.Sort("Paradoxe Temporel",3,0,0,[Effets.EffetEntiteLanceSort("Complice|Cadran de Xélor",activationParadoxeTemporel)], 1,1,2,0,"cercle",description="Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran). Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles. Fixe le temps de relance de Cadran de Xélor et de Complice à 1."))
            sorts.append(Sort.Sort("Faille Temporelle",3,0,0,[Effets.EffetEchangePlace(zone=Zones.TypeZoneCercle(99),cibles_possibles="Cadran de Xélor|Complice",generer_TF=True),Effets.EffetEtat(Etats.EtatEffetFinTour("Retour faille temporelle", 1,1,Effets.EffetTeleportePosPrec(1),"Fin faille Temporelle","cible")), Effets.EffetEtat(Etats.Etat("Faille_temporelle",0,1),zone=Zones.TypeZoneCercle(99),cibles_possibles="Xelor")], 1,1,3,0,"cercle",description="Le lanceur échange sa position avec celle du Complice (ou du Cadran). À la fin du tour, le Complice (ou le Cadran) revient à sa position précédente. La Synchro ne peut pas être déclenchée pendant la durée de Faille Temporelle."))
            sorts.append(Sort.Sort("Synchro",2,1,4,[Effets.EffetInvoque("Synchro",cibles_possibles="",faire_au_vide=True)], 1,1,3,0,"cercle",description="Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour. La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag. Elle n'est pas affectée par les effets de Rembobinage. À partir du tour suivant son lancer, son invocateur perd 1 PA."))
            sorts.append(Sort.Sort("Désynchronisation",2,1,6,[Effets.EffetPiege(Zones.TypeZoneCercle(0),activationDesynchro,"Désynchronisation",(255,0,255),faire_au_vide=True)],2,2,0,1, "cercle", description="Pose un piège qui téléporte symétriquement les entités proches."))
            sorts.append(Sort.Sort("Contre",2,0,6,[Effets.EffetEtat(Etats.EtatContre("Contre",0,2, 50,1),zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Lanceur", faire_au_vide=True)], 1,1,5,0,"cercle", description="Renvoie une partie des dommages subis en mêlée à l'attaquant."))
            sorts.append(Sort.Sort("Bouclier Temporel",3,0,3,[Effets.EffetEtat(Etats.EtatEffetSiSubit("Bouclier temporel",0,1, Effets.EffetTeleportePosPrec(1),"Bouclier Temporel","lanceur",""))], 1,1,3,0,"cercle",description="Si la cible subit des dommages, son attaquant revient à sa position précédente."))
            sorts.append(Sort.Sort("Fuite",1,0,5,[Effets.EffetEtat(Etats.EtatEffetDebutTour("Fuite", 1,1,Effets.EffetTeleportePosPrec(1),"Fuite","cible"))], 4,2,0,0,"cercle",description="Téléporte la cible sur sa position précédente au début du prochain tour du lanceur."))
            sorts.append(Sort.Sort("Horloge",5,1,6,[Effets.EffetVolDeVie(36,39,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostPA("Horloge",1,1,1)),Effets.EffetRetPA(4,cibles_possibles="Ennemis",etat_requis="Telefrag",consomme_etat=True)], 3,2,0,0,"ligne", chaine=True,description="Vole de vie dans l'élément Eau. Le lanceur gagne 1 PA au début de son prochain tour. Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état. Le retrait de PA ne peut pas être désenvoûté."))
            sorts.append(Sort.Sort("Clepsydre",4,1,3,[Effets.EffetDegats(30,34,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostPA("Clepsydre",1,1,2),etat_requis="Telefrag",consomme_etat=True)], 2,2,0,0,"cercle", chaine=True,description="Occasionne des dommages Eau. Si la cible est dans l'état Téléfrag, le lanceur gagne 2 PA au prochain tour. Retire l'état Téléfrag."))
            sorts.append(Sort.Sort("Frappe de Xélor",3,1,3,[Effets.EffetDegats(23,27,"terre",cibles_possibles="Ennemis"), Effets.EffetTpSymSelf()], 3,2,0,0,"cercle",chaine=False,description="Occasionne des dommages Terre aux ennemis. Téléporte la cible symétriquement par rapport au lanceur du sort."))
            sorts.append(Sort.Sort("Engrenage",3,1,5,[Effets.EffetDegats(31,35,"terre",zone=Zones.TypeZoneLignePerpendiculaire(1),cibles_possibles="Ennemis"), Effets.EffetTpSymCentre(zone=Zones.TypeZoneLignePerpendiculaire(1))], 2,2,0,0,"ligne",chaine=False,description="Occasionne des dommages Terre et téléporte les cibles symétriquement par rapport au centre de la zone d'effet."))
            sorts.append(Sort.Sort("Momification",2,0,0,[Effets.EffetEtat(Etats.EtatBoostPM("Momification",0,1,2)),Effets.EffetEtat(Etats.EtatTelefrag("Telefrag",0,2,"Momification"),zone=Zones.TypeZoneCercle(99)),Effets.EffetEtat(Etats.EtatBoostDommage("Momie",0,1,-99999999))], 1,1,3,0,"cercle",description="Le lanceur ne peut plus occasionner de dommages avec ses sorts élémentaires et gagne 2 PM pendant 1 tour. Fixe l'état Téléfrag à tous les alliés et ennemis pendant 2 tours. Quand l'état Téléfrag est retiré, le lanceur gagne 100 Puissance pendant 2 tours."))
            sorts.append(Sort.Sort("Glas",15,0,3,[Effets.EffetTeleporteDebutCombat(),Effets.EffetEtat(Etats.EtatBoostPerDommageSorts("Glas",1,1,-50)),Effets.EffetRetireEtat("Glas",zone=Zones.TypeZoneCercle(99),cibles_possibles="Lanceur")], 1,1,3,0,"ligne",description=" Renvoie la cible à sa cellule de début de combat (en ignorant les états qui empêchent les déplacements) et divise ses dommages occasionnés par 2 pendant 1 tour. Le coût en PA est réduit en fonction du nombre de téléfrags générés depuis son dernier lancer."))
        elif(classe=="Iop"):
            activationRassemblement= Sort.Sort("AttireAllies",0,0,0,[Effets.EffetAttire(2,zone=Zones.TypeZoneCroix(3))],99,99,0,0,"cercle")
            activationFriction= Sort.Sort("Attire",0,0,0,[Effets.EffetAttire(1,zone=Zones.TypeZoneCroix(99))],99,99,0,0,"cercle")
            sorts.append(Sort.Sort("Pression",3,1,3,[Effets.EffetEtat(Etats.EtatBoostErosion("Pression",0,2,10)), Effets.EffetDegats(21,25,"terre")], 99,3,0,0,"cercle",description="Occasionne des dommages Terre et applique un malus d'Érosion."))
            sorts.append(Sort.Sort("Tannée",4,1,7,[Effets.EffetDegats(30,34,"air",zone=Zones.TypeZoneLignePerpendiculaire(1)),Effets.EffetRetPM(3,zone=Zones.TypeZoneLignePerpendiculaire(1))], 2,2,0,0,"ligne",description="Occasionne des dommages Air en zone et retire des PM."))
            sorts.append(Sort.Sort("Bond",5,1,6,[Effets.EffetTp(cibles_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatModDegPer("Bond",0,1,115),zone=Zones.TypeZoneCercle(1),cibles_possibles="Ennemis")], 1,1,2,0,"cercle",description="Téléporte sur la case ciblée. Augmente les dommages reçus par les ennemis situés sur les cases adjacentes."))
            sorts.append(Sort.Sort("Détermination",2,0,0,[Effets.EffetEtat(Etats.Etat("Indeplacable",0,1)),Effets.EffetEtat(Etats.EtatModDegPer("Determination",0,1,75))], 1,1,2,0,"cercle",description="Fixe l'état Indéplaçable et réduit 25%% des dommages subis pendant 1 tour. Ne peut pas être désenvoûté."))
            sorts.append(Sort.Sort("Intimidation",2,1,2,[Effets.EffetDegats(11,13,"terre"),Effets.EffetPousser(4)], 3,2,0,0,"ligne",description="Occasionne des dommages Neutre sur les ennemis et repousse la cible."))
            sorts.append(Sort.Sort("Menace",3,0,3,[Effets.EffetDegats(26,28,"eau",cibles_exclues="Lanceur"),Effets.EffetAttire(2,cibles_exclues="Lanceur")], 3,2,0,0,"cercle",description="Occasionne des dommages Eau et attire la cible. Le lanceur gagne des points de bouclier."))
            sorts.append(Sort.Sort("Déferlement",3,0,5,[Effets.EffetDegats(28,32,"eau",cibles_exclues="Lanceur"),Effets.EffetAttireAttaquant(4,cibles_exclues="Lanceur")], 3,2,0,0,"ligne",description="Occasionne des dommages Eau aux ennemis et rapproche le lanceur de la cible. Le lanceur gagne des points de bouclier."))
            sorts.append(Sort.Sort("Conquête",3,1,6,[Effets.EffetInvoque("Stratège Iop",cible_possibles="",faire_au_vide=True),Effets.EffetEtat(Etats.EtatRedistribuerPer("Strategie iop",0,-1, 50,"Ennemis|Allies",2))], 1,1,3,0,"ligne",description="Invoque un épouvantail qui redistribue à proximité (2 cases) 50%% des dommages qu'il subit."))
            sorts.append(Sort.Sort("Epée Divine",3,0,0,[Effets.EffetDegats(21,23,"air",zone=Zones.TypeZoneCroix(3),cibles_possibles="Ennemis"), Effets.EffetEtat(Etats.EtatBoostDommage("Epee Divine",0,4,20),zone=Zones.TypeZoneCroix(3),cibles_possibles="Allies|Lanceur")], 2,2,0,0,"cercle",chaine=False,description="Occasionne des dommages Air et augmente les dommages des alliés ciblés."))
            sorts.append(Sort.Sort("Fendoir",5,0,4,[Effets.EffetDegats(47,53,"eau",zone=Zones.TypeZoneCroix(1),cibles_exclues="Lanceur")], 2,2,0,0,"cercle",description="Occasionne des dommages Eau en zone. Applique des points de bouclier pour chaque ennemi touché."))
            sorts.append(Sort.Sort("Épée Destructrice",4,1,5,[Effets.EffetDegats(32,36,"feu",zone=Zones.TypeZoneLignePerpendiculaire(1))], 2,2,0,0,"ligne",description="Occasionne des dommages Feu et réduit la probabilité que la cible occasionne des coups critiques."))
            sorts.append(Sort.Sort("Anneau Destructeur",3,0,2,[Effets.EffetDegats(26,30,"air",zone=Zones.TypeZoneAnneau(3), faire_au_vide=True), Effets.EffetAttire(1,zone=Zones.TypeZoneAnneau(3),faire_au_vide=True)], 2,2,0,0,"cercle",description="Occasionne des dommages Air en anneau et attire les cibles."))
            sorts.append(Sort.Sort("Massacre",2,1,7,[Effets.EffetEtat(Etats.EtatRedistribuerPer("Massacre",0,2,50,"Ennemis",1))], 1,1,3,0,"cercle",description="Lorsque la cible ennemie reçoit des dommages de sorts, elle occasionne 50% de ces dommages aux entités au contact."))
            sorts.append(Sort.Sort("Rassemblement",2,1,6,[Effets.EffetAttire(2,zone=Zones.TypeZoneCroix(3),cibles_possibles="Ennemis"),Effets.EffetEtat(Etats.EtatLanceSortSiSubit("Rassemblement",0,1,activationRassemblement),cible_possibles="Ennemis")], 1,1,2,0,"cercle",description="La cible attire ses alliés à proximité (2 cases) lorsqu'elle est attaquée."))
            sorts.append(Sort.Sort("Souffle",2,2,8,[Effets.EffetPousser(1,zone=Zones.TypeZoneCercleSansCentre(1),faire_au_vide=True)],1,1,2,0,"cercle",description="Repousse les alliés et les ennemis situés autour de la cellule ciblée."))
            sorts.append(Sort.Sort("Violence",2,0,0,[Effets.EffetAttire(1,zone=Zones.TypeZoneCercle(2),cibles_possibles="Allies|Ennemis"),Effets.EffetEtat(Etats.EtatBoostDoPou("Violence",0,1,50))],1,1,0,0,"cercle",description="Attire les entités à proximité et augmente les dommages de poussée et le Tacle pour chaque ennemi dans la zone d'effet."))
            sorts.append(Sort.Sort("Concentration",2,1,1,[Effets.EffetDegats(20,24,"terre")],4,3,0,0,"ligne",description="Occasionne des dommages Terre. Les dommages sont augmentés contre les Invocations."))
            sorts.append(Sort.Sort("Accumulation",3,0,4,[Effets.EffetDegats(28,32,"terre",cibles_possibles="Ennemis"),Effets.EffetRetireEtat("Accumulation",zone=Zones.TypeZoneCercle(99),cible_possibles="Iop"),Effets.EffetEtat(Etats.EtatBoostBaseDeg("Accumulation",0,3,"Accumulation",20),cibles_possibles="Lanceur")],2,2,0,0,"ligne",chaine=False,description="Occasionne des dommages Terre. Si le sort est lancé sur soi, le sort n'occasionne pas de dommages et ils sont augmentés pour les prochains lancers."))
            sorts.append(Sort.Sort("Couper",3,1,4,[Effets.EffetDegats(18,22,"feu",zone=Zones.TypeZoneLigne(3)),Effets.EffetRetPM(3,zone=Zones.TypeZoneLigne(3))],2,2,0,1,"ligne",description="Occasionne des dommages Feu et retire des PM."))
            sorts.append(Sort.Sort("Fracture",4,1,4,[Effets.EffetEtat(Etats.EtatBoostErosion("Fracture",0,2,13), zone=Zones.TypeZoneLigneJusque(0)), Effets.EffetDegats(26,30,"air",zone=Zones.TypeZoneLigneJusque(0))],2,2,0,0,"ligne",description="Occasionne des dommages Air jusqu'à la cellule ciblée. Applique un malus d'Érosion."))
            sorts.append(Sort.Sort("Friction",2,0,5,[Effets.EffetAttire(1,zone=Zones.TypeZoneCroix(99)),Effets.EffetEtat(Etats.EtatLanceSortSiSubit("Friction",0,2,activationFriction))],1,1,3,0,"cercle",description="La cible se rapproche de l'attaquant si elle reçoit des dommages issus de sorts. Nécessite d'être aligné avec la cible."))
            sorts.append(Sort.Sort("Coup pour coup",2,1,3,[Effets.EffetPousser(2),Effets.EffetEtat(Etats.EtatRepousserSiSubit("Coup_pour_coup",0,2,2))],1,1,3,0,"cercle",description="La cible est repoussée de 2 cases à chaque fois qu'elle attaque le lanceur."))
            sorts.append(Sort.Sort("Duel",3,1,1,[],1,1,4,0,"cercle",description="Retire leurs PM à la cible et au lanceur, leur applique l'état Pesanteur et les rend invulnérable aux dommages à distance. Ne fonctionne que si lancé sur un ennemi."))
            sorts.append(Sort.Sort("Emprise",3,1,1,[],1,1,4,0,"cercle",description="Retire tous les PM de l'ennemi ciblé mais le rend invulnérable."))
            sorts.append(Sort.Sort("Épée du Jugement",4,1,5,[Effets.EffetDegats(20,28,"air"),Effets.EffetVolDeVie(10,12,"feu")],3,2,0,0,"cercle",description="Occasionne des dommages Air et vole de la vie dans l'élément Feu sans ligne de vue."))
            sorts.append(Sort.Sort("Condamnation",3,1,6,[
                Effets.EffetDegats(33,37,"feu",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_2",consomme_etat=False),
                Effets.EffetDegats(33,37,"air",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_2",consomme_etat=True),
                Effets.EffetEtat(Etats.Etat("Condamnation_lancer_2",0,-1),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=True),
                Effets.EffetDegats(23,27,"feu",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=False),
                Effets.EffetDegats(23,27,"air",zone=Zones.TypeZoneCercle(99),etat_requis_cibles="Condamnation_lancer_1",consomme_etat=True),
                Effets.EffetEtat(Etats.Etat("Condamnation_lancer_1",0,-1),etat_requis_cibles="!Condamnation_lancer_2")
                ],3,2,0,0,"cercle",chaine=False,description="Occasionne des dommages Air et Feu. Les dommages sont appliqués lorsque le sort est lancé sur une autre cible. Peut se cumuler 2 fois sur une même cible."))
            sorts.append(Sort.Sort("Puissance",3,0,6,[Effets.EffetEtat(Etats.EtatBoostPuissance("Puissance",0,2,300))],1,1,3,0,"cercle",description="Augmente la Puissance de la cible."))
            sorts.append(Sort.Sort("Vertu",3,0,0,[Effets.EffetEtat(Etats.EtatBoostPuissance("Vertu",0,2,-150),zone=Zones.TypeZoneCercle(1))],1,1,3,0,"cercle",description="Applique un bouclier zone mais réduit la Puissance du lanceur."))
            sorts.append(Sort.Sort("Précipitation",2,0,6,[Effets.EffetEtat(Etats.EtatBoostPA("Precipite",0,1,5)),Effets.EffetEtat(Etats.EtatBoostPA("Sortie de Precipitation",1,1,-3))],1,1,2,0,"cercle",description="Augmente les PA de la cible pour le tour en cours mais lui retire des PA le tour suivant. Interdit l'utilisation des armes et du sort Colère de Iop."))
            sorts.append(Sort.Sort("Agitation",2,0,5,[Effets.EffetEtat(Etats.EtatBoostPM("Agitation",0,1,2)),Effets.EffetEtat(Etats.Etat("Intaclable",1,1))],2,2,0,0,"cercle",description="Augmente les PM et la Fuite pour le tours en cours."))
            sorts.append(Sort.Sort("Tempête de Puissance",3,3,5,[Effets.EffetDegats(34,38,"feu")],3,2,0,0,"cercle",description="Occasionne des dommages Feu."))
            sorts.append(Sort.Sort("Tumulte",4,2,5,[Effets.EffetDegats(19,21,"feu",zone=Zones.TypeZoneCroix(1))],1,1,1,0,"cercle",description="Occasionne des dommages Feu en zone. Plus le nombre de cibles est important, plus les dommages sont importants.*"))
            sorts.append(Sort.Sort("Épée Céleste",4,0,4,[Effets.EffetDegats(36,40,"air",zone=Zones.TypeZoneCercle(2))],2,2,0,0,"ligne",description="Occasionne des dommages Air en zone."))
            sorts.append(Sort.Sort("Zénith",5,1,3,[Effets.EffetDegats(86,94,"air",zone=Zones.TypeZoneLigne(4))],1,1,0,0,"ligne",description="Occasionne des dommages Air en zone. Les dommages sont augmentés pour chaque PM disponible lorsque le sort est lancé."))
            sorts.append(Sort.Sort("Vitalité",3,0,6,[Effets.EffetEtat(Etats.EtatBoostVita("Vitalite",0,4,20))],1,1,2,0,"cercle",description="Augmente temporairement les PV de la cible en pourcentage. Le bonus de PV est plus faible sur les alliés que sur le lanceur."))
            sorts.append(Sort.Sort("Endurance",4,0,1,[Effets.EffetDegats(34,38,"eau",cibles_exclues="Lanceur")],3,2,0,0,"cercle",description="Occasionne des dommages Eau. Applique des points de bouclier au lanceur."))
            sorts.append(Sort.Sort("Épée de Iop",4,1,6,[Effets.EffetDegats(37,41,"terre",zone=Zones.TypeZoneCroix(3),cibles_possibles="Allies|Ennemis",cibles_exclues="Lanceur",faire_au_vide=True)],2,2,0,0,"ligne",description="Occasionne des dommages Terre en croix.")) 
            sorts.append(Sort.Sort("Pugilat",2,1,4,[Effets.EffetDegats(9,11,"terre",zone=Zones.TypeZoneCercle(2),cibles_exclues="Lanceur"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Pugilat",0,1,"Pugilat",20))],4,1,0,0,"cercle",description="Occasionne des dommages Terre en zone. Les dommages sont augmentés pendant 1 tour après chaque lancer.")) 
            sorts.append(Sort.Sort("Épée du Destin",4,1,1,[Effets.EffetDegats(38,42,"feu"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Epee_du_destin", 2,1,"Épée du Destin",30))], 1,1,2,0,"ligne",description="Occasionne des dommages Feu. Les dommages sont augmentés à partir du second lancer.")) 
            sorts.append(Sort.Sort("Sentence",2,1,6,[Effets.EffetDegats(13,16,"feu"),Effets.EffetEtat(Etats.EtatEffetFinTour("Sentence", 1,1,Effets.EffetDegats(13,16,"feu",zone=Zones.TypeZoneCercle(2)),"Sentence","lanceur"))], 3,1,0,0,"ligne",description="Occasionne des dommages Feu. Occasionne des dommages Feu supplémentaires en zone à la fin du tour de la cible.")) 
            sorts.append(Sort.Sort("Colère de Iop",7,1,1,[Effets.EffetDegats(81,100,"terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Colere_de_Iop", 3,1,"Colère de Iop",110))], 1,1,3,0,"ligne",description="Occasionne des dommages Terre. Augmente les dommages du sort au troisième tour après son lancer.")) 
            sorts.append(Sort.Sort("Fureur",3,1,1,[Effets.EffetDegats(28,32,"terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fureur", 1,2,"Fureur",40))], 1,1,0,0,"ligne",description="Occasionne des dommages Terre. Les dommages sont augmentés à chaque lancer du sort, mais ce bonus est perdu si le sort n'est pas relancé."))
        elif classe=="Crâ":
            sorts.append(Sort.Sort("Flèche Magique",3,1,12,[Effets.EffetDegats(19,21,"air"),Effets.EffetEtat(Etats.EtatBoostPO("Fleche Magique",1,1,-2)),Effets.EffetEtatSelf(Etats.EtatBoostPO("Fleche Magique",0,1,2))],3,2,0,1,"cercle",description="Occasionne des dommages Air et vole la portée de la cible."))
            sorts.append(Sort.Sort("Flèche de Concentration",3,3,8,[Effets.EffetDegats(22,26,"air",zone=Zones.TypeZoneCroix(3),cibles_possibles="Ennemis" ),Effets.EffetAttireVersCible(2,zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis")],2,1,0,1,"cercle",description="Occasionne des dommages Air et attire vers la cible."))
            sorts.append(Sort.Sort("Flèche de Recul",3,1,8,[Effets.EffetDegats(25,28,"air"),Effets.EffetRepousser(4)],2,1,0,0,"ligne",description="Occasionne des dommages Air aux ennemis et pousse la cible."))
            sorts.append(Sort.Sort("Flèche Érosive",3,1,3,[Effets.EffetEtat(Etats.EtatBoostErosion("Fleche Erosive",0,2,10)), Effets.EffetDegats(25,29,"terre")],3,2,0,1,"ligne",description="Occasionne des dommages Terre et applique un malus d'Érosion."))
            sorts.append(Sort.Sort("Flèche de Dispersion",3,1,12,[Effets.EffetPousser(2,zone=Zones.TypeZoneCroix(2),faire_au_vide=True)],1,1,2,1,"cercle",description="Pousse les ennemis et alliés, même s'ils sont bloqués par d'autres entités."))
            sorts.append(Sort.Sort("Représailles",4,2,5,[Effets.EffetEtat(Etats.EtatBoostPM("Immobilise",1,1,-100)),Effets.EffetEtat(Etats.Etat("Pesanteur",1,1))],1,1,5,0,"ligne",description="Immobilise la cible."))
            sorts.append(Sort.Sort("Flèche Glacée",3,3,6,[Effets.EffetDegats(17,19,"feu"),Effets.EffetRetPA(2)],99,2,0,1,"cercle",description="Occasionne des dommages Feu et retire des PA."))
            sorts.append(Sort.Sort("Flèche Paralysante",5,2,6,[Effets.EffetDegats(39,42,"feu",zone=Zones.TypeZoneCroix(1)),Effets.EffetRetPA(4,zone=Zones.TypeZoneCroix(1))],1,1,0,0,"cercle",description="Occasionne des dommages Feu et retire des PA."))
            sorts.append(Sort.Sort("Flèche Enflammée",4,1,8,[Effets.EffetDegats(33,35,"feu",zone=Zones.TypeZoneLigne(5) ,faire_au_vide=True),Effets.EffetPousser(1,zone=Zones.TypeZoneLigne(5),faire_au_vide=True)],2,2,0,1,"ligne",description="Occasionne des dommages Feu et pousse les cibles présentes dans la zone d'effet du sort."))
            sorts.append(Sort.Sort("Flèche Repulsive",3,1,7,[Effets.EffetDegats(28,32,"feu",zone=Zones.TypeZoneLignePerpendiculaire(1),faire_au_vide=True),Effets.EffetPousser(1,zone=Zones.TypeZoneLignePerpendiculaire(1),faire_au_vide=True)],2,2,0,0,"ligne",description="Occasionne des dommages Feu et repousse de 1 case."))
            sorts.append(Sort.Sort("Tir Éloigne",3,0,0,[Effets.EffetEtat(Etats.EtatBoostPO("Tir_eloigne",0,4,6),zone=Zones.TypeZoneCercle(3))],1,1,5,0,"cercle",description="Augmente la portée des cibles présentes dans la zone d'effet."))
            sorts.append(Sort.Sort("Acuité Absolue",4,0,0,[Effets.EffetEtat(Etats.Etat("Desactive_ligne_de_vue",0,1))],1,1,3,0,"cercle",description="Tous les sorts du Crâ peuvent être lancés au travers des obstacles."))
            sorts.append(Sort.Sort("Flèche d'Expiation",4,6,10,[Effets.EffetDegats(35,37,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_d_expiation",0,-1,"Flèche d'Expiation",36))],1,1,3,1,"cercle",description="Occasionne des dommages Eau, augmente les dommages du sort tous les 3 tours et empêche la cible d'utiliser des sorts de déplacement."))
            sorts.append(Sort.Sort("Flèche de Rédemption",3,6,8,[Effets.EffetDegats(19,22,"eau"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_de_redemption",1,1,"Flèche de Rédemption",12))],3,2,0,1,"cercle",description="Occasionne des dommages Eau qui sont augmentés si le sort est relancé le tour suivant."))
            sorts.append(Sort.Sort("Oeil de Taupe",3,5,10,[Effets.EffetVolDeVie(16,18,"eau",zone=Zones.TypeZoneCercle(3), faire_au_vide=True),Effets.EffetEtat(Etats.EtatBoostPO("Oeil_de_taupe",1,3,-3),zone=Zones.TypeZoneCercle(3)),Effets.EffetRetireEtat("Invisible",zone=Zones.TypeZoneCercle(3)),Effets.EffetDevoilePiege(zone=Zones.TypeZoneCercle(3), faire_au_vide=True)],1,1,4,1,"cercle",chaine=False,description="Réduit la portée des personnages ciblés, vole de la vie dans l'élément Eau et repère les objets invisibles dans sa zone d'effet."))
            sorts.append(Sort.Sort("Flèche Écrasante",3,5,7,[Effets.EffetDegats(34,38,"feu",zone=Zones.TypeZoneCroixDiagonale(1)),Effets.EffetEtat(Etats.Etat("Pesanteur",1,1),zone=Zones.TypeZoneCroixDiagonale(1))],1,1,3,1,"cercle",description="Occasionne des dommages Feu et applique l'état Pesanteur."))
            sorts.append(Sort.Sort("Tir Critique",2,0,6,[Effets.EffetEtat(Etats.Etat("Tir_critique",0,4))],1,1,5,1,"cercle",description="Augmente la probabilité de faire un coup critique."))
            sorts.append(Sort.Sort("Balise de Rappel",2,1,5,[Effets.EffetInvoque("Balise de rappel",cibles_possibles="",faire_au_vide=True)],1,1,2,0,"cercle",description="Invoque une balise qui échange sa position avec celle du lanceur (au début du prochain tour)."))
            sorts.append(Sort.Sort("Flèche d'Immobilisation",2,1,6,[Effets.EffetDegats(10,11,"eau"),Effets.EffetEtat(Etats.EtatBoostPM("Fleche_d_immobilisation",1,1,-1)),Effets.EffetEtatSelf(Etats.EtatBoostPM("Fleche_d_immobilisation",0,1,1))],4,2,0,1,"cercle",description="Occasionne des dommages Eau et vole des PM à la cible."))
            sorts.append(Sort.Sort("Flèche Assaillante",3,2,6,[Effets.EffetDegats(33,37,"eau",cibles_possibles="Ennemis"),Effets.EffetPousser(1,cibles_possibles="Ennemis"),Effets.EffetAttireAttaquant(1,cibles_possibles="Allies")],3,2,0,1,"ligne",description="Occasionne des dommages Eau sur les ennemis et le lanceur recule de 1 case. Sur un allié : rapproche le lanceur de 1 case."))
            sorts.append(Sort.Sort("Flèche Punitive",4,6,8,[Effets.EffetDegats(29,31,"terre"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_punitive",0,-1,"Flèche Punitive",30))],1,1,2,1,"cercle",description="Occasionne des dommages Terre et augmente les dommages du sort tous les 2 tours."))
            sorts.append(Sort.Sort("Flèche du Jugement",3,5,7,[Effets.EffetDegats(39,45,"terre")],3,2,0,1,"cercle",description="Occasionne des dommages Terre. Plus le pourcentage de PM du personnage au lancement du sort est important, plus les dommages occasionnés sont importants."))
            sorts.append(Sort.Sort("Tir Puissant",3,0,6,[Effets.EffetEtat(Etats.EtatBoostPuissance("Tir_puissant",0,3,250))],1,1,6,1,"cercle",description="Augmente les dommages des sorts."))
            sorts.append(Sort.Sort("Balise Tactique",1,1,10,[Effets.EffetInvoque("Balise Tactique",cibles_possibles="", faire_au_vide=True)],1,1,2,1,"cercle",description="Invoque une Balise qui peut servir d'obstacle et de cible. La Balise subit 2 fois moins de dommages des alliés."))
            sorts.append(Sort.Sort("Flèche Harcelante",3,1,7,[Effets.EffetDegats(13,15,"air")],1,1,2,1,"cercle",description="Occasionne des dommages Air sans ligne de vue."))
            sorts.append(Sort.Sort("Flèche Massacrante",4,4,8,[Effets.EffetDegats(34,38,"air"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_massacrante",1,1,"Flèche Massacrante",10))],3,2,0,1,"ligne",description="Occasionne des dommages Air. Les dommages du sort sont augmentés au tour suivant."))
            sorts.append(Sort.Sort("Flèche Empoisonnée",3,1,10,[Effets.EffetRetPM(3),Effets.EffetEtat(Etats.EtatEffetDebutTour("Fleche_empoisonnee", 1,2,Effets.EffetDegats(17,18,"terre"),"Fleche_empoisonnee","lanceur"))],4,1,0,1,"cercle",description="Occasionne des dommages Neutre sur plusieurs tours et retire des PM."))
            sorts.append(Sort.Sort("Flèche Persecutrice",3,5,8,[Effets.EffetDegats(15,17,"feu"),Effets.EffetDegats(15,17,"air")],99,2,0,1,"ligne",description="Occasionne des dommages Air et Feu."))
            sorts.append(Sort.Sort("Flèche Tyrannique",4,2,7,[Effets.EffetEtat(Etats.EtatEffetSiPousse("Fleche_tyrannique_air",0,2, Effets.EffetDegats(12,12,"air"),"Fleche_tyrannique","lanceur")),Effets.EffetEtat(Etats.EtatEffetSiSubit("Fleche_tyrannique_feu",0,2, Effets.EffetDegats(12,12,"feu"),"Fleche_tyrannique","doPou","lanceur"))],99,1,0,1,"ligne",description="Occasionne des dommages Air si la cible est poussée. Occasionne des dommages Feu si la cible subit des dommages de poussée."))
            sorts.append(Sort.Sort("Flèche Destructrice",4,5,8,[Effets.EffetDegats(30,32,"terre"),Effets.EffetEtat(Etats.EtatBoostDommage("Flèche destructrice",1,1,-60))],99,2,0,1,"cercle",description="Occasionne des dommages Terre et réduit les dommages occasionnés par la cible."))
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
            sorts.append(Sort.Sort("Flèche cinglante",2,1,9,[Effets.EffetEtat(Etats.EtatBoostErosion("Fleche cinglante",0,2,10)), Effets.EffetPousser(2)],4,2,0,1,"ligne",description="Applique de l'Érosion aux ennemis et repousse de 2 cases."))
            sorts.append(Sort.Sort("Flèche de repli",1,2,7,[Effets.EffetPousser(1,zone=Zones.TypeZoneCercleSansCentre(5),cible_possibles="Lanceur")],4,2,0,1,"ligne",description="Le lanceur du sort recule de 2 cases."))
            sorts.append(Sort.Sort("Flèche ralentissante",4,1,8,[Effets.EffetRetPA(3,zone=Zones.TypeZoneCercle(2)),Effets.EffetDegats(36,38,"eau",zone=Zones.TypeZoneCercle(2))],2,1,0,1,"ligne",description="Occasionne des dommages Eau et retire des PA en zone."))
            sorts.append(Sort.Sort("Flèche percutante",2,1,6,[Effets.EffetDegats(6,10,"eau"),Effets.EffetEtat(Etats.EtatEffetFinTour("Fleche_percutante_retardement", 1,1,Effets.EffetDegats(6,10,"eau",zone=Zones.TypeZoneCercleSansCentre(2)),"Fleche_percutante_retardement","lanceur")),Effets.EffetEtat(Etats.EtatEffetFinTour("Fleche_percutante_retardementPA", 1,1,Effets.EffetRetPA(2,zone=Zones.TypeZoneCercleSansCentre(2)),"Fleche_percutante_retardementPA","lanceur"))],2,1,0,1,"cercle",description="Occasionne des dommages Eau. À la fin de son tour, la cible occasionne des dommages Eau et retire des PA en cercle de taille 2 autour d'elle."))
            sorts.append(Sort.Sort("Flèche explosive",4,1,8,[Effets.EffetDegats(30,34,"feu",zone=Zones.TypeZoneCercle(3))],2,1,0,1,"cercle",description="Occasionne des dommages Feu en zone."))
            fleche_fulminante=Sort.Sort("Flèche Fulminante",4,1,8,[Effets.EffetDegats(34,38,"feu",cibles_possibles="Ennemis|Balise Tactique"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_Fulminante_boost",0,1,"Flèche Fulminante Rebond",10))],1,1,0,1,"cercle",description="Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
            fleche_fulminante_rebond=Sort.Sort("Flèche Fulminante Rebond",0,0,99,[Effets.EffetDegats(34,38,"feu",cibles_possibles="Ennemis|Balise Tactique"),Effets.EffetEtatSelf(Etats.EtatBoostBaseDeg("Fleche_Fulminante_boost",0,1,"Flèche Fulminante Rebond",10))],9,1,0,0,"cercle",description="Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
            fleche_fulminante.effets.append(Effets.EffetPropage(fleche_fulminante_rebond,Zones.TypeZoneCercle(2),cibles_possibles="Ennemis|Balise Tactique"))
            fleche_fulminante_rebond.effets.append(Effets.EffetPropage(fleche_fulminante_rebond,Zones.TypeZoneCercle(2),cibles_possibles="Ennemis|Balise Tactique"))
            sorts.append(fleche_fulminante)
            sorts.append(Sort.Sort("Maîtrise de l'arc",2,0,6,[Effets.EffetEtat(Etats.EtatBoostDommage("Maitrise de l'arc",0,3,60))],1,1,5,1,"cercle",description="Augmente les dommages."))
            sorts.append(Sort.Sort("Sentinelle",2,0,0,[Effets.EffetEtatSelf(Etats.EtatBoostPerDommageSorts("Sentinelle",1,1,30)),Effets.EffetEtatSelf(Etats.EtatBoostPM("Sentinelle",1,1,-100))],1,1,3,0,"cercle",description="Au tour suivant, le lanceur perd tous ses PM mais gagne un bonus de dommages."))
        elif classe=="Sram":
            activationPiegeSournois = [Effets.EffetAttire(1,zone=Zones.TypeZoneCercle(1), faire_au_vide=True)]
            activationPiegeRepulsif =[Effets.EffetPousser(2,zone=Zones.TypeZoneCercle(1), faire_au_vide=True)]
            #sorts.append(Sort.Sort(u"Sournoiserie",3,1,5,[Effets.EffetDegats(20,22,"terre")],99,3,0,1, "cercle", description=u"Occasionne des dommages Terre."))
            sorts.append(Sort.Sort("Piège sournois",3,1,8,[Effets.EffetPiege(Zones.TypeZoneCroix(1),activationPiegeSournois,"Piège sournois",(255,0,0),faire_au_vide=True)],1,1,0,1, "cercle", description="Occasionne des dommages Feu et attire."))
            sorts.append(Sort.Sort("Piège répulsif",3,1,7,[Effets.EffetPiege(Zones.TypeZoneCercle(1),activationPiegeRepulsif,"Piège répulsif",(255,0,255),faire_au_vide=True)],1,1,1,1, "cercle", description="Occasionne des dommages Feu et attire."))
        sorts.append(Sort.Sort("Cawotte",4,1,6,[Effets.EffetInvoque("Cawotte",cibles_possibles="", faire_au_vide=True)], 1,1,6,0,"cercle",description="Invoque une Cawotte")) 
        
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
                    niveau.pieges.remove(piege)
                    i-=1
                    sestApplique, cibles = niveau.lancerEffet(effet,piege.centre_x,piege.centre_y,piege.nomSort, piege.centre_x,piege.centre_y,piege.lanceur)          
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
                

    def deepcopy(self):
        """@summary: clone le personnage
        @return: le clone du personnage"""
        cp = Personnage(self.classe, self.vie, self.fo, self.agi, self.cha, self.int, self.pui,self.do,self.doFo,self.doAgi,self.doCha,self.doInt,self.doPou,self.PM,self.PA,self.PO,self.lvl,self.team,self.icone)
        cp.sorts = Personnage.ChargerSorts(cp.classe)
        return cp


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
        if self.vie - degats < 0:
            totalPerdu = self.vie
        for etat in self.etats:
            if etat.actif():
                etat.triggerAvantSubirDegats(self,niveau,totalPerdu,typeDegats,attaquant)
                
        self.vie -= totalPerdu
        erosion_base = 10
        erosion = erosion_base + self.erosion
        if erosion > 50: # L'érosion est capé à 50% dans le jeu
            erosion = 50
        elif erosion < 10: # L'érosion est capé mini à 10% dans le jeu
            erosion = 10
        self._vie -= int(totalPerdu * (erosion/100))
        if self._vie < 0:
            self._vie = 0

        print(self.classe+" a "+str(self.vie) +"/"+str(self._vie)+" PV ")
        if self.vie <= 0:
            niveau.tue(self)
        else:
            for etat in self.etats:
                if etat.actif():
                    etat.triggerApresSubirDegats(self,niveau,attaquant)

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
        #Touche clavier appuyée
        
            

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
        cp = PersonnageMur(self.classe, self.vie, self.fo, self.agi, self.cha, self.int, self.pui,self.do,self.doFo,self.doAgi,self.doCha,self.doInt,self.doPou,self.retPA, self.retPM, self.esqPA, self.esqPM, self.PM,self.PA,self.PO,self.lvl,self.team,self.icone)
        cp.sorts = Personnage.ChargerSorts(cp.classe)
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
        cp = PersonnageSansPM(self.classe, self.vie, self.fo, self.agi, self.cha, self.int, self.pui,self.do,self.doFo,self.doAgi,self.doCha,self.doInt,self.doPou,self.PM,self.PA,self.PO,self.lvl,self.team,self.icone)
        cp.sorts = Personnage.ChargerSorts(cp.classe)
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
"Cadran de Xélor" : PersonnageSansPM("Cadran de Xélor",1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"cadran_de_xelor.png"),
"Cawotte" : PersonnageMur("Cawotte",800,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"cawotte.png"),
"Synchro" : PersonnageMur("Synchro",1200,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"synchro.png"),
"Complice" : PersonnageMur("Complice",650,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"complice.png"),
"Balise de Rappel" : PersonnageSansPM("Balise de Rappel",1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"balise_de_rappel.png"),
"Balise Tactique" : PersonnageMur("Balise Tactique",1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"balise_tactique.png"),
"Stratège Iop" : PersonnageMur("Stratège Iop",1385,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"conquete.png")
}
