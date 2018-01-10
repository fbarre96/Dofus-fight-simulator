
from .Dofuk import Personnage
from .zones import *
import random
class Effet(object):
    def __init__(self, *args,**kwargs):
        self.etatRequis = kwargs.get('etat_requis',"")
        self.consommeEtat = kwargs.get('consomme_etat',False)
        self.ciblesPossibles = kwargs.get('cibles_possibles',"Allies|Ennemis|Lanceur").split("|")
        self.ciblesExclues = kwargs.get('cibles_exclues',"").split("|")
        self.typeZone = kwargs.get('zone',TypeZoneCercle(0))
    def APorteZone(self, departZone_x,departZone_y, testDansZone_x,testDansZone_y, j_x, j_y):
        #Le lanceur peut pas etre dans la zone si y a le - a la fin du type zone
        return self.typeZone.testCaseEstDedans([departZone_x,departZone_y],[testDansZone_x,testDansZone_y],[j_x,j_y])
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        print "Effet non existant"
class EffetDegats(Effet):
    def __init__(self,minJet,maxJet,typeDegats, *args, **kwargs):
        self.minJet = minJet
        self.maxJet = maxJet
        self.typeDegats = typeDegats
        super(EffetDegats, self).__init__(kwargs)
    def appliquerDegats(self,niveau,joueurCaseEffet, joueurLanceur):
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
                if etat.nom == "BoostDommage":
                    dos+=etat.tabCarac[0]
                elif etat.nom == "BoostBaseDeg" and nomSort == etat.tabCarac[0]:
                    baseDeg += etat.tabCarac[1]
                elif etat.nom == "Puissance":
                    carac += etat.tabCarac[0]
                elif etat.nom == "Momie":
                    total = -100000
        total += baseDeg + (baseDeg * ((carac) / 100)) + dos
        #appliquer les effets des etats sur les degats total du joueur cible
        for etat in joueurCaseEffet.etats:
            if etat.nom == "ModDegPer" and etat.actif():
                total = (total * etat.tabCarac[0])/100
        if total < 0:
            total = 0
        print joueurCaseEffet.classe+" perd "+ str(total) + "PV"
        joueurCaseEffet.subit(joueurLanceur,niveau,total,self.typeDegats)
        return total
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        self.appliquerDegats(niveau,joueurCaseEffet, joueurLanceur)
        
