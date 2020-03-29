"""@summary: Une IA d'invoc
"""
from pygame.locals import K_F1, K_1, K_9, K_ESCAPE
import pygame
import constantes

class JoueurIA:
    """
    @summary: Permet à un joueur de choisir ses sorts
    """
    def __init__(self):
        self.interactif = True

    def joue(self, event, joueur, niveau, mouseXY, sortSelectionne):
        """@summary: Fonction appelé par la boucle principale pour demandé
                     à un Personnage d'effectuer ses actions.
                     Dans la classe Personnage, c'est contrôle par utilisateur clavier/souris.
        @event: les évenements pygames survenus
        @type: Event pygame
        @niveau: La grille de jeu
        @type: Niveau
        @mouseXY: Les coordonnées de la souris
        @type: int
        @sortSelectionne: Le sort sélectionné plus tôt dans la partie s'il y en a un
        @type: Sort

        @return: Le nouveau sortSelectionne éventuel"""

        # Clic souris
        if event.type == pygame.KEYDOWN:
            if event.key == K_F1:  # touche F1 = fin du tour
                sortSelectionne = None
                niveau.finTour()
            if event.key == K_ESCAPE:  # touche échap = déselection de sort.
                sortSelectionne = None
            if event.key >= K_1 and event.key <= K_9:
                aLance = niveau.tourDe.sorts[event.key - K_1]
                sortSelectionne = joueur.selectionSort(aLance, niveau)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicGauche, _, clicDroit = pygame.mouse.get_pressed()
            # Clic gauche
            if clicGauche:
                # Clic gauche sort = tentative de sélection de sort
                if mouseXY[1] > constantes.y_sorts:
                    for sort in niveau.tourDe.sorts:
                        if sort.vue.isMouseOver(mouseXY):
                            sortSelectionne = joueur.selectionSort(sort, niveau)
                            niveau.setPrevisu(True)
                            break
                # Clic gauche grille de jeu = tentative de lancé un sort
                #  si un sort est selectionné ou tentative de déplacement sinon
                else:
                    # Un sort est selectionne
                    if sortSelectionne is not None:
                        caseCibleX = int(
                            mouseXY[0]/constantes.taille_sprite)
                        caseCibleY = int(
                            mouseXY[1]/constantes.taille_sprite)
                        niveau.setPrevisu(False)
                        sortSelectionne.lance(
                            niveau.tourDe.posX, niveau.tourDe.posY, niveau, caseCibleX, caseCibleY)
                        sortSelectionne = None
                    # Aucun sort n'est selectionne: on pm
                    else:
                        niveau.deplacement(mouseXY)
            # Clic droit
            elif clicDroit:
                # Clic droit grille de jeu = affichage détaillé de l'état d'un personnage.
                if mouseXY[1] < constantes.y_sorts:
                    caseX = int(mouseXY[0]/constantes.taille_sprite)
                    caseY = int(mouseXY[1]/constantes.taille_sprite)
                    joueurInfo = niveau.getJoueurSur(caseX, caseY)
                    if joueurInfo is not None:
                        print("--------------------------------")
                        for etat in joueurInfo.etats:
                            if etat.actif():
                                print(joueurInfo.nomPerso+" est dans l'etat " +
                                      etat.nom+" ("+str(etat.duree)+")")
                            elif etat.debuteDans > 0:
                                print(joueurInfo.nomPerso+" sera dans l'etat " +
                                      etat.nom+" dans "+str(etat.debuteDans)+" tour(s)")
                        print("--------------------------------")
                        if joueurInfo.porteUid is not None or joueurInfo.porteurUid is not None:
                            joueurInfoBisUid = joueurInfo.porteUid if joueurInfo.porteUid \
                                                                        is not None \
                                                                   else joueurInfo.porteurUid
                            joueurInfo = niveau.getJoueurAvecUid(joueurInfoBisUid)
                            print("--------------------------------")
                            for etat in joueurInfo.etats:
                                if etat.actif():
                                    print(joueurInfo.nomPerso+" est dans l'etat " +
                                          etat.nom+" ("+str(etat.duree)+")")
                                elif etat.debuteDans > 0:
                                    print(joueurInfo.nomPerso+" sera dans l'etat " +
                                          etat.nom+" dans "+str(etat.debuteDans)+" tour(s)")
                            print("--------------------------------")
                    if sortSelectionne is not None:
                        niveau.setPrevisu(False)
                        sortSelectionne = None
        return sortSelectionne
