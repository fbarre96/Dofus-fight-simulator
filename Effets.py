# -*- coding: utf-8 -*
import zones
import random
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
        self.typeZone = kwargs.get('zone',zones.TypeZoneCercle(0))

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
        joueurCaseEffet.appliquerEtat(Etats.Etat("temporaire",0,1),joueurLanceur)
        joueursAppliquables = niveau.getJoueurslesPlusProches(joueurCaseEffet.posX,joueurCaseEffet.posY,joueurLanceur,self.zone,["!temporaire"],self.ciblesPossibles)
        if len(joueursAppliquables)>0 and self.limiteCumul:
            joueurCaseEffet.lanceSort(self.sort,niveau, joueursAppliquables[0].posX, joueursAppliquables[0].posY,joueurLanceur)
class EffetEtat(Effet):
    def __init__(self, etat_etat, **kwargs):
        self.etat = etat_etat
        super(EffetEtat, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        if joueurCaseEffet != None:
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
class EffetTeleporteDebutCombat(Effet):
    def __init__(self, **kwargs):
        super(EffetTeleporteDebutCombat, self).__init__(**kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        niveau.gereDeplacementTF(joueurCaseEffet,joueurCaseEffet.posDebCombat,joueurLanceur,"Renvoi",AjouteHistorique=True)            
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
