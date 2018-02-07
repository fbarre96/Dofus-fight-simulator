# -*- coding: utf-8 -*
import Personnages
import Zones
import constantes
import pygame
import Overlays
import Effets
import Etats
import Sort
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

class Case:
    def __init__(self, typ, hitbox):
        self.type = typ
        self.hitbox = hitbox
        self.effetsSur = []

class Niveau:
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
        synchro.lanceSort(Sort.Sort("Fin_des_temps",0,0,0,[Effets.EffetDegats(int(reelLanceur.lvl*1.90)*(nbTF*2-1),int(reelLanceur.lvl*1.90)*(nbTF*2-1),"air",zone=Zones.TypeZoneCercle(3),cibles_possibles="Ennemis")], 99,99,0,0,"cercle"),self,synchro.posX,synchro.posY)
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

    def getJoueurslesPlusProches(self, case_x,case_y,lanceur,zone=Zones.TypeZoneCercle(99),etatRequisCibles=[],ciblesPossibles=[],ciblesExclues=[],ciblesTraitees=[]):
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
