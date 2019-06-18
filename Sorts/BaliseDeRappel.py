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
    """@summary: charge les sorts de début de combat
    @return: List <Sort>
    """
    # pylint: disable=unused-argument
    sorts = []
    sorts.append(Sort.Sort("Rappel", 0, 0, 0, 0, [
        EffetEchangePlace(zone=Zones.TypeZoneInfini(), cibles_possibles="Cra"), EffetTue(
            zone=Zones.TypeZoneInfini(), cibles_possibles="Lanceur")
        ], [], 0, 99, 99, 0, 0, "cercle", False))
    return sorts
