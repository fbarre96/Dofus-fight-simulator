# -*- coding: utf-8 -*
import Zones
import random
import Personnages
import Niveau
import Etats

class Effet(object):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
                 Cette classe est 'abstraite' et doit être héritée."""
    def __init__(self,**kwargs):
        """@summary: Initialise un Effet.
        @kwargs: Options de l'effets, possibilitées: etat_requis (string séparé par |, aucun par défaut),
                                                     etat_requis_cibles (string séparé par |, aucun par défaut),
                                                     consomme_etat (booléen, Faux par défaut),
                                                     cibles_possibles (string, "Allies|Ennemis|Lanceur" par défaut)
                                                     cibles_exclues (string, aucune par défaut)
                                                     faire_au_vide (booléen, Faux par défaut). Indique si l'effet peut être lancé s'il n'a pas de cible direct (autrement dit si le sort est lancé sur une case vide).
                                                     zone (Zone, Zones.TypeZoneCercle(0) par défaut = sort mono cible)
        @type: **kwargs"""
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
        self.typeZone = kwargs.get('zone',Zones.TypeZoneCercle(0))
        self.kwargs = kwargs

    def deepcopy(self):
        return Effet(**self.kwargs)

    def estLancable(self, joueurLanceur, joueurCible):
        """@summary: Test si un effet peut etre lance selon les options de l'effets.
        @joueurLanceur: Le joueur lançant l'effet
        @type: Personnage
        @joueurCible: Le joueur dans la zone d'effet testé
        @type: Personnage
        @joueurCibleDirect: Le joueur sur lequel l'effet est lancé à la base (peut-être identique à joueurCible.
        @type: Personnage ou None
        @ciblesDejaTraitees: Les cibles déjà touchées par l'effet
        @type: tableau de Personnage
        @return: booléen indiquant vrai si la cible est valide, faux sinon"""
        return True,""

    def cibleValide(self, joueurLanceur, joueurCible,joueurCibleDirect, ciblesDejaTraitees):
        """@summary: Test si un joueur cible est un cible valide selon les options de l'effets.
        @joueurLanceur: Le joueur lançant l'effet
        @type: Personnage
        @joueurCible: Le joueur dans la zone d'effet testé
        @type: Personnage
        @joueurCibleDirect: Le joueur sur lequel l'effet est lancé à la base (peut-être identique à joueurCible.
        @type: Personnage ou None
        @ciblesDejaTraitees: Les cibles déjà touchées par l'effet
        @type: tableau de Personnage
        @return: booléen indiquant vrai si la cible est valide, faux sinon"""

        #Test si la cible est dans les cibles possibles
        if (joueurCible.team == joueurLanceur.team and joueurCible != joueurLanceur and "Allies" in self.ciblesPossibles) or (joueurCible.team == joueurLanceur.team and joueurCible == joueurLanceur and "Lanceur" in self.ciblesPossibles) or (joueurCible.team != joueurLanceur.team and "Ennemis" in self.ciblesPossibles) or (joueurCible.classe in self.ciblesPossibles) or (joueurCible.invocateur is not None and "Invoc" in self.ciblesPossibles):
            #Test si la cible est exclue
            if joueurCible.classe in self.ciblesExclues or (joueurCible.classe == joueurLanceur.classe and "Lanceur" in self.ciblesExclues) or (joueurCible.invocateur is not None and "Invoc" in self.ciblesExclues):
                print(" : Invalide : Cible Exclue")
                return False
            #Test si la cible est déjà traitée
            if joueurCible in ciblesDejaTraitees:
                print("DEBUG : Invalide : Cible deja traitee")
                return False
            #Test si un état est requis sur la cible direct et qu'une cible direct existe
            if (joueurCibleDirect == None and len(self.etatRequisCibleDirect)!=0):
                print("DEBUG : Invalide : Cible direct non renseigne et etatRequis pour cible direct ("+str(self.etatRequisCibleDirect)+")")
                return False
            #Test si une cible direct n'existe pas si l'effet doit être jouée
            if (joueurCibleDirect == None and not self.faireAuVide):
                print("DEBUG : Invalide : Cible direct non renseigne et pas faire au vide")
                return False
            #Test si la cible est une case vide et que l'effet ne nécessite pas d'êtat pour la cible
            if (joueurCible == None and len(self.etatRequisCibles)!=0):
                print("DEBUG : Invalide : Cible  non renseigne et etatRequis pour cible")
                return False
            #Test si la cible n'est pas une case vide qu'il a bien les états requis
            if joueurCible != None:
                if not joueurCible.aEtatsRequis(self.etatRequisCibles):
                    print("DEBUG : Invalide :etatRequis pour cible non present")
                    return False
            #Test si la cible firect n'est pas une case vide qu'il a bien les états requis
            if joueurCibleDirect != None:
                if not joueurCibleDirect.aEtatsRequis(self.etatRequisCibleDirect):
                    print("DEBUG : Invalide :etatRequis pour cible direct non present")
                    return False
            #La cible a passé tous les tests
            return True
        print("DEBUG : Invalide : Cible "+joueurCible.classe +" pas dans la liste des cibles possibles ("+str(self.ciblesPossibles)+")")
        return False

    def APorteZone(self, departZone_x,departZone_y, testDansZone_x,testDansZone_y, j_x, j_y):
        """@summary: Test si une case appartient à une zone donnée. Wrapper pour la fonction testCaseEstDedans polymorphique.
        @departZone_x: L'abcisse de la case de départ de la zone, souvent le centre et souvent le centre de l'effet
        @type: int
        @departZone_y: L'ordonnée de la case de départ de la zone, souvent le centre et souvent le centre de l'effet
        @type: int
        @testDansZone_x: L'abcisse de la case dont ou souhait savoir si elle est dans la zone'
        @type: int
        @testDansZone_y: L'ordonnée de la case dont ou souhait savoir si elle est dans la zone'
        @type: int
        @j_x: L'abcisse de la case sur laquelle le joueur lançant l'effet se trouve. Utile pour certaines zones dépendants de la position du lanceur.
        @type: int
        @j_y: L'ordonnée de la case sur laquelle le joueur lançant l'effet se trouve. Utile pour certaines zones dépendants de la position du lanceur.
        @type: int
        @return: booléen indiquant vrai si la case testée est dans la zone, faux sinon"""

        #Le lanceur peut pas etre dans la zone si y a le - a la fin du type zone
        return self.typeZone.testCaseEstDedans([departZone_x,departZone_y],[testDansZone_x,testDansZone_y],[j_x,j_y])

    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Applique les modifications sur le jeu créées par l'effet.
        @niveau: la grille de simulation de combat.
        @type: Niveau
        @joueurCaseEffet: Le joueur sur se tenant sur une case de la zone d'effet traitée.
        @type: Personnage
        @joueurLanceur: Le joueur ayant lancé l'effet
        @type: Personnage
        @kwargs: Les paramètres optionnels supplémentaires pour chaque effet.s
        @type: **kwargs"""

        #Comportement neutre non défini
        niveau.ajoutFileEffets(self)

    def activerEffet(self,niveau,joueurCaseEffet,joueurLanceur):
        print("Activation non définie")

    def afficher(self):
        """@summary: Affiche un effet dans la console (DEBUG)"""
        print("Effet etatRequis:"+self.etatRequisCibleDirect + " consommeEtat:"+str(self.consommeEtat)+" ciblesPossibles:"+str(self.ciblesPossibles)+" cibles_exclues:"+str(self.ciblesExclues))

