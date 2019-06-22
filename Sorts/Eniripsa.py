"""@summary: Rassemble les sorts de l'éniripsa
"""
# pylint: disable=line-too-long
import Sort
from Effets.EffetDegats import EffetDegats, EffetVolDeVie, EffetDegatsPerPv
from Effets.EffetTue import EffetTue
from Effets.EffetPousser import EffetPousser, EffetAttire
from Effets.EffetSoin import EffetSoinSelonSubit, EffetSoin, EffetSoinPerPVMax
from Effets.EffetEtat import EffetEtat, EffetRetireEtat, EffetEtatSelf, EffetRafraichirEtats
from Effets.EffetInvoque import EffetInvoque
from Effets.EffetTp import EffetTp, EffetEchangePlace
from Effets.EffetGlyphe import EffetGlyphe
from Effets.EffetEntiteLanceSort import EffetEntiteLanceSort
from Effets.EffetRet import EffetRetPM, EffetRetPA
from Effets.EffetDevoilePiege import EffetDevoilePiege
from Etats.Etat import Etat
from Etats.EtatEffet import EtatEffetSiSubit, EtatEffetFinTour, EtatEffetSiMeurt, EtatEffetDebutTour, EtatEffetSiNouvelEtat
from Etats.EtatBoostCarac import EtatBoostCaracFixe
from Etats.EtatBoostSortCarac import EtatBoostSortCarac
from Etats.EtatModSoin import EtatModSoinPer
from Etats.EtatBouclier import EtatBouclierPerLvl
import Zones

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
    motDAirEffetAvant = EffetEtat(EtatEffetSiSubit('Etat temporaire', 0, 1, EffetSoinSelonSubit(
        100, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies"), "Mots d'Air", "lanceur", "attaquant"))
    motDAirEffetApres = EffetRetireEtat('Etat temporaire')
    motDAirTournoyantEffetAvant = EffetEtat(EtatEffetSiSubit('Etat temporaire', 0, 1, EffetSoinSelonSubit(
        100, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies"), "Mots d'Air", "lanceur", "attaquant"), zone=Zones.TypeZoneCarre(1))
    motDAirTournoyantEffetApres = EffetRetireEtat('Etat temporaire', zone=Zones.TypeZoneCarre(1))
    motDAirAnimeEffetAvant = EffetEtat(EtatEffetSiSubit('Mot Eau temporaire', 0, 1, EffetSoinSelonSubit(
        100, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies"), "Mots d'Eau", "lanceur", "cible"))
    motDAirAnimeEffetApres = EffetRetireEtat('Mot Eau temporaire', zone=Zones.TypeZoneInfini())
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Blessant", 1, 4, 1, 6, [motDAirEffetAvant, EffetDegats(13, 15, "Air"), motDAirEffetApres], [motDAirEffetAvant, EffetDegats(17, 17, "Air"), motDAirEffetApres], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air.
        Les alliés à proximité du lanceur (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True),

        Sort.Sort("Mot Blessant", 30, 4, 1, 7, [motDAirEffetAvant, EffetDegats(16, 18, "Air"), motDAirEffetApres], [motDAirEffetAvant, EffetDegats(20, 20, "Air"), motDAirEffetApres], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air.
        Les alliés à proximité du lanceur (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True),

        Sort.Sort("Mot Blessant", 60, 4, 1, 8, [motDAirEffetAvant, EffetDegats(19, 21, "Air"), motDAirEffetApres], [motDAirEffetAvant, EffetDegats(23, 23, "Air"), motDAirEffetApres], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air.
        Les alliés à proximité du lanceur (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Vexant", 110, 5, 1, 5, [EffetDegats(48, 52, "Air")], [EffetDegats(58, 62, "Air")], 5, 2, 1, 0, 0, "ligne", True, description="""Occasionne des dommages Air.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Alternatif", 1, 3, 1, 4, [EffetSoin(14, 17, cibles_possibles="Allies"), EffetDegats(10, 13, "Feu", cibles_possibles="Ennemis")], [EffetSoin(18, 18, cibles_possibles="Allies"), EffetDegats(13, 13, "Feu", cibles_possibles="Ennemis")], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Feu aux ennemis.
    Soigne les alliés.""", chaine=False),

        Sort.Sort("Mot Alternatif", 20, 3, 1, 6, [EffetSoin(19, 22, cibles_possibles="Allies"), EffetDegats(13, 16, "Feu", cibles_possibles="Ennemis")], [EffetSoin(23, 23, cibles_possibles="Allies"), EffetDegats(17, 17, "Feu", cibles_possibles="Ennemis")], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Feu aux ennemis.
    Soigne les alliés.""", chaine=False),

        Sort.Sort("Mot Alternatif", 40, 3, 1, 8, [EffetSoin(24, 27, cibles_possibles="Allies"), EffetDegats(16, 19, "Feu", cibles_possibles="Ennemis")], [EffetSoin(28, 28, cibles_possibles="Allies"), EffetDegats(21, 21, "Feu", cibles_possibles="Ennemis")], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Feu aux ennemis.
    Soigne les alliés.""", chaine=False)
    ]))
    activationMotMarquant = Sort.Sort("Glyphe Marquant", 0, 0, 0, 1, [EffetEtat(EtatEffetFinTour("Glyphe Marquant", 0, 1, EffetSoin(43, 47), "Glyphe Marquant", "lanceur"), cibles_possibles="Allies|Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False)
    sortieMotMarquant = Sort.Sort("Sortie Glyphe Marquant", 0, 0, 0, 2, [EffetRetireEtat("Glyphe Marquant", cibles_possibles="Allies|Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False)
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Marquant", 101, 4, 1, 5, [EffetGlyphe(Zones.TypeZoneCercleSansCentre(1), activationMotMarquant, activationMotMarquant, sortieMotMarquant, 1, "Mot Marquant", (252, 116, 172), cibles_possibles="Ennemis"), EffetDegats(30, 34, "Feu")], [EffetGlyphe(Zones.TypeZoneCercleSansCentre(1), activationMotMarquant, activationMotMarquant, sortieMotMarquant, 1, "Mot Marquant", (252, 116, 172), cibles_possibles="Ennemis"), EffetDegats(33, 37, "Feu")], 25, 3, 2, 0, 0, "cercle", True, description="""Occasionne des dommages Feu.
    Pose un glyphe autour de la cible ennemie. Le glyphe soigne les alliés en fin de tour.""", chaine=True)
    ]))
    sortTpLapino = Sort.Sort("Lapino TP", 0, 0, 0, 99, [EffetTp(cible_non_requise=True, cibles_possibles="")], [], 0, 99, 99, 0, 0, "cercle", False)
    lapinoGlyphe = Sort.Sort("Lapino Glyphe", 0, 0, 0, 1, [EffetEtat(EtatEffetFinTour("Lapino Glyphe", 0, 1, EffetSoinPerPVMax(10), "Lapino Glyphe", "lanceur"), cibles_possibles="Allies|Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False)
    sortieLapinoGlyphe = Sort.Sort("Sortie Lapino Marquant", 0, 0, 0, 3, [EffetRetireEtat("Lapino Glyphe", cibles_possibles="Allies|Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False)
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot d'Amitié", 1, 3, 1, 2, [
            EffetRetireEtat("Lapino mort delai", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur", cible_non_requise=True),
            # Etat pour test si le lapino est deja invoque
            EffetEtatSelf(Etat("Lapino invoqué", 0, 1), cibles_possibles="Lapino|Lapino protecteur", cible_non_requise=True, zone=Zones.TypeZoneInfini()),
            # S'il ne l'est pas, on l'invoque
            EffetInvoque("Lapino", 1, cible_non_requise=True, cibles_possibles="", etat_requis_lanceur="!Lapino invoqué"),
            # S'il ne l'était pas on stimule le lanceur
            EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini(), cibles_exclues="Lanceur", cible_non_requise=True, cumulMax=1, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtatSelf(EtatBoostCaracFixe("Stimulé", 0, -1, "PA", 2), cible_non_requise=True, cumulMax=1, etat_lanceur_requis="!Lapino invoqué"),
            # S'il ne l'était pas on met des états de mort (pose glyphe, délai de 3 tours et retire état stimulant)
            EffetEtat(EtatEffetSiMeurt("Stimulant", 0, -1, EffetRetireEtat("Stimulé", cibles_possibles="Invocateur", zone=Zones.TypeZoneInfini()), "Fin de stimulation", "mouru", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtat(EtatEffetSiMeurt("Lapino glyphe", 0, -1, EffetGlyphe(Zones.TypeZoneCercle(2), lapinoGlyphe, lapinoGlyphe, sortieLapinoGlyphe, 3, "Lapino Glyphe", (252, 116, 172)), "Lapino glyphe", "lanceur", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtat(EtatEffetSiMeurt("Lapino délai", 0, -1, EffetEtat(EtatBoostSortCarac("Lapino mort delai", 0, -1, "Mot d'Amitié", "nbTourEntreDeux", 3), cibles_possibles="Invocateur", zone=Zones.TypeZoneInfini()), "Lapino délai", "mouru", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            # S'il était déjà là on le fait se téléporté sur la case ciblé et on enlève l'état temporaire placé sur le lanceur.
            EffetEntiteLanceSort("Lapino", sortTpLapino, "CaseCible", etat_requis_lanceur="Lapino invoqué", consomme_etat=True, cible_non_requise=True),
            ], [], 0, 1, 1, 1, 0, "cercle", True, description="""Invoque un Lapino qui Stimule le lanceur tant qu'il est en vie : il donne 2 PA.
        Le Lapino soigne ses alliés.
        Si lancé alors que le Lapino est présent sur le terrain, téléporte le Lapino sur la cellule ciblée.
        Quand le Lapino meurt, il pose un glyphe de fin de tour qui soigne les alliés, et ne peut plus être invoqué pendant 3 tours.""", chaine=False),
        Sort.Sort("Mot d'Amitié", 25, 3, 1, 3, [
            EffetRetireEtat("Lapino mort delai", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur", cible_non_requise=True),
            # Etat pour test si le lapino est deja invoque
            EffetEtatSelf(Etat("Lapino invoqué", 0, 1), cibles_possibles="Lapino", cible_non_requise=True, zone=Zones.TypeZoneInfini()),
            # S'il ne l'est pas, on l'invoque
            EffetInvoque("Lapino", 1, cible_non_requise=True, cibles_possibles="", etat_requis_lanceur="!Lapino invoqué"),
            # S'il ne l'était pas on stimule le lanceur
            EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini(), cibles_exclues="Lanceur", cible_non_requise=True, cumulMax=1, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtatSelf(EtatBoostCaracFixe("Stimulé", 0, -1, "PA", 2), cible_non_requise=True, cumulMax=1, etat_lanceur_requis="!Lapino invoqué"),
            # S'il ne l'était pas on met des états de mort (pose glyphe, délai de 3 tours et retire état stimulant)
            EffetEtat(EtatEffetSiMeurt("Stimulant", 0, -1, EffetRetireEtat("Stimulé", cibles_possibles="Invocateur", zone=Zones.TypeZoneInfini()), "Fin de stimulation", "mouru", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtat(EtatEffetSiMeurt("Lapino glyphe", 0, -1, EffetGlyphe(Zones.TypeZoneCercle(2), lapinoGlyphe, lapinoGlyphe, sortieLapinoGlyphe, 3, "Lapino Glyphe", (252, 116, 172)), "Lapino glyphe", "lanceur", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtat(EtatEffetSiMeurt("Lapino délai", 0, -1, EffetEtat(EtatBoostSortCarac("Lapino mort delai", 0, -1, "Mot d'Amitié", "nbTourEntreDeux", 3), cibles_possibles="Invocateur", zone=Zones.TypeZoneInfini()), "Lapino délai", "mouru", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            # S'il était déjà là on le fait se téléporté sur la case ciblé et on enlève l'état temporaire placé sur le lanceur.
            EffetEntiteLanceSort("Lapino", sortTpLapino, "CaseCible", etat_requis_lanceur="Lapino invoqué", consomme_etat=True, cible_non_requise=True),
            ], [], 0, 1, 1, 1, 0, "cercle", True, description="""Invoque un Lapino qui Stimule le lanceur tant qu'il est en vie : il donne 2 PA.
        Le Lapino soigne ses alliés.
        Si lancé alors que le Lapino est présent sur le terrain, téléporte le Lapino sur la cellule ciblée.
        Quand le Lapino meurt, il pose un glyphe de fin de tour qui soigne les alliés, et ne peut plus être invoqué pendant 3 tours.""", chaine=False),

        Sort.Sort("Mot d'Amitié", 52, 3, 1, 3, [
            EffetRetireEtat("Lapino mort delai", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur", cible_non_requise=True),
            # Etat pour test si le lapino est deja invoque
            EffetEtatSelf(Etat("Lapino invoqué", 0, 1), cibles_possibles="Lapino", cible_non_requise=True, zone=Zones.TypeZoneInfini()),
            # S'il ne l'est pas, on l'invoque
            EffetInvoque("Lapino", 1, cible_non_requise=True, cibles_possibles="", etat_requis_lanceur="!Lapino invoqué"),
            # S'il ne l'était pas on stimule le lanceur
            EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini(), cibles_exclues="Lanceur", cible_non_requise=True, cumulMax=1, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtatSelf(EtatBoostCaracFixe("Stimulé", 0, -1, "PA", 2), cible_non_requise=True, cumulMax=1, etat_lanceur_requis="!Lapino invoqué"),
            # S'il ne l'était pas on met des états de mort (pose glyphe, délai de 3 tours et retire état stimulant)
            EffetEtat(EtatEffetSiMeurt("Stimulant", 0, -1, EffetRetireEtat("Stimulé", cibles_possibles="Invocateur", zone=Zones.TypeZoneInfini()), "Fin de stimulation", "mouru", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtat(EtatEffetSiMeurt("Lapino glyphe", 0, -1, EffetGlyphe(Zones.TypeZoneCercle(2), lapinoGlyphe, lapinoGlyphe, sortieLapinoGlyphe, 3, "Lapino Glyphe", (252, 116, 172)), "Lapino glyphe", "lanceur", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtat(EtatEffetSiMeurt("Lapino délai", 0, -1, EffetEtat(EtatBoostSortCarac("Lapino mort delai", 0, -1, "Mot d'Amitié", "nbTourEntreDeux", 3), cibles_possibles="Invocateur", zone=Zones.TypeZoneInfini()), "Lapino délai", "mouru", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            # S'il était déjà là on le fait se téléporté sur la case ciblé et on enlève l'état temporaire placé sur le lanceur.
            EffetEntiteLanceSort("Lapino", sortTpLapino, "CaseCible", etat_requis_lanceur="Lapino invoqué", consomme_etat=True, cible_non_requise=True),
            ], [], 0, 1, 1, 1, 0, "cercle", True, description="""Invoque un Lapino qui Stimule le lanceur tant qu'il est en vie : il donne 2 PA.
        Le Lapino soigne ses alliés.
        Si lancé alors que le Lapino est présent sur le terrain, téléporte le Lapino sur la cellule ciblée.
        Quand le Lapino meurt, il pose un glyphe de fin de tour qui soigne les alliés, et ne peut plus être invoqué pendant 3 tours.""", chaine=False),
    ]))
    sortTpLapinoProtecteur = Sort.Sort("Lapino Protecteur TP", 0, 0, 0, 99, [EffetTp(cible_non_requise=True, cibles_possibles="")], [], 0, 99, 99, 0, 0, "cercle", False)
    lapinoProtecteurGlyphe = Sort.Sort("Lapino protecteur Glyphe", 0, 0, 0, 1, [EffetEtat(EtatEffetFinTour("Lapino Protecteur Glyphe", 0, 1, EffetEtat(EtatBouclierPerLvl("Glyphe de lapino protecteur", 0, 1, 207)), "Lapino Protecteur Glyphe", "lanceur"), cibles_possibles="Allies|Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False)
    sortieLapinoProtecteurGlyphe = Sort.Sort("Sortie Lapino protecteur Marquant", 0, 0, 0, 3, [EffetRetireEtat("Lapino Protecteur Glyphe", cibles_possibles="Allies|Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False)
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot d'Affection", 105, 4, 1, 3, [
            EffetRetireEtat("Lapino mort delai", zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur", cible_non_requise=True),
            # Etat pour test si le lapino est deja invoque
            EffetEtatSelf(Etat("Lapino invoqué", 0, 1), cibles_possibles="Lapino", cible_non_requise=True, zone=Zones.TypeZoneInfini()),
            # S'il ne l'est pas, on l'invoque
            EffetInvoque("Lapino protecteur", 1, cible_non_requise=True, cibles_possibles="", etat_requis_lanceur="!Lapino invoqué"),
            # S'il ne l'était pas on stimule le lanceur
            EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini(), cibles_exclues="Lanceur", cible_non_requise=True, cumulMax=1, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtatSelf(EtatBoostCaracFixe("Stimulé", 0, -1, "PA", 2), cible_non_requise=True, cumulMax=1, etat_lanceur_requis="!Lapino invoqué"),
            # S'il ne l'était pas on met des états de mort (pose glyphe, délai de 3 tours et retire état stimulant)
            EffetEtat(EtatEffetSiMeurt("Stimulant", 0, -1, EffetRetireEtat("Stimulé", cibles_possibles="Invocateur", zone=Zones.TypeZoneInfini()), "Fin de stimulation", "mouru", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtat(EtatEffetSiMeurt("Lapino glyphe", 0, -1, EffetGlyphe(Zones.TypeZoneCercle(2), lapinoProtecteurGlyphe, lapinoProtecteurGlyphe, sortieLapinoProtecteurGlyphe, 3, "Lapino protecteur Glyphe", (148, 21, 239)), "Lapino protecteur glyphe", "lanceur", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            EffetEtat(EtatEffetSiMeurt("Lapino délai", 0, -1, EffetEtat(EtatBoostSortCarac("Lapino mort delai", 0, -1, "Mot d'Affection", "nbTourEntreDeux", 3), cibles_possibles="Invocateur", zone=Zones.TypeZoneInfini()), "Lapino délai", "mouru", "mouru"), cible_non_requise=True, etat_lanceur_requis="!Lapino invoqué"),
            # S'il était déjà là on le fait se téléporté sur la case ciblé et on enlève l'état temporaire placé sur le lanceur.
            EffetEntiteLanceSort("Lapino protecteur", sortTpLapinoProtecteur, "CaseCible", etat_requis_lanceur="Lapino invoqué", consomme_etat=True, cible_non_requise=True),
            ], [], 0, 1, 1, 1, 0, "cercle", True, description="""Invoque un Lapino protecteur qui Stimule le lanceur tant qu'il est en vie : il donne 2 PA.
        Le Lapino donne des points de bouclier à ses alliés.
        Si lancé alors que le Lapino est présent sur le terrain, téléporte le Lapino sur la cellule ciblée.
        Quand le Lapino meurt, il pose un glyphe de fin de tour qui donne des points de boucliers à ses alliés,
        et ne peut plus être invoqué pendant 3 tours.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Interdit", 3, 3, 1, 4, [motDAirAnimeEffetAvant, EffetDegats(11, 13, "Eau"), motDAirAnimeEffetApres], [motDAirAnimeEffetAvant, EffetDegats(15, 17, "Eau"), motDAirAnimeEffetApres], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau.
        Les alliés à proximité de la cible (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True),

        Sort.Sort("Mot Interdit", 35, 3, 1, 5, [motDAirAnimeEffetAvant, EffetDegats(14, 16, "Eau"), motDAirAnimeEffetApres], [motDAirAnimeEffetAvant, EffetDegats(18, 20, "Eau"), motDAirAnimeEffetApres], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau.
        Les alliés à proximité de la cible (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True),

        Sort.Sort("Mot Interdit", 67, 3, 1, 6, [motDAirAnimeEffetAvant, EffetDegats(17, 19, "Eau"), motDAirAnimeEffetApres], [motDAirAnimeEffetAvant, EffetDegats(21, 23, "Eau"), motDAirAnimeEffetApres], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau.
        Les alliés à proximité de la cible (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Tabou", 115, 4, 1, 7, [EffetDegats(34, 38, "Eau")], [EffetDegats(39, 43, "Eau")], 15, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Eau.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot de Frayeur", 6, 1, 1, 3, [EffetPousser(1)], [], 0, 3, 2, 0, 0, "ligne", True, description="""Pousse la cible.""", chaine=True),

        Sort.Sort("Mot de Frayeur", 42, 1, 1, 4, [EffetPousser(1)], [], 0, 3, 2, 0, 0, "ligne", True, description="""Pousse la cible.""", chaine=True),

        Sort.Sort("Mot de Frayeur", 74, 1, 1, 5, [EffetPousser(1)], [], 0, 3, 2, 0, 0, "ligne", True, description="""Pousse la cible.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot de Séduction", 120, 3, 1, 5,
                  [
                      EffetInvoque("Fiole", 1, cibles_possibles="", cible_non_requise=True),
                      EffetDegats(22, 26, "Terre", zone=Zones.TypeZoneCercleSansCentre(2))],
                  [
                      EffetInvoque("Fiole", 1, cibles_possibles="", cible_non_requise=True),
                      EffetDegats(26, 30, "Terre", zone=Zones.TypeZoneCercleSansCentre(2))
                  ], 15, 1, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Terre et invoque une fiole.
    Lorsqu''elle est attaquée par un allié, elle subit 2 fois moins de dommages et rend 100% des points de vie perdus à son attaquant.
    Lorsqu'elle meurt, elle occasionne des dommages en zone.
    Elle meurt si elle entre dans l'état Stimulé.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Stimulant", 9, 2, 1, 2, [EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini(), cibles_exclues="Lanceur"), EffetEtat(EtatBoostCaracFixe("Stimulé", 0, 3, "PA", 2), cibles_exclues="Eniripsa")], [], 0, 1, 1, 1, 0, "cercle", True, description="""La cible devient Stimulée : elle gagne 2 PA pendant 3 tours.
    N'affecte pas les Eniripsas.""", chaine=True),

        Sort.Sort("Mot Stimulant", 47, 2, 1, 4, [EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini(), cibles_exclues="Lanceur"), EffetEtat(EtatBoostCaracFixe("Stimulé", 0, 3, "PA", 2), cibles_exclues="Eniripsa")], [], 0, 1, 1, 1, 0, "cercle", True, description="""La cible devient Stimulée : elle gagne 2 PA pendant 3 tours.
    N'affecte pas les Eniripsas.""", chaine=True),

        Sort.Sort("Mot Stimulant", 87, 2, 1, 6, [EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini(), cibles_exclues="Lanceur"), EffetEtat(EtatBoostCaracFixe("Stimulé", 0, 3, "PA", 2), cibles_exclues="Eniripsa")], [], 0, 1, 1, 1, 0, "cercle", True, description="""La cible devient Stimulée : elle gagne 2 PA pendant 3 tours.
    N'affecte pas les Eniripsas.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot d'Abnégation", 125, 1, 1, 6, [EffetEtat(EtatBoostCaracFixe("Mot d'Abnégation", 0, 2, "pui", 250)), EffetEtat(EtatModSoinPer("Mot d'Abnégation", 0, 2, 75)), EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini(), cibles_exclues="Lanceur"), EffetEtat(EtatBoostCaracFixe('Stimulé', 0, 2, "PA", 2))], [], 0, 2, 1, 0, 0, "cercle", True, description="""Augmente la Puissance de la cible mais réduit les soins qu'elle reçoit.
    Applique l'état Stimulé.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Brutal", 13, 3, 1, 4, [EffetDegats(14, 16, "Terre")], [EffetDegats(18, 20, "Terre")], 5, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Terre.""", chaine=True),

        Sort.Sort("Mot Brutal", 54, 3, 1, 5, [EffetDegats(17, 19, "Terre")], [EffetDegats(21, 23, "Terre")], 5, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Terre.""", chaine=True),

        Sort.Sort("Mot Brutal", 94, 3, 1, 6, [EffetDegats(20, 22, "Terre")], [EffetDegats(24, 26, "Terre")], 5, 3, 2, 0, 0, "cercle", False, description="""Occasionne des dommages Terre.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Pernicieux", 130, 3, 2, 8, [EffetDegats(9, 11, "Terre"), EffetDegats(28, 32, "Terre", zone=Zones.TypeZoneCroix(1, 1), cibles_possibles="Ennemis")], [EffetDegats(11, 13, "Terre"), EffetDegats(34, 38, "Terre", zone=Zones.TypeZoneCroix(1, 1), cibles_possibles="Ennemis")], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Terre.
    Les dommages subis sont augmentés et occasionnés aux ennemis autour de la cible.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot de Jouvence", 17, 2, 0, 2, [EffetRafraichirEtats(1, cibles_possibles="Allies"), EffetSoinPerPVMax(6, cibles_possibles="Allies")], [], 0, 2, 1, 0, 1, "ligne", True, description="""Soigne un allié et lui retire 1 tour d'envoûtement.""", chaine=True),

        Sort.Sort("Mot de Jouvence", 58, 2, 0, 4, [EffetRafraichirEtats(1, cibles_possibles="Allies"), EffetSoinPerPVMax(8, cibles_possibles="Allies")], [], 0, 2, 1, 0, 1, "ligne", True, description="""Soigne un allié et lui retire 1 tour d'envoûtement.""", chaine=True),

        Sort.Sort("Mot de Jouvence", 102, 2, 0, 6, [EffetRafraichirEtats(1, cibles_possibles="Allies"), EffetSoinPerPVMax(10, cibles_possibles="Allies")], [], 0, 2, 1, 0, 1, "ligne", True, description="""Soigne un allié et lui retire 1 tour d'envoûtement.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Défendu", 135, 4, 1, 4, [EffetRafraichirEtats(1), EffetEtatSelf(EtatBoostCaracFixe("Mot défendu", 0, 1, "erosion", 20)), EffetDegats(38, 42, "Terre")], [EffetRafraichirEtats(1), EffetEtatSelf(EtatBoostCaracFixe("Mot défendu", 0, 1, "erosion", 20)), EffetDegats(46, 50, "Terre")], 5, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Terre.
    Réduit la durée des effets sur la cible.
    Applique un malus d'Érosion sur le lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Sélectif", 22, 3, 0, 6, [EffetSoin(13, 15, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3)), EffetDegats(9, 11, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis")], [EffetSoin(16, 16, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3)), EffetDegats(13, 13, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis")], 15, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu aux ennemis et soigne les alliés en zone.""", chaine=False),

        Sort.Sort("Mot Sélectif", 65, 3, 0, 6, [EffetSoin(18, 20, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3)), EffetDegats(12, 14, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis")], [EffetSoin(21, 21, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3)), EffetDegats(16, 16, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis")], 15, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu aux ennemis et soigne les alliés en zone.""", chaine=False),

        Sort.Sort("Mot Sélectif", 108, 3, 0, 6, [EffetSoin(23, 25, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3)), EffetDegats(15, 17, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis")], [EffetSoin(26, 26, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3)), EffetDegats(19, 19, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis")], 15, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu aux ennemis et soigne les alliés en zone.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Impartial", 140, 5, 1, 6, [EffetEtat(Etat("Mot Impartial", 0, 1), cibles_possibles="Ennemis"), EffetSoin(46, 50, etat_requis="!Mot Impartial"), EffetDegats(38, 42, "Feu", zone=Zones.TypeZoneCercleSansCentre(2), etat_requis="!Mot Impartial"), EffetDegats(38, 42, "Feu", etat_requis="Mot Impartial"), EffetSoin(46, 50, zone=Zones.TypeZoneCercleSansCentre(2), etat_requis="Mot Impartial", consomme_etat=True, cibles_possibles="Allies")], [EffetEtat(Etat("Mot Impartial", 0, 1), cibles_possibles="Ennemis"), EffetSoin(58, 62, etat_requis="!Mot Impartial"), EffetDegats(48, 52, "Feu", zone=Zones.TypeZoneCercleSansCentre(2), etat_requis="!Mot Impartial"), EffetDegats(48, 52, "Feu", etat_requis="Mot Impartial"), EffetSoin(58, 62, zone=Zones.TypeZoneCercleSansCentre(2), etat_requis="Mot Impartial", consomme_etat=True, cibles_possibles="Allies")], 5, 2, 1, 0, 1, "cercle", True, description="""Sur allié : soigne la cible et occasionne des dommages Feu autour de la cible.
    Sur ennemi : occasionne des dommages Feu et soigne autour de la cible.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Éclatant", 27, 4, 1, 4, [EffetEtat(EtatEffetSiSubit('Mot eau temporaire', 0, 1, EffetSoinSelonSubit(100, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies"), "Mots d'eau", "lanceur", "cible"), zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True), EffetDegats(19, 22, "Eau", cible_non_requise=True, zone=Zones.TypeZoneDemiCercle(2)), EffetRetireEtat("Mot eau temporaire", zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True)], [EffetEtat(EtatEffetSiSubit('Mot eau temporaire', 0, 1, EffetSoinSelonSubit(100, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies"), "Mots d'eau", "lanceur", "cible"), zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True), EffetDegats(24, 24, "Eau", cible_non_requise=True, zone=Zones.TypeZoneDemiCercle(2)), EffetRetireEtat("Mot eau temporaire", zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Eau en zone.
    Les alliés à proximité des cibles (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True),
        Sort.Sort("Mot Éclatant", 72, 4, 1, 5, [EffetEtat(EtatEffetSiSubit('Mot eau temporaire', 0, 1, EffetSoinSelonSubit(100, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies"), "Mots d'eau", "lanceur", "cible"), zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True), EffetDegats(23, 26, "Eau", cible_non_requise=True, zone=Zones.TypeZoneDemiCercle(2)), EffetRetireEtat("Mot eau temporaire", zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True)], [EffetEtat(EtatEffetSiSubit('Mot eau temporaire', 0, 1, EffetSoinSelonSubit(100, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies"), "Mots d'eau", "lanceur", "cible"), zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True), EffetDegats(28, 28, "Eau", cible_non_requise=True, zone=Zones.TypeZoneDemiCercle(2)), EffetRetireEtat("Mot eau temporaire", zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Eau en zone.
    Les alliés à proximité des cibles (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True),
        Sort.Sort("Mot Éclatant", 118, 4, 1, 6, [EffetEtat(EtatEffetSiSubit('Mot eau temporaire', 0, 1, EffetSoinSelonSubit(100, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies"), "Mots d'eau", "lanceur", "cible"), zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True), EffetDegats(27, 30, "Eau", cible_non_requise=True, zone=Zones.TypeZoneDemiCercle(2)), EffetRetireEtat("Mot eau temporaire", zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True)], [EffetEtat(EtatEffetSiSubit('Mot eau temporaire', 0, 1, EffetSoinSelonSubit(100, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies"), "Mots d'eau", "lanceur", "cible"), zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True), EffetDegats(32, 32, "Eau", cible_non_requise=True, zone=Zones.TypeZoneDemiCercle(2)), EffetRetireEtat("Mot eau temporaire", zone=Zones.TypeZoneDemiCercle(2), cible_non_requise=True)], 15, 2, 99, 0, 0, "ligne", True, description="""Occasionne des dommages Eau en zone.
    Les alliés à proximité des cibles (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Retentissant", 145, 3, 1, 6, [EffetDegats(23, 25, "Eau", zone=Zones.TypeZoneCercle(2))], [EffetDegats(26, 28, "Eau", zone=Zones.TypeZoneCercle(2))], 25, 3, 2, 0, 1, "ligne", True, description="""Occasionne des dommages Eau.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot de Prévention", 32, 2, 0, 2, [EffetEtat(EtatBouclierPerLvl("Mot de Prévention", 0, 2, 450))], [EffetEtat(EtatBouclierPerLvl("Mot de Prévention", 0, 2, 510))], 5, 1, 1, 4, 1, "ligne", True, description="""La cible gagne des points de bouclier pendant 2 tours.""", chaine=True),

        Sort.Sort("Mot de Prévention", 81, 2, 0, 4, [EffetEtat(EtatBouclierPerLvl("Mot de Prévention", 0, 2, 450))], [EffetEtat(EtatBouclierPerLvl("Mot de Prévention", 0, 2, 510))], 5, 1, 1, 4, 1, "ligne", True, description="""La cible gagne des points de bouclier pendant 2 tours.""", chaine=True),

        Sort.Sort("Mot de Prévention", 124, 2, 0, 6, [EffetEtat(EtatBouclierPerLvl("Mot de Prévention", 0, 2, 450))], [EffetEtat(EtatBouclierPerLvl("Mot de Prévention", 0, 2, 510))], 5, 1, 1, 4, 1, "ligne", True, description="""La cible gagne des points de bouclier pendant 2 tours.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot d'Agonie", 150, 2, 2, 5, [EffetDegats(7, 9, "Terre"), EffetDegats(22, 26, "Terre", zone=Zones.TypeZoneCroix(1, 1)), EffetPousser(1, "CaseCible", zone=Zones.TypeZoneCroix(1))], [EffetDegats(9, 11, "Terre"), EffetDegats(28, 32, "Terre", zone=Zones.TypeZoneCroix(1, 1)), EffetPousser(1, "CaseCible", zone=Zones.TypeZoneCroix(1))], 5, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Terre.
    Les dommages subis sont augmentés et occasionnés aux ennemis autour de la cible.
    Les ennemis affectés sont repoussés.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Turbulent", 38, 3, 1, 5, [EffetVolDeVie(18, 20, "Air")], [EffetVolDeVie(24, 24, "Air")], 5, 3, 2, 0, 1, "ligne", True, description="""Vole de la vie dans l'élément Air.""", chaine=True),

        Sort.Sort("Mot Turbulent", 90, 3, 1, 5, [EffetVolDeVie(22, 24, "Air")], [EffetVolDeVie(28, 28, "Air")], 5, 3, 2, 0, 1, "ligne", True, description="""Vole de la vie dans l'élément Air.""", chaine=True),

        Sort.Sort("Mot Turbulent", 132, 3, 1, 5, [EffetVolDeVie(26, 28, "Air")], [EffetVolDeVie(32, 32, "Air")], 5, 3, 2, 0, 1, "ligne", True, description="""Vole de la vie dans l'élément Air.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Espiègle", 155, 3, 1, 6, [motDAirEffetAvant, EffetDegats(17, 19, "Air"), motDAirEffetApres], [motDAirEffetAvant, EffetDegats(19, 21, "Air"), motDAirEffetApres], 25, 3, 2, 0, 1, "cercle", True, description="""Occasionne des dommages Air.
    Les alliés à proximité du lanceur (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot d'Immobilisation", 44, 2, 1, 4, [EffetEtat(EtatBoostCaracFixe("Mot d'Immobilisation", 0, 1, "PM", -2)), EffetEtat(EtatEffetFinTour("Mot d'Immobilisation", 0, 1, EffetSoinPerPVMax(8, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies|Lanceur", cibles_possibles_direct="Ennemis|Allies"), "Mot d'immobilisation", "lanceur"))], [], 0, 1, 1, 1, 0, "cercle", True, description="""Enlève des PM pendant 1 tour.
    À la fin de son tour, la cible soigne les alliés à proximité (2 cases ou moins).""", chaine=True),

        Sort.Sort("Mot d'Immobilisation", 97, 2, 1, 4, [EffetEtat(EtatBoostCaracFixe("Mot d'Immobilisation", 0, 1, "PM", -2)), EffetEtat(EtatEffetFinTour("Mot d'Immobilisation", 0, 1, EffetSoinPerPVMax(10, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies|Lanceur", cibles_possibles_direct="Ennemis|Allies"), "Mot d'immobilisation", "lanceur"))], [], 0, 1, 1, 1, 0, "cercle", True, description="""Enlève des PM pendant 1 tour.
    À la fin de son tour, la cible soigne les alliés à proximité (2 cases ou moins).""", chaine=True),

        Sort.Sort("Mot d'Immobilisation", 137, 2, 1, 4, [EffetEtat(EtatBoostCaracFixe("Mot d'Immobilisation", 0, 1, "PM", -3)), EffetEtat(EtatEffetFinTour("Mot d'Immobilisation", 0, 1, EffetSoinPerPVMax(12, zone=Zones.TypeZoneCercleSansCentre(2), cibles_possibles="Allies|Lanceur", cibles_possibles_direct="Ennemis|Allies"), "Mot d'immobilisation", "lanceur"))], [], 0, 1, 1, 1, 0, "cercle", True, description="""Enlève des PM pendant 1 tour.
    À la fin de son tour, la cible soigne les alliés à proximité (2 cases ou moins).""", chaine=True),
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Vivifiant", 160, 1, 1, 3, [EffetEtat(EtatBoostCaracFixe("Stimulé", 0, 2, "PM", 3), etat_requis="Stimulé")], [], 0, 1, 99, 0, 0, "cercle", True, description="""Augmente les PM pendant 3 tours si la cible est dans l'état Stimulé.
    Le bonus de PM est retiré si la cible perd l'état Stimulé.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Déroutant", 50, 4, 1, 4, [EffetSoin(30, 35, cibles_possibles="Allies"), EffetDegats(21, 26, "Feu", cibles_possibles="Ennemis")], [EffetSoin(36, 41, cibles_possibles="Allies"), EffetDegats(26, 31, "Feu", cibles_possibles="Ennemis")], 25, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu aux ennemis et soigne les alliés.""", chaine=False),

        Sort.Sort("Mot Déroutant", 103, 4, 1, 5, [EffetSoin(36, 41, cibles_possibles="Allies"), EffetDegats(26, 31, "Feu", cibles_possibles="Ennemis")], [EffetSoin(42, 47, cibles_possibles="Allies"), EffetDegats(31, 36, "Feu", cibles_possibles="Ennemis")], 25, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu aux ennemis et soigne les alliés.""", chaine=False),

        Sort.Sort("Mot Déroutant", 143, 4, 1, 6, [EffetSoin(42, 47, cibles_possibles="Allies"), EffetDegats(31, 36, "Feu", cibles_possibles="Ennemis")], [EffetSoin(48, 53, cibles_possibles="Allies"), EffetDegats(36, 41, "Feu", cibles_possibles="Ennemis")], 25, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu aux ennemis et soigne les alliés.""", chaine=False)
    ]))
    effetBoostPuissance = EffetEtat(EtatBoostCaracFixe("Mot Furieux", 0, 1, "pui", 100))
    effetBoostPuissanceCC = EffetEtat(EtatBoostCaracFixe("Mot Furieux", 0, 1, "pui", 200))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Furieux", 165, 4, 2, 5, [EffetDegats(14, 16, "Terre"), EffetEtat(EtatEffetSiNouvelEtat("Boost Mot Furieux", 0, 1, effetBoostPuissance, "Mot Furieux", "lanceur", "Mot Furieux Compteur")), EffetEtat(Etat("Mot Furieux Compteur", 0, 1), cibles_possibles="Ennemis", zone=Zones.TypeZoneCroix(1, 1)), EffetDegats(42, 48, "Terre", zone=Zones.TypeZoneCroix(1, 11)), EffetRetireEtat("Boost Mot Furieux"), EffetRetireEtat("Mot Furieux Compteur", zone=Zones.TypeZoneCroix(1))], [EffetDegats(16, 18, "Terre"), EffetEtat(EtatEffetSiNouvelEtat("Boost Mot Furieux", 0, 1, effetBoostPuissanceCC, "Mot Furieux", "lanceur", "Mot Furieux Compteur")), EffetEtat(Etat("Mot Furieux Compteur", 0, 1), cibles_possibles="Ennemis", zone=Zones.TypeZoneCroix(1, 1)), EffetDegats(48, 54, "Terre", zone=Zones.TypeZoneCroix(1)), EffetRetireEtat("Boost Mot Furieux"), EffetRetireEtat("Mot Furieux Compteur", zone=Zones.TypeZoneCroix(1))], 15, 2, 1, 0, 0, "cercle", True, description="""Occasionne des dommages Terre et augmente la Puissance de la cible alliée en fonction du nombre d'ennemis au contact.
    Les dommages subis par la cible sont augmentés et occasionnés autour d'elle.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Tournoyant", 56, 4, 1, 4, [motDAirTournoyantEffetAvant, EffetDegats(17, 21, "Air", zone=Zones.TypeZoneCarre(1), cible_non_requise=True), motDAirTournoyantEffetApres], [motDAirTournoyantEffetAvant, EffetDegats(19, 23, "Air", zone=Zones.TypeZoneCarre(1), cible_non_requise=True), motDAirTournoyantEffetApres], 25, 1, 1, 1, 0, "cercle", True, description="""Occasionne des dommages Air en zone.
    Les alliés à proximité du lanceur (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=False),

        Sort.Sort("Mot Tournoyant", 112, 4, 1, 5, [motDAirTournoyantEffetAvant, EffetDegats(22, 26, "Air", zone=Zones.TypeZoneCarre(1), cible_non_requise=True), motDAirTournoyantEffetApres], [motDAirTournoyantEffetAvant, EffetDegats(24, 28, "Air", zone=Zones.TypeZoneCarre(1), cible_non_requise=True), motDAirTournoyantEffetApres], 25, 1, 1, 1, 0, "cercle", True, description="""Occasionne des dommages Air en zone.
    Les alliés à proximité du lanceur (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=False),

        Sort.Sort("Mot Tournoyant", 147, 4, 1, 6, [motDAirTournoyantEffetAvant, EffetDegats(27, 31, "Air", zone=Zones.TypeZoneCarre(1), cible_non_requise=True), motDAirTournoyantEffetApres], [motDAirTournoyantEffetAvant, EffetDegats(29, 33, "Air", zone=Zones.TypeZoneCarre(1), cible_non_requise=True), motDAirTournoyantEffetApres], 25, 1, 1, 1, 0, "cercle", True, description="""Occasionne des dommages Air en zone.
    Les alliés à proximité du lanceur (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Tourbillonnant", 170, 4, 1, 5, [EffetVolDeVie(30, 34, "Air", zone=Zones.TypeZoneCroix(2))], [EffetVolDeVie(35, 39, "Air", zone=Zones.TypeZoneCroix(2))], 15, 1, 99, 0, 1, "cercle", True, description="""Vole de la vie dans l'élément Air.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Fracassant", 62, 5, 1, 4, [EffetDegats(28, 33, "Eau"), EffetRetPA(2)], [EffetDegats(34, 39, "Eau"), EffetRetPA(2)], 25, 2, 1, 0, 0, "cercle", True, description="""Occasionne des dommages Eau et retire des PA aux ennemis.""", chaine=True),

        Sort.Sort("Mot Fracassant", 116, 5, 1, 5, [EffetDegats(35, 40, "Eau"), EffetRetPA(2)], [EffetDegats(41, 46, "Eau"), EffetRetPA(2)], 25, 2, 1, 0, 0, "cercle", True, description="""Occasionne des dommages Eau et retire des PA aux ennemis.""", chaine=True),

        Sort.Sort("Mot Fracassant", 153, 5, 1, 6, [EffetDegats(42, 47, "Eau"), EffetRetPA(3)], [EffetDegats(48, 53, "Eau"), EffetRetPA(3)], 25, 2, 1, 0, 0, "cercle", True, description="""Occasionne des dommages Eau et retire des PA aux ennemis.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Accablant", 175, 5, 1, 5, [motDAirAnimeEffetAvant, EffetDegats(36, 40, "Eau"), EffetRetPM(3), motDAirAnimeEffetApres], [motDAirAnimeEffetAvant, EffetDegats(44, 48, "Eau"), EffetRetPM(3), motDAirAnimeEffetApres], 5, 2, 1, 0, 0, "cercle", True, description="""Occasionne des dommages Eau et retire des PM.
    Les alliés à proximité de la cible (2 cases ou moins) sont soignés à hauteur de 100% des dommages occasionnés.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot de Silence", 69, 4, 0, 1, [EffetRetPA(2, cibles_possibles="Ennemis", cible_non_requise=True, zone=Zones.TypeZoneCercle(3)), EffetRetPA(2, cibles_possibles="Allies", etat_requis="!Stimulé", cible_non_requise=True, zone=Zones.TypeZoneCercle(3)), EffetDevoilePiege(zone=Zones.TypeZoneCercle(3), cible_non_requise=True), EffetRetireEtat("Invisible", zone=Zones.TypeZoneCercle(3), cible_non_requise=True)], [], 0, 1, 1, 3, 0, "cercle", True, description="""Retire des PA en zone et dévoile les entités invisibles.
    Les alliés Stimulés ainsi que le lanceur ne sont pas affectés.""", chaine=False),

        Sort.Sort("Mot de Silence", 122, 4, 0, 2, [EffetRetPA(3, cibles_possibles="Ennemis", cible_non_requise=True, zone=Zones.TypeZoneCercle(3)), EffetRetPA(3, cibles_possibles="Allies", etat_requis="!Stimulé", cible_non_requise=True, zone=Zones.TypeZoneCercle(3)), EffetDevoilePiege(zone=Zones.TypeZoneCercle(3), cible_non_requise=True), EffetRetireEtat("Invisible", zone=Zones.TypeZoneCercle(3), cible_non_requise=True)], [], 0, 1, 1, 3, 0, "cercle", True, description="""Retire des PA en zone et dévoile les entités invisibles.
    Les alliés Stimulés ainsi que le lanceur ne sont pas affectés.""", chaine=False),

        Sort.Sort("Mot de Silence", 162, 4, 0, 3, [EffetRetPA(4, cibles_possibles="Ennemis", cible_non_requise=True, zone=Zones.TypeZoneCercle(3)), EffetRetPA(4, cibles_possibles="Allies", etat_requis="!Stimulé", cible_non_requise=True, zone=Zones.TypeZoneCercle(3)), EffetDevoilePiege(zone=Zones.TypeZoneCercle(3), cible_non_requise=True), EffetRetireEtat("Invisible", zone=Zones.TypeZoneCercle(3), cible_non_requise=True)], [], 0, 1, 1, 3, 0, "cercle", True, description="""Retire des PA en zone et dévoile les entités invisibles.
    Les alliés Stimulés ainsi que le lanceur ne sont pas affectés.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Sacrificiel", 180, 2, 1, 3, [EffetEtat(EtatModSoinPer("Mot Sacrificiel", 0, 2, 125), cibles_possibles="Allies"), EffetEtat(EtatEffetSiSubit("Mot Sacrificiel", 0, 2, EffetSoinSelonSubit(20, zone=Zones.TypeZoneInfini(), cibles_possibles="Allies|Lanceur", etat_requis_cibles="Stimulé"), "Mot Sacrificiel", "lanceur", "cible"), cibles_possibles="Allies")], [], 0, 1, 1, 2, 0, "cercle", True, description="""Les soins reçus par l'allié ciblé sont augmentés pendant 2 tours.
    Les dommages reçus par l'allié ciblé soignent les alliés dans l'état Stimulé.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot de Régénération", 77, 2, 0, 2, [EffetEtat(EtatEffetDebutTour("Mot de Régénération", 0, 1, EffetSoinPerPVMax(10), "Mot de Régénération", "lanceur")), EffetEtat(EtatEffetDebutTour("Mot de Régénération", 1, 1, EffetSoinPerPVMax(10), "Mot de Régénération", "lanceur"))], [], 0, 1, 1, 3, 0, "ligne", True, description="""La cible est soignée à retardement : au début du prochain tour du lanceur, et au tour suivant.""", chaine=True),

        Sort.Sort("Mot de Régénération", 128, 2, 0, 4, [EffetEtat(EtatEffetDebutTour("Mot de Régénération", 0, 1, EffetSoinPerPVMax(10), "Mot de Régénération", "lanceur")), EffetEtat(EtatEffetDebutTour("Mot de Régénération", 1, 1, EffetSoinPerPVMax(10), "Mot de Régénération", "lanceur"))], [], 0, 1, 1, 2, 0, "ligne", True, description="""La cible est soignée à retardement : au début du prochain tour du lanceur, et au tour suivant.""", chaine=True),

        Sort.Sort("Mot de Régénération", 172, 2, 0, 6, [EffetEtat(EtatEffetDebutTour("Mot de Régénération", 0, 1, EffetSoinPerPVMax(10), "Mot de Régénération", "lanceur")), EffetEtat(EtatEffetDebutTour("Mot de Régénération", 1, 1, EffetSoinPerPVMax(10), "Mot de Régénération", "lanceur"))], [], 0, 1, 1, 1, 0, "ligne", True, description="""La cible est soignée à retardement : au début du prochain tour du lanceur, et au tour suivant.""", chaine=True)
    ]))
    activationMarqueDeRegeneration = Sort.Sort("Marque de Régénération", 0, 0, 0, 0, [EffetEtat(EtatEffetFinTour("Marque de Régénération", 0, 1, EffetSoinPerPVMax(15), "Marque de Régénération", "lanceur"))], [], 0, 99, 99, 0, 0, "cercle", False)
    sortieMarqueDeRegeneration = Sort.Sort("Sortie Marque de Régénération", 0, 0, 0, 1, [EffetRetireEtat("Marque de Régénération")], [], 0, 99, 99, 0, 0, "cercle", False)
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Marque de Régénération", 185, 3, 1, 6, [EffetGlyphe(Zones.TypeZoneCercle(0), activationMarqueDeRegeneration, activationMarqueDeRegeneration, sortieMarqueDeRegeneration, 1, "Marque de Régénération", (206, 22, 123))], [], 0, 1, 99, 0, 1, "cercle", True, description="""Pose un glyphe de fin de tour qui soigne.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot d'Envol", 84, 4, 1, 3, [
            # Marque le lapino
            EffetEtat(Etat("Etat Lapino", 0, 1), cibles_possibles="Lapino|Lapino protecteur"),
            # Si le lapino est cible
            EffetEchangePlace(cibles_possibles="Allies", etat_requis="Etat Lapino"),
            # Si un allie non invoc est ciblé
            EffetEchangePlace(cibles_possibles="Allies", cibles_exclues="Invoc", etat_requis="!Etat Lapino"),
            # Tue le lapino s'il a été ciblé
            EffetTue(zone=Zones.TypeZoneInfini(), etat_requis_cibles="Etat Lapino"),
            # Etat insoignable au lanceur si l'allié n'est pas stimulé.
            EffetEtatSelf(EtatModSoinPer("Insoignable", 0, 2, 0), etat_requis="!Stimulé"),
            # Retrait stimule
            EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini())
        ], [], 0, 1, 1, 3, 0, "cercle", False, description="""Échange de place avec un allié (hors invocations).
    Retire l'état Stimulé. Applique l'état Insoignable au lanceur si l'allié n'est pas Stimulé.
    Le Lapino peut être ciblé mais il est tué.""", chaine=False),

        Sort.Sort("Mot d'Envol", 84, 4, 1, 5, [
            # Marque le lapino
            EffetEtat(Etat("Etat Lapino", 0, 1), cibles_possibles="Lapino|Lapino protecteur"),
            # Si le lapino est cible
            EffetEchangePlace(cibles_possibles="Allies", cibles_exclues="Invoc", etat_requis="Etat Lapino"),
            # Si un allie non invoc est ciblé
            EffetEchangePlace(cibles_possibles="Allies", cibles_exclues="Invoc", etat_requis="!Etat Lapino"),
            # Tue le lapino s'il a été ciblé
            EffetTue(etat_requis="Etat Lapino"),
            # Etat insoignable au lanceur si l'allié n'est pas stimulé.
            EffetEtatSelf(EtatModSoinPer("Insoignable", 0, 2, 0), etat_requis="!Stimulé"),
            # Retrait stimule
            EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini())
        ], [], 0, 1, 1, 3, 0, "cercle", False, description="""Échange de place avec un allié (hors invocations).
    Retire l'état Stimulé. Applique l'état Insoignable au lanceur si l'allié n'est pas Stimulé.
    Le Lapino peut être ciblé mais il est tué.""", chaine=False),

        Sort.Sort("Mot d'Envol", 84, 4, 1, 7, [
            # Marque le lapino
            EffetEtat(Etat("Etat Lapino", 0, 1), cibles_possibles="Lapino"),
            # Si le lapino est cible
            EffetEchangePlace(cibles_possibles="Allies", cibles_exclues="Invoc", etat_requis="Etat Lapino"),
            # Si un allie non invoc est ciblé
            EffetEchangePlace(cibles_possibles="Allies", cibles_exclues="Invoc", etat_requis="!Etat Lapino"),
            # Tue le lapino s'il a été ciblé
            EffetTue(etat_requis="Etat Lapino"),
            # Etat insoignable au lanceur si l'allié n'est pas stimulé.
            EffetEtatSelf(EtatModSoinPer("Insoignable", 0, 2, 0), etat_requis="!Stimulé"),
            # Retrait stimule
            EffetRetireEtat("Stimulé", zone=Zones.TypeZoneInfini())
        ], [], 0, 1, 1, 3, 0, "cercle", False, description="""Échange de place avec un allié (hors invocations).
    Retire l'état Stimulé. Applique l'état Insoignable au lanceur si l'allié n'est pas Stimulé.
    Le Lapino peut être ciblé mais il est tué.""", chaine=False),
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot de Ralliement", 190, 2, 1, 5, [EffetAttire(2, source="JoueurCaseEffet", cible="Lanceur", cibles_possibles="Allies", etat_requis="Stimulé"), EffetAttire(2, cibles_possibles="Allies", etat_requis="Stimulé"), EffetAttire(2, source="JoueurCaseEffet", cible="Lanceur", cibles_possibles="Lapino|Lapino protecteur"), EffetAttire(2, cibles_possibles="Lapino|Lapino protecteur")], [], 0, 1, 1, 2, 0, "cercle", True, description="""Rapproche le lanceur d'un allié puis l'attire.
    Nécessite l'état Stimulé sur l'allié.
    Peut être lancé sur le Lapino sans qu'il ne soit dans l'état Stimulé.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Revitalisant", 92, 3, 0, 0, [EffetSoinPerPVMax(20, zone=Zones.TypeZoneInfini(), etat_requis_cibles="Stimulé", consomme_etat=True), EffetTue(cibles_possibles="Lapino|Lapino protecteur", cibles_possibles_direct="Lanceur", zone=Zones.TypeZoneInfini()), EffetEtatSelf(EtatBoostSortCarac("Mot Revitalisant", 0, 1, "Mot Stimulant", "nbTourEntreDeux", 1)), EffetEtatSelf(EtatBoostSortCarac("Mot Revitalisant", 0, 1, "Mot d'Abnégation", "nbTourEntreDeux", 1))], [], 0, 1, 1, 3, 0, "cercle", False, description="""Tous les alliés Stimulés sont soignés, mais l'état Stimulé est retiré.
    Tue le Lapino s'il était invoqué.
    Passe l'intervalle de relance des sorts Mot Stimulant et Mot d'Abnégation à 1 tour.""", chaine=False),

        Sort.Sort("Mot Revitalisant", 141, 3, 0, 0, [EffetSoinPerPVMax(27, zone=Zones.TypeZoneInfini(), etat_requis_cibles="Stimulé", consomme_etat=True), EffetTue(cibles_possibles="Lapino|Lapino protecteur", cibles_possibles_direct="Lanceur", zone=Zones.TypeZoneInfini()), EffetEtatSelf(EtatBoostSortCarac("Mot Revitalisant", 0, 1, "Mot Stimulant", "nbTourEntreDeux", 1)), EffetEtatSelf(EtatBoostSortCarac("Mot Revitalisant", 0, 1, "Mot d'Abnégation", "nbTourEntreDeux", 1))], [], 0, 1, 1, 3, 0, "cercle", False, description="""Tous les alliés Stimulés sont soignés, mais l'état Stimulé est retiré.
    Tue le Lapino s'il était invoqué.
    Passe l'intervalle de relance des sorts Mot Stimulant et Mot d'Abnégation à 1 tour.""", chaine=False),

        Sort.Sort("Mot Revitalisant", 187, 3, 0, 0, [EffetSoinPerPVMax(33, zone=Zones.TypeZoneInfini(), etat_requis_cibles="Stimulé", consomme_etat=True), EffetTue(cibles_possibles="Lapino|Lapino protecteur", cibles_possibles_direct="Lanceur", zone=Zones.TypeZoneInfini()), EffetEtatSelf(EtatBoostSortCarac("Mot Revitalisant", 0, 1, "Mot Stimulant", "nbTourEntreDeux", 1)), EffetEtatSelf(EtatBoostSortCarac("Mot Revitalisant", 0, 1, "Mot d'Abnégation", "nbTourEntreDeux", 1))], [], 0, 1, 1, 3, 0, "cercle", False, description="""Tous les alliés Stimulés sont soignés, mais l'état Stimulé est retiré.
    Tue le Lapino s'il était invoqué.
    Passe l'intervalle de relance des sorts Mot Stimulant et Mot d'Abnégation à 1 tour.""", chaine=False)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot Galvanisant", 195, 5, 0, 0, [EffetEtat(EtatBoostCaracFixe("Stimulé", 0, 3, "PA", 2), cibles_exclues="Lanceur", zone=Zones.TypeZoneInfini())], [], 0, 1, 1, 5, 0, "cercle", False, description="""Applique les effets de Mot Stimulant à tous les alliés pendant 3 tours.
    N'affecte pas le lanceur.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot de Reconstitution", 100, 4, 0, 3, [EffetSoinPerPVMax(100), EffetEtat(EtatModSoinPer("Insoignable", 0, 3, 0))], [], 0, 1, 1, 8, 1, "ligne", True, description="""Soigne totalement la cible alliée mais la rend ensuite Insoignable pour 3 tours.""", chaine=True),

        Sort.Sort("Mot de Reconstitution", 149, 4, 0, 5, [EffetSoinPerPVMax(100), EffetEtat(EtatModSoinPer("Insoignable", 0, 3, 0))], [], 0, 1, 1, 7, 1, "ligne", True, description="""Soigne totalement la cible alliée mais la rend ensuite Insoignable pour 3 tours.""", chaine=True),

        Sort.Sort("Mot de Reconstitution", 197, 4, 0, 7, [EffetSoinPerPVMax(100), EffetEtat(EtatModSoinPer("Insoignable", 0, 3, 0))], [], 0, 1, 1, 6, 1, "ligne", True, description="""Soigne totalement la cible alliée mais la rend ensuite Insoignable pour 3 tours.""", chaine=True)
    ]))
    sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
        Sort.Sort("Mot de Solidarité", 200, 1, 0, 6, [
            #Sur allié non stimulé : il transfère 10% de ses PV aux autres alliés stimulés.
            EffetEtat(EtatEffetSiSubit("Mot solidaire", 0, 1, EffetSoinSelonSubit(100, zone=Zones.TypeZoneInfini(), cibles_possibles="Allies|Lanceur", cibles_possibles_direct="Lanceur|Allies", etat_requis_cibles="Stimulé"), "Mot de Solidarité", "cible", "cible"), cibles_possibles="Allies", etat_requis="!Stimulé"),
            EffetDegatsPerPv(10, etat_requis="!Stimulé", cibles_possibles="Allies", consomme_etat=True),
            # Sur allié stimulé : tous les autres alliés stimulés lui transfèrent 10% de leurs PV.
            EffetEtat(EtatEffetSiSubit("Mot solidaire", 0, 1, EffetSoinSelonSubit(100), "Mot solidaire", "cible", "attaquant"), cibles_possibles="Allies", etat_requis="Stimulé", etat_requis_cibles="Stimulé"),
            EffetDegatsPerPv(10, zone=Zones.TypeZoneInfini(), cibles_possibles="Allies", etat_requis_cibles="Mot solidaire", consomme_etat=True)
        ], [], 0, 2, 1, 0, 0, "cercle", False, description="""Sur allié stimulé : tous les autres alliés stimulés lui transfèrent 10% de leurs PV.
    Sur allié non stimulé : il transfère 10% de ses PV aux autres alliés stimulés.""", chaine=False)
    ]))
    return sorts
