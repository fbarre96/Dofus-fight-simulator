"""@summary: Les sorts de la balise de rappel
"""

from Effets.EffetTp import EffetEchangePlace
from Effets.EffetTue import EffetTue
import Sort
import Zones


def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sortsDebutCombat = []
    return sortsDebutCombat


def getSorts(lvl):
    """@summary: charge les sorts
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sorts = []
    sorts.append(Sort.Sort("Rappel", 0, 0, 0, 0, [
        EffetEchangePlace(zone=Zones.TypeZoneInfini(), cibles_possibles_direct="Lanceur",
                          cibles_possibles="Cra", pile=False),
        EffetTue(zone=Zones.TypeZoneInfini(), cibles_possibles_direct="Cra",
                 cibles_possibles="Lanceur", pile=False)
        ], [], 0, 99, 99, 0, 0, "cercle", False, chaine=False))
    return sorts
