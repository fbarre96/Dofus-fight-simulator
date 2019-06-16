import Sort as Sort
from Effets.EffetDegats import EffetDegats, EffetVolDeVie
from Effets.EffetEtat import EffetEtat, EffetEtatSelf, EffetEtatSelfTF
from Effets.EffetEtat import EffetRetireEtat, EffetRafraichirEtats
from Effets.EffetEntiteLanceSort import EffetEntiteLanceSort
from Effets.EffetGlyphe import EffetActiveGlyphe, EffetGlyphe
from Effets.EffetTp import EffetTeleportePosPrec, EffetTeleporteDebutCombat, EffetTeleporteDebutTour
from Effets.EffetTp import EffetTpSym, EffetTpSymSelf, EffetTpSymCentre, EffetEchangePlace, EffetTp
from Effets.EffetRet import EffetRetPA
from Effets.EffetTue import EffetTue
from Effets.EffetInvoque import EffetInvoque
from Effets.EffetPiege import EffetPiege
from Effets.EffetRune import EffetRune

from Etats.Etat import Etat
from Etats.EtatEffet import EtatEffetSiTFGenere, EtatEffetSiSubit, EtatEffetDebutTour, EtatEffetFinTour
from Etats.EtatBoostCarac import EtatBoostCaracFixe
from Etats.EtatBoostSortCarac import EtatBoostSortCarac
from Etats.EtatBoostBaseDeg import EtatBoostBaseDeg
from Etats.EtatActiveSort import EtatActiveSort
from Etats.EtatRetourCaseDepart import EtatRetourCaseDepart
from Etats.EtatModDeg import EtatModDegPer
from Etats.EtatContre import EtatContre
from Etats.EtatTelefrag import EtatTelefrag

import Zones as Zones
import Personnages as Personnages


def getSortsDebutCombat(lvl):
    sortsDebutCombat = []
    sortsDebutCombat.append(
        Sort.Sort("Téléfrageur", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetSiTFGenere("Téléfrageur", 0, -1, EffetEtatSelfTF(EtatBoostCaracFixe("toReplace", 0, -1,
                                                                                                                                                     "PA", 2), "Rembobinage", cumulMax=1), "Téléfrageur", "reelLanceur", "reelLanceur"))], [], 0, 99, 99, 0, 0, "cercle", False, description="""""", chaine=False),
    )
    sortsDebutCombat.append(
        Sort.Sort("Glas Boost", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetSiTFGenere("Glas Boost", 0, -1, EffetEtatSelf(EtatBoostBaseDeg(
            "Glas", 0, -1, "Glas", 4), cumulMax=10), "Glas", "porteur", "porteur"))], [], 0, 99, 99, 0, 0, "cercle", False, description="""""", chaine=False),
    )
    sortsDebutCombat.append(
        Sort.Sort("Instabilité Temporelle Réactivation", 0, 0, 0, 0, [EffetEtatSelf(EtatEffetSiTFGenere("Instabilité Temporelle Réactivation", 0, -1, EffetActiveGlyphe(
            "Instabilité Temporelle"), "Instabilité Temporelle", "reelLanceur", "reelLanceur", False, "Activation Instabilité Temporelle"))], [], 0, 99, 99, 0, 0, "cercle", False, description="""""", chaine=False),
    )
    return sortsDebutCombat


