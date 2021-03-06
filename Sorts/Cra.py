"""@summary: Rassemble les sorts du Crâ
"""
# pylint: disable=line-too-long
import Sort
import Zones
import os
import Personnages
from Effets.EffetDegats import EffetDegats, EffetVolDeVie, EffetDegatsSelonPMUtilises
from Effets.EffetSoin import EffetSoinPerPVMax
from Effets.EffetEtat import EffetEtat, EffetEtatSelf
from Effets.EffetPousser import EffetAttire, EffetPousser
from Effets.EffetRet import EffetRetPA, EffetRetPM
from Effets.EffetDevoilePiege import EffetDevoilePiege
from Effets.EffetInvoque import EffetInvoque
from Effets.EffetTue import EffetTue
from Effets.EffetPropage import EffetPropage

from Etats.Etat import Etat
from Etats.EtatBoostCarac import EtatBoostCaracFixe
from Etats.EtatBoostBaseDeg import EtatBoostBaseDeg
from Etats.EtatModDeg import EtatModDegPer
from Etats.EtatEffet import EtatEffetDebutTour, EtatEffetFinTour, EtatEffetSiPousse, EtatEffetSiSubit
from Etats.EtatModSoin import EtatModSoinPer
from Etats.EtatBoostSorts import EtatBoostSortsPer


