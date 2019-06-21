"""@summary: Rassemble les sorts du Iop
"""
# pylint: disable=line-too-long
import Sort
from Effets.EffetDegats import EffetDegats, EffetDegatsSelonPMUtilises
from Effets.EffetEtat import EffetEtat, EffetEtatSelf
from Effets.EffetInvoque import EffetInvoque
from Effets.EffetPousser import EffetAttire, EffetPousser
from Effets.EffetTp import EffetTp
from Effets.EffetRet import EffetRetPM
import Zones
from Etats.EtatBoostCarac import EtatBoostCaracFixe
from Etats.EtatModDeg import EtatModDegPer
from Etats.Etat import Etat
from Etats.EtatBouclier import EtatBouclierPerLvl
from Etats.EtatLanceSort import EtatLanceSortSiSubit
from Etats.EtatBoostBaseDeg import EtatBoostBaseDeg
from Etats.EtatBoostCarac import EtatBoostCaracPer
from Etats.EtatEffet import EtatEffetFinTour
from Etats.EtatRedistribuerPer import EtatRedistribuerPer
import Personnages


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
    activationRassemblement = Sort.Sort("Déclenche Rassemblement", 0, 0, 0, 0, [EffetAttire(
        2, zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies")], [], 0, 99, 99, 0, 0, "cercle", False)
    activationFriction = Sort.Sort("Frikt", 0, 0, 0, 0, [EffetAttire(1, "Lanceur", "JoueurCaseEffet", zone=Zones.TypeZoneCroix(
        99), etat_requis_cibles="Frikt")], [], 0, 99, 99, 0, 0, "cercle", False)
    activationCoupPourCoup = Sort.Sort("Déclenche Coup pour Coup", 0, 0, 0, 0, [EffetPousser(
        2, zone=Zones.TypeZoneCroix(99), etat_requis_cibles="Coup pour coup")], [], 0, 99, 99, 0, 0, "cercle", False)
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Pression", 1, 3, 1, 3, [EffetEtat(EtatBoostCaracFixe("Pression", 0, 2, "erosion", 10), cibles_possibles="Ennemis"), EffetDegats(14, 18, "Terre")], [EffetEtat(EtatBoostCaracFixe(
            "Pression", 0, 2, "erosion", 10), cibles_possibles="Ennemis"), EffetDegats(19, 23, "Terre")], 5, 99, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Terre et applique un malus d'érosion.""", chaine=True),
        Sort.Sort("Pression", 30, 3, 1, 3, [EffetEtat(EtatBoostCaracFixe("Pression", 0, 2, "erosion", 10), cibles_possibles="Ennemis"), EffetDegats(19, 23, "Terre")], [EffetEtat(EtatBoostCaracFixe(
            "Pression", 0, 2, "erosion", 10), cibles_possibles="Ennemis"), EffetDegats(24, 28, "Terre")], 5, 99, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Terre et applique un malus d'érosion.""", chaine=True),
        Sort.Sort("Pression", 60, 3, 1, 3, [EffetEtat(EtatBoostCaracFixe("Pression", 0, 2, "erosion", 10), cibles_possibles="Ennemis"), EffetDegats(24, 28, "Terre")], [EffetEtat(EtatBoostCaracFixe(
            "Pression", 0, 2, "erosion", 10), cibles_possibles="Ennemis"), EffetDegats(29, 33, "Terre")], 5, 99, 3, 0, 0, "cercle", True, description="""Occasionne des dommages Terre et applique un malus d'érosion.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Tannée", 110, 4, 1, 7, [EffetDegats(30, 34, "Air", zone=Zones.TypeZoneLignePerpendiculaire(1)), EffetRetPM(3, zone=Zones.TypeZoneLignePerpendiculaire(1))], [EffetDegats(
            36, 40, "Air", zone=Zones.TypeZoneLignePerpendiculaire(1)), EffetRetPM(3, zone=Zones.TypeZoneLignePerpendiculaire(1))], 5, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Air en zone et retire des PM.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Bond", 1, 5, 1, 5, [EffetTp(cibles_possibles="", cible_non_requise=True), EffetEtat(EtatModDegPer("Bond", 0, 1, 115), zone=Zones.TypeZoneCercle(1), cibles_possibles="Ennemis")], [EffetTp(cibles_possibles="", cible_non_requise=True), EffetEtat(EtatModDegPer("Bond", 0, 1, 118), zone=Zones.TypeZoneCercle(1), cibles_possibles="Ennemis")], 15, 1, 1, 2, 0, "cercle", False, description="""Téléporte sur la case ciblée.
    Augmente les dommages reçus par les ennemis situés sur les cases adjacentes.""", chaine=True),

        Sort.Sort("Bond", 20, 5, 1, 5, [EffetTp(cibles_possibles="", cible_non_requise=True), EffetEtat(EtatModDegPer("Bond", 0, 1, 115), zone=Zones.TypeZoneCercle(1), cibles_possibles="Ennemis")], [EffetTp(cibles_possibles="", cible_non_requise=True), EffetEtat(EtatModDegPer("Bond", 0, 1, 118), zone=Zones.TypeZoneCercle(1), cibles_possibles="Ennemis")], 15, 1, 1, 1, 0, "cercle", False, description="""Téléporte sur la case ciblée.
    Augmente les dommages reçus par les ennemis situés sur les cases adjacentes.""", chaine=True),

        Sort.Sort("Bond", 40, 5, 1, 6, [EffetTp(cibles_possibles="", cible_non_requise=True), EffetEtat(EtatModDegPer("Bond", 0, 1, 115), zone=Zones.TypeZoneCercle(1), cibles_possibles="Ennemis")], [EffetTp(cibles_possibles="", cible_non_requise=True), EffetEtat(EtatModDegPer("Bond", 0, 1, 118), zone=Zones.TypeZoneCercle(1), cibles_possibles="Ennemis")], 15, 1, 99, 0, 0, "cercle", False, description="""Téléporte sur la case ciblée.
    Augmente les dommages reçus par les ennemis situés sur les cases adjacentes.""", chaine=True)
    ]))

    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Détermination", 101, 2, 0, 0, [EffetEtat(Etat("Indeplacable", 0, 1)), EffetEtat(EtatModDegPer("Determination", 0, 1, 75))], [], 0, 1, 1, 2, 0, "cercle", False, description="""Fixe l'êtat Indéplaçable et réduit 25% des dommages subis pendant 1 tour.
    Ne peut pas être désenvoûté.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Intimidation", 1, 2, 1, 2, [EffetDegats(7, 9, "Neutre"), EffetPousser(2)], [EffetDegats(9, 11, "Neutre"), EffetPousser(
            2)], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Neutre sur les ennemis et repousse la cible.""", chaine=True),

        Sort.Sort("Intimidation", 25, 2, 1, 2, [EffetDegats(9, 11, "Neutre"), EffetPousser(3)], [EffetDegats(11, 13, "Neutre"), EffetPousser(
            3)], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Neutre sur les ennemis et repousse la cible.""", chaine=True),

        Sort.Sort("Intimidation", 52, 2, 1, 2, [EffetDegats(11, 13, "Neutre"), EffetPousser(3)], [EffetDegats(13, 15, "Neutre"), EffetPousser(
            3)], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Neutre sur les ennemis et repousse la cible.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Conquête", 105, 3, 1, 6, [EffetInvoque("Stratege Iop", True, cibles_possibles="", cible_non_requise=True), EffetEtat(EtatRedistribuerPer("Strategie iop", 0, -1, 50, "Ennemis|Allies", 2))], [
        ], 0, 1, 1, 3, 0, "cercle", True, description="""Invoque un épouvantail qui redistribue à proximité (2 cases) 50% des dommages de sort qu'il subit.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Déferlement", 3, 4, 0, 5, [EffetAttire(4, "JoueurCaseEffet", "Lanceur", cibles_exclues="Lanceur"), EffetDegats(24, 28, "Eau", cibles_exclues="Lanceur"), EffetEtatSelf(EtatBouclierPerLvl("Déferlement", 0, 1, 100))], [EffetAttire(4, "JoueurCaseEffet", "Lanceur", cibles_exclues="Lanceur"), EffetDegats(32, 36, "Eau", cibles_exclues="Lanceur"), EffetEtatSelf(EtatBouclierPerLvl("Déferlement", 0, 1, 100))], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Eau aux ennemis et rapproche le lanceur de la cible.
    Le lanceur gagne des points de bouclier.""", chaine=True),

        Sort.Sort("Déferlement", 35, 4, 0, 5, [EffetAttire(4, "JoueurCaseEffet", "Lanceur", cibles_exclues="Lanceur"), EffetDegats(31, 35, "Eau", cibles_exclues="Lanceur"), EffetEtatSelf(EtatBouclierPerLvl("Déferlement", 0, 1, 100))], [EffetAttire(4, "JoueurCaseEffet", "Lanceur", cibles_exclues="Lanceur"), EffetDegats(39, 43, "Eau", cibles_exclues="Lanceur"), EffetEtatSelf(EtatBouclierPerLvl("Déferlement", 0, 1, 100))], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Eau aux ennemis et rapproche le lanceur de la cible.
    Le lanceur gagne des points de bouclier.""", chaine=True),

        Sort.Sort("Déferlement", 67, 4, 0, 5, [EffetAttire(4, "JoueurCaseEffet", "Lanceur", cibles_exclues="Lanceur"), EffetDegats(38, 42, "Eau", cibles_exclues="Lanceur"), EffetEtatSelf(EtatBouclierPerLvl("Déferlement", 0, 1, 100))], [EffetAttire(4, "JoueurCaseEffet", "Lanceur", cibles_exclues="Lanceur"), EffetDegats(46, 50, "Eau", cibles_exclues="Lanceur"), EffetEtatSelf(EtatBouclierPerLvl("Déferlement", 0, 1, 100))], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Eau aux ennemis et rapproche le lanceur de la cible.
    Le lanceur gagne des points de bouclier.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Menace", 115, 3, 0, 3, [EffetDegats(26, 28, "Eau"), EffetAttire(2), EffetEtatSelf(EtatBouclierPerLvl("Menace", 0, 1, 100))], [EffetDegats(31, 33, "Eau"), EffetAttire(2), EffetEtatSelf(EtatBouclierPerLvl("Menace", 0, 1, 100))], 5, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Eau et attire la cible.
    Le lanceur gagne des points de bouclier.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Epée Divine", 6, 3, 0, 0, [EffetDegats(15, 17, "Air", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"), EffetEtat(EtatBoostCaracFixe("Epée Divine", 0, 4, "do", 10), zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")], [EffetDegats(24, 24, "Air", zone=Zones.TypeZoneCroix(
            3), cibles_possibles="Ennemis"), EffetEtat(EtatBoostCaracFixe("Epée Divine", 0, 4, "do", 13), zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")], 5, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Air et augmente les dommages des alliés ciblés.""", chaine=False),

        Sort.Sort("Epée Divine", 42, 3, 0, 0, [EffetDegats(18, 20, "Air", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"), EffetEtat(EtatBoostCaracFixe("Epée Divine", 0, 4, "do", 15), zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")], [EffetDegats(27, 27, "Air", zone=Zones.TypeZoneCroix(
            3), cibles_possibles="Ennemis"), EffetEtat(EtatBoostCaracFixe("Epée Divine", 0, 4, "do", 18), zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")], 5, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Air et augmente les dommages des alliés ciblés.""", chaine=False),

        Sort.Sort("Epée Divine", 74, 3, 0, 0, [EffetDegats(21, 23, "Air", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"), EffetEtat(EtatBoostCaracFixe("Epée Divine", 0, 4, "do", 20), zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")], [EffetDegats(30, 30, "Air", zone=Zones.TypeZoneCroix(
            3), cibles_possibles="Ennemis"), EffetEtat(EtatBoostCaracFixe("Epée Divine", 0, 4, "do", 23), zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Lanceur")], 5, 2, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Air et augmente les dommages des alliés ciblés.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Fendoir", 120, 5, 0, 4, [EffetDegats(47, 53, "Eau", zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis"), EffetEtatSelf(EtatBouclierPerLvl("Fendoir", 0, 1, 100), zone=Zones.TypeZoneCroix(1))], [EffetDegats(52, 58, "Eau", zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis"), EffetEtatSelf(EtatBouclierPerLvl("Fendoir", 0, 1, 100), zone=Zones.TypeZoneCroix(1))], 25, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Eau en zone.
    Applique des points de bouclier pour chaque ennemi touché.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Epée Destructrice", 9, 4, 1, 5, [EffetDegats(24, 28, "Feu", zone=Zones.TypeZoneLignePerpendiculaire(1), cible_non_requise=True), EffetAttire(2, zone=Zones.TypeZoneLignePerpendiculaire(1), cible_non_requise=True)], [EffetDegats(30, 34, "Feu", zone=Zones.TypeZoneLignePerpendiculaire(
            1), cible_non_requise=True), EffetAttire(2, zone=Zones.TypeZoneLignePerpendiculaire(1), cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Feu aux ennemis et attire les cibles vers le lanceur.""", chaine=False),

        Sort.Sort("Epée Destructrice", 47, 4, 1, 5, [EffetDegats(28, 32, "Feu", zone=Zones.TypeZoneLignePerpendiculaire(1), cible_non_requise=True), EffetAttire(2, zone=Zones.TypeZoneLignePerpendiculaire(1), cible_non_requise=True)], [EffetDegats(34, 38, "Feu", zone=Zones.TypeZoneLignePerpendiculaire(
            1), cible_non_requise=True), EffetAttire(2, zone=Zones.TypeZoneLignePerpendiculaire(1), cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Feu aux ennemis et attire les cibles vers le lanceur.""", chaine=False),

        Sort.Sort("Epée Destructrice", 87, 4, 1, 5, [EffetDegats(32, 36, "Feu", zone=Zones.TypeZoneLignePerpendiculaire(1), cible_non_requise=True), EffetAttire(2, zone=Zones.TypeZoneLignePerpendiculaire(1), cible_non_requise=True)], [EffetDegats(38, 42, "Feu", zone=Zones.TypeZoneLignePerpendiculaire(
            1), cible_non_requise=True), EffetAttire(2, zone=Zones.TypeZoneLignePerpendiculaire(1), cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Feu aux ennemis et attire les cibles vers le lanceur.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Anneau Destructeur", 125, 3, 0, 2, [EffetDegats(26, 30, "Air", zone=Zones.TypeZoneAnneau(3), cibles_possibles="Ennemis", cible_non_requise=True), EffetAttire(1, "CaseCible", zone=Zones.TypeZoneAnneau(3), cible_non_requise=True)], [EffetDegats(30, 34, "Air", zone=Zones.TypeZoneAnneau(
            3), cibles_possibles="Ennemis", cible_non_requise=True), EffetAttire(1, "CaseCible", zone=Zones.TypeZoneAnneau(3), cible_non_requise=True)], 15, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Air en anneau et attire les cibles.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Massacre", 13, 2, 1, 3, [EffetEtat(EtatRedistribuerPer("Massacre", 0, 2, 50, "Allies", 1))], [], 0, 1, 1, 3, 0, "cercle", True,
                  description="""Lorsque la cible ennemie reçoit des dommages de sorts, elle occasionne 50% de ces dommages aux ennemis au contact.""", chaine=True),

        Sort.Sort("Massacre", 54, 2, 1, 5, [EffetEtat(EtatRedistribuerPer("Massacre", 0, 2, 50, "Allies", 1))], [], 0, 1, 1, 3, 0, "cercle", True,
                  description="""Lorsque la cible ennemie reçoit des dommages de sorts, elle occasionne 50% de ces dommages aux ennemis au contact.""", chaine=True),

        Sort.Sort("Massacre", 94, 2, 1, 7, [EffetEtat(EtatRedistribuerPer("Massacre", 0, 2, 50, "Allies", 1))], [], 0, 1, 1, 3, 0, "cercle", True,
                  description="""Lorsque la cible ennemie reçoit des dommages de sorts, elle occasionne 50% de ces dommages aux ennemis au contact.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Rassemblement", 130, 2, 1, 6, [EffetAttire(2, source="CaseCible", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis"), EffetEtat(EtatLanceSortSiSubit("Rassemblement", 0, 1, activationRassemblement, "Porteur"), cibles_possibles="Ennemis")], [], 0, 1, 1, 2, 0, "cercle", True, description="""Rapproche les ennemis de la cible.
    Si la cible est un ennemi, elle attire ensuite ses alliés quand elle est attaquée pendant 1 tour.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Souffle", 17, 2, 2, 4, [EffetPousser(1, "CaseCible", zone=Zones.TypeZoneCroix(1), cible_non_requise=True)], [
        ], 0, 1, 1, 2, 0, "cercle", False, description="""Repousse les alliés et les ennemis situés autour de la cellule ciblée.""", chaine=True),

        Sort.Sort("Souffle", 58, 2, 2, 6, [EffetPousser(1, "CaseCible", zone=Zones.TypeZoneCroix(1), cible_non_requise=True)], [
        ], 0, 1, 1, 2, 0, "cercle", False, description="""Repousse les alliés et les ennemis situés autour de la cellule ciblée.""", chaine=True),

        Sort.Sort("Souffle", 102, 2, 2, 8, [EffetPousser(1, "CaseCible", zone=Zones.TypeZoneCroix(1), cible_non_requise=True)], [
        ], 0, 1, 1, 2, 0, "cercle", False, description="""Repousse les alliés et les ennemis situés autour de la cellule ciblée.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Violence", 135, 2, 0, 0, [EffetAttire(1, zone=Zones.TypeZoneCercle(2)), EffetEtatSelf(EtatBoostCaracFixe("Violence tacle", 0, 1, "tacle", 25), zone=Zones.TypeZoneCercle(2), cibles_possibles="Ennemis"), EffetEtatSelf(EtatBoostCaracFixe(
            "Violence dopou", 0, 1, "doPou", 50), zone=Zones.TypeZoneCercle(2), cibles_possibles="Ennemis")], [], 0, 1, 99, 0, 0, "cercle", False, description="""Attire les entités é proximité et augmente les dommages de poussée et le Tacle pour chaque ennemi dans la zone d'effet.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Concentration", 22, 2, 1, 1, [EffetDegats(20, 24, "Terre", cibles_possibles="Invoc"), EffetDegats(12, 16, "Terre", cibles_exclues="Invoc")], [EffetDegats(25, 29, "Terre", cibles_possibles="Invoc"), EffetDegats(17, 21, "Terre", cibles_exclues="Invoc")], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Terre.
    Les dommages sont augmentés contre les Invocations.""", chaine=False),

        Sort.Sort("Concentration", 65, 2, 1, 1, [EffetDegats(24, 28, "Terre", cibles_possibles="Invoc"), EffetDegats(16, 20, "Terre", cibles_exclues="Invoc")], [EffetDegats(29, 33, "Terre", cibles_possibles="Invoc"), EffetDegats(21, 25, "Terre", cibles_exclues="Invoc")], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Terre.
    Les dommages sont augmentés contre les Invocations.""", chaine=False),

        Sort.Sort("Concentration", 108, 2, 1, 1, [EffetDegats(30, 34, "Terre", cibles_possibles="Invoc"), EffetDegats(20, 24, "Terre", cibles_exclues="Invoc")], [EffetDegats(36, 40, "Terre", cibles_possibles="Invoc"), EffetDegats(26, 30, "Terre", cibles_exclues="Invoc")], 5, 4, 3, 0, 0, "ligne", True, description="""Occasionne des dommages Terre.
    Les dommages sont augmentés contre les Invocations.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Accumulation", 140, 3, 0, 4, [EffetDegats(22, 26, "Terre", cibles_possibles="Ennemis"), EffetEtat(EtatBoostBaseDeg("Accumulation", 0, 3, "Accumulation", 20), cibles_possibles="Lanceur")], [EffetDegats(27, 31, "Terre", cibles_possibles="Ennemis"), EffetEtat(EtatBoostBaseDeg("Accumulation", 0, 3, "Accumulation", 24), cibles_possibles="Lanceur")], 5, 3, 2, 0, 0, "ligne", True, description="""Occasionne des dommages Terre.
    Si le sort est lancé sur soi, le sort n'occasionne pas de dommages et ils sont augmentés pour les prochains lancers.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Couper", 27, 3, 1, 3, [EffetDegats(12, 16, "Feu", zone=Zones.TypeZoneLigne(3), cible_non_requise=True), EffetRetPM(2, zone=Zones.TypeZoneLigne(3), cible_non_requise=True)], [EffetDegats(19, 19, "Feu", zone=Zones.TypeZoneLigne(
            3), cible_non_requise=True), EffetRetPM(2, zone=Zones.TypeZoneLigne(3), cible_non_requise=True)], 5, 2, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Feu et retire des PM.""", chaine=True),

        Sort.Sort("Couper", 72, 3, 1, 3, [EffetDegats(15, 19, "Feu", zone=Zones.TypeZoneLigne(3), cible_non_requise=True), EffetRetPM(2, zone=Zones.TypeZoneLigne(3), cible_non_requise=True)], [EffetDegats(22, 22, "Feu", zone=Zones.TypeZoneLigne(
            3), cible_non_requise=True), EffetRetPM(2, zone=Zones.TypeZoneLigne(3), cible_non_requise=True)], 5, 2, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Feu et retire des PM.""", chaine=True),

        Sort.Sort("Couper", 118, 3, 1, 4, [EffetDegats(18, 22, "Feu", zone=Zones.TypeZoneLigne(3), cible_non_requise=True), EffetRetPM(3, zone=Zones.TypeZoneLigne(3), cible_non_requise=True)], [EffetDegats(25, 25, "Feu", zone=Zones.TypeZoneLigne(
            3), cible_non_requise=True), EffetRetPM(3, zone=Zones.TypeZoneLigne(3), cible_non_requise=True)], 5, 2, 99, 0, 1, "ligne", True, description="""Occasionne des dommages Feu et retire des PM.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Fracture", 145, 4, 1, 4, [EffetEtat(EtatBoostCaracFixe("Fracture", 0, 2, "erosion", 13), zone=Zones.TypeZoneLigneJusque(), cible_non_requise=True), EffetDegats(34, 38, "Air", zone=Zones.TypeZoneLigneJusque(), cible_non_requise=True)], [EffetEtat(EtatBoostCaracFixe("Fracture", 0, 2, "erosion", 13), zone=Zones.TypeZoneLigneJusque(), cible_non_requise=True), EffetDegats(39, 43, "Air", zone=Zones.TypeZoneLigneJusque(), cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", False, description="""Occasionne des dommages Air jusqu'é la cellule ciblée.
    Applique un malus d'érosion.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Friction", 32, 2, 0, 4, [EffetEtat(EtatLanceSortSiSubit("Frikt", 0, 2, activationFriction, "Attaquant")), EffetAttire(1)], [], 0, 1, 1, 5, 0, "cercle", False, description="""Attire la cible d'une case.
    La cible se rapproche ensuite de l'attaquant si elle reçoit des dommages issus de sorts pendant 2 tours.
    Nécessite d'être aligné avec la cible.""", chaine=True),

        Sort.Sort("Friction", 81, 2, 0, 4, [EffetEtat(EtatLanceSortSiSubit("Frikt", 0, 2, activationFriction, "Attaquant")), EffetAttire(1)], [], 0, 1, 1, 4, 0, "cercle", False, description="""Attire la cible d'une case.
    La cible se rapproche ensuite de l'attaquant si elle reçoit des dommages issus de sorts pendant 2 tours.
    Nécessite d'être aligné avec la cible.""", chaine=True),

        Sort.Sort("Friction", 124, 2, 0, 5, [EffetEtat(EtatLanceSortSiSubit("Frikt", 0, 2, activationFriction, "Attaquant")), EffetAttire(1)], [], 0, 1, 1, 3, 0, "cercle", False, description="""Attire la cible d'une case.
    La cible se rapproche ensuite de l'attaquant si elle reçoit des dommages issus de sorts pendant 2 tours.
    Nécessite d'être aligné avec la cible.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Coup pour coup", 150, 2, 1, 3, [EffetEtatSelf(EtatLanceSortSiSubit("Rend coup pour coup", 0, 2, activationCoupPourCoup, "Porteur")), EffetEtat(Etat("Coup pour coup", 0, 2)), EffetPousser(2)], [], 0, 1, 1, 3, 0, "cercle", True, description="""Repousse un ennemi.
    La cible est ensuite repoussée de 2 cases à chaque fois qu'elle attaque le lanceur pendant 2 tours.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Duel", 38, 3, 1, 1, [EffetEtat(EtatBoostCaracFixe("Duel: Invulnérabilité à distance", 0, 1, "reDist", 999999), cible_possible="Ennemis"), EffetEtatSelf(EtatBoostCaracFixe("Duel: Invulnérabilité à distance", 0, 1, "reDist", 999999), cible_possible="Ennemis"), EffetEtat(Etat("Pesanteur", 0, 1), cible_possible="Ennemis"), EffetEtatSelf(Etat("Pesanteur", 0, 2), cible_possible="Ennemis"), EffetEtat(EtatBoostCaracFixe("Duel: Immobilisation", 0, 1, "PM", -100), cible_possible="Ennemis"), EffetEtatSelf(EtatBoostCaracFixe("Duel: Immobilisation", 0, 2, "PM", -100), cible_possible="Ennemis")], [], 0, 1, 1, 6, 0, "cercle", False, description="""Retire leurs PM à la cible et au lanceur, leur applique l'état Pesanteur et les rend invuln�rable aux dommages � distance.
    Ne fonctionne que si lancé sur un ennemi.""", chaine=True),

        Sort.Sort("Duel", 90, 3, 1, 1, [EffetEtat(EtatBoostCaracFixe("Duel: Invulnérabilité à distance", 0, 1, "reDist", 999999), cible_possible="Ennemis"), EffetEtatSelf(EtatBoostCaracFixe("Duel: Invulnérabilité à distance", 0, 1, "reDist", 999999), cible_possible="Ennemis"), EffetEtat(Etat("Pesanteur", 0, 1), cible_possible="Ennemis"), EffetEtatSelf(Etat("Pesanteur", 0, 2), cible_possible="Ennemis"), EffetEtat(EtatBoostCaracFixe("Duel: Immobilisation", 0, 1, "PM", -100), cible_possible="Ennemis"), EffetEtatSelf(EtatBoostCaracFixe("Duel: Immobilisation", 0, 2, "PM", -100), cible_possible="Ennemis")], [], 0, 1, 1, 5, 0, "cercle", False, description="""Retire leurs PM à la cible et au lanceur, leur applique l'état Pesanteur et les rend invuln�rable aux dommages � distance.
    Ne fonctionne que si lancé sur un ennemi.""", chaine=True),

        Sort.Sort("Duel", 132, 3, 1, 1, [EffetEtat(EtatBoostCaracFixe("Duel: Invulnérabilité à distance", 0, 1, "reDist", 999999), cible_possible="Ennemis"), EffetEtatSelf(EtatBoostCaracFixe("Duel: Invulnérabilité à distance", 0, 1, "reDist", 999999), cible_possible="Ennemis"), EffetEtat(Etat("Pesanteur", 0, 1), cible_possible="Ennemis"), EffetEtatSelf(Etat("Pesanteur", 0, 2), cible_possible="Ennemis"), EffetEtat(EtatBoostCaracFixe("Duel: Immobilisation", 0, 1, "PM", -100), cible_possible="Ennemis"), EffetEtatSelf(EtatBoostCaracFixe("Duel: Immobilisation", 0, 2, "PM", -100), cible_possible="Ennemis")], [], 0, 1, 1, 4, 0, "cercle", False, description="""Retire leurs PM à la cible et au lanceur, leur applique l'état Pesanteur et les rend invuln�rable aux dommages � distance.
    Ne fonctionne que si lancé sur un ennemi.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Emprise", 155, 3, 1, 1, [EffetEtat(EtatModDegPer("Emprise: Invulnérable", 0, 1, 0)), EffetEtat(EtatBoostCaracFixe(
            "Emprise", 0, 1, "PM", -100))], [], 0, 1, 1, 4, 0, "cercle", False, description="""Retire tous les PM de l'ennemi cible mais le rend invulnérable.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Épée du Jugement", 44, 4, 1, 4, [EffetDegats(13, 15, "Air"), EffetDegats(13, 15, "Feu")], [EffetDegats(17, 19, "Air"), EffetDegats(
            17, 19, "Feu")], 5, 2, 1, 0, 0, "cercle", False, description="""Occasionne des dommages Air et Feu sans ligne de vue.""", chaine=True),

        Sort.Sort("Épée du Jugement", 97, 4, 1, 4, [EffetDegats(16, 18, "Air"), EffetDegats(16, 18, "Feu")], [EffetDegats(20, 22, "Air"), EffetDegats(
            20, 22, "Feu")], 5, 2, 1, 0, 0, "cercle", False, description="""Occasionne des dommages Air et Feu sans ligne de vue.""", chaine=True),

        Sort.Sort("Épée du Jugement", 137, 4, 1, 5, [EffetDegats(19, 21, "Air"), EffetDegats(19, 21, "Feu")], [EffetDegats(23, 25, "Air"), EffetDegats(
            23, 25, "Feu")], 5, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Air et Feu sans ligne de vue.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Condamnation", 160, 3, 1, 6, [
            EffetDegats(41, 45, "feu", zone=Zones.TypeZoneCercleSansCentre(
                99), etat_requis_cibles="Condamnation 2", consomme_etat=True),
            EffetEtat(Etat("Condamnation 2", 0, -1),
                      etat_requis_cibles="Condamnation 1", consomme_etat=True),
            EffetDegats(25, 29, "feu", zone=Zones.TypeZoneCercleSansCentre(
                99), etat_requis_cibles="Condamnation 1", consomme_etat=True),
            EffetEtat(Etat("Condamnation 1", 0, -1),
                      etat_requis_cibles="!Condamnation 2"),
            EffetDegats(25, 29, "air")
        ], [], 0, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Air.
    Occasionne des dommages Feu sur la cible initiale lorsque le sort est lanc� sur une autre cible.
    Les dommages Feu sont augment�s si le sort est utilis� une deuxi�me fois sur la cible initiale.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Puissance", 50, 3, 0, 2, [EffetEtat(EtatBoostCaracFixe("Puissance", 0, 2, "pui", 100))], [EffetEtat(EtatBoostCaracFixe(
            "Puissance", 0, 2, "pui", 120))], 15, 1, 1, 3, 0, "cercle", True, description="""Augmente la Puissance de la cible.""", chaine=True),

        Sort.Sort("Puissance", 103, 3, 0, 4, [EffetEtat(EtatBoostCaracFixe("Puissance", 0, 2, "pui", 200))], [EffetEtat(EtatBoostCaracFixe(
            "Puissance", 0, 2, "pui", 240))], 15, 1, 1, 3, 0, "cercle", True, description="""Augmente la Puissance de la cible.""", chaine=True),

        Sort.Sort("Puissance", 143, 3, 0, 6, [EffetEtat(EtatBoostCaracFixe("Puissance", 0, 2, "pui", 300))], [EffetEtat(EtatBoostCaracFixe(
            "Puissance", 0, 2, "pui", 350))], 15, 1, 1, 3, 0, "cercle", True, description="""Augmente la Puissance de la cible.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Vertu", 165, 3, 0, 0, [EffetEtat(EtatBouclierPerLvl("Vertu : bouclier", 0, 2, 500), zone=Zones.TypeZoneCroix(1)), EffetEtat(EtatBoostCaracFixe(
            "Vertu: malus puissance", 0, 2, "pui", -150))], [], 0, 1, 1, 3, 0, "cercle", False, description="""Applique un bouclier zone mais réduit la Puissance du lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Précipitation", 56, 2, 0, 2, [EffetEtat(EtatBoostCaracFixe("Précipité", 0, 1, "PA", 5)), EffetEtat(EtatBoostCaracFixe("Sortie de précipitation", 1, 1, "PA", -3))], [], 0, 1, 1, 4, 0, "cercle", True, description="""Augmente les PA de la cible pour le tour en cours mais lui retire des PA le tour suivant.
    Interdit l'utilisation des armes et du sort Colère de Iop.""", chaine=True),

        Sort.Sort("Précipitation", 112, 2, 0, 4, [EffetEtat(EtatBoostCaracFixe("Précipité", 0, 1, "PA", 5)), EffetEtat(EtatBoostCaracFixe("Sortie de précipitation", 1, 1, "PA", -3))], [], 0, 1, 1, 3, 0, "cercle", True, description="""Augmente les PA de la cible pour le tour en cours mais lui retire des PA le tour suivant.
    Interdit l'utilisation des armes et du sort Colère de Iop.""", chaine=True),

        Sort.Sort("Précipitation", 147, 2, 0, 6, [EffetEtat(EtatBoostCaracFixe("Précipité", 0, 1, "PA", 5)), EffetEtat(EtatBoostCaracFixe("Sortie de précipitation", 1, 1, "PA", -3))], [], 0, 1, 1, 2, 0, "cercle", True, description="""Augmente les PA de la cible pour le tour en cours mais lui retire des PA le tour suivant.
    Interdit l'utilisation des armes et du sort Colère de Iop.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Agitation", 170, 2, 0, 5, [EffetEtat(EtatBoostCaracFixe("Agitation", 0, 1, "PM", 2)), EffetEtat(EtatBoostCaracFixe("Intaclable", 0, 1, "fuite", 999999))], [
        ], 0, 1, 1, 2, 0, "cercle", True, description="""Augmente les PM et rend Intaclable pour le tour en cours.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Tempête de Puissance", 62, 3, 3, 4, [EffetDegats(24, 28, "Feu")], [EffetDegats(
            29, 33, "Feu")], 5, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Feu.""", chaine=True),

        Sort.Sort("Tempête de Puissance", 116, 3, 3, 4, [EffetDegats(29, 33, "Feu")], [EffetDegats(
            34, 38, "Feu")], 5, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Feu.""", chaine=True),

        Sort.Sort("Tempête de Puissance", 153, 3, 3, 5, [EffetDegats(34, 38, "Feu")], [EffetDegats(
            41, 45, "Feu")], 5, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Feu.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Tumulte", 175, 4, 2, 5, [EffetEtatSelf(EtatBoostBaseDeg("Tumulte", 0, 1, "Tumulte", 30), zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis"), EffetDegats(19, 21, "Feu", zone=Zones.TypeZoneCroix(1))], [EffetEtatSelf(EtatBoostBaseDeg("Tumulte", 0, 1, "Tumulte", 30), zone=Zones.TypeZoneCroix(1), cibles_possibles="Ennemis"), EffetDegats(23, 25, "Feu", zone=Zones.TypeZoneCroix(1))], 5, 1, 1, 1, 0, "cercle", True, description="""Occasionne des dommages Feu en zone.
        Plus le nombre de cibles ennemies est important, plus les dommages sont importants.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Épée Céleste", 69, 4, 0, 3, [EffetDegats(28, 32, "Air", zone=Zones.TypeZoneCercle(2))], [EffetDegats(
            34, 38, "Air", zone=Zones.TypeZoneCercle(2))], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Air en zone.""", chaine=True),

        Sort.Sort("Épée Céleste", 122, 4, 0, 3, [EffetDegats(32, 36, "Air", zone=Zones.TypeZoneCercle(2))], [EffetDegats(
            38, 42, "Air", zone=Zones.TypeZoneCercle(2))], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Air en zone.""", chaine=True),

        Sort.Sort("Épée Céleste", 162, 4, 0, 4, [EffetDegats(36, 40, "Air", zone=Zones.TypeZoneCercle(2))], [EffetDegats(
            42, 46, "Air", zone=Zones.TypeZoneCercle(2))], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Air en zone.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Zénith", 180, 5, 1, 3, [EffetDegatsSelonPMUtilises(86, 94, "Air", zone=Zones.TypeZoneLigne(4), cible_non_requise=True)], [EffetDegatsSelonPMUtilises(104, 112, "Air", zone=Zones.TypeZoneLigne(4), cible_non_requise=True)], 5, 1, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Air en zone.
    Moins le lanceur a utilisé de PM pendant son tour de jeu, plus les dommages occasionnés sont importants.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Vitalité", 77, 3, 0, 2, [EffetEtat(EtatBoostCaracPer("Vitalite", 0, 4, "vie", 16))], [EffetEtat(EtatBoostCaracPer("Vitalite", 0, 4, "vie", 18))], 25, 1, 1, 2, 0, "cercle", True, description="""Augmente temporairement la Vitalité de la cible en pourcentage.
    Le bonus de Vitalité est divisé par 2 sur les cibles autres que le lanceur.""", chaine=True),

        Sort.Sort("Vitalité", 128, 3, 0, 4, [EffetEtat(EtatBoostCaracPer("Vitalite", 0, 4, "vie", 18))], [EffetEtat(EtatBoostCaracPer("Vitalite", 0, 4, "vie", 20))], 25, 1, 1, 2, 0, "cercle", True, description="""Augmente temporairement la Vitalité de la cible en pourcentage.
    Le bonus de Vitalité est divisé par 2 sur les cibles autres que le lanceur.""", chaine=True),

        Sort.Sort("Vitalité", 172, 3, 0, 6, [EffetEtat(EtatBoostCaracPer("Vitalite", 0, 4, "vie", 20))], [EffetEtat(EtatBoostCaracPer("Vitalite", 0, 4, "vie", 22))], 25, 1, 1, 2, 0, "cercle", True, description="""Augmente temporairement la Vitalité de la cible en pourcentage.
    Le bonus de Vitalité est divisé par 2 sur les cibles autres que le lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Endurance", 185, 3, 1, 1, [EffetDegats(34, 38, "Eau"), EffetEtatSelf(EtatBouclierPerLvl("Endurance", 0, 1, 150))], [EffetDegats(39, 43, "Eau"), EffetEtatSelf(EtatBouclierPerLvl("Endurance", 0, 1, 150))], 15, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Eau.
    Applique des points de bouclier au lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Épée de Iop", 84, 4, 1, 5, [EffetDegats(27, 31, "Terre", zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", cible_non_requise=True)], [EffetDegats(
            32, 36, "Terre", zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Terre en croix.""", chaine=True),

        Sort.Sort("Épée de Iop", 134, 4, 1, 5, [EffetDegats(32, 36, "Terre", zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", cible_non_requise=True)], [EffetDegats(
            37, 41, "Terre", zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Terre en croix.""", chaine=True),

        Sort.Sort("Épée de Iop", 178, 4, 1, 6, [EffetDegats(37, 41, "Terre", zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", cible_non_requise=True)], [EffetDegats(
            42, 46, "Terre", zone=Zones.TypeZoneCroix(3), cibles_possibles="Allies|Ennemis", cibles_exclues="Lanceur", cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Terre en croix.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Pugilat", 190, 2, 1, 6, [EffetDegats(9, 11, "Terre", zone=Zones.TypeZoneCercle(2), cibles_exclues="Lanceur"), EffetEtatSelf(EtatBoostBaseDeg("Pugilat", 0, 1, "Pugilat", 15))], [EffetDegats(11, 13, "Terre", cibles_exclues="Lanceur", zone=Zones.TypeZoneCercle(2)), EffetEtatSelf(EtatBoostBaseDeg("Pugilat", 0, 1, "Pugilat", 18))], 5, 4, 1, 0, 0, "cercle", True, description="""Occasionne des dommages Terre en zone.
    Les dommages sont augmentés pendant 1 tour après chaque lancer.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Épée du destin", 92, 4, 1, 1, [EffetDegats(28, 32, "Feu"), EffetEtatSelf(EtatBoostBaseDeg("Épée du destin", 2, 1, "Épée du destin", 30))], [EffetDegats(33, 37, "Feu"), EffetEtatSelf(EtatBoostBaseDeg("Épée du destin", 2, 1, "Épée du destin", 35))], 25, 1, 1, 2, 0, "ligne", True, description="""Occasionne des dommages Feu.
    Les dommages sont augmentés à partir du second lancer.""", chaine=True),

        Sort.Sort("Épée du destin", 141, 4, 1, 1, [EffetDegats(33, 37, "Feu"), EffetEtatSelf(EtatBoostBaseDeg("Épée du destin", 2, 1, "Épée du destin", 35))], [EffetDegats(38, 42, "Feu"), EffetEtatSelf(EtatBoostBaseDeg("Épée du destin", 2, 1, "Épée du destin", 40))], 25, 1, 1, 2, 0, "ligne", True, description="""Occasionne des dommages Feu.
    Les dommages sont augmentés à partir du second lancer.""", chaine=True),

        Sort.Sort("Épée du destin", 187, 4, 1, 1, [EffetDegats(38, 42, "Feu"), EffetEtatSelf(EtatBoostBaseDeg("Épée du destin", 2, 1, "Épée du destin", 40))], [EffetDegats(43, 47, "Feu"), EffetEtatSelf(EtatBoostBaseDeg("Épée du destin", 2, 1, "Épée du destin", 45))], 25, 1, 1, 2, 0, "ligne", True, description="""Occasionne des dommages Feu.
    Les dommages sont augmentés à partir du second lancer.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Sentence", 195, 2, 1, 6, [EffetDegats(13, 16, "Feu"), EffetEtat(EtatEffetFinTour("Sentence", 0, 1, EffetDegats(13, 16, "feu", zone=Zones.TypeZoneCercle(2), cibles_possibles="Ennemis"), "Sentence", "lanceur"))], [EffetDegats(15, 18, "Feu"), EffetEtat(EtatEffetFinTour("Sentence", 1, 1, EffetDegats(15, 18, "feu", zone=Zones.TypeZoneCercle(2)), "Sentence", "lanceur"))], 25, 3, 1, 0, 1, "cercle", True, description="""Occasionne des dommages Feu.
    Occasionne des dommages Feu supplémentaires aux ennemis à proximité de la cible (2 cases ou moins) à la fin de son tour.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Colère de Iop", 100, 7, 1, 1, [EffetDegats(61, 80, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Colère de Iop", 3, 1, "Colère de Iop", 90))], [EffetDegats(71, 90, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Colère de Iop", 3, 1, "Colère de Iop", 100))], 25, 1, 1, 3, 0, "cercle", True, description="""Occasionne des dommages Terre.
    Augmente les dommages du sort au troisième tour après son lancer.""", chaine=True),

        Sort.Sort("Colère de Iop", 149, 7, 1, 1, [EffetDegats(71, 90, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Colère de Iop", 3, 1, "Colère de Iop", 100))], [EffetDegats(81, 100, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Colère de Iop", 3, 1, "Colère de Iop", 110))], 25, 1, 1, 3, 0, "cercle", True, description="""Occasionne des dommages Terre.
    Augmente les dommages du sort au troisième tour après son lancer.""", chaine=True),

        Sort.Sort("Colère de Iop", 197, 7, 1, 1, [EffetDegats(81, 100, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Colère de Iop", 3, 1, "Colère de Iop", 110))], [EffetDegats(91, 110, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Colère de Iop", 3, 1, "Colère de Iop", 120))], 25, 1, 1, 3, 0, "cercle", True, description="""Occasionne des dommages Terre.
    Augmente les dommages du sort au troisième tour après son lancer.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Fureur", 200, 3, 1, 1, [EffetDegats(28, 32, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Fureur", 0, 2, "Fureur", 30))], [EffetDegats(34, 38, "Terre"), EffetEtatSelf(EtatBoostBaseDeg("Fureur", 0, 2, "Fureur", 36))], 5, 1, 99, 0, 0, "cercle", False, description="""Occasionne des dommages Terre.
    Les dommages sont augmentés à chaque lancer du sort, mais ce bonus est perdu si le sort n'est pas relancé.""", chaine=True)
    ]))
    return sorts
