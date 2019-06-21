"""@summary: Rassemble les sorts de l'éniripsa
"""
# pylint: disable=line-too-long
import Sort
from Effets.EffetDegats import EffetDegats
from Effets.EffetPousser import EffetPousser
from Effets.EffetSoin import EffetSoinSelonSubit, EffetSoin, EffetSoinPerPVMax
from Effets.EffetEtat import EffetEtat, EffetRetireEtat, EffetEtatSelf, EffetRafraichirEtats
from Effets.EffetInvoque import EffetInvoque
from Effets.EffetTp import EffetTp
from Effets.EffetGlyphe import EffetGlyphe
from Effets.EffetEntiteLanceSort import EffetEntiteLanceSort
from Etats.Etat import Etat
from Etats.EtatEffet import EtatEffetSiSubit, EtatEffetFinTour, EtatEffetSiMeurt
from Etats.EtatBoostCarac import EtatBoostCaracFixe
from Etats.EtatBoostSortCarac import EtatBoostSortCarac
from Etats.EtatModSoin import EtatModSoinPer

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
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Mot d'Affection", 105, 4, 1, 3, [TODO(Invoque : Lapino protecteur), zone=Zones.TypeZoneCercle(99)), TODO(Fixe l'intervalle de relance de Mot d'Affection à 3 tour(s)), zone=Zones.TypeZoneCercle(99)), TODO(10711), zone=Zones.TypeZoneCercle(99))], [], 0, 1, 1, 1, 0, "cercle", True, description="""Invoque un Lapino qui applique des points de bouclier sur les alliés et applique l'état Stimulé sur son invocateur.
    # Lorsque le Lapino meurt, il pose un glyphe de fin de tour qui applique des points de bouclier, et ne peut plus être invoqué pendant 3 tours.""", chaine=True)
    # ]))
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
    # sorts.append(Personnages.Personnage.getSortRightLvl(lvl, [
    #     Sort.Sort("Mot de Séduction", 120, 3, 1, 5, [TODO(Invoque : Fiole), zone=Zones.TypeZoneCercle(2)), EffetDegats(22, 26, "Terre", zone=Zones.TypeZoneCercle(2))], [TODO(Invoque : Fiole), zone=Zones.TypeZoneCercle(2)), EffetDegats(26, 30, "Terre", zone=Zones.TypeZoneCercle(2))], 15, 1, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Terre et invoque une fiole.
    # Lorsqu''elle est attaquée par un allié, elle subit 2 fois moins de dommages et rend 100% des points de vie perdus à son attaquant.
    # Lorsqu'elle meurt, elle occasionne des dommages en zone.
    # Elle meurt si elle entre dans l'état Stimulé.""", chaine=True)
    # ]))
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
        Sort.Sort("Mot Sélectif", 22, 3, 0, 6, [EffetSoin(13, 15, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3), cible_non_requise=True), EffetDegats(9, 11, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis", cible_non_requise=True)], [EffetSoin(16, 16, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3), cible_non_requise=True), EffetDegats(13, 13, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis", cible_non_requise=True)], 15, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu aux ennemis et soigne les alliés en zone.""", chaine=False),

        Sort.Sort("Mot Sélectif", 65, 3, 0, 6, [EffetSoin(18, 20, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3), cible_non_requise=True), EffetDegats(12, 14, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis", cible_non_requise=True)], [EffetSoin(21, 21, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3), cible_non_requise=True), EffetDegats(16, 16, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis", cible_non_requise=True)], 15, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu aux ennemis et soigne les alliés en zone.""", chaine=False),

        Sort.Sort("Mot Sélectif", 108, 3, 0, 6, [EffetSoin(23, 25, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3), cible_non_requise=True), EffetDegats(15, 17, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis", cible_non_requise=True)], [EffetSoin(26, 26, cibles_possibles="Allies|Lanceur", zone=Zones.TypeZoneCroix(3), cible_non_requise=True), EffetDegats(19, 19, "Feu", zone=Zones.TypeZoneCroix(3), cibles_possibles="Ennemis", cible_non_requise=True)], 15, 2, 99, 0, 0, "cercle", True, description="""Occasionne des dommages Feu aux ennemis et soigne les alliés en zone.""", chaine=False)
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
    return sorts
