"""@summary: Rassemble les sorts de l'éniripsa
"""
# pylint: disable=line-too-long
import Sort
from Effets.EffetDegats import EffetDegats
from Effets.EffetSoin import EffetSoinSelonSubit, EffetSoin, EffetSoinPerPVMax
from Effets.EffetEtat import EffetEtat, EffetRetireEtat, EffetEtatSelf
from Effets.EffetInvoque import EffetInvoque
from Effets.EffetTp import EffetTp
from Effets.EffetGlyphe import EffetGlyphe
from Effets.EffetEntiteLanceSort import EffetEntiteLanceSort
from Etats.Etat import Etat
from Etats.EtatEffet import EtatEffetSiSubit, EtatEffetFinTour, EtatEffetSiMeurt
from Etats.EtatBoostCarac import EtatBoostCaracFixe
from Etats.EtatBoostSortCarac import EtatBoostSortCarac

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
    return sorts
