# -*- coding: utf-8 -*

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
    def __init__(self, nom, debDans,duree, pourcentage,cibles, tailleZone,lanceur=None,desc=""):
        self.pourcentage = pourcentage
        self.tailleZone = tailleZone
        self.cibles = cibles
        super(EtatRedistribuerPer, self).__init__(nom, debDans,duree, lanceur,desc)

    def deepcopy(self):
        return EtatRedistribuerPer(self.nom, self.debuteDans,self.duree,  self.pourcentage, self.cibles, self.tailleZone, self.lanceur,self.desc)

    def triggerAvantSubirDegats(self,cibleAttaque,niveau,totalPerdu,typeDegats,attaquant):
        cibleAttaque.lanceSort(Sort("Redistribution",0,0,0,[EffetDegats(totalPerdu,totalPerdu,typeDegats,zone=zones.TypeZoneCercle(self.tailleZone),cibles_possibles=self.cibles,cibles_exclues="Lanceur")],99,99,0,0,"cercle"), niveau, cibleAttaque.posX, cibleAttaque.posY)

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
                cibleAttaque.lanceSort(Sort("Contre",0,0,0,[EffetDegats(totalPerdu,totalPerdu,typeDegats,zone=zones.TypeZoneCercle(self.tailleZone),cibles_possibles="Ennemis")],99,99,0,0,"cercle"), niveau, self.posX, self.posY)

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
            pass
            #self.lanceur.appliquerEtat(EtatBoostPuissance("Momification",0,2,100,self.lanceur),self.lanceur)