class EffetVolDeVie(EffetDegats):
    def __init__(self,minJet,maxJet,typeDegats, *args, **kwargs):
        super(EffetVolDeVie, self).__init__(minJet,maxJet,typeDegats,kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        total = super(EffetVolDeVie, self).appliquerDegats(niveau,joueurCaseEffet, joueurLanceur)
        print joueurLanceur.classe+" vol "+ str(total/2) + "PV" 
        joueurLanceur.vie += (total/2)
        if joueurLanceur.vie > joueurLanceur._vie:
            joueurLanceur.vie = joueurLanceur._vie

class EffetDegatsPosLanceur(EffetDegats):
    def __init__(self,minJet,maxJet,typeDegats, *args, **kwargs):
        super(EffetDegatsPosLanceur, self).__init__(minJet,maxJet,typeDegats,kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurLanceur = niveau.getJoueurSur(kwargs.get("prov_x"),kwargs.get("prov_y"))
        total = super(EffetDegatsPosLanceur, self).appliquerDegats(niveau,joueurCaseEffet, joueurLanceur)

 
        
class EffetRetPA(Effet):
    def __init__(self,retrait, **kwargs):
        self.retrait = retrait
        super(EffetRetPa, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        print joueurCaseEffet.classe+" -"+ str(self.retrait) + "PA"
        
class EffetRetPM(Effet):
    def __init__(self,retrait, **kwargs):
        self.retrait = retrait
        super(EffetRetPM, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        print joueurCaseEffet.classe+" -"+ str(self.retrait) + "PM"
        
class EffetEtat(Effet):
    def __init__(self,nom,duree, debuteDans, tabCarac, **kwargs):
        self.nom = nom
        self.duree = duree
        self.debuteDans = debuteDans
        self.tabCarac = tabCarac
        super(EffetEtat, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        etat = Etat(self.nom,self.duree,self.debuteDans,self.tabCarac, joueurLanceur)
        if "Condamnation_lancer_" in etat.nom:
            listePersos1 = niveau.joueursAvecEtat("Condamnation_lancer_1")
            listePersos2 = niveau.joueursAvecEtat("Condamnation_lancer_2")
            if len(listePersos1) == 0 and len(listePersos2)==0:
                joueurCaseEffet.appliquerEtat(self.etat,joueurLanceur)
            elif len(listePersos1) == 1 and len(listePersos2) == 0:
                if listePersos1[0] == joueurCaseEffet:
                    etat.nom = "Condamnation_lancer_2"
                    listePersos1[0].retirerEtats("Condamnation_lancer_1")
                    joueurCaseEffet.appliquerEtat(etat,joueurLanceur)
                else:
                    joueurLanceur.lanceSort(Sort("Condamnationx1",0,0,99,[Effet([23,27,"feu"],TypeZoneCercle(0),"deg","Allies|Ennemis|Lanceur","","Condamnation_lancer_1",False),Effet([23,27,"air"],TypeZoneCercle(0),"deg","Allies|Ennemis|Lanceur","","Condamnation_lancer_1",True)],99,99,0,0,"cercle"), self, listePersos1[0].posX,listePersos1[0].posY)
                    joueurCaseEffet.appliquerEtat(etat,joueurLanceur)
                    #listePersos1[0] doit subir les degats + retirer les etats
            elif len(listePersos2) == 1:
                #listePersos2[0] doit subir les degats + retirer les etats
                joueurLanceur.lanceSort(Sort("Condamnationx2",0,0,99,[Effet([33,37,"feu"],TypeZoneCercle(0),"deg","Allies|Ennemis|Lanceur","","Condamnation_lancer_2",False),Effet([33,37,"air"],TypeZoneCercle(0),"deg","Allies|Ennemis|Lanceur","","Condamnation_lancer_2",True)],99,99,0,0,"cercle"), self, listePersos2[0].posX,listePersos2[0].posY)
                joueurCaseEffet.appliquerEtat(etat,joueurLanceur)
            else:
                print "Cas non pris en compte"
        elif etat.nom == "BoostVita":
            pourcentageBoost = etat.tabCarac[0]
            etat.tabCarac[0] = int(joueurCaseEffet._vie * (pourcentageBoost/100.0))
            joueurCaseEffet.appliquerEtat(etat,joueurLanceur)
        else:    
            joueurCaseEffet.appliquerEtat(etat,joueurLanceur)
        
class EffetGlyphe(Effet):
    def __init__(self,sortGlyphe,duree,nom,couleur, **kwargs):
        self.sortGlyphe = sortGlyphe
        self.duree = duree
        self.nom = nom
        self.couleur = couleur
        super(EffetGlyphe, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        nouvelleGlyphe = Glyphe(self.nom, self.sortGlyphe, self.duree, kwargs.get("case_cible_x"), kwargs.get("case_cible_y"), joueurLanceur,self.couleur)
        glypheID = niveau.poseGlyphe(nouvelleGlyphe)
        
class EffetPousser(Effet):
    def __init__(self,nbCase, **kwargs):
        self.nbCase = nbCase
        super(EffetPousser, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.pousser(self.nbCase,joueurCaseEffet,True, kwargs.get("case_cible_x"), kwargs.get("case_cible_y"))
        
class EffetRepousser(Effet):
    def __init__(self,nbCase, **kwargs):
        self.nbCase = nbCase
        super(EffetRepousser, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.pousser(self.nbCase,joueurCaseEffet)
        
class EffetAttire(Effet):
    def __init__(self,nbCase, **kwargs):
        self.nbCase = nbCase
        super(EffetAttire, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.attire(self.nbCase,joueurCaseEffet,joueurLanceur)
        

class EffetAttireAllies(Effet):
    def __init__(self,nbCase, **kwargs):
        self.nbCase = nbCase
        super(EffetAttireAllies, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        if joueurCaseEffet.team == joueurLanceur.team:
            niveau.attire(self.nbCase,joueurCaseEffet,joueurLanceur)
        
class EffetDureeEtats(Effet):
    def __init__(self,deXTours, **kwargs):
        self.deXTours = deXTours
        super(EffetDureeEtats, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurCaseEffet.changeDureeEffets(self.deXTours, niveau)
        
class EffetTeleportePosPrec(Effet):
    def __init__(self,nbCase, **kwargs):
        self.nbCase = nbCase
        super(EffetTeleportePosPrec, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurCaseEffet.tpPosPrec(self.nbCase,niveau,joueurLanceur, kwargs.get("nom_sort"))

class EffetTeleportePosPrecLanceur(Effet):
    def __init__(self,nbCase,**kwargs):
        self.nbCase = nbCase
        super(EffetTeleportePosPrecLanceur, self).__init__(nbCase,kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurLanceur = niveau.getJoueurSur(kwargs.get("prov_x"),kwargs.get("prov_y"))
        joueurCaseEffet.tpPosPrec(self.nbCase,niveau,joueurLanceur, kwargs.get("nom_sort"))
                      
class EffetTeleporteDebutTour(Effet):
    def __init__(self, **kwargs):
        super(EffetTeleporteDebutTour, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.gereDeplacementTF(joueurCaseEffet,joueurCaseEffet.posDebTour,joueurLanceur,"Renvoi",AjouteHistorique=True)
        
class EffetTpSym(Effet):
    def __init__(self, **kwargs):
        super(EffetTpSym, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        distanceX = (joueurCaseEffet.posX-joueurLanceur.posX)
        distanceY = (joueurCaseEffet.posY-joueurLanceur.posY)
        arriveeX = joueurCaseEffet.posX+distanceX
        arriveeY = joueurCaseEffet.posY+distanceY
        niveau.gereDeplacementTF(joueurLanceur,[arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"),AjouteHistorique=True)
        
class EffetTpSymSelf(Effet):
    def __init__(self, **kwargs):
        super(EffetTpSymSelf, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        distanceX = (joueurCaseEffet.posX-joueurLanceur.posX)
        distanceY = (joueurCaseEffet.posY-joueurLanceur.posY)
        arriveeX = joueurLanceur.posX-distanceX
        arriveeY = joueurLanceur.posY-distanceY
        niveau.gereDeplacementTF(joueurCaseEffet,[arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"), AjouteHistorique=True)
        
class EffetTpSymCentre(Effet):
    def __init__(self, **kwargs):
        super(EffetTpSymCentre, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        distanceX = (joueurCaseEffet.posX-kwargs.get("case_cible_x"))
        distanceY = (joueurCaseEffet.posY-kwargs.get("case_cible_y"))
        arriveeX = kwargs.get("case_cible_x")-distanceX
        arriveeY = kwargs.get("case_cible_y")-distanceY
        joueurTF = niveau.gereDeplacementTF(joueurCaseEffet,[arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"), AjouteHistorique=True)
        if joueurTF != None:
            kwargs.get("cibles_traitees").append(joueurTF)
        
class EffetEtatSelf(Effet):
    def __init__(self,nom,duree, debuteDans, tabCarac, **kwargs):
        self.nom = nom
        self.duree = duree
        self.debuteDans = debuteDans
        self.tabCarac = tabCarac
        super(EffetEtatSelf, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        etat = Etat(self.nom,self.duree,self.debuteDans,self.tabCarac, joueurLanceur)
        joueurLanceur.appliquerEtat(etat,joueurLanceur)
        
class EffetEntiteLanceSort(Effet):
    def __init__(self,nomEntites,sortALancer, **kwargs):
        self.nomEntites = nomEntites
        self.sortALancer = sortALancer
        super(EffetEntiteLanceSort, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueursLanceurs = niveau.getJoueurs(self.nomEntites)
        for joueur in joueursLanceurs:
            joueur.lanceSort(self.sortALancer,niveau, joueur.posX, joueur.posY)
        
class EffetEchangePlace(Effet):
    def __init__(self, **kwargs):
        super(EffetEchangePlace, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        joueurTF = self.gereDeplacementTF(joueurLanceur,[joueurCaseEffet.posX, joueurCaseEffet.posY], joueurLanceur, kwargs.get("nom_sort"), AjouteHistorique=True)
        if joueurTF != None:
            kwargs.get("cibles_traitees").append(joueurTF)
        
class EffetTp(Effet):
    def __init__(self, **kwargs):
        super(EffetTp, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.structure[joueurLanceur.posY][joueurLanceur.posX].type = "v"
        niveau.structure[kwargs.get("case_cible_y")][kwargs.get("case_cible_x")].type = "j"
        joueurLanceur.bouge(kwargs.get("case_cible_x"),kwargs.get("case_cible_y"))
        
INVOCS = {
"Cawotte" : Personnage("Cawotte",800,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,cerveau="Stratege_iop",icone="cawotte.png"),
"Synchro" : Personnage("Synchro",1200,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,cerveau="Cadran_de_xelor",icone="synchro.png"),
"Cadran_de_xelor" : Personnage("Cadran_de_xelor",1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,cerveau="Cadran_de_xelor",icone="cadran_de_xelor.png"),
"Complice" : Personnage("Complice",650,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,cerveau="Stratege_iop",icone="complice.png"),
"Stratege_iop" : Personnage("Stratege_iop",1385,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,cerveau="Stratege_iop",icone="conquete.png")
}
class EffetInvoque(Effet):
    def __init__(self, nominvoque, **kwargs):
        self.nomInvoque = nominvoque
        super(EffetInvoque, self).__init__(kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        invoc = INVOCS[self.nomInvoque].copy()
        invoc.invocateur = joueurLanceur
        invoc.team = joueurLanceur.team
        invoc.lvl = joueurLanceur.lvl
        niveau.invoque(invoc,kwargs.get("case_cible_x"),kwargs.get("case_cible_y"))