class EffetDegats(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet inflige des dégâts à une cible."""
    def __init__(self,int_minJet,int_maxJet,str_typeDegats, **kwargs):
        """@summary: Initialise un effet de dégâts.
        @int_minJet: le jet minimum possible de dégâts de base de l'effet
        @type: int
        @int_maxJet: le jet maximum possible de dégâts de base de l'effet
        @type: int
        @str_typeDegats: l'élément dans lequel les dégâts seront infligés [terre,feu,air,chance,neutre]
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.minJet = int_minJet
        self.maxJet = int_maxJet
        self.typeDegats = str_typeDegats.lower()
        self.kwargs = kwargs
        super(EffetDegats, self).__init__(**kwargs)

    def deepcopy(self):
        return EffetDegats(self.minJet,self.maxJet,self.typeDegats,**self.kwargs)

    def calculDegats(self,niveau,joueurCaseEffet, joueurLanceur,nomSort, case_cible_x, case_cible_y):
        if joueurCaseEffet == None:
            return None
        
        baseDeg=random.randrange(self.minJet,self.maxJet+1)
        print("Will do damage "+str(baseDeg)+ " to "+str(joueurCaseEffet.classe))
        carac = 0
        dos = 0
        resFixes = 0
        rePer = 0
        if self.typeDegats == "eau":
            if self.kwargs.get("bypassDmgCalc",False) == False:
                carac+=joueurLanceur.cha
                dos += joueurLanceur.doEau
            resFixes += joueurCaseEffet.reEau
            rePer = joueurCaseEffet.rePerEau
        elif self.typeDegats == "air":
            if self.kwargs.get("bypassDmgCalc",False) == False:
                carac+=joueurLanceur.agi
                dos += joueurLanceur.doAir
            resFixes += joueurCaseEffet.reAir
            rePer = joueurCaseEffet.rePerAir
        elif self.typeDegats == "terre":
            if self.kwargs.get("bypassDmgCalc",False) == False:
                carac+=joueurLanceur.fo
                dos += joueurLanceur.doTerre
            resFixes += joueurCaseEffet.reTerre
            rePer = joueurCaseEffet.rePerTerre
        elif self.typeDegats == "feu":
            if self.kwargs.get("bypassDmgCalc",False) == False:
                carac+=joueurLanceur.int
                dos += joueurLanceur.doFeu
            resFixes += joueurCaseEffet.reFeu
            rePer = joueurCaseEffet.rePerFeu
        elif self.typeDegats == "neutre":
            if self.kwargs.get("bypassDmgCalc",False) == False:
                carac += joueurLanceur.fo
                dos += joueurLanceur.doNeutre
            resFixes += joueurCaseEffet.reNeutre
            rePer = joueurCaseEffet.rePerNeutre
        if self.kwargs.get("piege",False) == True:
            if self.kwargs.get("bypassDmgCalc",False) == False:
                carac += joueurLanceur.doPiegesPui
                dos += joueurLanceur.doPieges
        if self.kwargs.get("bypassDmgCalc",False) == False:
            if nomSort != "cac":
                dos += joueurLanceur.doSorts
            else:
                dos += joueurLanceur.doArmes
            dos += joueurLanceur.do
            carac += joueurLanceur.pui
        
        distance = Zones.getDistancePoint([joueurCaseEffet.posX, joueurCaseEffet.posY], [joueurLanceur.posX, joueurLanceur.posY])
        if distance == 1:
            if self.kwargs.get("bypassDmgCalc",False) == False:
                dos += joueurLanceur.doMelee
                resFixes += joueurCaseEffet.reMelee
        else:
            if self.kwargs.get("bypassDmgCalc",False) == False:
                dos += joueurLanceur.doDist
                resFixes += joueurCaseEffet.reDist

        #Etats du lanceur
        total = 0
        for etat in joueurLanceur.etats:
            if etat.actif():
                dos,baseDeg,carac = etat.triggerAvantCalculDegats(dos,baseDeg,carac,nomSort)
        total += baseDeg + (baseDeg * ((carac) / 100)) + dos
    
        #appliquer les effets des etats sur les degats total du joueur cible
        eloignement = Zones.getDistancePoint([joueurCaseEffet.posX, joueurCaseEffet.posY],[case_cible_x,case_cible_y])
        total = total * (10-eloignement)/10
        total = int(total)

        
        vaSubir = total - resFixes
        vaSubir = (vaSubir) - int((rePer/100)*vaSubir)
        for etat in joueurLanceur.etats:
            if etat.actif():
                vaSubir = etat.triggerApresCalculDegats(vaSubir,self.typeDegats)

        for etat in joueurCaseEffet.etats:
            if etat.actif():
                vaSubir = etat.triggerApresCalculDegats(vaSubir,self.typeDegats)
        if vaSubir < 0:
            vaSubir = 0
        
        return vaSubir

    def appliquerDegats(self,niveau,joueurCaseEffet, joueurLanceur):
        """@summary: calcul les dégâts à infligés et applique ces dégâts à la cible.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage

        @return: Le total de dégâts infligés"""
        
        joueurCaseEffet.subit(joueurLanceur,niveau,self.total,self.typeDegats)
        return self.total

    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet, wrapper pour la fonction appliquer dégâts.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        if joueurCaseEffet is not None:
            self.total = self.calculDegats(niveau,joueurCaseEffet, joueurLanceur,kwargs.get("nom_sort",""),kwargs.get("case_cible_x"),kwargs.get("case_cible_y"))
            niveau.ajoutFileEffets(self,joueurCaseEffet, joueurLanceur)

    def activerEffet(self,niveau,joueurCaseEffet,joueurLanceur):
        if joueurCaseEffet is not None:
            self.appliquerDegats(niveau,joueurCaseEffet, joueurLanceur)

class EffetVolDeVie(EffetDegats):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Hérite de EffetsDegats.
    Cet effet inflige des dégâts à une cible et soigne le lanceur de la moitié des dégâts infligés."""
    def __init__(self,int_minJet,int_maxJet,str_typeDegats, **kwargs):
        """@summary: Initialise un effet de vol de vie.
        @int_minJet: le jet minimum possible de dégâts de base de l'effet
        @type: int
        @int_maxJet: le jet maximum possible de dégâts de base de l'effet
        @type: int
        @str_typeDegats: l'élément dans lequel les dégâts seront infligés [terre,feu,air,chance,neutre]
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetVolDeVie, self).__init__(int_minJet,int_maxJet,str_typeDegats,**kwargs)
    def deepcopy(self):
        return EffetVolDeVie(self.minJet,self.maxJet,self.typeDegats,**self.kwargs)

    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""

        #Utilisation du parent EffetDegats
        if joueurCaseEffet is not None:
            self.total = super(EffetVolDeVie, self).calculDegats(niveau,joueurCaseEffet, joueurLanceur,kwargs.get("nom_sort",""),kwargs.get("case_cible_x"),kwargs.get("case_cible_y"))
            niveau.ajoutFileEffets(self,joueurCaseEffet, joueurLanceur)
        

    def activerEffet(self,niveau,joueurCaseEffet,joueurLanceur):
        #Et enfin le vol de  vie
        
        if joueurCaseEffet is not None:
            #Le soin est majoré à la vie de début du combat
            if joueurLanceur.vie > joueurLanceur._vie:
                joueurLanceur.vie = joueurLanceur._vie
            self.appliquerDegats(niveau,joueurCaseEffet, joueurLanceur)
            #Soin
            
            joueurLanceur.vie += (self.total/2)
            joueurLanceur.vie = int(joueurLanceur.vie)
            print(joueurLanceur.classe+" vol "+ str(int(self.total/2)) + "PV")

