"""@summary: Les sorts de Lapino
"""

import Sort
from Effets.EffetSoin import EffetSoinPerPVMax


def getSortsDebutCombat(lvl):
    """@summary: charge les sorts de début combat
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
    sorts.append(Sort.Sort("Lapino de vie", 0, 3, 0, 4, [EffetSoinPerPVMax(
        10, cibles_possibles="Allies|Lanceur")], [], 0, 99, 99, 0, 0, "cercle", False,
                           description="""Soigne de 5% de la vie maximale de la cible allié."""))
    return sorts