def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de début de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    sorts = []
    

    with open("")
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Magique", 1, 3, 1, 8, [EffetDegats(13, 15, "Air"), EffetEtat(EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", -2)), EffetEtatSelf(EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", 2))], [EffetDegats(16, 18, "Air"), EffetEtat(
    #         EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", -2)), EffetEtatSelf(EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", 2))], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air et vole la portée de la cible.""", chaine=True),

    #     Sort.Sort("Flèche Magique", 20, 3, 1, 10, [EffetDegats(16, 18, "Air"), EffetEtat(EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", -2)), EffetEtatSelf(EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", 2))], [EffetDegats(19, 21, "Air"), EffetEtat(
    #         EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", -2)), EffetEtatSelf(EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", 2))], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air et vole la portée de la cible.""", chaine=True),

    #     Sort.Sort("Flèche Magique", 40, 3, 1, 12, [EffetDegats(19, 21, "Air"), EffetEtat(EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", -2)), EffetEtatSelf(EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", 2))], [EffetDegats(22, 24, "Air"), EffetEtat(
    #         EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", -2)), EffetEtatSelf(EtatBoostCaracFixe("Fleche Magique", 0, 1, "PO", 2))], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air et vole la portée de la cible.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche de Concentration", 101, 3, 3, 8, [EffetDegats(22, 26, "Air", zone=Zones.TypeZoneCroix(3), cibles_exclues="Lanceur"), EffetAttire(2, "CaseCible", zone=Zones.TypeZoneCroix(3), cibles_exclues="Lanceur")], [EffetDegats(25, 29, "Air", zone=Zones.TypeZoneCroix(3), cibles_exclues="Lanceur"), EffetAttire(2, "CaseCible", zone=Zones.TypeZoneCroix(3), cibles_exclues="Lanceur")], 15, 2, 1, 0, 1, "cercle", True, description="""Occasionne des dommages Air et attire vers la cible.
    # N'affecte pas le lanceur.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche de Recul", 1, 3, 1, 4, [EffetDegats(17, 20, "Air"), EffetPousser(2)], [EffetDegats(21, 24, "Air"), EffetPousser(
    #         2)], 25, 2, 1, 0, 0, "ligne", True, description="""Occasionne des dommages Air aux ennemis et pousse la cible.""", chaine=True),

    #     Sort.Sort("Flèche de Recul", 25, 3, 1, 6, [EffetDegats(21, 24, "Air"), EffetPousser(3)], [EffetDegats(25, 28, "Air"), EffetPousser(
    #         3)], 25, 2, 1, 0, 0, "ligne", True, description="""Occasionne des dommages Air aux ennemis et pousse la cible.""", chaine=True),

    #     Sort.Sort("Flèche de Recul", 52, 3, 1, 8, [EffetDegats(25, 28, "Air"), EffetPousser(4)], [EffetDegats(29, 32, "Air"), EffetPousser(
    #         4)], 25, 2, 1, 0, 0, "ligne", True, description="""Occasionne des dommages Air aux ennemis et pousse la cible.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche érosive", 105, 3, 1, 3, [EffetEtat(EtatBoostCaracFixe("Fleche Erosive", 0, 2, "erosion", 10)), EffetDegats(25, 29, "Terre")], [EffetEtat(EtatBoostCaracFixe(
    #         "Fleche Erosive", 0, 2, "erosion", 10)), EffetDegats(29, 33, "Terre")], 15, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Terre et applique un malus d'érosion.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche de dispersion", 1, 3, 1, 6, [EffetPousser(2, "CaseCible", reversedTreatmentOrder=True, zone=Zones.TypeZoneCroix(2), cible_non_requise=True)], [
    #     ], 0, 1, 1, 2, 1, "cercle", True, description="""Pousse les ennemis et alliés, même s'ils sont bloqués par d'autres entités.""", chaine=True),

    #     Sort.Sort("Flèche de dispersion", 30, 3, 1, 9, [EffetPousser(2, "CaseCible", reversedTreatmentOrder=True, zone=Zones.TypeZoneCroix(2), cible_non_requise=True)], [
    #     ], 0, 1, 1, 2, 1, "cercle", True, description="""Pousse les ennemis et alliés, même s'ils sont bloqués par d'autres entités.""", chaine=True),

    #     Sort.Sort("Flèche de dispersion", 60, 3, 1, 12, [EffetPousser(2, "CaseCible", reversedTreatmentOrder=True, zone=Zones.TypeZoneCroix(2), cible_non_requise=True)], [
    #     ], 0, 1, 1, 2, 1, "cercle", True, description="""Pousse les ennemis et alliés, même s'ils sont bloqués par d'autres entités.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Represailles", 110, 4, 2, 5, [EffetEtat(EtatBoostCaracFixe("Represailles", 0, 1, "PM", -100)), EffetEtat(Etat(
    #         "Pesanteur", 0, 1))], [], 0, 1, 1, 5, 0, "ligne", True, description="""Immobilise la cible et applique l'état Pesanteur.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Glacée", 3, 3, 3, 6, [EffetDegats(9, 11, "Feu"), EffetRetPA(2)], [EffetDegats(12, 14, "Feu"), EffetRetPA(
    #         2)], 5, 99, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Feu et retire des PA.""", chaine=True),

    #     Sort.Sort("Flèche Glacée", 35, 3, 3, 8, [EffetDegats(13, 15, "Feu"), EffetRetPA(2)], [EffetDegats(16, 18, "Feu"), EffetRetPA(
    #         2)], 5, 99, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Feu et retire des PA.""", chaine=True),

    #     Sort.Sort("Flèche Glacée", 67, 3, 3, 10, [EffetDegats(17, 19, "Feu"), EffetRetPA(2)], [EffetDegats(20, 22, "Feu"), EffetRetPA(
    #         2)], 5, 99, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Feu et retire des PA.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Paralysante", 115, 5, 2, 6, [EffetDegats(39, 42, "Feu", cible_non_requise=True, zone=Zones.TypeZoneCroix(1)), EffetRetPA(4, zone=Zones.TypeZoneCroix(1), cible_non_requise=True)], [EffetDegats(
    #         43, 46, "Feu", zone=Zones.TypeZoneCroix(1), cible_non_requise=True), EffetRetPA(4, zone=Zones.TypeZoneCroix(1), cible_non_requise=True)], 25, 1, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu et retire des PA.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Enflammée", 6, 4, 1, 4, [EffetDegats(23, 25, "Feu", cible_non_requise=True, zone=Zones.TypeZoneLigne(5)), EffetPousser(1, zone=Zones.TypeZoneLigne(5), cible_non_requise=True, reversedTreatmentOrder=True)], [EffetDegats(26, 28, "Feu", zone=Zones.TypeZoneLigne(
    #         5), cible_non_requise=True), EffetPousser(1, zone=Zones.TypeZoneLigne(5), cible_non_requise=True, reversedTreatmentOrder=True)], 25, 2, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Feu et pousse les cibles présentes dans la zone d'effet du sort.""", chaine=True),

    #     Sort.Sort("Flèche Enflammée", 42, 4, 1, 6, [EffetDegats(27, 29, "Feu", cible_non_requise=True, zone=Zones.TypeZoneLigne(5)), EffetPousser(1, zone=Zones.TypeZoneLigne(5), cible_non_requise=True, reversedTreatmentOrder=True)], [EffetDegats(30, 32, "Feu", zone=Zones.TypeZoneLigne(
    #         5), cible_non_requise=True), EffetPousser(1, zone=Zones.TypeZoneLigne(5), cible_non_requise=True, reversedTreatmentOrder=True)], 25, 2, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Feu et pousse les cibles présentes dans la zone d'effet du sort.""", chaine=True),

    #     Sort.Sort("Flèche Enflammée", 74, 4, 1, 8, [EffetDegats(33, 35, "Feu", cible_non_requise=True, zone=Zones.TypeZoneLigne(5)), EffetPousser(1, zone=Zones.TypeZoneLigne(5), cible_non_requise=True, reversedTreatmentOrder=True)], [EffetDegats(39, 41, "Feu", zone=Zones.TypeZoneLigne(
    #         5), cible_non_requise=True), EffetPousser(1, zone=Zones.TypeZoneLigne(5), cible_non_requise=True, reversedTreatmentOrder=True)], 25, 2, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Feu et pousse les cibles présentes dans la zone d'effet du sort.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Répulsive", 120, 3, 1, 7, [EffetDegats(28, 32, "Feu", cible_non_requise=True, zone=Zones.TypeZoneLignePerpendiculaire(1)), EffetPousser(1, "CaseCible", cible_non_requise=True, zone=Zones.TypeZoneLignePerpendiculaire(1))], [EffetDegats(
    #         34, 38, "Feu", zone=Zones.TypeZoneLignePerpendiculaire(1), cible_non_requise=True), EffetPousser(1, "CaseCible", cible_non_requise=True, zone=Zones.TypeZoneLignePerpendiculaire(1))], 5, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Feu et repousse de 1 case.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Tir éloigné", 9, 3, 0, 0, [EffetEtat(EtatBoostCaracFixe("Tir_eloigne", 0, 4, "PO", 2), zone=Zones.TypeZoneCercle(2))], [EffetEtat(EtatBoostCaracFixe(
    #         "Tir_eloigne", 0, 4, "PO", 3), zone=Zones.TypeZoneCercle(2))], 25, 1, 1, 5, 0, "cercle", False, description="""Augmente la portée des cibles présentes dans la zone d'effet.""", chaine=True),

    #     Sort.Sort("Tir éloigné", 47, 3, 0, 0, [EffetEtat(EtatBoostCaracFixe("Tir_eloigne", 0, 4, "PO", 4), zone=Zones.TypeZoneCercle(2))], [EffetEtat(EtatBoostCaracFixe(
    #         "Tir_eloigne", 0, 4, "PO", 5), zone=Zones.TypeZoneCercle(2))], 25, 1, 1, 5, 0, "cercle", False, description="""Augmente la portée des cibles présentes dans la zone d'effet.""", chaine=True),

    #     Sort.Sort("Tir éloigné", 87, 3, 0, 0, [EffetEtat(EtatBoostCaracFixe("Tir_eloigne", 0, 4, "PO", 6), zone=Zones.TypeZoneCercle(3))], [EffetEtat(EtatBoostCaracFixe(
    #         "Tir_eloigne", 0, 4, "PO", 7), zone=Zones.TypeZoneCercle(3))], 25, 1, 1, 5, 0, "cercle", False, description="""Augmente la portée des cibles présentes dans la zone d'effet.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Acuité Absolue", 125, 4, 0, 0, [EffetEtat(EtatBoostCaracFixe("Acuité Absolue", 0, 1, "checkLdv", False))], [
    #     ], 0, 1, 1, 3, 0, "cercle", False, description="""Tous les sorts du Crâ peuvent être lancés au travers des obstacles pendant 1 tour.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche d'Expiation", 13, 4, 6, 10, [EffetDegats(19, 21, "Eau"), EffetEtatSelf(EtatBoostBaseDeg("Flèche d'Expiation", 0, -1, "Flèche d'Expiation", 22))], [EffetDegats(25, 27, "Eau"), EffetEtatSelf(
    #         EtatBoostBaseDeg("Flèche d'Expiation", 0, -1, "Flèche d'Expiation", 28))], 25, 1, 1, 3, 1, "cercle", True, description="""Occasionne des dommages Eau, augmente les dommages du sort tous les 3 tours.""", chaine=False),

    #     Sort.Sort("Flèche d'Expiation", 54, 4, 6, 10, [EffetDegats(27, 29, "Eau"), EffetEtatSelf(EtatBoostBaseDeg("Flèche d'Expiation", 0, -1, "Flèche d'Expiation", 30))], [EffetDegats(33, 35, "Eau"), EffetEtatSelf(
    #         EtatBoostBaseDeg("Flèche d'Expiation", 0, -1, "Flèche d'Expiation", 36))], 25, 1, 1, 3, 1, "cercle", True, description="""Occasionne des dommages Eau, augmente les dommages du sort tous les 3 tours.""", chaine=False),

    #     Sort.Sort("Flèche d'Expiation", 94, 4, 6, 10, [EffetDegats(35, 37, "Eau"), EffetEtatSelf(EtatBoostBaseDeg("Flèche d'Expiation", 0, -1, "Flèche d'Expiation", 36))], [EffetDegats(41, 43, "Eau"), EffetEtatSelf(
    #         EtatBoostBaseDeg("Flèche d'Expiation", 0, -1, "Flèche d'Expiation", 42))], 25, 1, 1, 3, 1, "cercle", True, description="""Occasionne des dommages Eau, augmente les dommages du sort tous les 3 tours.""", chaine=False)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche de Rédemption", 130, 3, 6, 8, [EffetDegats(19, 22, "Eau"), EffetEtatSelf(EtatBoostBaseDeg("Flèche de rédemption", 1, 1, "Flèche de Rédemption", 12))], [EffetDegats(23, 26, "Eau"), EffetEtatSelf(
    #         EtatBoostBaseDeg("Flèche de rédemption", 1, 1, "Flèche de Rédemption", 12))], 25, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau qui sont augmentés si le sort est relancé le tour suivant.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Oeil de Taupe", 17, 3, 5, 6, [EffetEtat(EtatBoostCaracFixe("Oeil de taupe", 0, 3, "PO", -2), zone=Zones.TypeZoneCercle(2), cible_non_requise=True), EffetVolDeVie(8, 10, "Eau", zone=Zones.TypeZoneCercle(2), cible_non_requise=True), EffetDevoilePiege(zone=Zones.TypeZoneCercle(2), cible_non_requise=True)], [EffetEtat(EtatBoostCaracFixe("Oeil de taupe", 0, 3, "PO", -2), cible_non_requise=True,
    #                                                                                                                                                                                                                                                                                                                                            zone=Zones.TypeZoneCercle(2)), EffetVolDeVie(11, 13, "Eau", cible_non_requise=True, zone=Zones.TypeZoneCercle(2)), EffetDevoilePiege(zone=Zones.TypeZoneCercle(2), cible_non_requise=True)], 25, 1, 1, 4, 1, "cercle", True, description="""Réduit la portée des personnages ciblés, vole de la vie dans l'élément Eau et repére les objets invisibles dans sa zone d'effet.""", chaine=True),

    #     Sort.Sort("Oeil de Taupe", 58, 3, 5, 8, [EffetEtat(EtatBoostCaracFixe("Oeil de taupe", 0, 3, "PO", -4), zone=Zones.TypeZoneCercle(2), cible_non_requise=True), EffetVolDeVie(12, 14, "Eau", zone=Zones.TypeZoneCercle(2), cible_non_requise=True), EffetDevoilePiege(zone=Zones.TypeZoneCercle(2), cible_non_requise=True)], [EffetEtat(EtatBoostCaracFixe("Oeil de taupe", 0, 3, "PO", -4), cible_non_requise=True,
    #                                                                                                                                                                                                                                                                                                                                             zone=Zones.TypeZoneCercle(2)), EffetVolDeVie(15, 17, "Eau", cible_non_requise=True, zone=Zones.TypeZoneCercle(2)), EffetDevoilePiege(zone=Zones.TypeZoneCercle(2), cible_non_requise=True)], 25, 1, 1, 4, 1, "cercle", True, description="""Réduit la portée des personnages ciblés, vole de la vie dans l'élément Eau et repére les objets invisibles dans sa zone d'effet.""", chaine=True),

    #     Sort.Sort("Oeil de Taupe", 102, 3, 5, 10, [EffetEtat(EtatBoostCaracFixe("Oeil de taupe", 1, 3, "PO", -6), zone=Zones.TypeZoneCercle(3), cible_non_requise=True), EffetVolDeVie(16, 18, "Eau", zone=Zones.TypeZoneCercle(3), cible_non_requise=True), EffetDevoilePiege(zone=Zones.TypeZoneCercle(3), cible_non_requise=True)], [EffetEtat(EtatBoostCaracFixe("Oeil de taupe", 0, 3, "PO", -6), cible_non_requise=True,
    #                                                                                                                                                                                                                                                                                                                                               zone=Zones.TypeZoneCercle(3)), EffetVolDeVie(19, 21, "Eau", cible_non_requise=True, zone=Zones.TypeZoneCercle(3)), EffetDevoilePiege(zone=Zones.TypeZoneCercle(3), cible_non_requise=True)], 25, 1, 1, 4, 1, "cercle", True, description="""Réduit la portée des personnages ciblés, vole de la vie dans l'élément Eau et repére les objets invisibles dans sa zone d'effet.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche écrasante", 135, 3, 5, 7, [EffetEtat(Etat("Pesanteur", 0, 1), cible_non_requise=True, zone=Zones.TypeZoneCroixDiagonale(1)), EffetDegats(34, 38, "Feu", cible_non_requise=True, zone=Zones.TypeZoneCroixDiagonale(1))], [EffetEtat(Etat(
    #         "Pesanteur", 1, 1), cible_non_requise=True, zone=Zones.TypeZoneCroixDiagonale(1)), EffetDegats(37, 41, "Feu", cible_non_requise=True, zone=Zones.TypeZoneCroixDiagonale(1))], 25, 1, 1, 3, 1, "cercle", True, description="""Occasionne des dommages Feu et applique l'état Pesanteur.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Tir Critique", 22, 2, 0, 2, [EffetEtat(EtatBoostCaracFixe("Tir Critique", 0, 4, "cc", 10))], [EffetEtat(EtatBoostCaracFixe("Tir Critique", 0, 4, "cc", 10)), EffetEtat(
    #         EtatBoostCaracFixe("Tir Critique Critique", 0, 4, "pui", 10))], 25, 1, 1, 5, 1, "cercle", True, description="""Augmente la probabilité de faire un coup critique.""", chaine=True),

    #     Sort.Sort("Tir Critique", 65, 2, 0, 4, [EffetEtat(EtatBoostCaracFixe("Tir Critique", 0, 4, "cc", 12))], [EffetEtat(EtatBoostCaracFixe("Tir Critique", 0, 4, "cc", 12)), EffetEtat(
    #         EtatBoostCaracFixe("Tir Critique Critique", 0, 4, "pui", 30))], 25, 1, 1, 5, 1, "cercle", True, description="""Augmente la probabilité de faire un coup critique.""", chaine=True),

    #     Sort.Sort("Tir Critique", 108, 2, 0, 6, [EffetEtat(EtatBoostCaracFixe("Tir Critique", 0, 4, "cc", 14))], [EffetEtat(EtatBoostCaracFixe("Tir Critique", 0, 4, "cc", 14)), EffetEtat(
    #         EtatBoostCaracFixe("Tir Critique Critique", 0, 4, "pui", 50))], 25, 1, 1, 5, 1, "cercle", True, description="""Augmente la probabilité de faire un coup critique.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Balise de Rappel", 140, 2, 1, 5, [EffetInvoque("Balise de Rappel", True, cibles_possibles="", cible_non_requise=True)], [
    #     ], 0, 1, 1, 2, 0, "cercle", True, description="""Invoque une balise qui échange sa position avec celle du lanceur (au début du prochain tour).""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche d'Immobilisation", 27, 2, 1, 6, [EffetDegats(6, 7, "Eau"), EffetEtat(EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", -1)), EffetEtatSelf(EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", 1))], [EffetDegats(7, 8, "Eau"), EffetEtat(
    #         EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", -1)), EffetEtatSelf(EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", 1))], 5, 4, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau et vole des PM é la cible.""", chaine=True),

    #     Sort.Sort("Flèche d'Immobilisation", 72, 2, 1, 8, [EffetDegats(8, 9, "Eau"), EffetEtat(EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", -1)), EffetEtatSelf(EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", 1))], [EffetDegats(9, 10, "Eau"), EffetEtat(
    #         EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", -1)), EffetEtatSelf(EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", 1))], 5, 4, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau et vole des PM é la cible.""", chaine=True),

    #     Sort.Sort("Flèche d'Immobilisation", 118, 2, 1, 10, [EffetDegats(10, 11, "Eau"), EffetEtat(EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", -1)), EffetEtatSelf(EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", 1))], [EffetDegats(12, 13, "Eau"), EffetEtat(
    #         EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", -1)), EffetEtatSelf(EtatBoostCaracFixe("Flèche d'Immobilisation", 0, 1, "PM", 1))], 5, 4, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau et vole des PM é la cible.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Assaillante", 145, 4, 2, 6, [EffetDegats(33, 37, "Eau", zone=Zones.TypeZoneCroix(1)), EffetEtatSelf(EtatBoostCaracFixe("Assaillante", 0, 1, "pui", 100), zone=Zones.TypeZoneCroix(1))], [EffetDegats(36, 40, "Eau", zone=Zones.TypeZoneCroix(1)), EffetEtatSelf(EtatBoostCaracFixe("Assaillante", 0, 1, "pui", 100), zone=Zones.TypeZoneCroix(1))], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau en zone.
    # Pour chaque entité comprise dans la zone d'effet, le lanceur gagne 100 Puissance pendant 1 tour.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Punitive", 32, 4, 6, 8, [EffetDegats(19, 21, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Flèche Punitive", 0, -1, "Flèche Punitive", 20))], [EffetDegats(23, 25, "Terre"), EffetEtatSelf(
    #         EtatBoostBaseDeg("Flèche Punitive", 0, -1, "Flèche Punitive", 24))], 25, 1, 1, 2, 1, "cercle", True, description="""Occasionne des dommages Terre et augmente les dommages du sort tous les 2 tours.""", chaine=True),

    #     Sort.Sort("Flèche Punitive", 81, 4, 6, 8, [EffetDegats(24, 26, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Flèche Punitive", 0, -1, "Flèche Punitive", 25))], [EffetDegats(28, 30, "Terre"), EffetEtatSelf(
    #         EtatBoostBaseDeg("Flèche Punitive", 0, -1, "Flèche Punitive", 29))], 25, 1, 1, 2, 1, "cercle", True, description="""Occasionne des dommages Terre et augmente les dommages du sort tous les 2 tours.""", chaine=True),

    #     Sort.Sort("Flèche Punitive", 124, 4, 6, 8, [EffetDegats(29, 31, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Flèche Punitive", 0, -1, "Flèche Punitive", 30))], [EffetDegats(35, 37, "Terre"), EffetEtatSelf(
    #         EtatBoostBaseDeg("Flèche Punitive", 0, -1, "Flèche Punitive", 36))], 25, 1, 1, 2, 1, "cercle", True, description="""Occasionne des dommages Terre et augmente les dommages du sort tous les 2 tours.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche du Jugement", 150, 3, 5, 9, [EffetDegatsSelonPMUtilises(39, 45, "Terre")], [EffetDegatsSelonPMUtilises(47, 53, "Terre")], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Terre.
    # Moins le lanceur a utilisé de PM pendant son tour de jeu, plus les dommages occasionnés sont importants.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Tir Puissant", 38, 3, 0, 2, [EffetEtat(EtatBoostCaracFixe("Tir Puissant", 0, 3, "pui", 150))], [EffetEtat(EtatBoostCaracFixe(
    #         "Tir Puissant", 0, 3, "pui", 170))], 25, 1, 1, 6, 1, "cercle", True, description="""Augmente les dommages des sorts.""", chaine=True),

    #     Sort.Sort("Tir Puissant", 90, 3, 0, 4, [EffetEtat(EtatBoostCaracFixe("Tir Puissant", 0, 3, "pui", 200))], [EffetEtat(EtatBoostCaracFixe(
    #         "Tir Puissant", 0, 3, "pui", 230))], 25, 1, 1, 6, 1, "cercle", True, description="""Augmente les dommages des sorts.""", chaine=True),

    #     Sort.Sort("Tir Puissant", 132, 3, 0, 6, [EffetEtat(EtatBoostCaracFixe("Tir Puissant", 0, 3, "pui", 250))], [EffetEtat(EtatBoostCaracFixe(
    #         "Tir Puissant", 0, 3, "pui", 290))], 25, 1, 1, 6, 1, "cercle", True, description="""Augmente les dommages des sorts.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Balise Tactique", 155, 1, 1, 10, [EffetTue(cibles_possibles="Balise Tactique", zone=Zones.TypeZoneInfini()), EffetInvoque("Balise Tactique", True, cibles_possibles="", cible_non_requise=True), EffetEtat(EtatModDegPer("Balise Tactique", 0, -1, 50, "Allies"))], [], 0, 1, 1, 2, 1, "cercle", True, description="""Invoque une Balise qui peut servir d'obstacle et de cible.
    # La Balise subit 2 fois moins de dommages des alliés.""", chaine=False)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Harcelante", 44, 3, 1, 5, [EffetDegats(9, 11, "Air")], [EffetDegats(
    #         11, 13, "Air")], 5, 4, 2, 0, 1, "cercle", False, description="""Occasionne des dommages Air sans ligne de vue.""", chaine=True),

    #     Sort.Sort("Flèche Harcelante", 97, 3, 1, 6, [EffetDegats(11, 13, "Air")], [EffetDegats(
    #         13, 15, "Air")], 5, 4, 2, 0, 1, "cercle", False, description="""Occasionne des dommages Air sans ligne de vue.""", chaine=True),

    #     Sort.Sort("Flèche Harcelante", 137, 3, 1, 7, [EffetDegats(13, 15, "Air")], [EffetDegats(
    #         16, 18, "Air")], 5, 4, 2, 0, 1, "cercle", False, description="""Occasionne des dommages Air sans ligne de vue.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Massacrante", 160, 4, 4, 8, [EffetDegats(34, 38, "Air"), EffetEtatSelf(EtatBoostBaseDeg("Flèche massacrante", 1, 1, "Flèche Massacrante", 18))], [EffetDegats(41, 45, "Air"), EffetEtatSelf(EtatBoostBaseDeg("Fleche_massacrante", 1, 1, "Flèche Massacrante", 21))], 5, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air.
    # Les dommages du sort sont augmentés au tour suivant.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Empoisonnée", 50, 3, 1, 6, [EffetRetPM(2), EffetEtat(EtatEffetDebutTour("Flèche Empoisonnée", 0, 2, EffetDegats(11, 12, "Neutre"), "Flèche Empoisonnée", "lanceur"))], [EffetRetPM(2), EffetEtat(EtatEffetDebutTour(
    #         "Flèche Empoisonnée", 0, 2, EffetDegats(14, 15, "Neutre"), "Flèche Empoisonnée", "lanceur"))], 5, 4, 1, 0, 1, "cercle", True, description="""Occasionne des dommages Neutre sur plusieurs tours et retire des PM.""", chaine=True),

    #     Sort.Sort("Flèche Empoisonnée", 103, 3, 1, 8, [EffetRetPM(2), EffetEtat(EtatEffetDebutTour("Flèche Empoisonnée", 0, 2, EffetDegats(14, 15, "Neutre"), "Flèche Empoisonnée", "lanceur"))], [EffetRetPM(2), EffetEtat(EtatEffetDebutTour(
    #         "Flèche Empoisonnée", 0, 2, EffetDegats(17, 18, "Neutre"), "Flèche Empoisonnée", "lanceur"))], 5, 4, 1, 0, 1, "cercle", True, description="""Occasionne des dommages Neutre sur plusieurs tours et retire des PM.""", chaine=True),

    #     Sort.Sort("Flèche Empoisonnée", 143, 3, 1, 10, [EffetRetPM(3), EffetEtat(EtatEffetDebutTour("Flèche Empoisonnée", 0, 2, EffetDegats(17, 18, "Neutre"), "Flèche Empoisonnée", "lanceur"))], [EffetRetPM(3), EffetEtat(EtatEffetDebutTour(
    #         "Flèche Empoisonnée", 0, 2, EffetDegats(21, 22, "Neutre"), "Flèche Empoisonnée", "lanceur"))], 5, 4, 1, 0, 1, "cercle", True, description="""Occasionne des dommages Neutre sur plusieurs tours et retire des PM.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Curative", 165, 3, 3, 6, [EffetSoinPerPVMax(10), EffetEtat(EtatModSoinPer("Flèche Curative", 1, 1, 130))], [EffetSoinPerPVMax(12), EffetEtat(
    #         EtatModSoinPer("Flèche Curative", 1, 1, 130))], 15, 3, 1, 0, 1, "ligne", True, description="""Soigne et augmente les soins reéus par la cible.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Persécutrice", 56, 3, 5, 8, [EffetDegats(7, 9, "Feu"), EffetDegats(7, 9, "Air")], [EffetDegats(10, 12, "Feu"), EffetDegats(
    #         10, 12, "Air")], 5, 99, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air et Feu.""", chaine=True),

    #     Sort.Sort("Flèche Persécutrice", 112, 3, 5, 8, [EffetDegats(9, 11, "Feu"), EffetDegats(9, 11, "Air")], [EffetDegats(12, 14, "Feu"), EffetDegats(
    #         12, 14, "Air")], 5, 99, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air et Feu.""", chaine=True),

    #     Sort.Sort("Flèche Persécutrice", 147, 3, 5, 8, [EffetDegats(11, 13, "Feu"), EffetDegats(11, 13, "Air")], [EffetDegats(
    #         13, 15, "Feu"), EffetDegats(13, 15, "Air")], 5, 99, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Air et Feu.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Tyrannique", 170, 4, 2, 7, [EffetEtat(EtatEffetSiPousse("Flèche tyrannique air", 0, 2, EffetDegats(15, 15, "Air"), "Flèche tyrannique", "lanceur")), EffetEtat(EtatEffetSiSubit("Flèche tyrannique feu", 0, 2, EffetDegats(15, 15, "Feu"), "Flèche tyrannique", "lanceur", "cible", "doPou"))], [], 0, 3, 1, 0, 1, "ligne", True, description="""Occasionne des dommages Air si la cible est poussée.
    # Occasionne des dommages Feu si la cible subit des dommages de poussée.
    # Les dommages de chaque élément peuvent être déclenchés 3 fois par tour.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Destructrice", 62, 4, 5, 8, [EffetDegats(20, 22, "Terre"), EffetEtat(EtatBoostCaracFixe("Flèche Destructrice", 0, 1, "do", -20))], [EffetDegats(24, 26, "Terre"), EffetEtat(
    #         EtatBoostCaracFixe("Flèche Destructrice", 0, 1, "do", -22))], 15, 99, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Terre et réduit les dommages occasionnés par la cible.""", chaine=True),

    #     Sort.Sort("Flèche Destructrice", 116, 4, 5, 8, [EffetDegats(25, 27, "Terre"), EffetEtat(EtatBoostCaracFixe("Flèche Destructrice", 0, 1, "do", -40))], [EffetDegats(29, 31, "Terre"), EffetEtat(
    #         EtatBoostCaracFixe("Flèche Destructrice", 0, 1, "do", -44))], 15, 99, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Terre et réduit les dommages occasionnés par la cible.""", chaine=True),

    #     Sort.Sort("Flèche Destructrice", 153, 4, 5, 8, [EffetDegats(30, 32, "Terre"), EffetEtat(EtatBoostCaracFixe("Flèche Destructrice", 0, 1, "do", -60))], [EffetDegats(34, 36, "Terre"), EffetEtat(
    #         EtatBoostCaracFixe("Flèche Destructrice", 0, 1, "do", -66))], 15, 99, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Terre et réduit les dommages occasionnés par la cible.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Tir de Barrage", 175, 4, 4, 8, [EffetDegats(29, 33, "Terre"), EffetPousser(2)], [EffetDegats(35, 39, "Terre"), EffetPousser(
    #         2)], 25, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Terre et repousse la cible.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Absorbante", 69, 4, 6, 8, [EffetVolDeVie(19, 21, "Air")], [EffetVolDeVie(
    #         23, 25, "Air")], 15, 3, 2, 0, 1, "cercle", True, description="""Vole de la vie dans l'élément Air.""", chaine=True),

    #     Sort.Sort("Flèche Absorbante", 122, 4, 6, 8, [EffetVolDeVie(24, 26, "Air")], [EffetVolDeVie(
    #         28, 30, "Air")], 15, 3, 2, 0, 1, "cercle", True, description="""Vole de la vie dans l'élément Air.""", chaine=True),

    #     Sort.Sort("Flèche Absorbante", 162, 4, 6, 8, [EffetVolDeVie(29, 31, "Air")], [EffetVolDeVie(
    #         33, 35, "Air")], 15, 3, 2, 0, 1, "cercle", True, description="""Vole de la vie dans l'élément Air.""", chaine=True)
    # ]))

    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Dévorante", 180, 3, 1, 6, [
    #         EffetDegats(70, 74, "Air", zone=Zones.TypeZoneInfini(), etat_requis="!Flèche dévorante lancer 3|!Flèche dévorante lancer 2|!Flèche dévorante lancer 1",
    #                     etat_requis_cibles="Flèche dévorante lancer 3", consomme_etat=True, pile=False),
    #         EffetDegats(52, 56, "Air", zone=Zones.TypeZoneInfini(), etat_requis="!Flèche dévorante lancer 3|!Flèche dévorante lancer 2|!Flèche dévorante lancer 1",
    #                     etat_requis_cibles="Flèche dévorante lancer 2", consomme_etat=True, pile=False),
    #         EffetDegats(34, 38, "Air", zone=Zones.TypeZoneInfini(), etat_requis="!Flèche dévorante lancer 3|!Flèche dévorante lancer 2|!Flèche dévorante lancer 1",
    #                     etat_requis_cibles="Flèche dévorante lancer 1", consomme_etat=True, pile=False),
    #         EffetEtat(Etat("Flèche dévorante lancer 3", 0, -1),
    #                   etat_requis="Flèche dévorante lancer 2", consomme_etat=True, pile=False),
    #         EffetEtat(Etat("Flèche dévorante lancer 2", 0, -1),
    #                   etat_requis="Flèche dévorante lancer 1", consomme_etat=True, pile=False),
    #         EffetEtat(Etat("Flèche dévorante lancer 1", 0, -1),
    #                   etat_requis="!Flèche dévorante lancer 3|!Flèche dévorante lancer 2|!Flèche dévorante lancer 1", consomme_etat=True, pile=False),
    #         ],
    #               [
    #                   EffetDegats(81, 85, "Air", zone=Zones.TypeZoneInfini(), etat_requis="!Flèche dévorante lancer 3|!Flèche dévorante lancer 2|!Flèche dévorante lancer 1",
    #                               etat_requis_cibles="Flèche dévorante lancer 3", consomme_etat=True, pile=False),
    #                   EffetDegats(60, 64, "Air", zone=Zones.TypeZoneInfini(), etat_requis="!Flèche dévorante lancer 3|!Flèche dévorante lancer 2|!Flèche dévorante lancer 1",
    #                               etat_requis_cibles="Flèche dévorante lancer 2", consomme_etat=True, pile=False),
    #                   EffetDegats(39, 43, "Air", zone=Zones.TypeZoneInfini(), etat_requis="!Flèche dévorante lancer 3|!Flèche dévorante lancer 2|!Flèche dévorante lancer 1",
    #                               etat_requis_cibles="Flèche dévorante lancer 1", consomme_etat=True, pile=False),
    #                   EffetEtat(Etat("Flèche dévorante lancer 3", 0, -1),
    #                             etat_requis="Flèche dévorante lancer 2", consomme_etat=True, pile=False),
    #                   EffetEtat(Etat("Flèche dévorante lancer 2", 0, -1),
    #                             etat_requis="Flèche dévorante lancer 1", consomme_etat=True, pile=False),
    #                   EffetEtat(Etat("Flèche dévorante lancer 1", 0, -1),
    #                             etat_requis="!Flèche dévorante lancer 3|!Flèche dévorante lancer 2|!Flèche dévorante lancer 1", consomme_etat=True, pile=False)],
    #               15, 2, 1, 0, 1, "cercle", True, description="""Occasionne des dommages Air.
    # Les dommages sont appliqués lorsque le sort est lancé sur une autre cible.
    # Peut se cumuler 3 fois sur une même cible.""", chaine=False)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Cinglante", 77, 2, 1, 5, [EffetEtat(EtatBoostCaracFixe("Fleche cinglante", 0, 2, "erosion", 10)), EffetPousser(
    #         2)], [], 0, 4, 2, 0, 1, "ligne", True, description="""Applique de l'érosion aux ennemis et repousse de 2 cases.""", chaine=True),

    #     Sort.Sort("Flèche Cinglante", 128, 2, 1, 7, [EffetEtat(EtatBoostCaracFixe("Fleche cinglante", 0, 2, "erosion", 10)), EffetPousser(
    #         2)], [], 0, 4, 2, 0, 1, "ligne", True, description="""Applique de l'érosion aux ennemis et repousse de 2 cases.""", chaine=True),

    #     Sort.Sort("Flèche Cinglante", 172, 2, 1, 9, [EffetEtat(EtatBoostCaracFixe("Fleche cinglante", 0, 2, "erosion", 10)), EffetPousser(
    #         2)], [], 0, 4, 2, 0, 1, "ligne", True, description="""Applique de l'érosion aux ennemis et repousse de 2 cases.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche de Repli", 185, 1, 2, 7, [EffetPousser(2, source="CaseCible", cible="Lanceur")], [
    #     ], 0, 3, 2, 0, 1, "ligne", True, description="""Le lanceur du sort recule de 2 cases.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Fèche Ralentissante", 84, 4, 1, 8, [EffetRetPA(2, zone=Zones.TypeZoneCercle(2)), EffetDegats(26, 28, "Eau", zone=Zones.TypeZoneCercle(2))], [EffetRetPA(2, zone=Zones.TypeZoneCercle(
    #         2)), EffetDegats(32, 34, "Eau", zone=Zones.TypeZoneCercle(2))], 15, 2, 1, 0, 1, "ligne", True, description="""Occasionne des dommages Eau et retire des PA en zone.""", chaine=True),

    #     Sort.Sort("Flèche Ralentissante", 134, 4, 1, 8, [EffetRetPA(2, zone=Zones.TypeZoneCercle(2)), EffetDegats(31, 33, "Eau", zone=Zones.TypeZoneCercle(2))], [EffetRetPA(2, zone=Zones.TypeZoneCercle(
    #         2)), EffetDegats(37, 39, "Eau", zone=Zones.TypeZoneCercle(2))], 15, 2, 1, 0, 1, "ligne", True, description="""Occasionne des dommages Eau et retire des PA en zone.""", chaine=True),

    #     Sort.Sort("Flèche Ralentissante", 178, 4, 1, 8, [EffetRetPA(3, zone=Zones.TypeZoneCercle(2)), EffetDegats(36, 38, "Eau", zone=Zones.TypeZoneCercle(2))], [EffetRetPA(3, zone=Zones.TypeZoneCercle(
    #         2)), EffetDegats(42, 44, "Eau", zone=Zones.TypeZoneCercle(2))], 15, 2, 1, 0, 1, "ligne", True, description="""Occasionne des dommages Eau et retire des PA en zone.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Percutante", 190, 2, 1, 6, [EffetDegats(6, 10, "Eau"), EffetEtat(EtatEffetFinTour("Flèche percutante à retardement", 0, 1, EffetDegats(6, 10, "eau", zone=Zones.TypeZoneCercleSansCentre(2)), "Flèche percutante à retardement", "lanceur")), EffetEtat(EtatEffetFinTour("Flèche percutante à retardement PA", 0, 1, EffetRetPA(2, zone=Zones.TypeZoneCercleSansCentre(2)), "Flèche percutante à retardement PA", "lanceur"))], [EffetDegats(9, 13, "Eau"), EffetEtat(EtatEffetFinTour("Flèche percutante à retardement", 0, 1, EffetDegats(9, 13, "eau", zone=Zones.TypeZoneCercleSansCentre(2)), "Flèche percutante à retardement", "lanceur")), EffetEtat(EtatEffetFinTour("Flèche percutante à retardement PA", 0, 1, EffetRetPA(2, zone=Zones.TypeZoneCercleSansCentre(2)), "Flèche percutante à retardement PA", "lanceur"))], 5, 4, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau.
    # à la fin de son tour, la cible occasionne des dommages Eau et retire des PA en cercle de taille 2 autour d'elle.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Flèche Explosive", 92, 4, 1, 8, [EffetDegats(22, 26, "Feu", zone=Zones.TypeZoneCercle(2))], [EffetDegats(
    #         27, 31, "Feu", zone=Zones.TypeZoneCercle(2))], 25, 2, 1, 0, 1, "cercle", True, description="""Occasionne des dommages Feu en zone.""", chaine=True),

    #     Sort.Sort("Flèche Explosive", 141, 4, 1, 8, [EffetDegats(26, 30, "Feu", zone=Zones.TypeZoneCercle(2))], [EffetDegats(
    #         31, 35, "Feu", zone=Zones.TypeZoneCercle(2))], 25, 2, 1, 0, 1, "cercle", True, description="""Occasionne des dommages Feu en zone.""", chaine=True),

    #     Sort.Sort("Flèche Explosive", 187, 4, 1, 8, [EffetDegats(30, 34, "Feu", zone=Zones.TypeZoneCercle(3))], [EffetDegats(
    #         35, 39, "Feu", zone=Zones.TypeZoneCercle(3))], 25, 2, 1, 0, 1, "cercle", True, description="""Occasionne des dommages Feu en zone.""", chaine=True)
    # ]))
    # flecheFulminante = Sort.Sort("Flèche Fulminante", 195, 4, 1, 8, [EffetDegats(38, 42, "Feu", cibles_possibles="Ennemis|Balise Tactique", pile=False), EffetEtatSelf(EtatBoostBaseDeg("Flèche Fulminante boost", 0, 1, "Flèche Fulminante", 10), pile=False), EffetPropage(2, cibles_possibles="Ennemis|Balise Tactique", pile=False)], [], 0, 1, 1, 0, 1, "cercle", True, description="Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
    # # flecheFulminanteRebond = Sort.Sort("Flèche Fulminante Rebond", 195, 0, 0, 99, [EffetDegats(38, 42, "Feu", cibles_possibles="Ennemis|Balise Tactique"), EffetEtatSelf(EtatBoostBaseDeg("Flèche Fulminante boost", 0, 1, "Flèche Fulminante Rebond", 10))], [
    # # ], 0, 9, 1, 0, 0, "cercle", True, description="Occasionne des dommages Feu. Se propage sur l'ennemi le plus proche dans un rayon de 2 cellules. Peut rebondir sur la Balise Tactique. À chaque cible supplémentaire, les dommages du sort sont augmentés.")
    # #flecheFulminante.effets.append(EffetPropage(flecheFulminanteRebond, Zones.TypeZoneCercle(
    # #    2), cibles_possibles="Ennemis|Balise Tactique"))
    # #flecheFulminanteRebond.effets.append(EffetPropage(
    # #    flecheFulminanteRebond, Zones.TypeZoneCercle(2), cibles_possibles="Ennemis|Balise Tactique"))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [flecheFulminante]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Maîtrise de l'Arc", 100, 2, 0, 2, [EffetEtat(EtatBoostCaracFixe("Maitrise de l'arc", 0, 3, "do", 40))], [EffetEtat(
    #         EtatBoostCaracFixe("Maitrise de l'arc", 0, 3, "do", 50))], 25, 1, 1, 5, 1, "cercle", False, description="""Augmente les dommages.""", chaine=True),

    #     Sort.Sort("Maîtrise de l'Arc", 149, 2, 0, 4, [EffetEtat(EtatBoostCaracFixe("Maitrise de l'arc", 0, 3, "do", 50))], [EffetEtat(
    #         EtatBoostCaracFixe("Maitrise de l'arc", 0, 3, "do", 60))], 25, 1, 1, 5, 1, "cercle", False, description="""Augmente les dommages.""", chaine=True),

    #     Sort.Sort("Maîtrise de l'Arc", 197, 2, 0, 6, [EffetEtat(EtatBoostCaracFixe("Maitrise de l'arc", 0, 3, "do", 60))], [EffetEtat(
    #         EtatBoostCaracFixe("Maitrise de l'arc", 0, 3, "do", 70))], 25, 1, 1, 5, 1, "cercle", False, description="""Augmente les dommages.""", chaine=True)
    # ]))
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Sentinelle", 200, 3, 0, 0, [EffetEtatSelf(EtatBoostCaracFixe("Sentinelle", 1, 1, "PM", -100)), EffetEtatSelf(EtatBoostSortsPer("Sentinelle", 1, 1, 30))], [
    #     ], 0, 1, 1, 3, 0, "cercle", False, description="""Le lanceur perd tous ses PM mais gagne un bonus de dommages pour le tour en cours.""", chaine=True)
    # ]))
    return sorts