class EffetDegatsPosLanceur(EffetDegats):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Hérite de EffetsDegats.
    Cet effet inflige des dégâts en ciblant la position actuelle du lanceur."""
    def __init__(self,int_minJet,int_maxJet,str_typeDegats, **kwargs):
        """@summary: Initialise un effet de vol de vie.
        @int_minJet: le jet minimum possible de dégâts de base de l'effet
        @type: int
        @int_maxJet: le jet maximum possible de dégâts de base de l'effet
        @type: int
        @str_typeDegats: l'élément dans lequel les dégâts seront infligés [terre,feu,air,chance,neutre]
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetDegatsPosLanceur, self).__init__(int_minJet,int_maxJet,str_typeDegats,**kwargs)
    
    def deepcopy(self):
        return EffetDegatsPosLanceur(self.minJet,self.maxJet,self.typeDegats,**self.kwargs)

    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, prov_x et prov_y et nom_sort doivent être mentionées
        @type: **kwargs"""
        joueurLanceur = niveau.getJoueurSur(kwargs.get("prov_x"),kwargs.get("prov_y"))
        total = super(EffetDegatsPosLanceur, self).appliquerDegats(niveau,joueurCaseEffet, joueurLanceur,str(kwargs.get("nom_sort")))

class EffetTue(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet tue immédiatement les cibles."""
    def __init__(self, **kwargs):
        """@summary: Initialise un effet tueur.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetTue , self).__init__(**kwargs)

    def deepcopy(self):
        return EffetTue(**self.kwargs)

    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        niveau.tue(joueurCaseEffet)

class EffetRetPA(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire des PA esquivables normalement (pas implémenté l'esquive).
    https://www.dofus.com/fr/forum/1003-divers/2281673-formule-calcul-retrait-ou-esquives-pa-pm"""
    def __init__(self,int_retrait, **kwargs):
        """@summary: Initialise un effet de retrait de PA.
        @int_retrait: le nombre de PA qui vont être retiré au maximum
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.retrait = int_retrait
        super(EffetRetPA, self).__init__(**kwargs)

    def deepcopy(self):
        return EffetRetPA(self.retrait,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        totalRet = 0
        for i in range(self.retrait):
            esqPa = joueurCaseEffet.esqPA if joueurCaseEffet.esqPA != 0 else 1
            basePa = joueurCaseEffet._PA if joueurCaseEffet._PA != 0 else 1
            probaRet = 0.5 * (float(joueurLanceur.retPA)/float(esqPa)) * (float(joueurCaseEffet.PA)/float(basePa))
            rand = random.random()
            if rand <= probaRet:
                totalRet += 1
        joueurCaseEffet.PA -= totalRet
        print(joueurCaseEffet.classe+" -"+ str(totalRet) + "PA")
        
class EffetRetPM(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire des PM esquivables normalement (pas implémenté l'esquive)."""
    def __init__(self,int_retrait, **kwargs):
        """@summary: Initialise un effet de retrait de PM.
        @int_retrait: le nombre de PM qui vont être retiré au maximum
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.retrait = int_retrait
        super(EffetRetPM, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetRetPM(self.retrait,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        print(joueurCaseEffet.classe+" -"+ str(self.retrait) + "PM")

class EffetPropage(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet propage un sort à la cible la plus proche dans la portée du sort (Flèche fulminante par exemple)."""
    def __init__(self,sort_sort,zone_zone, **kwargs):
        """@summary: Initialise un effet de propagation de sort.
        @sort_sort: le sort qui va être propagé
        @type: Sort
        @zone_zone: la zone de propagation possible à partir de la dernière cible
        @type: Zone
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.zone = zone_zone
        self.sort = sort_sort
        super(EffetPropage, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetPropage(self.sort,self.zone,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""

        #Etat temporaire pour marqué la cible comme déjà touché par la propagation
        joueurCaseEffet.appliquerEtat(Etats.Etat("temporaire",0,1),joueurLanceur)
        #Récupérations des joueurs respectant les critères du sort les plus proches, etat requis = pas temporaire
        joueursAppliquables = niveau.getJoueurslesPlusProches(joueurCaseEffet.posX,joueurCaseEffet.posY,joueurLanceur,self.zone,["!temporaire"],self.ciblesPossibles)
        if len(joueursAppliquables)>0:
            self.sort.lance(joueurCaseEffet.posX,joueurCaseEffet.posY,niveau, joueursAppliquables[0].posX, joueursAppliquables[0].posY,joueurLanceur)

class EffetEtat(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet applique un état à la cible."""
    def __init__(self, etat_etat, **kwargs):
        """@summary: Initialise un effet appliquant un état.
        @etat_etat: l'état qui va être appliqué
        @type: Etat
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.etat = etat_etat
        super(EffetEtat, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetEtat(self.etat,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        if joueurCaseEffet != None:
            # On copie l'état parce que l'effet peut être appliquer plusieurs fois.
            etatCopier = self.etat.deepcopy()
            joueurCaseEffet.appliquerEtat(etatCopier,joueurLanceur, niveau)

class EffetGlyphe(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pose une glyphe sur la grille de jeu."""
    def __init__(self,sort_sort,int_duree,str_nom, tuple_couleur, **kwargs):
        """@summary: Initialise un effet posant une glyphe.
        @sort_sort: le sort monocible qui est lancé sur les joueurs restants dans la glyphe
        @type: Sort
        @int_duree: le nombre de tour où la glyphe sera active
        @type: int
        @str_nom: le nom de la glyphe
        @type: string
        @tuple_couleur: la couleur de la glyphe
        @type: tuple de couleur format RGB
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.sort = sort_sort
        self.duree = int_duree
        self.nom = str_nom
        self.couleur = tuple_couleur
        super(EffetGlyphe, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetGlyphe(self.sort,self.duree,self.nom,self.couleur,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, case_cible_x et case_cible_y doivent être mentionés
        @type: **kwargs"""
        nouvelleGlyphe = Niveau.Glyphe(self.nom, self.sort, self.duree, kwargs.get("case_cible_x"), kwargs.get("case_cible_y"), joueurLanceur,self.couleur)
        glypheID = niveau.poseGlyphe(nouvelleGlyphe)
        