def getSorts(lvl):
    sorts = []
    retourParadoxe = Sort.Sort("Retour Paradoxe", 0, 0, 0, 0, [EffetTpSymCentre(zone=Zones.TypeZoneInfini(
    ), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", etat_requis_cibles="ParadoxeTemporel", consomme_etat=True)], [], 0, 99, 99, 0, 0, "cercle", False)
    activationInstabiliteTemporelle = Sort.Sort("Activation Instabilité Temporelle", 0, 0, 0, 3, [
                                                EffetTeleportePosPrec(1)], [], 0, 99, 99, 0, 0, "cercle", False)
    sortieInstabiliteTemporelle = Sort.Sort("Instabilité Temporelle: Sortie", 0, 0, 0, 99, [
                                            EffetRetireEtat("Intaclable")], [], 0, 99, 99, 0, 0, "cercle", False)
    deplacementInstabiliteTemporelle = Sort.Sort("Instabilité Temporelle: Intaclabe", 0, 0, 0, 3, [EffetEtat(EtatBoostCaracFixe(
        "Intaclable", 0, 1, "fuite", 999999), etat_requis_cibles="!Intaclable")], [], 0, 99, 99, 0, 0, "cercle", False)
    activationParadoxeTemporel = Sort.Sort("Paradoxe Temporel", 0, 0, 0, 0, [EffetTpSymCentre(zone=Zones.TypeZoneCercle(4), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur|Xelor|Synchro"), EffetEtat(Etat("ParadoxeTemporel", 0, 2), zone=Zones.TypeZoneCercleSansCentre(
        4), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur|Xelor|Synchro"), EffetEtatSelf(EtatActiveSort("RetourParadoxe", 1, 1, retourParadoxe), cibles_possibles="Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False)
    activationDesynchro = [EffetTpSymCentre(
        zone=Zones.TypeZoneCercleSansCentre(3))]
    activationRune = [EffetTp(genererTF=True, cible_requise=True)]
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Ralentissement", 1, 2, 1, 4, [EffetDegats(4, 5, "Eau"), EffetRetPA(1, cibles_possibles="Allies|Ennemis"), EffetRetPA(1, cibles_possibles="Allies|Ennemis", etat_requis_cibles="Telefrag")], [EffetDegats(7, 8, "Eau"), EffetRetPA(1, cibles_possibles="Allies|Ennemis"), EffetRetPA(1, cibles_possibles="Allies|Ennemis", etat_requis_cibles="Telefrag")], 5, 4, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau et retire 1 PA à la cible.
    Retire 1 PA supplémentaire aux ennemis dans l'état Téléfrag.
    Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),
        Sort.Sort("Ralentissement", 25, 2, 1, 5, [EffetDegats(6, 7, "Eau"), EffetRetPA(1, cibles_possibles="Allies|Ennemis"), EffetRetPA(1, cibles_possibles="Allies|Ennemis", etat_requis_cibles="Telefrag")], [EffetDegats(9, 10, "Eau"), EffetRetPA(1, cibles_possibles="Allies|Ennemis"), EffetRetPA(1, cibles_possibles="Allies|Ennemis", etat_requis_cibles="Telefrag")], 5, 4, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau et retire 1 PA à la cible.
    Retire 1 PA supplémentaire aux ennemis dans l'état Téléfrag.
    Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),
        Sort.Sort("Ralentissement", 52, 2, 1, 6, [EffetDegats(8, 9, "Eau"), EffetRetPA(1, cibles_possibles="Allies|Ennemis"), EffetRetPA(1, cibles_possibles="Allies|Ennemis", etat_requis_cibles="Telefrag")], [EffetDegats(11, 12, "Eau"), EffetRetPA(1, cibles_possibles="Allies|Ennemis"), EffetRetPA(1, cibles_possibles="Allies|Ennemis", etat_requis_cibles="Telefrag")], 5, 4, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau et retire 1 PA à la cible.
    Retire 1 PA supplémentaire aux ennemis dans l'état Téléfrag.
    Le retrait de PA ne peut pas être désenvoûté.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Souvenir", 105, 4, 1, 6, [EffetDegats(26, 30, "Terre"), EffetTeleportePosPrec(1)], [EffetDegats(30, 34, "Terre"), EffetTeleportePosPrec(
            1)], 15, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Terre et téléporte la cible à sa position précédente.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Aiguille", 1, 3, 1, 4, [EffetDegats(14, 18, "Feu"), EffetRetPA(1), EffetRetPA(2, etat_requis_cibles="Telefrag", consomme_etat=True)], [EffetDegats(20, 20, "Feu"), EffetRetPA(1), EffetRetPA(2, etat_requis_cibles="Telefrag", consomme_etat=True)], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Feu et retire 1 PA à la cible.
    Retire des PA supplémentaires aux ennemis dans l'état Téléfrag.
    Le retrait de PA ne peut pas être désenvoûté.
    Retire l'état Téléfrag.""", chaine=True),
        Sort.Sort("Aiguille", 30, 3, 1, 6, [EffetDegats(18, 22, "Feu"), EffetRetPA(1), EffetRetPA(2, etat_requis_cibles="Telefrag", consomme_etat=True)], [EffetDegats(24, 24, "Feu"), EffetRetPA(1), EffetRetPA(2, etat_requis_cibles="Telefrag", consomme_etat=True)], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Feu et retire 1 PA à la cible.
    Retire des PA supplémentaires aux ennemis dans l'état Téléfrag.
    Le retrait de PA ne peut pas être désenvoûté.
    Retire l'état Téléfrag.""", chaine=True),
        Sort.Sort("Aiguille", 60, 3, 1, 8, [EffetDegats(22, 26, "Feu"), EffetRetPA(1), EffetRetPA(2, etat_requis_cibles="Telefrag", consomme_etat=True)], [EffetDegats(28, 28, "Feu"), EffetRetPA(1), EffetRetPA(2, etat_requis_cibles="Telefrag", consomme_etat=True)], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Feu et retire 1 PA à la cible.
    Retire des PA supplémentaires aux ennemis dans l'état Téléfrag.
    Le retrait de PA ne peut pas être désenvoûté.
    Retire l'état Téléfrag.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Rouage", 110, 3, 1, 7, [EffetDegats(12, 14, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Rouage", 1, 1, "PA", 1))], [EffetDegats(15, 17, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Rouage", 1, 1, "PA", 1))], 5, 2, 99, 0, 1, "cercle", True, description="""Occasionne des dommages Eau.
    Le lanceur gagne 1 PA au tour suivant.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Téléportation", 1, 2, 1, 3, [EffetTpSym()], [], 0, 1, 1, 5, 0, "cercle", False, description="""Téléporte le lanceur symétriquement par rapport à la cible.
    Le lanceur gagne 2 PA pour 1 tour à chaque fois qu’il génère un Téléfrag.
    Le temps de relance est supprimé quand un Téléfrag est généré ou consommé.
    Un Téléfrag est généré lorsqu'une entité prend la place d'une autre.""", chaine=True),
        Sort.Sort("Téléportation", 20, 2, 1, 4, [EffetTpSym()], [], 0, 1, 1, 4, 0, "cercle", False, description="""Téléporte le lanceur symétriquement par rapport à la cible.
    Le lanceur gagne 2 PA pour 1 tour à chaque fois qu’il génère un Téléfrag.
    Le temps de relance est supprimé quand un Téléfrag est généré ou consommé.
    Un Téléfrag est généré lorsqu'une entité prend la place d'une autre.""", chaine=True),
        Sort.Sort("Téléportation", 40, 2, 1, 5, [EffetTpSym()], [], 0, 1, 1, 3, 0, "cercle", False, description="""Téléporte le lanceur symétriquement par rapport à la cible.
    Le lanceur gagne 2 PA pour 1 tour à chaque fois qu’il génère un Téléfrag.
    Le temps de relance est supprimé quand un Téléfrag est généré ou consommé.
    Un Téléfrag est généré lorsqu'une entité prend la place d'une autre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Retour Spontané", 101, 1, 0, 7, [EffetTeleportePosPrec(1)], [
        ], 0, 3, 99, 0, 1, "cercle", False, description="""La cible revient à sa position précédente.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Flétrissement", 3, 3, 1, 4, [EffetDegats(16, 19, "Air"), EffetDegats(8, 8, "air", etat_requis_cibles="Telefrag")], [EffetDegats(21, 24, "Air"), EffetDegats(8, 8, "air", etat_requis_cibles="Telefrag")], 15, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air en ligne.
    Occasionne des dommages supplémentaires aux ennemis dans l'état Téléfrag.""", chaine=True),
        Sort.Sort("Flétrissement", 35, 3, 1, 5, [EffetDegats(21, 24, "Air"), EffetDegats(9, 9, "air", etat_requis_cibles="Telefrag")], [EffetDegats(26, 29, "Air"), EffetDegats(9, 9, "air", etat_requis_cibles="Telefrag")], 15, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air en ligne.
    Occasionne des dommages supplémentaires aux ennemis dans l'état Téléfrag.""", chaine=True),
        Sort.Sort("Flétrissement", 67, 3, 1, 6, [EffetDegats(26, 29, "Air"), EffetDegats(10, 10, "air", etat_requis_cibles="Telefrag")], [EffetDegats(31, 34, "Air"), EffetDegats(10, 10, "air", etat_requis_cibles="Telefrag")], 15, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air en ligne.
    Occasionne des dommages supplémentaires aux ennemis dans l'état Téléfrag.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Dessèchement", 115, 4, 1, 6, [EffetDegats(38, 42, "Air"), EffetEtat(EtatEffetDebutTour("Dessèchement", 1, 1, EffetDegats(44, 48, "air", cibles_possbiles="Ennemis", zone=Zones.TypeZoneCercleSansCentre(2)), "Dessechement", "lanceur"))], [EffetDegats(44, 48, "Air"), EffetEtat(EtatEffetDebutTour("Dessèchement", 1, 1, EffetDegats(44, 48, "air", cibles_possbiles="Ennemis", zone=Zones.TypeZoneCercleSansCentre(2)), "Dessechement", "lanceur"))], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Air.
    Occasionne des dommages Air supplémentaires aux ennemis autour de la cible au début du prochain tour du lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Rembobinage", 6, 2, 0, 2, [EffetEtat(EtatRetourCaseDepart("Bobine", 0, 1, "Rembobinage"), cibles_possibles="Allies|Lanceur")], [
        ], 0, 1, 1, 3, 0, "ligne", True, description="""À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour.""", chaine=True),
        Sort.Sort("Rembobinage", 42, 2, 0, 4, [EffetEtat(EtatRetourCaseDepart("Bobine", 0, 1, "Rembobinage"), cibles_possibles="Allies|Lanceur")], [
        ], 0, 1, 1, 3, 0, "ligne", True, description="""À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour.""", chaine=True),
        Sort.Sort("Rembobinage", 74, 2, 0, 6, [EffetEtat(EtatRetourCaseDepart("Bobine", 0, 1, "Rembobinage"), cibles_possibles="Allies|Lanceur")], [
        ], 0, 1, 1, 3, 0, "ligne", True, description="""À la fin de son tour, téléporte l'allié ciblé sur sa position de début de tour.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Renvoi", 120, 3, 1, 6, [EffetTeleporteDebutTour()], [], 0, 1, 1, 2, 0, "ligne", True,
                  description="""Téléporte la cible ennemie à sa cellule de début de tour.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Frappe de Xelor", 9, 3, 1, 3, [EffetTpSymSelf(), EffetDegats(15, 19, "Terre", cibles_possibles="Ennemis")], [EffetTpSymSelf(), EffetDegats(21, 25, "Terre", cibles_possibles="Ennemis")], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Terre aux ennemis.
    Téléporte la cible symétriquement par rapport au lanceur du sort.""", chaine=False),

        Sort.Sort("Frappe de Xelor", 47, 3, 1, 3, [EffetTpSymSelf(), EffetDegats(19, 23, "Terre", cibles_possibles="Ennemis")], [EffetTpSymSelf(), EffetDegats(25, 29, "Terre", cibles_possibles="Ennemis")], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Terre aux ennemis.
    Téléporte la cible symétriquement par rapport au lanceur du sort.""", chaine=False),

        Sort.Sort("Frappe de Xelor", 87, 3, 1, 3, [EffetTpSymSelf(), EffetDegats(23, 27, "Terre", cibles_possibles="Ennemis")], [EffetTpSymSelf(), EffetDegats(29, 33, "Terre", cibles_possibles="Ennemis")], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Terre aux ennemis.
    Téléporte la cible symétriquement par rapport au lanceur du sort.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Engrenage", 125, 3, 1, 5, [EffetTpSymCentre(zone=Zones.TypeZoneLignePerpendiculaire(1), cible_requise=True), EffetDegats(31, 35, "Terre", cibles_possibles="Ennemis", zone=Zones.TypeZoneLignePerpendiculaire(1),  cible_requise=True)], [EffetTpSymCentre(zone=Zones.TypeZoneLignePerpendiculaire(
            1), cible_requise=True), EffetDegats(34, 38, "Terre", cibles_possibles="Ennemis", zone=Zones.TypeZoneLignePerpendiculaire(1), cible_requise=True)], 25, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Terre et téléporte les cibles symétriquement par rapport au centre de la zone d'effet.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Complice", 13, 2, 1, 3, [EffetInvoque("Complice", False, cibles_possibles="", cible_requise=True), EffetTue(cibles_possibles="Cadran de Xelor|Complice", zone=Zones.TypeZoneCercleSansCentre(99))], [], 0, 1, 99, 0, 0, "cercle", True, description="""Invoque un Complice statique qui ne possède aucun sort.
    Il est tué si un autre Complice est invoqué.""", chaine=True),

        Sort.Sort("Complice", 54, 2, 1, 4, [EffetInvoque("Complice", False, cibles_possibles="", cible_requise=True), EffetTue(cibles_possibles="Cadran de Xelor|Complice", zone=Zones.TypeZoneCercleSansCentre(99))], [], 0, 1, 99, 0, 0, "cercle", True, description="""Invoque un Complice statique qui ne possède aucun sort.
    Il est tué si un autre Complice est invoqué.""", chaine=True),

        Sort.Sort("Complice", 94, 2, 1, 5, [EffetInvoque("Complice", False, cibles_possibles="", cible_requise=True), EffetTue(cibles_possibles="Cadran de Xelor|Complice", zone=Zones.TypeZoneCercleSansCentre(99))], [], 0, 1, 99, 0, 0, "cercle", True, description="""Invoque un Complice statique qui ne possède aucun sort.
    Il est tué si un autre Complice est invoqué.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Cadran de Xelor", 130, 3, 1, 5, [EffetInvoque("Cadran de Xelor", False, cibles_possibles="", cible_requise=True), EffetTue(cibles_possibles="Cadran de Xelor|Complice", zone=Zones.TypeZoneCercleSansCentre(99))], [], 0, 1, 1, 3, 0, "cercle", True, description="""Invoque un Cadran qui occasionne des dommages Feu en zone et retire des PA aux ennemis dans l'état Téléfrag.
    Donne des PA aux alliés autour de lui et dans l'état Téléfrag.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Gelure", 17, 2, 2, 4, [EffetDegats(5, 7, "Air", cibles_possibles="Ennemis|Lanceur"), EffetTeleportePosPrec(1)], [EffetDegats(11, 11, "Air", cibles_possibles="Ennemis|Lanceur"), EffetTeleportePosPrec(1)], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air aux ennemis.
    Téléporte la cible à sa position précédente.""", chaine=False),

        Sort.Sort("Gelure", 58, 2, 2, 4, [EffetDegats(8, 10, "Air", cibles_possibles="Ennemis|Lanceur"), EffetTeleportePosPrec(1)], [EffetDegats(14, 14, "Air", cibles_possibles="Ennemis|Lanceur"), EffetTeleportePosPrec(1)], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air aux ennemis.
    Téléporte la cible à sa position précédente.""", chaine=False),

        Sort.Sort("Gelure", 102, 2, 2, 5, [EffetDegats(11, 13, "Air", cibles_possibles="Ennemis|Lanceur"), EffetTeleportePosPrec(1)], [EffetDegats(17, 17, "Air", cibles_possibles="Ennemis|Lanceur"), EffetTeleportePosPrec(1)], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air aux ennemis.
    Téléporte la cible à sa position précédente.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Perturbation", 135, 2, 1, 4, [EffetDegats(9, 11, "Feu", cibles_possibles="Ennemis|Lanceur"), EffetTpSymSelf()], [EffetDegats(11, 13, "Feu", cibles_possibles="Ennemis|Lanceur"), EffetTpSymSelf(
        )], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Feu et téléporte la cible symétriquement par rapport au lanceur.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Sablier de Xelor", 22, 2, 1, 6, [EffetDegats(9, 11, "Feu"), EffetRetPA(2), EffetDegats(9, 11, "feu", zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag"), EffetRetPA(2, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag")], [EffetDegats(13, 15, "Feu"), EffetRetPA(2), EffetDegats(13, 15, "feu", zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag"), EffetRetPA(2, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag")], 5, 3, 1, 0, 1, "ligne", False, description="""Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue.
    Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone.
    Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

        Sort.Sort("Sablier de Xelor", 65, 2, 1, 6, [EffetDegats(12, 14, "Feu"), EffetRetPA(2), EffetDegats(12, 14, "feu", zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag"), EffetRetPA(2, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag")], [EffetDegats(16, 18, "Feu"), EffetRetPA(2), EffetDegats(16, 15, "feu", zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag"), EffetRetPA(2, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag")], 5, 3, 1, 0, 1, "ligne", False, description="""Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue.
    Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone.
    Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

        Sort.Sort("Sablier de Xelor", 108, 2, 1, 7, [EffetDegats(15, 17, "Feu"), EffetRetPA(2), EffetDegats(15, 17, "feu", zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag"), EffetRetPA(2, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag")], [EffetDegats(19, 21, "Feu"), EffetRetPA(2), EffetDegats(19, 21, "feu", zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag"), EffetRetPA(2, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag")], 5, 3, 1, 0, 1, "ligne", False, description="""Occasionne des dommages Feu et retire des PA à la cible en ligne et sans ligne de vue.
    Si la cible est dans l'état Téléfrag, l'effet du sort se joue en zone.
    Le retrait de PA ne peut pas être désenvoûté.""", chaine=True)
    ]))

    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Distorsion Temporelle", 140, 4, 0, 0, [EffetDegats(34, 38, "Air", zone=Zones.TypeZoneCarre(1), cibles_possibles="Ennemis"), EffetTeleportePosPrec(1, zone=Zones.TypeZoneCarre(1), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur")], [EffetDegats(38, 42, "Air", cibles_possibles="Ennemis", zone=Zones.TypeZoneCarre(1)), EffetTeleportePosPrec(1, zone=Zones.TypeZoneCarre(1), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur")], 15, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Air aux ennemis.
    Téléporte les cibles à leur position précédente.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Vol du Temps", 27, 4, 1, 5, [EffetDegats(20, 24, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Vol du Temps", 1, 1, "PA", 1))], [EffetDegats(25, 29, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Vol du Temps", 1, 1, "PA", 1))], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Eau à la cible.
    Le lanceur gagne 1 PA au début de son prochain tour.""", chaine=True),

        Sort.Sort("Vol du Temps", 72, 4, 1, 5, [EffetDegats(25, 29, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Vol du Temps", 1, 1, "PA", 1))], [EffetDegats(30, 34, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Vol du Temps", 1, 1, "PA", 1))], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Eau à la cible.
    Le lanceur gagne 1 PA au début de son prochain tour.""", chaine=True),

        Sort.Sort("Vol du Temps", 118, 4, 1, 5, [EffetDegats(30, 34, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Vol du Temps", 1, 1, "PA", 1))], [EffetDegats(35, 39, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Vol du Temps", 1, 1, "PA", 1))], 15, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Eau à la cible.
    Le lanceur gagne 1 PA au début de son prochain tour.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Pétrification", 145, 5, 1, 7, [EffetDegats(34, 38, "Eau"), EffetEtatSelf(EtatBoostSortCarac("Pétrification", 0, 2, "Pétrification", "coutPA", -1), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", etat_requis="Telefrag"), EffetRetPA(2)], [EffetDegats(38, 42, "Eau"), EffetEtatSelf(EtatBoostSortCarac("Pétrification", 0, 2, "Pétrification", "coutPA", -1), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", etat_requis="Telefrag"), EffetRetPA(2)], 25, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Eau et retire des PA.
    Si la cible est dans l'état Téléfrag, le coût en PA du sort est réduit pendant 2 tours.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Flou", 32, 2, 1, 1, [EffetEtat(EtatBoostCaracFixe("Flou", 0, 1, "PA", -2), zone=Zones.TypeZoneCercle(3), cible_requise=True, cibles_exclues="Lanceur"), EffetEtat(EtatBoostCaracFixe("Flou", 1, 1, "PA", 2), zone=Zones.TypeZoneCercle(3), cible_requise=True)], [], 0, 1, 1, 5, 0, "cercle", False, description="""Retire des PA en zone le tour en cours.
    Augmente les PA en zone le tour suivant.""", chaine=True),

        Sort.Sort("Flou", 81, 2, 1, 2, [EffetEtat(EtatBoostCaracFixe("Flou", 0, 1, "PA", -2), zone=Zones.TypeZoneCercle(3), cible_requise=True, cibles_exclues="Lanceur"), EffetEtat(EtatBoostCaracFixe("Flou", 1, 1, "PA", 2), zone=Zones.TypeZoneCercle(3), cible_requise=True)], [], 0, 1, 1, 4, 0, "cercle", True, description="""Retire des PA en zone le tour en cours.
    Augmente les PA en zone le tour suivant.""", chaine=True),

        Sort.Sort("Flou", 124, 2, 1, 3, [EffetEtat(EtatBoostCaracFixe("Flou", 0, 1, "PA", -2), zone=Zones.TypeZoneCercle(3), cible_requise=True, cibles_exclues="Lanceur"), EffetEtat(EtatBoostCaracFixe("Flou", 1, 1, "PA", 2), zone=Zones.TypeZoneCercle(3), cible_requise=True)], [], 0, 1, 1, 3, 0, "cercle", True, description="""Retire des PA en zone le tour en cours.
    Augmente les PA en zone le tour suivant.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Conservation", 150, 2, 0, 5, [EffetEtat(EtatModDegPer("Conservation", 0, 1, 130), zone=Zones.TypeZoneCercle(2), cible_requise=True, cibles_possibles="Allies|Lanceur"), EffetEtat(EtatModDegPer("Conservation", 1, 1, 70), zone=Zones.TypeZoneCercle(2), cible_requise=True, cibles_possibles="Allies|Lanceur")], [], 0, 1, 1, 2, 0, "cercle", True, description="""Augmente les dommages subis par les alliés en zone de 30% pour le tour en cours.
    Au tour suivant, les cibles réduisent les dommages subis de 30%.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Poussière Temporelle", 38, 4, 0, 4, [EffetDegats(22, 25, "Feu", cibles_possibles="Ennemis", zone=Zones.TypeZoneCercle(3)), EffetDegats(22, 25, "Feu", zone=Zones.TypeZoneCercle(3), etat_requis_cibles="Telefrag"), EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3), etat_requis_cibles="Telefrag")], [EffetDegats(26, 29, "Feu", cibles_possibles="Ennemis", zone=Zones.TypeZoneCercle(3)), EffetDegats(26, 29, "Feu", zone=Zones.TypeZoneCercle(3), etat_requis_cibles="Telefrag"), EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3), etat_requis_cibles="Telefrag")], 25, 2, 99, 0, 1, "cercle", True, description="""Occasionne des dommages Feu.
    Les entités dans l'état Téléfrag dans la zone d'effet subissent également des dommages Feu et sont téléportées symétriquement par rapport à la cellule ciblée.""", chaine=True),

        Sort.Sort("Poussière Temporelle", 90, 4, 0, 5, [EffetDegats(28, 31, "Feu", cibles_possibles="Ennemis", zone=Zones.TypeZoneCercle(3)), EffetDegats(28, 31, "Feu", zone=Zones.TypeZoneCercle(3), etat_requis_cibles="Telefrag"), EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3), etat_requis_cibles="Telefrag")], [EffetDegats(32, 35, "Feu", cibles_possibles="Ennemis", zone=Zones.TypeZoneCercle(3)), EffetDegats(32, 35, "Feu", zone=Zones.TypeZoneCercle(3), etat_requis_cibles="Telefrag"), EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3), etat_requis_cibles="Telefrag")], 25, 2, 99, 0, 1, "cercle", True, description="""Occasionne des dommages Feu.
    Les entités dans l'état Téléfrag dans la zone d'effet subissent également des dommages Feu et sont téléportées symétriquement par rapport à la cellule ciblée.""", chaine=True),

        Sort.Sort("Poussière Temporelle", 132, 4, 0, 6, [EffetDegats(34, 37, "Feu", cibles_possibles="Ennemis", zone=Zones.TypeZoneCercle(3)), EffetDegats(34, 37, "Feu", zone=Zones.TypeZoneCercle(3), etat_requis_cibles="Telefrag"), EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3), etat_requis_cibles="Telefrag")], [EffetDegats(38, 41, "Feu", cibles_possibles="Ennemis", zone=Zones.TypeZoneCercle(3)), EffetDegats(38, 41, "Feu", zone=Zones.TypeZoneCercle(3), etat_requis_cibles="Telefrag"), EffetTpSymCentre(zone=Zones.TypeZoneCercleSansCentre(3), etat_requis_cibles="Telefrag")], 25, 2, 99, 0, 1, "cercle", True, description="""Occasionne des dommages Feu.
    Les entités dans l'état Téléfrag dans la zone d'effet subissent également des dommages Feu et sont téléportées symétriquement par rapport à la cellule ciblée.""", chaine=True)
    ]))

    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Suspension Temporelle", 155, 3, 1, 6, [EffetRafraichirEtats(1, etat_requis="Telefrag", consomme_etat=True), EffetDegats(25, 29, "Feu")], [EffetRafraichirEtats(1, etat_requis="Telefrag", consomme_etat=True), EffetDegats(29, 33, "Feu")], 15, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Feu sur les ennemis.
    Réduit la durée des effets sur les cibles ennemies dans l'état Téléfrag et retire l'état.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Raulebaque", 44, 2, 0, 0, [EffetTeleportePosPrec(1, zone=Zones.TypeZoneInfini())], [
        ], 0, 1, 1, 4, 0, "cercle", False, description="""Replace tous les personnages à leurs positions précédentes.""", chaine=True),

        Sort.Sort("Raulebaque", 97, 2, 0, 0, [EffetTeleportePosPrec(1, zone=Zones.TypeZoneInfini())], [
        ], 0, 1, 1, 3, 0, "cercle", False, description="""Replace tous les personnages à leurs positions précédentes.""", chaine=True),

        Sort.Sort("Raulebaque", 137, 2, 0, 0, [EffetTeleportePosPrec(1, zone=Zones.TypeZoneInfini())], [
        ], 0, 1, 1, 2, 0, "cercle", False, description="""Replace tous les personnages à leurs positions précédentes.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Instabilité Temporelle", 160, 3, 0, 7, [EffetGlyphe(activationInstabiliteTemporelle, deplacementInstabiliteTemporelle, sortieInstabiliteTemporelle, 2, "Instabilité Temporelle", (255, 255, 0), zone=Zones.TypeZoneCercle(3), cible_requise=True)], [], 0, 1, 1, 3, 1, "cercle", False, description="""Pose un glyphe qui renvoie les entités à leur position précédente.
    Les entités dans le glyphe sont dans l'état Intaclable.
    Les effets du glyphe sont également exécutés lorsque le lanceur génère un Téléfrag.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Démotivation", 50, 3, 1, 3, [EffetRafraichirEtats(1, cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", etat_requis="Telefrag", consomme_etat=True), EffetDegats(17, 20, "Terre", cibles_possibles="Ennemis")], [EffetRafraichirEtats(1, cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", etat_requis="Telefrag", consomme_etat=True), EffetDegats(22, 25, "Terre", cibles_possibles="Ennemis")], 25, 3, 2, 0, 0, "diagonale", True, description="""Occasionne des dommages Terre aux ennemis en diagonale.
    Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état.""", chaine=True),

        Sort.Sort("Démotivation", 103, 3, 1, 4, [EffetRafraichirEtats(1, cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", etat_requis="Telefrag", consomme_etat=True), EffetDegats(20, 23, "Terre", cibles_possibles="Ennemis")], [EffetRafraichirEtats(1, cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", etat_requis="Telefrag", consomme_etat=True), EffetDegats(25, 28, "Terre", cibles_possibles="Ennemis")], 25, 3, 2, 0, 0, "diagonale", True, description="""Occasionne des dommages Terre aux ennemis en diagonale.
    Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état.""", chaine=True),

        Sort.Sort("Démotivation", 143, 3, 1, 5, [EffetRafraichirEtats(1, cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", etat_requis="Telefrag", consomme_etat=True), EffetDegats(23, 26, "Terre", cibles_possibles="Ennemis")], [EffetRafraichirEtats(1, cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", etat_requis="Telefrag", consomme_etat=True), EffetDegats(28, 31, "Terre", cibles_possibles="Ennemis")], 25, 3, 2, 0, 0, "diagonale", True, description="""Occasionne des dommages Terre aux ennemis en diagonale.
    Réduit la durée des effets sur les cibles dans l'état Téléfrag et retire l'état.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Pendule", 165, 4, 1, 5, [EffetTpSym(), EffetDegats(38, 42, "Air", zone=Zones.TypeZoneCercle(2), cibles_possibles="Ennemis"), EffetTeleportePosPrec(1, zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")], [EffetTpSym(), EffetDegats(46, 50, "Air", zone=Zones.TypeZoneCercle(2), cibles_possibles="Ennemis"), EffetTeleportePosPrec(1, zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")], 5, 2, 1, 0, 0, "cercle", True, description="""Le lanceur se téléporte symétriquement par rapport à la cible et occasionne des dommages Air en zone sur sa cellule de destination.
    Il revient ensuite à sa position précédente.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Paradoxe Temporel", 56, 3, 0, 0, [EffetEntiteLanceSort("Complice|Cadran de Xelor", activationParadoxeTemporel)], [], 0, 1, 1, 4, 0, "cercle", False, description="""Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran).
    Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles.
    Fixe le temps de relance de Cadran de Xelor et de Complice à 1.""", chaine=True),

        Sort.Sort("Paradoxe Temporel", 112, 3, 0, 0, [EffetEntiteLanceSort("Complice|Cadran de Xelor", activationParadoxeTemporel)], [], 0, 1, 1, 3, 0, "cercle", False, description="""Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran).
    Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles.
    Fixe le temps de relance de Cadran de Xelor et de Complice à 1.""", chaine=True),

        Sort.Sort("Paradoxe Temporel", 147, 3, 0, 0, [EffetEntiteLanceSort("Complice|Cadran de Xelor", activationParadoxeTemporel)], [], 0, 1, 1, 2, 0, "cercle", False, description="""Téléporte symétriquement par rapport au Complice (ou au Cadran) les alliés et ennemis (dans une zone de 4 cases autour du Cadran).
    Au début du tour du Complice (ou du Cadran) : téléporte à nouveau symétriquement les mêmes cibles.
    Fixe le temps de relance de Cadran de Xelor et de Complice à 1.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Faille Temporelle", 170, 3, 0, 0, [EffetEchangePlace(zone=Zones.TypeZoneInfini(), cibles_possibles="Cadran de Xelor|Complice", genererTF=True), EffetEtat(EtatEffetFinTour("Retour faille temporelle", 0, 1, EffetTeleportePosPrec(1), "Fin faille Temporelle", "cible")), EffetEtat(Etat("Faille_temporelle", 0, 1), zone=Zones.TypeZoneInfini(), cibles_possibles="Xelor")], [], 0, 1, 1, 2, 0, "cercle", False, description="""Le lanceur échange sa position avec celle du Complice (ou du Cadran).
    À la fin du tour, le Complice (ou le Cadran) revient à sa position précédente.
    La Synchro ne peut pas être déclenchée pendant la durée de Faille Temporelle.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Synchro", 62, 2, 1, 2, [EffetTue(zone=Zones.TypeZoneInfini(), cibles_possibles="Synchro"), EffetInvoque("Synchro", False, cibles_possibles="", cible_requise=True), EffetEtatSelf(EtatBoostCaracFixe("Synchro", 1, -1, "PA", -1))], [], 0, 1, 1, 3, 0, "cercle", False, description="""Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour.
    La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag.
    Elle n'est pas affectée par les effets de Rembobinage.
    À partir du tour suivant son lancer, son invocateur perd 1 PA.""", chaine=False),

        Sort.Sort("Synchro", 116, 2, 1, 3, [EffetTue(zone=Zones.TypeZoneInfini(), cibles_possibles="Synchro"), EffetInvoque("Synchro", False, cibles_possibles="", cible_requise=True), EffetEtatSelf(EtatBoostCaracFixe("Synchro", 1, -1, "PA", -1))], [], 0, 1, 1, 3, 0, "cercle", False, description="""Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour.
    La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag.
    Elle n'est pas affectée par les effets de Rembobinage.
    À partir du tour suivant son lancer, son invocateur perd 1 PA.""", chaine=False),

        Sort.Sort("Synchro", 153, 2, 1, 4, [EffetTue(zone=Zones.TypeZoneInfini(), cibles_possibles="Synchro"), EffetInvoque("Synchro", False, cibles_possibles="", cible_requise=True), EffetEtatSelf(EtatBoostCaracFixe("Synchro", 1, -1, "PA", -1))], [], 0, 1, 1, 3, 0, "cercle", False, description="""Invoque Synchro qui gagne en puissance et se soigne quand un Téléfrag est généré, 1 fois par tour.
    La Synchro meurt en occasionnant des dommages Air en zone de 3 cases si elle subit un Téléfrag.
    Elle n'est pas affectée par les effets de Rembobinage.
    À partir du tour suivant son lancer, son invocateur perd 1 PA.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Désynchronisation", 175, 2, 1, 6, [EffetPiege(Zones.TypeZoneCercle(0), activationDesynchro, "Désynchronisation", (255, 0, 255), cible_requise=True)], [
        ], 0, 2, 99, 0, 1, "cercle", False, description="""Pose un piège qui téléporte symétriquement les entités proches.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Contre", 69, 2, 0, 2, [EffetEtat(EtatContre("Contre", 0, 2, 30, 1), zone=Zones.TypeZoneCercle(2), cibles_possibles="Allies|Lanceur", cible_requise=True)], [
        ], 0, 1, 1, 5, 0, "cercle", True, description="""Renvoie une partie des dommages subis en mêlée à l'attaquant.""", chaine=True),
        Sort.Sort("Contre", 122, 2, 0, 4, [EffetEtat(EtatContre("Contre", 0, 2, 40, 1), zone=Zones.TypeZoneCercle(2), cibles_possibles="Allies|Lanceur", cible_requise=True)], [
        ], 0, 1, 1, 5, 0, "cercle", True, description="""Renvoie une partie des dommages subis en mêlée à l'attaquant.""", chaine=True),
        Sort.Sort("Contre", 162, 2, 0, 6, [EffetEtat(EtatContre("Contre", 0, 2, 50, 1), zone=Zones.TypeZoneCercle(2), cibles_possibles="Allies|Lanceur", cible_requise=True)], [
        ], 0, 1, 1, 5, 0, "cercle", True, description="""Renvoie une partie des dommages subis en mêlée à l'attaquant.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Bouclier Temporel", 180, 3, 0, 3, [EffetEtat(EtatEffetSiSubit("Bouclier temporel", 0, 1, EffetTeleportePosPrec(1), "Bouclier Temporel", "lanceur", "attaquant", ""))], [
        ], 0, 1, 1, 3, 0, "cercle", True, description="""Si la cible subit des dommages, son attaquant et elle reviennent à leur position précédente.""", chaine=True)
    ]))

    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Fuite", 77, 1, 0, 1, [EffetEtat(EtatEffetDebutTour("Fuite", 1, 1, EffetTeleportePosPrec(1), "Fuite", "cible"))], [
        ], 0, 2, 1, 0, 0, "cercle", False, description="""Téléporte la cible sur sa position précédente au début du prochain tour du lanceur.""", chaine=True),

        Sort.Sort("Fuite", 128, 1, 0, 3, [EffetEtat(EtatEffetDebutTour("Fuite", 1, 1, EffetTeleportePosPrec(1), "Fuite", "cible"))], [
        ], 0, 3, 1, 0, 0, "cercle", False, description="""Téléporte la cible sur sa position précédente au début du prochain tour du lanceur.""", chaine=True),

        Sort.Sort("Fuite", 172, 1, 0, 5, [EffetEtat(EtatEffetDebutTour("Fuite", 1, 1, EffetTeleportePosPrec(1), "Fuite", "cible"))], [
        ], 0, 4, 2, 0, 0, "cercle", False, description="""Téléporte la cible sur sa position précédente au début du prochain tour du lanceur.""", chaine=True)
    ]))

    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Prémonition", 185, 2, 1, 5, [EffetRune(1, activationRune, "Prémonition", (164, 78, 163), cible_requise=True)], [
        ], 0, 1, 1, 1, 0, "cercle", False, description="""Au prochain tour, le lanceur se téléporte sur la cellule ciblée.""", chaine=True)
    ]))

    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Horloge", 84, 5, 1, 4, [EffetVolDeVie(28, 31, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Horloge", 1, 1, "PA", 1)), EffetRetPA(2, cibles_possibles="Ennemis", etat_requis="Telefrag", consomme_etat=True)], [EffetVolDeVie(32, 35, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Horloge", 1, 1, "PA", 1)), EffetRetPA(2, cibles_possibles="Ennemis", etat_requis="Telefrag", consomme_etat=True)], 25, 3, 2, 0, 0, "ligne", True, description="""Vole de vie dans l'élément Eau.
    Le lanceur gagne 1 PA au début de son prochain tour.
    Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état.
    Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

        Sort.Sort("Horloge", 134, 5, 1, 5, [EffetVolDeVie(32, 35, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Horloge", 1, 1, "PA", 1)), EffetRetPA(3, cibles_possibles="Ennemis", etat_requis="Telefrag", consomme_etat=True)], [EffetVolDeVie(36, 39, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Horloge", 1, 1, "PA", 1)), EffetRetPA(3, cibles_possibles="Ennemis", etat_requis="Telefrag", consomme_etat=True)], 25, 3, 2, 0, 0, "ligne", True, description="""Vole de vie dans l'élément Eau.
    Le lanceur gagne 1 PA au début de son prochain tour.
    Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état.
    Le retrait de PA ne peut pas être désenvoûté.""", chaine=True),

        Sort.Sort("Horloge", 178, 5, 1, 6, [EffetVolDeVie(36, 39, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Horloge", 1, 1, "PA", 1)), EffetRetPA(4, cibles_possibles="Ennemis", etat_requis="Telefrag", consomme_etat=True)], [EffetVolDeVie(40, 43, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Horloge", 1, 1, "PA", 1)), EffetRetPA(4, cibles_possibles="Ennemis", etat_requis="Telefrag", consomme_etat=True)], 25, 3, 2, 0, 0, "ligne", True, description="""Vole de vie dans l'élément Eau.
    Le lanceur gagne 1 PA au début de son prochain tour.
    Retire des PA aux ennemis dans l'état Téléfrag et leur retire l'état.
    Le retrait de PA ne peut pas être désenvoûté.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Clepsydre", 190, 4, 1, 3, [EffetDegats(30, 34, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Clepsydre", 1, 1, "PA", 2), etat_requis="Telefrag", consomme_etat=True)], [EffetDegats(36, 40, "Eau"), EffetEtatSelf(EtatBoostCaracFixe("Clepsydre", 1, 1, "PA", 2), etat_requis="Telefrag", consomme_etat=True)], 15, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Eau.
    Si la cible est dans l'état Téléfrag, le lanceur gagne 2 PA au prochain tour.
    Retire l'état Téléfrag.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Rayon Obscur", 92, 5, 1, 4, [EffetDegats(27, 31, "Terre", etat_requis="!Telefrag"), EffetDegats(54, 62, "Terre", etat_requis="Telefrag", consomme_etat=True)], [EffetDegats(34, 38, "Terre", etat_requis="!Telefrag"), EffetDegats(68, 76, "Terre", etat_requis="Telefrag", consomme_etat=True)], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Terre en ligne.
    Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag.
    Retire l'état Téléfrag.""", chaine=False),

        Sort.Sort("Rayon Obscur", 141, 5, 1, 5, [EffetDegats(30, 34, "Terre", etat_requis="!Telefrag"), EffetDegats(60, 68, "Terre", etat_requis="Telefrag", consomme_etat=True)], [EffetDegats(37, 41, "Terre", etat_requis="!Telefrag"), EffetDegats(74, 82, "Terre", etat_requis="Telefrag", consomme_etat=True)], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Terre en ligne.
    Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag.
    Retire l'état Téléfrag.""", chaine=False),

        Sort.Sort("Rayon Obscur", 187, 5, 1, 6, [EffetDegats(33, 37, "Terre", etat_requis="!Telefrag"), EffetDegats(66, 74, "Terre", etat_requis="Telefrag", consomme_etat=True)], [EffetDegats(40, 44, "Terre", etat_requis="!Telefrag"), EffetDegats(80, 88, "Terre", etat_requis="Telefrag", consomme_etat=True)], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Terre en ligne.
    Les dommages de base du sort sont doublés contre les ennemis dans l'état Téléfrag.
    Retire l'état Téléfrag.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Rayon Ténébreux", 195, 3, 1, 5, [EffetDegats(19, 23, "Terre"), EffetDegats(19, 23, "terre", zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag")], [EffetDegats(23, 27, "Terre"), EffetDegats(23, 37, "terre", zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Ennemis", etat_requis="Telefrag")], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Terre.
    Si la cible est dans l'état Téléfrag, occasionne des dommages Terre en zone aux ennemis autour d'elle.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Momification", 100, 2, 0, 0, [EffetEtat(EtatBoostCaracFixe("Momification", 0, 1, "PM", 2)), EffetEtat(EtatTelefrag(
            "Telefrag", 0, 1, "Momification"), zone=Zones.TypeZoneInfini())], [], 0, 1, 1, 5, 0, "cercle", False, description="""Gagne 2 PM et fixe l'état Téléfrag à tous les alliés et ennemis.""", chaine=True),

        Sort.Sort("Momification", 147, 2, 0, 0, [EffetEtat(EtatBoostCaracFixe("Momification", 0, 1, "PM", 2)), EffetEtat(EtatTelefrag(
            "Telefrag", 0, 1, "Momification"), zone=Zones.TypeZoneInfini())], [], 0, 1, 1, 4, 0, "cercle", False, description="""Gagne 2 PM et fixe l'état Téléfrag à tous les alliés et ennemis.""", chaine=True),

        Sort.Sort("Momification", 197, 2, 0, 0, [EffetEtat(EtatBoostCaracFixe("Momification", 0, 1, "PM", 2)), EffetEtat(EtatTelefrag(
            "Telefrag", 0, 1, "Momification"), zone=Zones.TypeZoneInfini())], [], 0, 1, 1, 3, 0, "cercle", False, description="""Gagne 2 PM et fixe l'état Téléfrag à tous les alliés et ennemis.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Glas", 200, 3, 0, 3, [EffetDegats(4, 4, "Air", zone=Zones.TypeZoneCarre(1)), EffetDegats(4, 4, "Eau", zone=Zones.TypeZoneCarre(1)), EffetDegats(4, 4, "Terre", zone=Zones.TypeZoneCarre(1)), EffetDegats(4, 4, "Feu", zone=Zones.TypeZoneCarre(1)), EffetRetireEtat("Glas", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")], [], 0, 1, 1, 2, 0, "ligne", True, description="""Occasionne des dommages Air, Eau, Terre, Feu.
    Les dommages sont augmentés pour chaque Téléfrag généré depuis son dernier lancer.
    N'occasionne pas de dommages si aucun Téléfrag n'a été généré depuis son dernier lancer.""", chaine=True)
    ]))
    return sorts
