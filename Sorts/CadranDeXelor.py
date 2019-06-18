"""@summary: Les sorts de cadran de xélor
"""

import Sort
from Effets.EffetDegats import EffetDegats
from Effets.EffetEtat import EffetEtat
import Zones
from Etats.EtatBoostCarac import EtatBoostCaracFixe


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
    # pylint: disable=unused-argument
    sorts = []
    sorts.append(Sort.Sort("Synchronisation", 0, 0, 0, 0,
                           [
                               EffetDegats(100, 130, "feu", zone=Zones.TypeZoneCercleSansCentre(4),
                                           cibles_possibles="Ennemis|Lanceur",
                                           etat_requis_cibles="Telefrag"),
                               EffetEtat(EtatBoostCaracFixe("Synchronisation", 0, 1, "PA", 2),
                                         zone=Zones.TypeZoneCercleSansCentre(4),
                                         cibles_possibles="Allies|Lanceur",
                                         etat_requis_cibles="Telefrag")],
                           [], 0, 99, 99, 0, 0, "cercle", False, chaine=False))
    return sorts