class EffetPiege(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pose un piège sur la grille de jeu."""
    def __init__(self,zone_declenchement,list_effets,str_nom, tuple_couleur, **kwargs):
        """@summary: Initialise un effet posant un piège.
        @zone_declenchement: la zone où si un joueur marche le piège se déclenche.
        @type: Zones.TypeZone
        @sort_sort: le sort lancé sur la case centrale du piège
        @type: Sort
        @str_nom: le nom du piège
        @type: string
        @tuple_couleur: la couleur du piège
        @type: tuple de couleur format RGB
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.zone_declenchement = zone_declenchement
        self.effets = list_effets
        self.nom = str_nom
        self.couleur = tuple_couleur
        super(EffetPiege, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetPiege(self.zone_declenchement,self.effets,self.nom,self.couleur,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, case_cible_x et case_cible_y doivent être mentionés
        @type: **kwargs"""
        nouveauPiege = Niveau.Piege(self.nom, self.zone_declenchement,self.effets, kwargs.get("case_cible_x"), kwargs.get("case_cible_y"), joueurLanceur,self.couleur)
        piegeID = niveau.posePiege(nouveauPiege)

class EffetRune(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pose une rune sur la grille de jeu."""
    def __init__(self,duree,list_effets,str_nom, tuple_couleur, **kwargs):
        """@summary: Initialise un effet posant une rune.
        @duree: Le nombrede tour où la rune sera présente (avant déclenchement)
        @type: int
        @sort_sort: le sort lancé sur la case centrale du piège
        @type: Sort
        @str_nom: le nom de la rune
        @type: string
        @tuple_couleur: la couleur du piège
        @type: tuple de couleur format RGB
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.duree = duree
        self.effets = list_effets
        self.nom = str_nom
        self.couleur = tuple_couleur
        super(EffetRune, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetRune(self.duree,self.effets,self.nom,self.couleur,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, case_cible_x et case_cible_y doivent être mentionés
        @type: **kwargs"""
        nouvelleRune= Niveau.Rune(self.nom, self.duree,self.effets, kwargs.get("case_cible_x"), kwargs.get("case_cible_y"), joueurLanceur,self.couleur)
        runeID = niveau.poseRune(nouvelleRune)
   
class EffetPousser(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pousse un joueur à l'opposé une position donnée."""
    def __init__(self,int_nbCase, source="Lanceur", cible="JoueurCaseEffet", **kwargs):
        """@summary: Initialise un effet poussant un joueur à l'opposé d'une position donnée
        @int_nbCase: le nombre de case dont le joueur cible va être poussé.
        @type: int
        @source: une string indiquant la provenance de la poussée (Lanceur|)
        @type: str
        @cible: une string indiquant la direction de la poussée (Lanceur|)
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nbCase = int_nbCase
        self.source = source
        self.cible = cible
        super(EffetPousser, self).__init__(**kwargs)

    def deepcopy(self):
        return EffetPousser(self.nbCase, self.source, self.cible, **self.kwargs)
    def determinerSensPousser(self,niveau,cible,sourceX,sourceY):
        """@summary: Retourne des données permettant de calculer le sens dans lequel un joueur sera poussé.
        @joueurCible: le joueur qui va être poussé
        @type: Personnage
        @sourceX: la coordonnée x depuis laquelle le joueur se fait poussé. Si None est donné, c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        @type: int
        @sourceY: la coordonnée y depuis laquelle le joueur se fait poussé. Si None est donné, c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        @type: int

        @return: Retoure un point dans les coordonnées d'un repère normé de centre (0,0). Par exemple, (1,0) est horizontal vers la droite. (0,1) vertical haut. (1,-1) anti-diagonal vers le bas. 
        """ 

        #Calcul de la direction de la poussée
        cible_posX = cible[0]
        cible_posY = cible[1]
        dist_lignes = abs(cible_posY - sourceY)
        dist_colognes = abs(cible_posX - sourceX)
        self.coordonnees = [0,0]
        self.coordonnees[0] = 1 if (dist_colognes >= dist_lignes) else 0
        self.coordonnees[1] = 1 if (dist_colognes <= dist_lignes) else 0
        if self.coordonnees[0] == 1 and cible_posX < sourceX:
            self.coordonnees[0] = -1
        if self.coordonnees[1] == 1 and cible_posY < sourceY:
            self.coordonnees[1] = -1
        return self.coordonnees[1]

    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, case_cible_x et case_cible_y doivent être mentionés
        @type: **kwargs"""
        if self.source == "CaseCible":
            self.case_from_x = kwargs.get("case_cible_x")
            self.case_from_y = kwargs.get("case_cible_y")
        elif self.source == "Lanceur":
            self.case_from_x = joueurLanceur.posX
            self.case_from_y = joueurLanceur.posY
        if self.cible == "JoueurCaseEffet":
            if joueurCaseEffet is None:
                return
            self.joueurAPousser = niveau.getJoueurSur(joueurCaseEffet.posX, joueurCaseEffet.posY)
        self.determinerSensPousser(niveau,[self.joueurAPousser.posX, self.joueurAPousser.posY],self.case_from_x,self.case_from_y)
        niveau.ajoutFileEffets(self,joueurCaseEffet, joueurLanceur)

    def activerEffet(self,niveau,joueurCaseEffet,joueurLanceur):
        niveau.pousser(self, self.joueurAPousser,joueurLanceur,True, self.case_from_x, self.case_from_y)
        
class EffetAttire(EffetPousser):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet attire un joueur vers la position du lanceur."""
    def __init__(self,int_nbCase, source="Lanceur", cible="JoueurCaseEffet", **kwargs):
        """@summary: Initialise un effet repoussant un joueur à l'opposé de la position du lanceur
        @int_nbCase: le nombre de case dont le joueur cible va être attiré.
        @type: int
        @depuis: string qui définit la provenance de l'attirance
        @type: str
        @vers: string qui définit la direction de l'attirance
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.source = source
        self.cible = cible
        self.kwargs = kwargs
        super(EffetAttire, self).__init__(int_nbCase,source,cible,**kwargs)
    def deepcopy(self):
        return EffetAttire(self.nbCase,self.source, self.cible, **self.kwargs)
    def activerEffet(self,niveau,joueurCaseEffet,joueurLanceur):
        niveau.attire(self,self.joueurAAttirer,joueurLanceur,self.case_from_x, self.case_from_y)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, case_cible_x et case_cible_y doivent être mentionés
        @type: **kwargs"""
        if self.source == "CaseCible":
            self.case_from_x = kwargs.get("case_cible_x")
            self.case_from_y = kwargs.get("case_cible_y")
        elif self.source == "Lanceur":
            self.case_from_x = joueurLanceur.posX
            self.case_from_y = joueurLanceur.posY
        elif self.source == "JoueurCaseEffet":
            if joueurCaseEffet is None:
                return
            self.case_from_x = joueurCaseEffet.posX
            self.case_from_y = joueurCaseEffet.posY
        if self.cible == "Lanceur":
            self.joueurAAttirer = joueurLanceur
        elif self.cible == "JoueurCaseEffet":
            if joueurCaseEffet is None:
                return
            self.joueurAAttirer = joueurCaseEffet
        if self.joueurAAttirer != None:
            if self.joueurAAttirer.posX != self.case_from_x or self.joueurAAttirer.posY != self.case_from_y:
                super(EffetAttire, self).determinerSensPousser(niveau,[self.joueurAAttirer.posX, self.joueurAAttirer.posY],self.case_from_x,self.case_from_y)
                self.coordonnees[0] *= -1 # changement de sens par rapport au sens de pousser
                self.coordonnees[1] *= -1
                caseMax = self.determinerAttiranceMax() # Pour les attirances en diagonale il faut que je le joueur attirer s'arrête devant l'attireur
                self.nbCase = caseMax if self.nbCase > caseMax else self.nbCase
                niveau.ajoutFileEffets(self,joueurCaseEffet, joueurLanceur)
        
    def determinerAttiranceMax(self):
        if self.coordonnees[0] != 0:
            return abs(self.joueurAAttirer.posX - self.case_from_x)
        else:
            return abs(self.joueurAAttirer.posY - self.case_from_y)

class EffetDureeEtats(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet change la durée des états de la cible."""
    def __init__(self,int_deXTours, **kwargs):
        """@summary: Initialise un effet changeant la durée des états de la cible
        @int_deXTours: le nombre de tour qui vont être additionés (dans Z) à chaque état de la cible.
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.deXTours = int_deXTours
        super(EffetDureeEtats, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetDureeEtats(self.deXTours,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        joueurCaseEffet.changeDureeEffets(self.deXTours, niveau)

class EffetRetireEtat(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire les états de la cible qui portent un nom donné."""
    def __init__(self,str_nomEtat, **kwargs):
        """@summary: Initialise un effet retirant les états de la cible selon un paramètre donné.
        @str_nomEtat: le nom de l'état qui va être retiré de la cible.
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nomEtat = str_nomEtat
        super(EffetRetireEtat, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetRetireEtat(self.nomEtat ,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        if joueurCaseEffet != None:
            joueurCaseEffet.retirerEtats(self.nomEtat)

class EffetDevoilePiege(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet dévoile les pièges invisibles."""
    def __init__(self, **kwargs):
        """@summary: Initialise un effet retirant l'invisiblité des pièges.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetDevoilePiege, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetDevoilePiege(**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        case_effet_x=kwargs.get("case_effet_x")
        case_effet_y=kwargs.get("case_effet_y")
        for piege in niveau.pieges:
            if piege.aPorteDeclenchement(case_effet_x, case_effet_y):
                piege.invisible = False

class EffetTeleportePosPrec(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte un ennemi vers sa position précedente. L'historique des 2 derniers tours seulement est gardé."""
    def __init__(self,int_nbCase, **kwargs):
        """@summary: Initialise un effet téléportant sa cible vers sa position précédente. L'historique des 2 derniers tours seulement est gardé.
        @int_nbCase: le nombre de retour en arrière effectué. Par forcément égale au nombre de case reculés.
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nbCase = int_nbCase
        super(EffetTeleportePosPrec, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetTeleportePosPrec(self.nbCase ,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, l'option nom_sort doit être mentionée
        @type: **kwargs"""
        joueurCaseEffet.tpPosPrec(self.nbCase,niveau,joueurLanceur, kwargs.get("nom_sort"))

class EffetTeleportePosPrecLanceur(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte le lanceur vers sa position précedente. L'historique des 2 derniers tours seulement est gardé."""
    def __init__(self,int_nbCase,**kwargs):
        """@summary: Initialise un effet téléportant le lanceur vers sa position précédente. L'historique des 2 derniers tours seulement est gardé.
        @int_nbCase: le nombre de retour en arrière effectué. Par forcément égale au nombre de case reculés.
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nbCase = int_nbCase
        super(EffetTeleportePosPrecLanceur, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetTeleportePosPrecLanceur(self.nbCase ,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, l'option nom_sort, prov_x et prov_y doivent être mentionées
        @type: **kwargs"""
        joueurLanceur = niveau.getJoueurSur(kwargs.get("prov_x"),kwargs.get("prov_y"))
        joueurCaseEffet.tpPosPrec(self.nbCase,niveau,joueurLanceur, kwargs.get("nom_sort"))
                      
class EffetTeleporteDebutTour(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte la cible vers sa position de début de tour."""
    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant la cible vers sa position de début de tour.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetTeleporteDebutTour, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetTeleporteDebutTour(**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        niveau.gereDeplacementTF(joueurCaseEffet,joueurCaseEffet.posDebTour,joueurLanceur,"Renvoi",AjouteHistorique=True)

class EffetTeleporteDebutCombat(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte la cible vers sa position de début de combat."""
    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant la cible vers sa position de début de combat.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetTeleporteDebutCombat, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetTeleporteDebutCombat(**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        niveau.gereDeplacementTF(joueurCaseEffet,joueurCaseEffet.posDebCombat,joueurLanceur,"Renvoi",AjouteHistorique=True)

class EffetTpSym(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte le lanceur symétriquement par rapport au point de symétrie qui est le joueur cible."""
    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant le lanceur symétriquement par rapport au point de symétrie qui est le joueur cible.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetTpSym, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetTpSym(**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, l'option nom_sort, doit être mentionée
        @type: **kwargs"""
        distanceX = (joueurCaseEffet.posX-joueurLanceur.posX)
        distanceY = (joueurCaseEffet.posY-joueurLanceur.posY)
        arriveeX = joueurCaseEffet.posX+distanceX
        arriveeY = joueurCaseEffet.posY+distanceY
        niveau.gereDeplacementTF(joueurLanceur,[arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"),AjouteHistorique=True)
        
class EffetTpSymSelf(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte la cible symétriquement par rapport au point de symétrie qu'est le lanceur."""
    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant la cible symétriquement par rapport au point de symétrie qu'est le lanceur.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetTpSymSelf, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetTpSymSelf(**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, l'option nom_sort, doit être mentionée
        @type: **kwargs"""
        distanceX = (joueurCaseEffet.posX-joueurLanceur.posX)
        distanceY = (joueurCaseEffet.posY-joueurLanceur.posY)
        arriveeX = joueurLanceur.posX-distanceX
        arriveeY = joueurLanceur.posY-distanceY
        niveau.gereDeplacementTF(joueurCaseEffet,[arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"), AjouteHistorique=True)
        
class EffetTpSymCentre(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte la cible symétriquement par rapport au point de symétrie donné par case_cible_x et case_cible_y."""
    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant la cible symétriquement par rapport au point de symétrie donné par case_cible_x et case_cible_y.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetTpSymCentre, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetTpSymCentre(**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, l'option nom_sort, case_cible_x et case_cible_y doivent être mentionées
        @type: **kwargs"""
        distanceX = (joueurCaseEffet.posX-kwargs.get("case_cible_x"))
        distanceY = (joueurCaseEffet.posY-kwargs.get("case_cible_y"))
        arriveeX = kwargs.get("case_cible_x")-distanceX
        arriveeY = kwargs.get("case_cible_y")-distanceY
        joueurTF = niveau.gereDeplacementTF(joueurCaseEffet,[arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"), AjouteHistorique=True)
        #Evite de retéléporter les cibles s'étant déplacé après un téléfrags
        if joueurTF != None:
            kwargs.get("cibles_traitees").append(joueurTF)
        
class EffetEtatSelf(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet place un état sur le lanceur."""
    def __init__(self,etat_etat, **kwargs):
        """@summary: Initialise un effet placant un état sur le lanceur
        @etat_etat: l'état à placer sur le lanceur
        @type: Etat
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.etat = etat_etat
        self.kwargs = kwargs
        super(EffetEtatSelf, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetEtatSelf(self.etat,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        etatCopier = self.etat.deepcopy()
        joueurLanceur.appliquerEtat(etatCopier,joueurLanceur)
        
class EffetEntiteLanceSort(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet fait lancer un sort à une entité/joueur"""
    def __init__(self,str_nomEntites,sort_sort, **kwargs):
        """@summary: Initialise un effet lançant un sort à une entité/joueur
        @str_nomEntites: les entités devant lancer le sort
        @type: string
        @sort_sort: le sort qui sera lancé par les entités
        @type: Sort
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nomEntites = str_nomEntites
        self.sort = sort_sort
        super(EffetEntiteLanceSort, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetEtatSelf(self.etat,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        joueursLanceurs = niveau.getJoueurs(self.nomEntites)
        for joueur in joueursLanceurs:
            self.sort.lance(joueur.posX,joueur.posY,niveau, joueur.posX, joueur.posY)


        
class EffetEchangePlace(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet échange deux joueurs et peut provoquer un téléfrag"""
    def __init__(self, **kwargs):
        """@summary: Initialise un effet échangeant deux joueurs et puvant provoquer un téléfrag
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetEchangePlace, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetEchangePlace(**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, les options cible_traitees et nom_sort doivent être mentionnées. L'option generer_TF peut être mentionnée.
        @type: **kwargs"""
        genereTF = kwargs.get("generer_TF",False)
        joueurTF = niveau.gereDeplacementTF(joueurLanceur,[joueurCaseEffet.posX, joueurCaseEffet.posY], joueurLanceur, kwargs.get("nom_sort"), True,genereTF)
        if joueurTF != None:
            kwargs.get("cibles_traitees").append(joueurTF)
        
class EffetTp(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte le lanceur sur la case ciblée."""
    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant le lanceur sur la case ciblée.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetTp, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetTp(**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, les options case_cible_x et case_cible_y doivent être mentionnées.
        @type: **kwargs"""
        generer_TF = self.kwargs.get("generer_TF",False)
        if generer_TF:
            joueurTF = niveau.gereDeplacementTF(joueurLanceur,[kwargs.get("case_cible_x"), kwargs.get("case_cible_y")], joueurLanceur, kwargs.get("nom_sort"), True,generer_TF)
            if joueurTF != None:
                kwargs.get("cibles_traitees").append(joueurTF)
        else:
            joueurLanceur.bouge(niveau,kwargs.get("case_cible_x"),kwargs.get("case_cible_y"))
        

class EffetInvoque(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet invoque un personnage"""
    def __init__(self, str_nomInvoque, compteCommeInvocation, **kwargs):
        """@summary: Initialise un effet invoquant un personnage.
        @str_nomInvoque: le nom de l'invocation (pré-définies dans le dictionnaire Personnages.INVOCS)
        @type: string
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.compteCommeInvocation = compteCommeInvocation
        self.nomInvoque = str_nomInvoque
        super(EffetInvoque, self).__init__(**kwargs)
    def deepcopy(self):
        return EffetInvoque(self.nomInvoque, self.compteCommeInvocation,**self.kwargs)
    def appliquerEffet(self, niveau,joueurCaseEffet,joueurLanceur,**kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, les options case_cible_x et case_cible_y doivent être mentionnées.
        @type: **kwargs"""
        
        invoc = Personnages.INVOCS[self.nomInvoque].deepcopy()
        invoc.invocateur = joueurLanceur
        invoc.team = joueurLanceur.team
        invoc.lvl = joueurLanceur.lvl
        if self.estLancable(invoc.invocateur, None):
            joueurLanceur.invocations.append(invoc)
            niveau.invoque(invoc,kwargs.get("case_cible_x"),kwargs.get("case_cible_y"))

    def estLancable(self, joueurLanceur, joueurCible):
        """@summary: Test si un effet peut etre lance selon les options de l'effets.
        @joueurLanceur: Le joueur lançant l'effet
        @type: Personnage
        @joueurCible: Le joueur dans la zone d'effet testé
        @type: Personnage
        @joueurCibleDirect: Le joueur sur lequel l'effet est lancé à la base (peut-être identique à joueurCible.
        @type: Personnage ou None
        @ciblesDejaTraitees: Les cibles déjà touchées par l'effet
        @type: tableau de Personnage
        @return: booléen indiquant vrai si la cible est valide, faux sinon"""
        if self.compteCommeInvocation:
            if len(joueurLanceur.invocations) + 1 > joueurLanceur.invocationLimite:
                return False, "Limite d'invocation atteinte"
        return True,""